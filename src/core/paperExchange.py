"""
Author : Tao Serveaux
Date : 21/09/2026
Description: Simulated (paper trading) exchange used to test strategies
    without executing real trades. Mirrors the interface of the real
    Exchange class while tracking virtual positions and profit/loss locally.
"""

import time

class PaperExchange :

    def __init__(self, exchange, xLever):
        """
        Description: Initialize the paper exchange on top of a real ccxt
            exchange instance (used only for price lookups) and set the
            simulated leverage.

        Args:
            exchange: Underlying ccxt exchange instance used for price data.
            xLever (int): Simulated leverage multiplier.

        Returns:
            None
        """
        self._exchange =exchange
        self._trades = {}
        self._nextId = 0
        self._lever = xLever

    def checkPrice(self, pair):
        """
        Description: Fetch the last traded price for a trading pair.

        Args:
            pair (str): Trading pair symbol.

        Returns:
            float: Last traded price.
        """

        return  self._exchange.fetch_ticker(pair)['last']

    def lever(self, xLever=10):
        """
        Description: Set the simulated leverage multiplier.

        Args:
            xLever (int, optional): Leverage multiplier. Defaults to 10.

        Returns:
            None
        """
        self._lever = xLever

    def openPos(self, direction, symbol, amount, takeProfit=3, stopLoss=1.5):
        """
        Description: Simulate opening a position with an attached
            take-profit and stop-loss, and record it locally.

        Args:
            direction (str): 'long' or 'short'.
            symbol (str): Trading pair symbol.
            amount (float): Simulated order size.
            takeProfit (float, optional): Take-profit distance in percent.
                Defaults to 3.
            stopLoss (float, optional): Stop-loss distance in percent.
                Defaults to 1.5.

        Returns:
            dict: The newly opened simulated trade record.
        """
        price = self.checkPrice(symbol)
        self._nextId += 1
        tradeId = str(self._nextId)

        if direction == 'long' :
            direction = 'buy'
            tp =  price * (1 + takeProfit/100)
            sl = price * (1 - stopLoss/100)

        else :
            direction = 'sell'
            sl =  price * (1 + stopLoss/100)
            tp = price * (1 - takeProfit/100)


        trade = {}

        trade['openTimestamp'] = int(time.time() * 1000)
        trade['symbol'] = symbol
        trade['side'] = direction
        trade['openPrice'] = price
        trade['status'] = 'open'
        trade['id'] = tradeId

        trade['takeProfit'] = tp
        trade['stopLoss'] = sl
        trade['amount'] = amount

        self._trades[tradeId] = trade

        return trade


    def closePos(self, id):
        """
        Description: Simulate closing a position at the current market
            price and compute its leveraged profit.

        Args:
            id (str): Identifier of the trade to close.

        Returns:
            dict: The updated (closed) simulated trade record.
        """
        price = self.checkPrice( self._trades[id]['symbol'])

        if self._trades[id]['side'] == 'buy' :
            variation = (price - self._trades[id]['openPrice']) / self._trades[id]['openPrice']
            profit = variation * self._trades[id]['amount'] * self._lever
        else :
            variation = (self._trades[id]['openPrice'] - price) / self._trades[id]['openPrice']
            profit = variation * self._trades[id]['amount'] * self._lever

        self._trades[id]['closedTimestamp'] = int(time.time() * 1000)
        self._trades[id]['closedPrice'] = price
        self._trades[id]['status'] = 'closed'
        self._trades[id]['profit'] = profit

        return self._trades[id]

    def checkTPSL(self):
        """
        Description: Check every open simulated trade against its
            take-profit and stop-loss levels, closing any trade whose
            current price has reached either level.

        Args:
            None

        Returns:
            list: List of trade records that were closed during this check.
        """
        closed = []

        for id, trade in self._trades.items():

            if trade['status'] == 'closed' :
                continue

            price = self.checkPrice(trade['symbol'])

            if trade['side'] == 'buy':
                if price >= trade['takeProfit'] or price <= trade['stopLoss']:
                    self.closePos(id)
                    closed.append(trade)

            else:
                if price <= trade['takeProfit'] or price >= trade['stopLoss']:
                    self.closePos(id)
                    closed.append(trade)

        return closed

    def getExchange(self):
        """
        Description: Return the underlying real ccxt exchange instance used
            for price data.

        Args:
            None

        Returns:
            ccxt.Exchange: The underlying ccxt exchange client.
        """
        return self._exchange

    def getTrade(self, id):
        """
        Description: Retrieve a previously recorded simulated trade by its
            id.

        Args:
            id (str): Identifier of the trade.

        Returns:
            dict: The trade record.
        """
        return self._trades[id]
