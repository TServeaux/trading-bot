"""
Author : Tao Serveaux
Date : 21/09/2026
Description: Defines the Bot class, which orchestrates the main trading
    loop: fetching market data, computing strategy signals for every
    configured combination, and dispatching orders while handling exchange
    errors and rate limits.
"""

import time
import ccxt

from .core.exchange import Exchange
from .core.dataFeed import DataFeed
from .core.orderManager import OrderManager
from .core.paperExchange import PaperExchange

from .strategy.combinedStrategy import CombinedStrategie

from .risk.riskManager import RiskManager

from .utils.notifier import Notifier
from .utils.stats import Stats

class Bot:

    def __init__(self, apiKey, secretKey, tokenTelegram, chatId, symbol, combos, paperMode=True,
                 xLever=5, takeProfit=3, stopLoss=1.5, pourcentage=0.2,temps=900, timeFrame='15m', limit=100):
        """
        Description: Initialize the bot: connect to the exchange (real or
            paper), set up the notifier and data feed, and instantiate a
            dedicated risk manager, order manager, and stats tracker for
            each configured strategy combination.

        Args:
            apiKey (str): Kraken Futures API key.
            secretKey (str): Kraken Futures API secret.
            tokenTelegram (str): Telegram bot token used for notifications.
            chatId (str): Telegram chat id used for notifications.
            symbol (str): Trading pair symbol to trade.
            combos (dict): Mapping of combination name to a list of
                strategy classes.
            paperMode (bool, optional): If True, trade on the simulated
                PaperExchange instead of the real exchange. Defaults to
                True.
            xLever (int, optional): Leverage multiplier. Defaults to 5.
            takeProfit (float, optional): Take-profit distance in percent.
                Defaults to 3.
            stopLoss (float, optional): Stop-loss distance in percent.
                Defaults to 1.5.
            pourcentage (float, optional): Fraction of available cash to
                allocate per trade. Defaults to 0.2.
            temps (int, optional): Fallback loop interval in seconds,
                overwritten by setTime() based on timeFrame. Defaults to
                900.
            timeFrame (str, optional): Candle timeframe used to fetch data
                and pace the loop (e.g. '15m'). Defaults to '15m'.
            limit (int, optional): Number of candles to fetch per iteration.
                Defaults to 100.

        Returns:
            None
        """

        self._timeFrame = timeFrame
        self._symbol = symbol
        self._limit = limit
        self._takeProfit = takeProfit
        self._stopLoss = stopLoss
        self._pourcentage = pourcentage
        self._paperMode = paperMode
        self._lever = xLever
        self._combos = combos
        self._time = temps


        realExchange = Exchange(apiKey, secretKey)

        if paperMode:
            self._exchange = PaperExchange(realExchange.getExchange(), xLever)
        else:
            self._exchange = realExchange

        self._notifier = Notifier(tokenTelegram, chatId, self._symbol)
        self._dataFeed = DataFeed(self._exchange)
        self.setTime()

        self._strategies = {}
        for name, strats in combos.items():
            risk, stats = RiskManager(), Stats(self._symbol)
            stats.loadData(f'{name}.json')
            self._strategies[name] = {
                'combo': strats,
                'risk': risk,
                'order': OrderManager(self._exchange, risk, self._symbol, self._notifier, stats, name),
                'stats': stats
            }

    def setTime(self):
        """
        Description: Parse the configured timeframe string (e.g. '15m',
            '1h') and convert it into a number of seconds used to pace the
            main loop.

        Args:
            None

        Returns:
            None
        """
        letters = ['s','m','h','d']
        seconds = [1,60,3600,86400]

        for i in range(len(letters)):
            if letters[i] in self._timeFrame :
                tps = self._timeFrame.split(letters[i])[0]
                self._time = int(tps)*seconds[i]


    def run(self):
        """
        Description: Run the bot's main loop indefinitely: fetch candles,
            compute combined strategy signals, dispatch orders for each
            strategy combination, and handle exchange errors (timeouts,
            rate limiting, unexpected failures) by notifying and pausing
            before retrying.

        Args:
            None

        Returns:
            None
        """
        print("Bot démarré")

        while True :
            errorOccured = False

            try :
                candles = self._dataFeed.getCandles(self._symbol, self._timeFrame, self._limit)
                print(f"Prix actuel : {self._exchange.checkPrice(self._symbol)}")
                print(f"Nombre de bougies : {len(candles)}")

                signaux = CombinedStrategie(candles, self._combos).signal()
                print(f"Signaux : {signaux}")

                if self._paperMode:
                    self._exchange.checkTPSL()

                for key, signal in signaux.items():
                    self._strategies[key]['order'].takeOrder(signal, self._takeProfit, self._stopLoss, self._pourcentage)

            except ccxt.RequestTimeout as err :
                self._notifier.sendError(str(err))
                errorOccured = True

            except ccxt.DDoSProtection as err :
                self._notifier.sendError("Rate limit atteint. Pause de 60s...")
                time.sleep(60)
                errorOccured = True

            except Exception as err :
                self._notifier.sendError(f"Erreur critique imprévue : {err}")
                errorOccured = True

            if not errorOccured :
                time.sleep(self._time)
            else :
                time.sleep(30)
