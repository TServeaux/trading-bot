from dotenv import load_dotenv
from src.utils.telegramService import TelegramService
import os
import time

load_dotenv()

telegramChatId = os.getenv('TELEGRAM_CHAT_ID')
telegramToken = os.getenv('TELEGRAM_TOKEN')

if __name__ == "__main__" :
    
    try :
        telegramBot = TelegramService(telegramToken, telegramChatId)
        time.wait(3)
        
    except :
        time.wait(30)