import time
import ccxt

from .core.exchange import Exchange
from .core.dataFeed import DataFeed
from .core.orderManager import OrderManager
from .core.paperExchange import PaperExchange

from .strategy.strategieRSI import StrategieRSI
from .strategy.strategieBollinger import StrategieBollinger
from .strategy.strategieMACD import StrategieMACD
from .strategy.combinedStrategie import CombinedStrategie

from .risk.riskManager import RiskManager

from .utils.notifier import Notifier
from .utils.stats import Stats

class Bot:

    def __init__(self, apiKey, secretKey, tokenTelegram, chatId, symbol, paperMode=True,
                 xLever=5, takeProfit=30, stopLoss=20, pourcentage=0.2, timeFrame='5m', maxTime=7, limit=100):

        self._timeFrame = timeFrame
        self._symbol = symbol
        self._maxTime = maxTime #jours
        self._limit = limit
        self._takeProfit = takeProfit
        self._stopLoss = stopLoss
        self._pourcentage = pourcentage
        self._paperMode = paperMode
        self._lever = xLever

        realExchange = Exchange(apiKey, secretKey)

        if paperMode:
            self._exchange = PaperExchange(realExchange.getExchange(), xLever)
        else:
            self._exchange = realExchange
        
        self._notifier = Notifier(tokenTelegram, chatId)
        self._dataFeed = DataFeed(self._exchange)
        
        self._strategies = {}

        risk, stats = RiskManager(), Stats()
        self._strategies['RSIxMACD'] = {'combo': (StrategieRSI,StrategieMACD),
                                        'risk': risk,
                                        'order': OrderManager(self._exchange, risk, self._symbol, self._notifier, stats, 'RSIxMACD'),
                                        'stats': stats}
        
        risk, stats = RiskManager(), Stats()
        self._strategies['RSIxBollinger'] = {'combo': (StrategieRSI,StrategieBollinger), 
                                            'risk': risk,
                                            'order': OrderManager(self._exchange, risk, self._symbol, self._notifier, stats, 'RSIxBollinger'),
                                            'stats': stats}
        
        risk, stats = RiskManager(), Stats()
        self._strategies['BollingerxMACD'] = {'combo': (StrategieBollinger,StrategieMACD),
                                              'risk': risk,
                                              'order': OrderManager(self._exchange, risk, self._symbol, self._notifier, stats , 'BollingerxMACD'),
                                              'stats': stats}
        
    def run(self):

        start = time.time()
        print("Bot démarré")

        combos = {}
        for key in self._strategies:
            combos[key] = self._strategies[key]['combo']

        while time.time() - start < self._maxTime * 24 * 3600 :
            errorOccured = False    

            try :
                candles = self._dataFeed.getCandles(self._symbol, self._timeFrame, self._limit)
                print(f"Prix actuel : {self._exchange.checkPrice(self._symbol)}")
                print(f"Nombre de bougies : {len(candles)}")

                if self._paperMode:
                    self._exchange.checkTPSL()

                signaux = CombinedStrategie(candles, combos).signal()
                print(f"Signaux : {signaux}")
                
                for key, signal in signaux.items():
                    self._strategies[key]['order'].takeOrder(signal, self._takeProfit, self._stopLoss, self._pourcentage)

            except ccxt.RequestTimeout as err :
                self._notifier.sendError(str(err))
                errorOccured = True

            except ccxt.DDoSProtection as err :
                self._notifier.sendError("Rate limit atteint. Pause de 60s...")
                time.sleep(60)
                errorOccured = True

            except Exception as err :
                self._notifier.sendError(f"Erreur critique imprévue : {err}")
                errorOccured = True
            
            if not errorOccured :
                time.sleep(300)
            else :
                time.sleep(30)