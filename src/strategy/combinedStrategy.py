"""
Author : Tao Serveaux
Date : 21/09/2026
Description: Aggregates the signals produced by several individual
    strategies and returns a consensus signal (long, short, or hold) for
    each configured strategy combination.
"""

from .baseStrategie import BaseStrategie

class CombinedStrategie(BaseStrategie):

    def __init__(self, candles, combos, seuil = 2):
        """
        Description: Initialize the combined strategy with the candle data,
            the strategy combinations to evaluate, and the minimum number of
            agreeing signals required to produce a non-hold result.

        Args:
            candles (list): List of OHLCV candles.
            combos (dict): Mapping of combination name to a list of
                strategy classes (each inheriting from BaseStrategie).
            seuil (int, optional): Minimum number of strategies within a
                combination that must agree for a 'long' or 'short' signal
                to be returned. Defaults to 2.

        Returns:
            None
        """
        super().__init__(candles)
        self._combos = combos
        self._seuil = seuil

    def signal(self):
        """
        Description: Evaluate every configured strategy combination and
            derive a consensus signal for each one based on how many of its
            individual strategies agree.

        Args:
            None

        Returns:
            dict: Mapping of combination name to its consensus signal
                ('long', 'short' or 'hold').
        """

        results = {}

        for name, strats in self._combos.items():
            signaux = []

            for strat in strats :
                signaux.append(strat(self._candles).signal())

            if signaux.count('long') >= self._seuil :
                results[name] = 'long'

            elif signaux.count('short') >= self._seuil :
                results[name] = 'short'

            else :
                results[name] = 'hold'

        return results
