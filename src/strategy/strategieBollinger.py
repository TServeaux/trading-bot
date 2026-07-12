import pandas as pd
from baseStrategie import BaseStrategie
import ta

class StrategieBollinger(BaseStrategie):

    def __init__(self, candles):
        super().__init__(candles)
    
    def signal(self):

        data = pd.DataFrame(self._candles, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume'])
        bollinger = ta.volatility.BollingerBands(close=data['close'], window=20)

        lowBollinger = bollinger.bollinger_lband()
        highBollinger= bollinger.bollinger_hband()

        if data['close'].iloc[-1] < lowBollinger.iloc[-1] :
            return 'long'
        
        elif data['close'].iloc[-1] > highBollinger.iloc[-1] :
            return 'short'

        else : 
            return 'hold'
    