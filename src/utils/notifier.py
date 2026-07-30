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
    
    def sendStats(self, strategies):

        text = "📊 Statistiques\n\n"

        for name, data in strategies.items():
            stats, trades = data['stats'].getStats()
            text += f"{name}\n"
            text += f"Trades: {stats['totalsTrades']} | "
            text += f"Winrate: {stats['winrate']:.0f}%\n\n"

        self._sendMessage(text)

    def sendComboStat(self, comboName, strategies):
        
        stats, trades = strategies[comboName]["stats"].getStats()

        text = "📊 Statistiques de " + comboName + "\n\n"
        text += f"Winrate: {stats['winrate']:.0f}%\n"
        text += f"Nombres Total de trades : {stats['totalsTrades']}\n"
        text += f"Position actuelle :\n"
        text += f"Profit total : {stats['totalsProfits']:.2f}€\n"
        text += f"Best Trade : {stats['bestTrade']} |"
        text += f"Worst Trade : {stats['worstTrade']}\n\n"

        self._sendMessage(text)

    def sendCombos(self, strategies) :

        text = "Liste des combos\n\n"

        for name in strategies.keys() :
            text += name+"\n"

        self._sendMessage(text)

    def getUpdates(self):
        url = f'https://api.telegram.org/bot{self._token}/getUpdates'
        r = requests.get(url, params={'offset': self._offset})
        data = r.json()

        received = []                             
    
        for update in data['result']:             
            texte = update['message']['text']
            received.append(texte)
            self._offset = update['update_id'] + 1  
        
        return received

    def getCommand(self, strategies):

        received = self.getUpdates()

        for mess in received :
            parts = mess.split()
            if parts[0] == '/stats':

                if len(parts) > 1 :

                    if parts[1] in strategies:
                        self.sendComboStat(parts[1], strategies)
                        
                    else:
                        self._sendMessage(f"Combo inconnu : {parts[1]}")
                    
                else :
                    self.sendStats(strategies)

            elif parts[0] == '/combos' :
                self.sendCombos(strategies)