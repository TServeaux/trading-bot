"""
Author : Tao Serveaux
Date : 21/09/2026
Description: Entry point script for the Telegram companion process. Loads
    Telegram credentials from environment variables and continuously polls
    Telegram for incoming commands (e.g. /stats), replying with trading
    statistics.
"""

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