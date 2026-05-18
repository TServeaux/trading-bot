
class DataFeed:
    
    def __init__(self, exchange) :
        
        self.__exchange = exchange.getExchange()
    
    def getCandles(self, symbol, timeFrame, limit) :
        
        candles = self.__exchange.fetch_ohlcv(symbol, timeFrame, limit)
        
        return candles