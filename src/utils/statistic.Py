class Statistic :

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

    def saveData(self):
        pass