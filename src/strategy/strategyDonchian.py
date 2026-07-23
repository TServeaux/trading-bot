import pandas as pd
from .baseStrategie import BaseStrategie
import ta

class StrategyDonchian(BaseStrategie):

    def __init__(self, candles, window = 20):
        super().__init__(candles)
        self._window = window

    def signal(self):
        data = pd.DataFrame(self._candles, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume'])
        donchian = ta.volatility.DonchianChannel(high=data['high'], low=data['low'], 
                                          close=data['close'], window=self._window)
        lowDon = donchian.donchian_channel_lband()
        highDon = donchian.donchian_channel_hband()

        if data['close'].iloc[-1] > highDon.iloc[-1] :
            return 'long'

        elif data['close'].iloc[-1] < lowDon.iloc[-1] :
            return 'short'

        else : 
            return 'hold'
        
