from .baseStrategie import BaseStrategie

class CombinedStrategie(BaseStrategie):

    def __init__(self, candles, combos, seuil = 2):
        super().__init__(candles)
        self._combos = combos
        self._seuil = seuil

    def signal(self):

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