import ccxt

class Exchange:
    
    def __init__(self, apiKey, secretKey, passPhrase):  
        
        self.__exchange = ccxt.bitget({
            'apiKey' : apiKey,
            'secret' : secretKey,
            'password' : passPhrase,
            'options' : {
                'defaultType' : 'swap'
            }
        })
                
        self.__pairsPrices = {}

    
    def checkPrice(self, pairList):
        
        for i in pairList :
            price = self.__exchange.fetch_ticker(f'{i}/USDT:USDT')
            self.__pairsPrices[i] = price
        
    def getExchange(self):
        return self.__exchange
        
    def lever(self):
        pass
    
    def setTakeProfit(self, takeProfit):
        pass
    
    def setStopLoss(self, stopLoss):
        pass
    
    def balanceAvalaible(self):
        pass
    
    def currentPos(self):
        pass
    
    def openPos(self, direction):
        pass
    
    def closePos(self):
        pass