import pandas as pd
from .baseStrategie import BaseStrategie
import ta

c:

    def __init__(self, candles, window=14):
        super().__init__(candles)
        self._window = window

    def signal(self):
        data = pd.DataFrame(self._candles, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume'])
        obv = ta.volume.OnBalanceVolumeIndicator(close=data['close'], volume=data['volume']).on_balance_volume()
        obvMean = obv.rolling(window=self._window).mean()

        if obv.iloc[-2] < obvMean.iloc[-2] and obv.iloc[-1] > obvMean.iloc[-1] :
            return 'long'

        elif obv.iloc[-2] > obvMean.iloc[-2] and obv.iloc[-1] < obvMean.iloc[-1] :
            return 'short'
                        
        else :
            return 'hold'