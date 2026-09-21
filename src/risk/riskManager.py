"""
Author : Tao Serveaux
Date : 21/09/2026
Description: Tracks available cash and the amount of capital currently
    engaged in trades, and decides how much capital can be allocated to a
    new trade without exceeding the configured maximum exposure.
"""

class RiskManager:

    def __init__(self, cash=100, maxTradingInvestement=0.5):
        """
        Description: Initialize the risk manager with a starting cash
            balance and a maximum fraction of cash that can be engaged at
            once.

        Args:
            cash (float, optional): Starting cash balance. Defaults to 100.
            maxTradingInvestement (float, optional): Maximum fraction of
                total cash that can be engaged in trades at the same time.
                Defaults to 0.5.

        Returns:
            None
        """
        self._cash = cash
        self._maxTradingInvestement = maxTradingInvestement
        self._engaged = 0

    def manageCash(self,profit):
        """
        Description: Apply a trade's profit or loss to the cash balance.

        Args:
            profit (float): Profit (positive) or loss (negative) from a
                closed trade.

        Returns:
            None
        """
        self._cash += profit

    def trade(self, pourcentage=0.20):
        """
        Description: Compute the amount of cash to allocate to a new trade,
            based on a percentage of the current balance, while respecting
            the maximum engaged-capital limit.

        Args:
            pourcentage (float, optional): Fraction of cash to allocate to
                the trade. Defaults to 0.20.

        Returns:
            float: The amount of cash allocated to the trade, or -1 if the
                trade cannot be funded (insufficient cash or exposure limit
                reached).
        """
        if self._cash < 1 :
            return -1

        elif self._engaged + pourcentage * self._cash > self._cash * self._maxTradingInvestement:
            return -1

        else :
            self._engaged += pourcentage * self._cash
            return pourcentage * self._cash

    def releaseCash(self,amount):
        """
        Description: Release previously engaged cash after a trade has been
            closed.

        Args:
            amount (float): Amount of cash to release from the engaged
                total.

        Returns:
            None
        """
        self._engaged -= amount

    def getCash(self):
        """
        Description: Return the current cash balance.

        Args:
            None

        Returns:
            float: Current cash balance.
        """
        return self._cash
