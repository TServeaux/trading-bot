import time

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
                 xLever=10, takeProfit=0.3, stopLoss=0.2, pourcentage=0.2, timeFrame='1h', maxTime=7, limit=100):

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
                                        'order': OrderManager(self._exchange, risk, self._symbol, self._notifier, stats),
                                        'stats': stats}
        
        risk, stats = RiskManager(), Stats()
        self._strategies['RSIxBollinger'] = {'combo': (StrategieRSI,StrategieBollinger), 
                                            'risk': risk,
                                            'order': OrderManager(self._exchange, risk, self._symbol, self._notifier, stats),
                                            'stats': stats}
        
        risk, stats = RiskManager(), Stats()
        self._strategies['BollingerxMACD'] = {'combo': (StrategieBollinger,StrategieMACD),
                                              'risk': risk,
                                              'order': OrderManager(self._exchange, risk, self._symbol, self._notifier, stats),
                                              'stats': stats}
        
    def run(self):

        start = time.time()

        combos = {}
        for key in self._strategies:
            combos[key] = self._strategies[key]['combo']

        while time.time() - start < self._maxTime * 24 * 3600 :
            candles = self._dataFeed.getCandles(self._symbol, self._timeFrame, self._limit)

            if self._paperMode:
                self._exchange.checkTPSL()

            signaux = CombinedStrategie(candles, combos).signal()
            
            for key, signal in signaux.items():
                self._strategies[key]['order'].takeOrder(signal, self._takeProfit, self._stopLoss, self._pourcentage)
        
            time.sleep(60)