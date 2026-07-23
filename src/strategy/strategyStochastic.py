import pandas as pd
from .baseStrategie import BaseStrategie
import ta

class StrategieStochastic(BaseStrategie):

    def __init__(self, candles, window = 14, highBarrier = 80, lowBarrier = 20):
        super().__init__(candles)
        self._window = window
        self._highBarrier = highBarrier
        self._lowBarrier = lowBarrier

    def signal(self):
        data = pd.DataFrame(self._candles, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume'])
        stochastic = ta.momentum.StochasticOscillator(high=data['high'],
                                             low=data['low'], close=data['close'], window=self._window).stoch()

        if stochastic.iloc[-1] < self._lowBarrier :
            return 'long'
        
        elif stochastic.iloc[-1] > self._highBarrier :
            return 'short'

        else : 
            return 'hold'