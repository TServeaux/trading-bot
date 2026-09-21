"""
Author : Tao Serveaux
Date : 21/09/2026
Description: Tracks and persists trading performance statistics (total
    trades, profit, winrate, best/worst trade) to a JSON file per symbol
    and strategy combination.
"""

import json
import os

class Stats:

    def __init__(self, symbol):
        """
        Description: Initialize an empty statistics tracker for a trading
            symbol.

        Args:
            symbol (str): Trading pair symbol (e.g. 'BTC/USD:USD'); only the
                base asset (before the '/') is kept for file naming.

        Returns:
            None
        """

        self._totalTrades = 0
        self._totalProfit = 0
        self._bestTrade = 0
        self._worstTrade = 0
        self._winrate = 0
        self._win = 0
        self._lose = 0
        self._alltrade = []
        self._symbol = symbol.split('/')[0]

    def tradeFinished(self,trade):
        """
        Description: Record a closed trade's outcome, updating aggregate
            statistics (totals, best/worst trade, winrate) and the trade
            history.

        Args:
            trade (dict): Closed trade record containing 'profit',
                'closedTimestamp', 'openTimestamp', 'openPrice' and
                'closedPrice'.

        Returns:
            None
        """

        self._totalTrades += 1
        self._totalProfit += trade['profit']

        if trade['profit'] < 0:
            if abs(self._worstTrade) < abs(trade['profit']) :
                self._worstTrade = trade['profit']

            self._lose += 1

        else :
            if self._bestTrade < trade['profit'] :
                self._bestTrade = trade['profit']

            self._win += 1

        self._winrate = (self._win/self._totalTrades)*100

        resume = {}
        for i in ['closedTimestamp', 'openTimestamp', 'openPrice', 'closedPrice', 'profit'] :
            resume[i] = trade[i]

        self._alltrade.append(resume)

    def getStats(self):
        """
        Description: Build a summary dictionary of the current aggregate
            statistics, along with the full trade history.

        Args:
            None

        Returns:
            tuple: A tuple (stats, trades) where stats is a dict with keys
                'totalsTrades', 'totalsProfits', 'bestTrade', 'worstTrade',
                'winrate', 'win', 'lose', and trades is the list of recorded
                trade summaries.
        """

        stats = {}

        stats['totalsTrades'] = self._totalTrades
        stats['totalsProfits'] = self._totalProfit
        stats['bestTrade'] = self._bestTrade
        stats['worstTrade'] = self._worstTrade
        stats['winrate'] = self._winrate
        stats['win'] = self._win
        stats['lose'] = self._lose

        return stats, self._alltrade

    def saveData(self, filename):
        """
        Description: Persist the current statistics and trade history to a
            JSON file under the 'data' directory, prefixed with the symbol.

        Args:
            filename (str): Base filename to save to (will be prefixed with
                the symbol, e.g. 'BTC_<filename>').

        Returns:
            None
        """

        os.makedirs('data', exist_ok=True)

        filename = f"{self._symbol}_{filename}"
        path = os.path.join('data', filename)
        stats, trades = self.getStats()
        data = {'stats' : stats, 'trades' : trades}

        with open(path, 'w') as f :
            json.dump(data, f, indent=4)

    def loadData(self, filename):
        """
        Description: Load previously saved statistics and trade history
            from a JSON file under the 'data' directory, if it exists.

        Args:
            filename (str): Base filename to load from (will be prefixed
                with the symbol, e.g. 'BTC_<filename>').

        Returns:
            None
        """

        filename = f"{self._symbol}_{filename}"
        path = os.path.join('data', filename)

        if not os.path.exists(path):
            return

        with open(path, 'r') as f:
            data = json.load(f)

        stats = data['stats']

        self._totalTrades = stats['totalsTrades']
        self._totalProfit = stats['totalsProfits']
        self._bestTrade = stats['bestTrade']
        self._worstTrade = stats['worstTrade']
        self._winrate = stats['winrate']
        self._win = stats['win']
        self._lose = stats['lose']
        self._alltrade = data['trades']
