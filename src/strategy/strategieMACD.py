import pandas as pd
from .baseStrategie import BaseStrategie
import ta

class StrategieMACD(BaseStrategie):

    def __init__(self, candles):
        super().__init__(candles)
    
    def signal(self):

        data = pd.DataFrame(self._candles, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume'])
        macd = ta.trend.MACD(close=data['close'])

        macdSignal = macd.macd_signal()
        macdLine = macd.macd()

        if macdLine.iloc[-2] < macdSignal.iloc[-2] and macdLine.iloc[-1] > macdSignal.iloc[-1] :
            return 'long'
        
        elif macdLine.iloc[-2] > macdSignal.iloc[-2] and macdLine.iloc[-1] < macdSignal.iloc[-1] :
            return 'short'
        
        else :
            return 'hold'
