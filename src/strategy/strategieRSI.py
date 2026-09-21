"""
Author : Tao Serveaux
Date : 21/09/2026
Description: Trading strategy based on the Relative Strength Index (RSI),
    generating a signal when RSI crosses configurable oversold/overbought
    barriers.
"""

import pandas as pd
from .baseStrategie import BaseStrategie
import ta

class StrategieRSI(BaseStrategie):

    def __init__(self,candles,lowBarrier = 25,highBarrier = 70, window=14):
        """
        Description: Initialize the RSI strategy.

        Args:
            candles (list): List of OHLCV candles.
            lowBarrier (float, optional): Oversold threshold. Defaults to
                25.
            highBarrier (float, optional): Overbought threshold. Defaults to
                70.
            window (int, optional): RSI calculation window. Defaults to 14.

        Returns:
            None
        """
        super().__init__(candles)
        self._lowBarrier = lowBarrier
        self._highBarrier = highBarrier
        self._window = window

    def signal(self):
        """
        Description: Compute RSI and compare the latest value to the
            oversold and overbought barriers.

        Args:
            None

        Returns:
            str: 'long' if RSI is below the low barrier, 'short' if RSI is
                above the high barrier, otherwise 'hold'.
        """
        data = pd.DataFrame(self._candles, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume'])
        index = ta.momentum.RSIIndicator(close=data['close'], window=self._window).rsi()
        if index.iloc[-1] < self._lowBarrier :
            return 'long'
        elif index.iloc[-1] > self._highBarrier :
            return 'short'
        else :
            return 'hold'
