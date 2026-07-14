import pandas as pd
from .baseStrategie import BaseStrategie
import ta

class StrategieRSI(BaseStrategie):

    def __init__(self,candles,lowBarrier = 25,highBarrier = 70, window=14):
        super().__init__(candles)
        self._lowBarrier = lowBarrier
        self._highBarrier = highBarrier
        self._window = window
    
    def signal(self):
        data = pd.DataFrame(self._candles, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume'])
        index = ta.momentum.RSIIndicator(close=data['close'], window=self._window).rsi()
        if index.iloc[-1] < self._lowBarrier :
            return 'long'
        elif index.iloc[-1] > self._highBarrier :
            return 'short'
        else : 
            return 'hold'