from dotenv import load_dotenv
from src.utils.telegramService import TelegramService
import os
import time

load_dotenv()

telegramChatId = os.getenv('TELEGRAM_CHAT_ID')
telegramToken = os.getenv('TELEGRAM_TOKEN')

if __name__ == "__main__" :
    
    telegramBot = TelegramService(telegramToken, telegramChatId)
    
    while True:
        try:
            telegramBot.getCommand()
        except Exception as e:
            print(e)
        time.sleep(2)