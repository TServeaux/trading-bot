class RiskManager:

    def __init__(self, cash=10, maxTradingInvestement=0.5):
        self._cash = cash
        self._maxTradingInvestement = maxTradingInvestement
        self._engaged = 0
    
    def manageCash(self,profit):
        self._cash += profit

    def trade(self, pourcentage=0.20):
        if self._cash < 1 :
            return -1
        
        elif self._engaged + pourcentage * self._cash > self._cash * self._maxTradingInvestement:
            return -1
        
        else :
            self._engaged += pourcentage * self._cash
            return pourcentage * self._cash
    
    def releaseCash(self,amount):
        self._engaged -= amount
    
    def getCash(self):
        return self._cash