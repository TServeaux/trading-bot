import requests

class Notifier:

    def __init__(self, token, chatId):
        self._token = token
        self._chatId = chatId
        self._offset = 0
    
    def _sendMessage(self, text):
        url = f'https://api.telegram.org/bot{self._token}/sendMessage'
        r= requests.post(f'https://api.telegram.org/bot{self._token}/sendMessage',
                       data={'chat_id' : self._chatId, 'text' : text})
        
        if not r.json().get('ok'):
            print(f"ÉCHEC — URL: {url}")
            print(f"chat_id: '{self._chatId}'")
            print(f"text: '{text}'")
            print(f"réponse: {r.json()}")

        print(r.json())

    def sendTradeOpened(self, trade):
        text = (
            f"Trade ouvert : {trade['openTimestamp']}\n"
            f"Position : {trade['side']}\n"
            f"Prix : {trade['openPrice']}\n"
            f"Montant : {trade['amount']}"
        )
        self._sendMessage(text=text)
    
    def sendTradeClosed(self, trade):
        text = (
            f"Trade ferme : {trade['closedTimestamp']}\n"
            f"Prix : {trade['closedPrice']}\n"
            f"Profit : {trade['profit']}"
        )
        self._sendMessage(text=text)

    def sendError(self,err):
        self._sendMessage(text=err)