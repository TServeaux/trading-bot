"""
Author : Tao Serveaux
Date : 21/09/2026
Description: Trading strategy based on the crossover of a short-term and a
    long-term Exponential Moving Average (EMA).
"""

import pandas as pd
from .baseStrategie import BaseStrategie
import ta

class StrategieEMA(BaseStrategie):

    def __init__(self, candles, shortWindow = 9, longWindow = 21):
        """
        Description: Initialize the EMA crossover strategy.

        Args:
            candles (list): List of OHLCV candles.
            shortWindow (int, optional): Window size for the short-term EMA.
                Defaults to 9.
            longWindow (int, optional): Window size for the long-term EMA.
                Defaults to 21.

        Returns:
            None
        """
        super().__init__(candles)
        self._shortWindow = shortWindow
        self._longWindow = longWindow


    def signal(self):
        """
        Description: Compute the short-term and long-term EMAs and detect a
            crossover between the last two candles.

        Args:
            None

        Returns:
            str: 'long' if the short EMA crosses above the long EMA, 'short'
                if it crosses below, otherwise 'hold'.
        """
        data = pd.DataFrame(self._candles, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume'])
        emaShort = ta.trend.EMAIndicator(close=data['close'], window=self._shortWindow).ema_indicator()
        emaLong = ta.trend.EMAIndicator(close=data['close'], window=self._longWindow).ema_indicator()

        if emaShort.iloc[-2] < emaLong.iloc[-2] and emaShort.iloc[-1] > emaLong.iloc[-1] :
            return 'long'

        elif emaShort.iloc[-2] > emaLong.iloc[-2] and emaShort.iloc[-1] < emaLong.iloc[-1] :
            return 'short'

        else :
            return 'hold'


