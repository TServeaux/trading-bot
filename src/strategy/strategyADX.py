import pandas as pd
from .baseStrategie import BaseStrategie
import ta

class StrategieADX(BaseStrategie):

    def __init__(self, candles, window = 14, seuil = 24):
        super().__init__(candles)
        self._window = window
        self._seuil = seuil

    def signal(self):
        data = pd.DataFrame(self._candles, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume'])
        indicators = ta.trend.ADXIndicator(high=data['high'], low=data['low'], close=data['close'], window=self._window)

        adx = indicators.adx()
        pos = indicators.adx_pos()
        neg = indicators.adx_neg()

        if adx.iloc[-1] > self._seuil :

            if pos.iloc[-1] < neg.iloc[-1] :
                return 'short'
            
            else :
                return 'long'
            
        else :
            return 'hold'