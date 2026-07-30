import json
import os

class Stats:

    def __init__(self):

        self._totalTrades = 0
        self._totalProfit = 0
        self._bestTrade = 0
        self._worstTrade = 0
        self._winrate = 0
        self._win = 0
        self._lose = 0
        self._alltrade = []

    def tradeFinished(self,trade):

        self._totalTrades += 1
        self._totalProfit += trade['profit']

        if trade['profit'] < 0:
            if abs(self._worstTrade) < abs(trade['profit']) :
                self._worstTrade = trade['profit']
            
            self._lose += 1

        else :
            if self._bestTrade < trade['profit'] :
                self._bestTrade = trade['profit']
            
            self._win += 1
        
        self._winrate = (self._win/self._totalTrades)*100

        resume = {}
        for i in ['closedTimestamp', 'openTimestamp', 'openPrice', 'closedPrice', 'profit'] :
            resume[i] = trade[i]
        
        self._alltrade.append(resume)
    
    def getStats(self):

        stats = {}

        stats['totalsTrades'] = self._totalTrades
        stats['totalsProfits'] = self._totalProfit
        stats['bestTrade'] = self._bestTrade
        stats['worstTrade'] = self._worstTrade
        stats['winrate'] = self._winrate
        stats['win'] = self._win
        stats['lose'] = self._lose

        return stats, self._alltrade

    def saveData(self, filename):
        
        os.makedirs('data', exist_ok=True)

        path = os.path.join('data', filename)
        stats, trades = self.getStats()
        data = {'stats' : stats, 'trades' : trades}

        with open(path, 'w') as f :
            json.dump(data, f, indent=4)

    def loadData(self, filename):

        path = os.path.join('data', filename)

        if not os.path.exists(path):
            return

        with open(path, 'r') as f:
            data = json.load(f)

        stats = data['stats']
        
        self._totalTrades = stats['totalsTrades']
        self._totalProfit = stats['totalsProfits']
        self._bestTrade = stats['bestTrade']
        self._worstTrade = stats['worstTrade']
        self._winrate = stats['winrate']
        self._win = stats['win']
        self._lose = stats['lose']
        self._alltrade = data['trades'] 