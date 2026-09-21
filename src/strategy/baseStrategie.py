"""
Author : Tao Serveaux
Date : 21/09/2026
Description: Defines the abstract base class that every trading strategy
    must inherit from, enforcing a common signal() interface.
"""

from abc import ABC, abstractmethod

class BaseStrategie(ABC) :

    def __init__(self, candles) :
        """
        Description: Store the candle data used by the strategy to compute
            its signal.

        Args:
            candles (list): List of OHLCV candles, each as
                [timestamp, open, high, low, close, volume].

        Returns:
            None
        """
        self._candles = candles

    @abstractmethod
    def signal(self):
        """
        Description: Compute the trading signal for this strategy. Must be
            implemented by subclasses.

        Args:
            None

        Returns:
            str: One of 'long', 'short' or 'hold'.
        """
        pass
