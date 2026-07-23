import pandas as pd
from .baseStrategie import BaseStrategie
import ta

class StrategyMFI(BaseStrategie):

    def __init__(self, candles, window = 14, high = 70, low = 20):
        super().__init__(candles)
        self._window = window
        self._high= high
        self._low = low

    def signal(self):
        data = pd.DataFrame(self._candles, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume'])
        MFI = ta.volume.MFIIndicator(high=data['high'], low=data['low'], 
                       close=data['close'], volume=data['volume'], 
                       window=self._window).money_flow_index()

        if MFI.iloc[-1] < self._low :
                    return 'long'
                
        elif MFI.iloc[-1] > self._high :
            return 'short'
        
        else : 
            return 'hold'
