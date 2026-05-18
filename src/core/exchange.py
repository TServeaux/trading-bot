import ccxt
import numpy as np

class Exchange:
    
    def __init__(self, apiKey, secretKey):  
        
        self.__exchange = ccxt.krakenfutures({
            'apiKey' : apiKey,
            'secret' : secretKey,
        })

        self.__balance = {}
        self.__trades = {}
    
    def checkPrice(self, pair):
  
        return  self.__exchange.fetch_ticker(pair)['last']
        
    def lever(self, pair, xLever=10):

        self.__exchange.set_leverage(xLever, pair)

    
    def balanceAvailable(self):

        currentBalance = self.__exchange.fetch_balance()

        self.__balance['total'] = currentBalance['total']['USDT']
        self.__balance['free'] = currentBalance['free']['USDT']
        self.__balance['used'] = currentBalance['used']['USDT']

        return self.__balance

    
    def currentPos(self):
        
        return self.__exchange.fetch_positions()
    
    def openPos(self, direction, symbol, amount, takeProfit=30, stopLoss=20):
        
        price = self.checkPrice(symbol)

        if direction == 'long' :
            direction = 'buy'
            tp =  price * (1 + takeProfit/100)
            sl = price * (1 - stopLoss/100)

        else :
            direction = 'sell'
            sl =  price * (1 + stopLoss/100)
            tp = price * (1 - takeProfit/100)
        
        info = self.__exchange.create_order(symbol, 'market', direction, amount,
                                            params={
                                                'takeProfitPrice' : tp,
                                                'stopLossPrice' : sl
                                            })

        trade = {}

        trade['openTimestamp'] = info['timestamp']
        trade['symbol'] = info['symbol']
        trade['side'] = info['side']
        trade['openPrice'] = info['price']
        trade['status'] = info['status']

        trade['takeProfit'] = tp
        trade['stopLoss'] = sl
        trade['amount'] = amount

        self.__trades[info['id']] = trade

        return trade

    
    def closePos(self, id):

        if self.__trades[id]['side'] == 'buy' :
            direction = 'sell'
        
        else :
            direction = 'buy'

        info = self.__exchange.create_order(self.__trades[id]['symbol'], 'market',
                                             direction, self.__trades[id]['amount'])
        
        if self.__trades[id]['side'] == 'buy' :
            profit = info['price'] - self.__trades[id]['openPrice']
        else :
            profit = self.__trades[id]['openPrice'] - info['price']

        self.__trades[id]['closedTimestamp'] = info['timestamp']
        self.__trades[id]['closedPrice'] = info['price']
        self.__trades[id]['status'] = 'closed'
        self.__trades[id]['profit'] = profit

        return self.__trades[id]