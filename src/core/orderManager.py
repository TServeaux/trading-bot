class OrderManager:

    def __init__(self, exchange, riskManager, symbol):

        self._isShort = False
        self._isLong = False
        self._id = None
        self._amount = None

        self._exchange = exchange
        self._riskManager = riskManager
        self._symbol = symbol
    
    def takeOrder(self, position, takeProfit, stopLoss, pourcentage):

        if position == 'hold' :
            return 0

        lastAmount = self._amount
        self._amount = self._riskManager.trade(pourcentage)
        
        if self._amount > 0 :

            if position == 'long' and not self._isLong:

                self._isLong = True

                if self._isShort:
                    self._riskManager.manageCash(self._exchange.closePos(self._id)['profit'])
                    self._riskManager.releaseCash(lastAmount)
                    self._isShort = False
                    self._id = self._exchange.openPos(position, self._symbol, self._amount, takeProfit, stopLoss)['id']

                else :
                    self._id = self._exchange.openPos(position,  self._symbol, self._amount, takeProfit, stopLoss)['id']
                
            
            elif position == 'short' and not self._isShort:
                self._isShort = True

                if self._isLong:
                    self._riskManager.manageCash(self._exchange.closePos(self._id)['profit'])
                    self._riskManager.releaseCash(lastAmount)
                    self._isLong = False
                    self._id = self._exchange.openPos(position, self._symbol, self._amount, takeProfit, stopLoss)['id']

                else :
                    self._id = self._exchange.openPos(position, self._symbol, self._amount, takeProfit, stopLoss)['id']

        else :
            return -1 