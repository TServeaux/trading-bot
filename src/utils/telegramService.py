import json
import os
import requests

class TelegramService:
    
    def __init__(self, token, chatId):
        self._token = token
        self._chatId = chatId
        self._offset = 0
    
    def readAllData(self):
        
        datas = os.listdir('data')
        files = [f for f in datas if f.endswith('.json')]
        export = {}
        
        for file in files :
            
            path = os.path.join('data', file)
            nom = file.replace('.json', '')
                  
            crypto, combo = nom.split('_')
            
            if crypto not in export :
                export[crypto] = {}
             
            with open(path) as f :
                data = json.load(f)
            
            export[crypto][combo] = data['stats']
        
        return export

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
    
    def sendStats(self):
        data = self.readAllData()
        text = "📊 Statistiques\n\n"
            
        for crypto, combos in data.items():
            text += f"=== {crypto} ===\n"
            for combo, stats in combos.items():
                text += f"{combo} : {stats['totalsTrades']} trades | {stats['winrate']:.0f}% | Profit : {stats['totalsProfits']:.2f}$\n"
            
        self._sendMessage(text)
        
    def sendComboStat(self, comboName):
                
        data = self.readAllData()
        text = f"📊 Statistiques du combo {comboName}\n\n"
        
        for crypto, combos in data.items() :
            if comboName in combos:
                stats = combos[comboName]
                text += f"=== {crypto} ===\n"
                text += f"Winrate : {stats['winrate']:.0f}%\n"
                text += f"Trades : {stats['totalsTrades']}\n"
                text += f"Profit total : {stats['totalsProfits']:.2f}$\n"
                text += f"Best : {stats['bestTrade']:.2f} | Worst : {stats['worstTrade']:.2f}\n\n"
        
        self._sendMessage(text)  
    
    def getUpdates(self):
        url = f'https://api.telegram.org/bot{self._token}/getUpdates'
        r = requests.get(url, params={'offset': self._offset}, timeout=30)
        data = r.json()

        received = []                             
    
        for update in data['result']:             
            texte = update['message']['text']
            received.append(texte)
            self._offset = update['update_id'] + 1  
        
        return received

    def getCommand(self):

        data = self.readAllData()
        received = self.getUpdates()

        for mess in received :
            parts = mess.split()
            if parts[0] == '/stats':

                if len(parts) > 1 :
                    self.sendComboStat(parts[1])
                    
                else :
                    self.sendStats()