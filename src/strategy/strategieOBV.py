"""
Author : Tao Serveaux
Date : 21/09/2026
Description: Trading strategy based on the On-Balance Volume (OBV)
    indicator, generating a signal when OBV crosses its rolling average.
"""

import pandas as pd
from .baseStrategie import BaseStrategie
import ta

class StrategyOBV(BaseStrategie):

    def __init__(self, candles, window=14):
        """
        Description: Initialize the OBV strategy.

        Args:
            candles (list): List of OHLCV candles.
            window (int, optional): Rolling window size for the OBV moving
                average. Defaults to 14.

        Returns:
            None
        """
        super().__init__(candles)
        self._window = window

    def signal(self):
        """
        Description: Compute OBV and its rolling average, and detect a
            crossover between the last two candles.

        Args:
            None

        Returns:
            str: 'long' if OBV crosses above its moving average, 'short' if
                it crosses below, otherwise 'hold'.
        """
        data = pd.DataFrame(self._candles, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume'])
        obv = ta.volume.OnBalanceVolumeIndicator(close=data['close'], volume=data['volume']).on_balance_volume()
        obvMean = obv.rolling(window=self._window).mean()

        if obv.iloc[-2] < obvMean.iloc[-2] and obv.iloc[-1] > obvMean.iloc[-1] :
            return 'long'

        elif obv.iloc[-2] > obvMean.iloc[-2] and obv.iloc[-1] < obvMean.iloc[-1] :
            return 'short'

        else :
            return 'hold'
