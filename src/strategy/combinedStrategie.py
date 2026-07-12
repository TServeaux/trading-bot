from baseStrategie import BaseStrategie

class CombinedStrategie(BaseStrategie):

    def __init__(self, candles, combos):
        super().__init__(candles)
        self._combos = combos
    
    def signal(self):
        results = {}

        for name, pairs in self._combos.items():

            signal1 = pairs[0](self._candles).signal()
            signal2 = pairs[1](self._candles).signal()

            if signal1 == signal2 and signal1 != 'hold':
                results[name] = signal1

            else :
                results[name] = 'hold'

        return results