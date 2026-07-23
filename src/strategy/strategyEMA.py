import pandas as pd
from .baseStrategie import BaseStrategie
import ta

class StrategieEMA(BaseStrategie):

    def __init__(self, candles, shortWindow = 9, longWindow = 21):
        super().__init__(candles)
        self._shortWindow = shortWindow
        self._longWindow = longWindow
        

    def signal(self):
        data = pd.DataFrame(self._candles, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume'])
        emaShort = ta.trend.EMAIndicator(close=data['close'], window=self._shortWindow).ema_indicator()
        emaLong = ta.trend.EMAIndicator(close=data['close'], window=self._longWindow).ema_indicator()

        if emaShort.iloc[-2] < emaLong.iloc[-2] and emaShort.iloc[-1] > emaLong.iloc[-1] :
            return 'long'
                
        elif emaShort.iloc[-2] > emaLong.iloc[-2] and emaShort.iloc[-1] < emaLong.iloc[-1] :
            return 'short'
                
        else :
            return 'hold'


