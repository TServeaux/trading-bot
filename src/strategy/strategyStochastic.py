"""
Author : Tao Serveaux
Date : 21/09/2026
Description: Trading strategy based on the Stochastic Oscillator,
    generating a signal when the oscillator crosses configurable low/high
    barriers.
"""

import pandas as pd
from .baseStrategie import BaseStrategie
import ta

class StrategieStochastic(BaseStrategie):

    def __init__(self, candles, window = 14, highBarrier = 80, lowBarrier = 20):
        """
        Description: Initialize the Stochastic Oscillator strategy.

        Args:
            candles (list): List of OHLCV candles.
            window (int, optional): Oscillator calculation window. Defaults
                to 14.
            highBarrier (float, optional): Overbought threshold. Defaults to
                80.
            lowBarrier (float, optional): Oversold threshold. Defaults to
                20.

        Returns:
            None
        """
        super().__init__(candles)
        self._window = window
        self._highBarrier = highBarrier
        self._lowBarrier = lowBarrier

    def signal(self):
        """
        Description: Compute the Stochastic Oscillator and compare the
            latest value to the low and high barriers.

        Args:
            None

        Returns:
            str: 'long' if the oscillator is below the low barrier, 'short'
                if it is above the high barrier, otherwise 'hold'.
        """
        data = pd.DataFrame(self._candles, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume'])
        stochastic = ta.momentum.StochasticOscillator(high=data['high'],
                                             low=data['low'], close=data['close'], window=self._window).stoch()

        if stochastic.iloc[-1] < self._lowBarrier :
            return 'long'

        elif stochastic.iloc[-1] > self._highBarrier :
            return 'short'

        else :
            return 'hold'
