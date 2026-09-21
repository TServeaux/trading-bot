"""
Author : Tao Serveaux
Date : 21/09/2026
Description: Sends Telegram notifications when a trade is opened or closed,
    or when an error occurs in the bot's main loop.
"""

import requests

class Notifier:

    def __init__(self, token, chatId,  symbol):
        """
        Description: Initialize the notifier with Telegram credentials and
            the trading symbol used in message text.

        Args:
            token (str): Telegram bot token.
            chatId (str): Telegram chat id to send messages to.
            symbol (str): Trading pair symbol shown in notifications.

        Returns:
            None
        """
        self._token = token
        self._chatId = chatId
        self._symbol = symbol
        self._offset = 0

    def _sendMessage(self, text):
        """
        Description: Send a raw text message to the configured Telegram
            chat, logging diagnostic details on failure.

        Args:
            text (str): Message text to send.

        Returns:
            None
        """
        url = f'https://api.telegram.org/bot{self._token}/sendMessage'
        r= requests.post(f'https://api.telegram.org/bot{self._token}/sendMessage',
                       data={'chat_id' : self._chatId, 'text' : text})

        if not r.json().get('ok'):
            print(f"ÉCHEC — URL: {url}")
            print(f"chat_id: '{self._chatId}'")
            print(f"text: '{text}'")
            print(f"réponse: {r.json()}")

        print(r.json())

    def sendTradeOpened(self, trade, strategy):
        """
        Description: Send a Telegram notification when a new trade is
            opened.

        Args:
            trade (dict): Trade record containing 'openTimestamp', 'side',
                'openPrice' and 'amount'.
            strategy (str): Name of the strategy combination that produced
                the trade.

        Returns:
            None
        """
        text = (
            f"Symbol : {self._symbol} | Strategie : {strategy}\n\n"
            f"Trade ouvert : {trade['openTimestamp']}\n"
            f"Position : {trade['side']}\n"
            f"Prix : {trade['openPrice']}\n"
            f"Montant : {trade['amount']}"
        )
        self._sendMessage(text=text)

    def sendTradeClosed(self, trade, strategy):
        """
        Description: Send a Telegram notification when a trade is closed.

        Args:
            trade (dict): Trade record containing 'closedTimestamp',
                'closedPrice' and 'profit'.
            strategy (str): Name of the strategy combination that closed
                the trade.

        Returns:
            None
        """
        text = (
            f"Symbol : {self._symbol} | Strategie : {strategy}\n\n"
            f"Trade ferme : {trade['closedTimestamp']}\n"
            f"Prix : {trade['closedPrice']}\n"
            f"Profit : {trade['profit']}"
        )
        self._sendMessage(text=text)

    def sendError(self,err):
        """
        Description: Send a Telegram notification reporting an error.

        Args:
            err (str): Error message to send.

        Returns:
            None
        """
        self._sendMessage(text=err)
