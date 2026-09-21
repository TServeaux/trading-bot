"""
Author : Tao Serveaux
Date : 21/09/2026
Description: Trading strategy based on Bollinger Bands, generating a signal
    when the closing price crosses below the lower band or above the upper
    band.
"""

import pandas as pd
from .baseStrategie import BaseStrategie
import ta

class StrategieBollinger(BaseStrategie):

    def __init__(self, candles, window=20):
        """
        Description: Initialize the Bollinger Bands strategy.

        Args:
            candles (list): List of OHLCV candles.
            window (int, optional): Rolling window size for the bands.
                Defaults to 20.

        Returns:
            None
        """
        super().__init__(candles)
        self._window = window

    def signal(self):
        """
        Description: Compute the Bollinger Bands and compare the latest
            closing price to the lower and upper bands.

        Args:
            None

        Returns:
            str: 'long' if price is below the lower band, 'short' if price
                is above the upper band, otherwise 'hold'.
        """

        data = pd.DataFrame(self._candles, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume'])
        bollinger = ta.volatility.BollingerBands(close=data['close'], window=self._window)

        lowBollinger = bollinger.bollinger_lband()
        highBollinger= bollinger.bollinger_hband()

        if data['close'].iloc[-1] < lowBollinger.iloc[-1] :
            return 'long'

        elif data['close'].iloc[-1] > highBollinger.iloc[-1] :
            return 'short'

        else :
            return 'hold'
