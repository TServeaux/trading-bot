"""
Author : Tao Serveaux
Date : 21/09/2026
Description: Trading strategy based on the Money Flow Index (MFI),
    generating a signal when MFI crosses configurable low/high barriers.
"""

import pandas as pd
from .baseStrategie import BaseStrategie
import ta

class StrategyMFI(BaseStrategie):

    def __init__(self, candles, window = 14, high = 70, low = 20):
        """
        Description: Initialize the MFI strategy.

        Args:
            candles (list): List of OHLCV candles.
            window (int, optional): MFI calculation window. Defaults to 14.
            high (float, optional): Overbought threshold. Defaults to 70.
            low (float, optional): Oversold threshold. Defaults to 20.

        Returns:
            None
        """
        super().__init__(candles)
        self._window = window
        self._high= high
        self._low = low

    def signal(self):
        """
        Description: Compute MFI and compare the latest value to the low and
            high barriers.

        Args:
            None

        Returns:
            str: 'long' if MFI is below the low barrier, 'short' if MFI is
                above the high barrier, otherwise 'hold'.
        """
        data = pd.DataFrame(self._candles, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume'])
        MFI = ta.volume.MFIIndicator(high=data['high'], low=data['low'],
                       close=data['close'], volume=data['volume'],
                       window=self._window).money_flow_index()

        if MFI.iloc[-1] < self._low :
                    return 'long'

        elif MFI.iloc[-1] > self._high :
            return 'short'

        else :
            return 'hold'
