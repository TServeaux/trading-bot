"""
Author : Tao Serveaux
Date : 21/09/2026
Description: Thin wrapper around an exchange client used to fetch OHLCV
    (candlestick) market data for a given trading pair.
"""

class DataFeed:

    def __init__(self, exchange) :
        """
        Description: Initialize the data feed with the underlying exchange
            client used to fetch candle data.

        Args:
            exchange: An Exchange or PaperExchange instance exposing a
                getExchange() method returning a ccxt exchange client.

        Returns:
            None
        """

        self.__exchange = exchange.getExchange()

    def getCandles(self, symbol, timeFrame, limit) :
        """
        Description: Fetch OHLCV candle data for a trading pair.

        Args:
            symbol (str): Trading pair symbol.
            timeFrame (str): Candle timeframe (e.g. '15m', '1h').
            limit (int): Maximum number of candles to fetch.

        Returns:
            list: List of OHLCV candles, each as
                [timestamp, open, high, low, close, volume].
        """

        candles = self.__exchange.fetch_ohlcv(symbol, timeFrame, limit=limit)

        return candles
