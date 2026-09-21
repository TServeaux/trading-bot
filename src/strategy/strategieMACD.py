"""
Author : Tao Serveaux
Date : 21/09/2026
Description: Trading strategy based on the MACD indicator, generating a
    signal on bullish or bearish crossovers between the MACD line and its
    signal line.
"""

import pandas as pd
from .baseStrategie import BaseStrategie
import ta

class StrategieMACD(BaseStrategie):

    def __init__(self, candles):
        """
        Description: Initialize the MACD strategy.

        Args:
            candles (list): List of OHLCV candles.

        Returns:
            None
        """
        super().__init__(candles)

    def signal(self):
        """
        Description: Compute the MACD line and its signal line, and detect
            a crossover between the last two candles.

        Args:
            None

        Returns:
            str: 'long' on a bullish crossover (MACD line crosses above the
                signal line), 'short' on a bearish crossover, otherwise
                'hold'.
        """

        data = pd.DataFrame(self._candles, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume'])
        macd = ta.trend.MACD(close=data['close'])

        macdSignal = macd.macd_signal()
        macdLine = macd.macd()

        if macdLine.iloc[-2] < macdSignal.iloc[-2] and macdLine.iloc[-1] > macdSignal.iloc[-1] :
            return 'long'

        elif macdLine.iloc[-2] > macdSignal.iloc[-2] and macdLine.iloc[-1] < macdSignal.iloc[-1] :
            return 'short'

        else :
            return 'hold'
