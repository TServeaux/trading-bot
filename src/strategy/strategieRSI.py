import pandas as pd
from baseStrategie import BaseStrategie
import ta

class StrategieRSI(BaseStrategie):

    def __init__(self,candles):
        super().__init__(candles)
    
    def signal(self):
        data = pd.DataFrame(self._candles, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume'])
        index = ta.momentum.RSIIndicator(close=data['close'], window=14).rsi()
        if index.iloc[-1] < 25 :
            return 'long'
        elif index.iloc[-1] > 70 :
            return 'short'
        else : 
            return 'hold'