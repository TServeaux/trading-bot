"""
Author : Tao Serveaux
Date : 21/09/2026
Description: Wrapper around the ccxt Kraken Futures client. Exposes price
    lookups, leverage control, balance retrieval, and position management
    (open/close) with automatic take-profit and stop-loss handling.
"""

import ccxt

class Exchange:

    def __init__(self, apiKey, secretKey):
        """
        Description: Initialize the connection to Kraken Futures and set up
            the internal balance and trade caches.

        Args:
            apiKey (str): Kraken Futures API key.
            secretKey (str): Kraken Futures API secret.

        Returns:
            None
        """

        self.__exchange = ccxt.krakenfutures({
            'apiKey' : apiKey,
            'secret' : secretKey,
        })

        self.__balance = {}
        self.__trades = {}

    def checkPrice(self, pair):
        """
        Description: Fetch the last traded price for a trading pair.

        Args:
            pair (str): Trading pair symbol (e.g. 'BTC/USD:USD').

        Returns:
            float: Last traded price.
        """

        return  self.__exchange.fetch_ticker(pair)['last']

    def lever(self, pair, xLever=10):
        """
        Description: Set the leverage multiplier used for a trading pair.

        Args:
            pair (str): Trading pair symbol.
            xLever (int, optional): Leverage multiplier. Defaults to 10.

        Returns:
            None
        """

        self.__exchange.set_leverage(xLever, pair)


    def balanceAvailable(self):
        """
        Description: Fetch and cache the current USDT balance (total, free
            and used) from the exchange.

        Args:
            None

        Returns:
            dict: Dictionary with 'total', 'free' and 'used' USDT amounts.
        """

        currentBalance = self.__exchange.fetch_balance()

        self.__balance['total'] = currentBalance['total']['USDT']
        self.__balance['free'] = currentBalance['free']['USDT']
        self.__balance['used'] = currentBalance['used']['USDT']

        return self.__balance


    def currentPos(self):
        """
        Description: Fetch all currently open positions from the exchange.

        Args:
            None

        Returns:
            list: List of open position dictionaries as returned by ccxt.
        """

        return self.__exchange.fetch_positions()

    def openPos(self, direction, symbol, amount, takeProfit=3, stopLoss=1.5):
        """
        Description: Open a market position with an attached take-profit and
            stop-loss, and record it in the internal trade cache.

        Args:
            direction (str): 'long' or 'short'.
            symbol (str): Trading pair symbol.
            amount (float): Order size.
            takeProfit (float, optional): Take-profit distance in percent.
                Defaults to 3.
            stopLoss (float, optional): Stop-loss distance in percent.
                Defaults to 1.5.

        Returns:
            dict: The newly opened trade record.
        """

        price = self.checkPrice(symbol)

        if direction == 'long' :
            direction = 'buy'
            tp =  price * (1 + takeProfit/100)
            sl = price * (1 - stopLoss/100)

        else :
            direction = 'sell'
            sl =  price * (1 + stopLoss/100)
            tp = price * (1 - takeProfit/100)

        info = self.__exchange.create_order(symbol, 'market', direction, amount,
                                            params={
                                                'takeProfitPrice' : tp,
                                                'stopLossPrice' : sl
                                            })

        trade = {}

        trade['openTimestamp'] = info['timestamp']
        trade['symbol'] = info['symbol']
        trade['side'] = info['side']
        trade['openPrice'] = info['price']
        trade['status'] = info['status']
        trade['id'] = info['id']

        trade['takeProfit'] = tp
        trade['stopLoss'] = sl
        trade['amount'] = amount

        self.__trades[info['id']] = trade

        return trade


    def closePos(self, id):
        """
        Description: Close an open position with a market order in the
            opposite direction, compute its profit, and update the trade
            record.

        Args:
            id (str): Identifier of the trade to close.

        Returns:
            dict: The updated (closed) trade record.
        """

        if self.__trades[id]['side'] == 'buy' :
            direction = 'sell'

        else :
            direction = 'buy'

        info = self.__exchange.create_order(self.__trades[id]['symbol'], 'market',
                                             direction, self.__trades[id]['amount'])

        if self.__trades[id]['side'] == 'buy' :
            profit = info['price'] - self.__trades[id]['openPrice']
        else :
            profit = self.__trades[id]['openPrice'] - info['price']

        self.__trades[id]['closedTimestamp'] = info['timestamp']
        self.__trades[id]['closedPrice'] = info['price']
        self.__trades[id]['status'] = 'closed'
        self.__trades[id]['profit'] = profit

        return self.__trades[id]

    def getExchange(self):
        """
        Description: Return the underlying ccxt exchange instance.

        Args:
            None

        Returns:
            ccxt.Exchange: The underlying ccxt exchange client.
        """
        return self.__exchange

    def getTrade(self, id):
        """
        Description: Retrieve a previously recorded trade by its id.

        Args:
            id (str): Identifier of the trade.

        Returns:
            dict: The trade record.
        """
        return self.__trades[id]
