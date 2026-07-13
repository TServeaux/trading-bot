class OrderManager:

    def __init__(self, exchange, riskManager, symbol, notifier, stats):

        self._isShort = False
        self._isLong = False
        self._id = None
        self._amount = None

        self._exchange = exchange
        self._riskManager = riskManager
        self._symbol = symbol
        self._notifier = notifier
        self._stats = stats
    
    def takeOrder(self, position, takeProfit, stopLoss, pourcentage):

        self.syncPosition()

        if position == 'hold' :
            return 0

        lastAmount = self._amount
        self._amount = self._riskManager.trade(pourcentage)
        
        if self._amount > 0 :

            if position == 'long' and not self._isLong:

                self._isLong = True

                if self._isShort:

                    closedTrade = self._exchange.closePos(self._id)
                    self._riskManager.manageCash(closedTrade['profit'])
                    self._riskManager.releaseCash(lastAmount)
                    self._isShort = False
                    self._stats.tradeFinished(closedTrade)
                    self._notifier.sendTradeClosed(closedTrade)

                    openedTrade = self._exchange.openPos(position, self._symbol, self._amount, takeProfit, stopLoss)
                    self._notifier.sendTradeOpened(openedTrade)
                    self._id =openedTrade['id']

                else :
                    openedTrade = self._exchange.openPos(position, self._symbol, self._amount, takeProfit, stopLoss)
                    self._notifier.sendTradeOpened(openedTrade)
                    self._id =openedTrade['id']
                
            
            elif position == 'short' and not self._isShort:
                self._isShort = True

                if self._isLong:
                    closedTrade = self._exchange.closePos(self._id)
                    self._riskManager.manageCash(closedTrade['profit'])
                    self._riskManager.releaseCash(lastAmount)
                    self._isLong = False
                    self._stats.tradeFinished(closedTrade)
                    self._notifier.sendTradeClosed(closedTrade)

                    openedTrade = self._exchange.openPos(position, self._symbol, self._amount, takeProfit, stopLoss)
                    self._notifier.sendTradeOpened(openedTrade)
                    self._id = openedTrade['id']

                else :
                    openedTrade = self._exchange.openPos(position, self._symbol, self._amount, takeProfit, stopLoss)
                    self._notifier.sendTradeOpened(openedTrade)
                    self._id =openedTrade['id']

        else :
            return -1 
    
    def syncPosition(self):
        if self._id and (self._isLong or self._isShort):
            trade = self._exchange.getTrade(self._id)
            if trade['status'] == 'closed':
                self._riskManager.manageCash(trade['profit'])
                self._riskManager.releaseCash(self._amount)
                self._stats.tradeFinished(trade)
                self._notifier.sendTradeClosed(trade)
                self._isLong = False
                self._isShort = False
                self._id = None