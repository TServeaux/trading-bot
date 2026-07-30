import time

class PaperExchange :

    def __init__(self, exchange, xLever):
        self._exchange =exchange
        self._trades = {}
        self._nextId = 0 
        self._lever = xLever

    def checkPrice(self, pair):
        
        return  self._exchange.fetch_ticker(pair)['last']

    def lever(self, xLever=10):
        self._lever = xLever

    def openPos(self, direction, symbol, amount, takeProfit=3, stopLoss=1.5):
        price = self.checkPrice(symbol)
        self._nextId += 1
        tradeId = str(self._nextId)

        if direction == 'long' :
            direction = 'buy'
            tp =  price * (1 + takeProfit/100)
            sl = price * (1 - stopLoss/100)

        else :
            direction = 'sell'
            sl =  price * (1 + stopLoss/100)
            tp = price * (1 - takeProfit/100)
        

        trade = {}

        trade['openTimestamp'] = int(time.time() * 1000)
        trade['symbol'] = symbol
        trade['side'] = direction
        trade['openPrice'] = price
        trade['status'] = 'open'
        trade['id'] = tradeId

        trade['takeProfit'] = tp
        trade['stopLoss'] = sl
        trade['amount'] = amount

        self._trades[tradeId] = trade

        return trade


    def closePos(self, id):
        price = self.checkPrice( self._trades[id]['symbol'])
    
        if self._trades[id]['side'] == 'buy' :
            variation = (price - self._trades[id]['openPrice']) / self._trades[id]['openPrice']
            profit = variation * self._trades[id]['amount'] * self._lever  
        else :
            variation = (self._trades[id]['openPrice'] - price) / self._trades[id]['openPrice']
            profit = variation * self._trades[id]['amount'] * self._lever

        self._trades[id]['closedTimestamp'] = int(time.time() * 1000)
        self._trades[id]['closedPrice'] = price
        self._trades[id]['status'] = 'closed'
        self._trades[id]['profit'] = profit

        return self._trades[id]
    
    def checkTPSL(self):
        closed = []

        for id, trade in self._trades.items():

            if trade['status'] == 'closed' :
                continue

            price = self.checkPrice(trade['symbol'])

            if trade['side'] == 'buy':
                if price >= trade['takeProfit'] or price <= trade['stopLoss']:
                    self.closePos(id)
                    closed.append(trade)
            
            else:
                if price <= trade['takeProfit'] or price >= trade['stopLoss']:
                    self.closePos(id)
                    closed.append(trade)
        
        return closed

    def getExchange(self):
        return self._exchange
    
    def getTrade(self, id):
        return self._trades[id]