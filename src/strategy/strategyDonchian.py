"""
Author : Tao Serveaux
Date : 21/09/2026
Description: Trading strategy based on Donchian Channels, generating a
    signal when the closing price breaks out above or below the channel.
"""

import pandas as pd
from .baseStrategie import BaseStrategie
import ta

class StrategyDonchian(BaseStrategie):

    def __init__(self, candles, window = 20):
        """
        Description: Initialize the Donchian Channel strategy.

        Args:
            candles (list): List of OHLCV candles.
            window (int, optional): Rolling window size for the channel.
                Defaults to 20.

        Returns:
            None
        """
        super().__init__(candles)
        self._window = window

    def signal(self):
        """
        Description: Compute the Donchian Channel and compare the latest
            closing price to its upper and lower bands.

        Args:
            None

        Returns:
            str: 'long' if price breaks above the upper band, 'short' if
                price breaks below the lower band, otherwise 'hold'.
        """
        data = pd.DataFrame(self._candles, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume'])
        donchian = ta.volatility.DonchianChannel(high=data['high'], low=data['low'],
                                          close=data['close'], window=self._window)
        lowDon = donchian.donchian_channel_lband()
        highDon = donchian.donchian_channel_hband()

        if data['close'].iloc[-1] > highDon.iloc[-1] :
            return 'long'

        elif data['close'].iloc[-1] < lowDon.iloc[-1] :
            return 'short'

        else :
            return 'hold'

