"""
Author : Tao Serveaux
Date : 21/09/2026
Description: Manages the lifecycle of a single strategy's trading position:
    opening, closing, and switching between long and short positions based
    on incoming signals, while keeping risk management, statistics, and
    Telegram notifications in sync.
"""

class OrderManager:

    def __init__(self, exchange, riskManager, symbol, notifier, stats, name):
        """
        Description: Initialize the order manager for a given strategy
            combination.

        Args:
            exchange: Exchange or PaperExchange instance used to place and
                close orders.
            riskManager (RiskManager): Risk manager tracking available and
                engaged cash.
            symbol (str): Trading pair symbol.
            notifier (Notifier): Notifier used to send Telegram messages on
                trade events.
            stats (Stats): Stats tracker for this strategy combination.
            name (str): Name of the strategy combination.

        Returns:
            None
        """

        self._isShort = False
        self._isLong = False
        self._id = None
        self._amount = None

        self._exchange = exchange
        self._riskManager = riskManager
        self._symbol = symbol
        self._notifier = notifier
        self._stats = stats
        self._name = name

    def takeOrder(self, position, takeProfit, stopLoss, pourcentage):
        """
        Description: Act on a new strategy signal: synchronize the current
            position state, then open, close, or flip the position
            depending on the requested direction.

        Args:
            position (str): Desired position, one of 'long', 'short' or
                'hold'.
            takeProfit (float): Take-profit distance in percent.
            stopLoss (float): Stop-loss distance in percent.
            pourcentage (float): Fraction of available cash to allocate to
                the trade.

        Returns:
            int or None: 0 if the signal was 'hold', -1 if no cash could be
                allocated, otherwise None after acting on the signal.
        """

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
                    self._notifier.sendTradeClosed(closedTrade, self._name)
                    self._stats.saveData(f'{self._name}.json')

                    openedTrade = self._exchange.openPos(position, self._symbol, self._amount, takeProfit, stopLoss)
                    self._notifier.sendTradeOpened(openedTrade,  self._name)
                    self._id =openedTrade['id']

                else :
                    openedTrade = self._exchange.openPos(position, self._symbol, self._amount, takeProfit, stopLoss)
                    self._notifier.sendTradeOpened(openedTrade,  self._name)
                    self._id =openedTrade['id']


            elif position == 'short' and not self._isShort:
                self._isShort = True

                if self._isLong:
                    closedTrade = self._exchange.closePos(self._id)
                    self._riskManager.manageCash(closedTrade['profit'])
                    self._riskManager.releaseCash(lastAmount)
                    self._isLong = False
                    self._stats.tradeFinished(closedTrade)
                    self._notifier.sendTradeClosed(closedTrade, self._name)
                    self._stats.saveData(f'{self._name}.json')

                    openedTrade = self._exchange.openPos(position, self._symbol, self._amount, takeProfit, stopLoss)
                    self._notifier.sendTradeOpened(openedTrade,  self._name)
                    self._id = openedTrade['id']

                else :
                    openedTrade = self._exchange.openPos(position, self._symbol, self._amount, takeProfit, stopLoss)
                    self._notifier.sendTradeOpened(openedTrade,  self._name)
                    self._id =openedTrade['id']

        else :
            return -1

    def syncPosition(self):
        """
        Description: Check whether the currently tracked trade has been
            closed externally (e.g. by a stop-loss/take-profit hit) and, if
            so, update risk management, statistics, and notifications, then
            reset the local position state.

        Args:
            None

        Returns:
            None
        """
        if self._id and (self._isLong or self._isShort):
            trade = self._exchange.getTrade(self._id)
            if trade['status'] == 'closed':
                self._riskManager.manageCash(trade['profit'])
                self._riskManager.releaseCash(self._amount)
                self._stats.tradeFinished(trade)
                self._notifier.sendTradeClosed(trade, self._name)
                self._stats.saveData(f'{self._name}.json')
                self._isLong = False
                self._isShort = False
                self._id = None
