from .core.exchange import Exchange
from .core.dataFeed import DataFeed
from .core.orderManager import OrderManager

from .strategy.strategieRSI import StrategieRSI
from .strategy.strategieBollinger import StrategieBollinger
from .strategy.strategieMACD import StrategieMACD
from .strategy.combinedStrategie import CombinedStrategie

from .risk.riskManager import RiskManager

from .utils.notifier import Notifier
from .utils.statitics import Statistic

class Bot:

    def __init__(self, apiKey, secretKey, tokenTelegram, chatId, symbol, timeFrame=5, maxTime=7):

        self._timeFrame = timeFrame
        self._symbol = symbol
        self._maxTime = maxTime #jours

        self._exchange = Exchange(apiKey, secretKey)
        self._notifier = Notifier(tokenTelegram, chatId)
        self._dataFeed = DataFeed(self._exchange)
        
        self._strategies = {}

        risk = RiskManager()
        self._strategies['RSIxMACD'] = [(StrategieRSI,StrategieMACD), risk,
                                         OrderManager(self._exchange, self._strategies['RSIxMACD'][1],self._symbol)]
        
        risk = RiskManager()
        self._strategies['RSIxBollinger'] = {'combos': (StrategieRSI,StrategieBollinger), 
                                            'risk': risk,
                                            'order':OrderManager(self._exchange, 
                                            self._strategies['RSIxBollinger'][1],self._symbol)
                                            'stats':}
        
        risk = RiskManager()
        self._strategies['BollingerxMACD'] = [(StrategieBollinger,StrategieMACD), risk,
                                         OrderManager(self._exchange, self._strategies['BollingerxMACD'][1],self._symbol)]
        
    def run(self):
        pass