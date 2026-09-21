"""
Author : Tao Serveaux
Date : 21/09/2026
Description: Trading strategy based on the Average Directional Index (ADX),
    generating a signal based on trend strength and the direction of the
    dominant directional movement indicator.
"""

import pandas as pd
from .baseStrategie import BaseStrategie
import ta

class StrategieADX(BaseStrategie):

    def __init__(self, candles, window = 14, seuil = 24):
        """
        Description: Initialize the ADX strategy.

        Args:
            candles (list): List of OHLCV candles.
            window (int, optional): ADX calculation window. Defaults to 14.
            seuil (float, optional): Minimum ADX value considered a trending
                market. Defaults to 24.

        Returns:
            None
        """
        super().__init__(candles)
        self._window = window
        self._seuil = seuil

    def signal(self):
        """
        Description: Compute ADX along with the positive and negative
            directional indicators, and derive a signal when the market is
            trending.

        Args:
            None

        Returns:
            str: 'long' if trending with positive directional dominance,
                'short' if trending with negative directional dominance,
                otherwise 'hold' when ADX is below the threshold.
        """
        data = pd.DataFrame(self._candles, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume'])
        indicators = ta.trend.ADXIndicator(high=data['high'], low=data['low'], close=data['close'], window=self._window)

        adx = indicators.adx()
        pos = indicators.adx_pos()
        neg = indicators.adx_neg()

        if adx.iloc[-1] > self._seuil :

            if pos.iloc[-1] < neg.iloc[-1] :
                return 'short'

            else :
                return 'long'

        else :
            return 'hold'
