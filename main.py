from dotenv import load_dotenv
from src.bot import Bot
import os

load_dotenv()

apiKey = os.getenv('KRAKEN_API_KEY')
secretKey = os.getenv('KRAKEN_SECRET_KEY')

telegramChatId = os.getenv('TELEGRAM_CHAT_ID')
telegramToken = os.getenv('TELEGRAM_TOKEN')

symbol = 'TAO/USD:USD'

if __name__ == '__main__':
    bot = Bot(apiKey, secretKey, telegramToken, telegramChatId, symbol)
    bot.run()