"""
Author : Tao Serveaux
Date : 21/09/2026
Description: Entry point script for the live/paper trading bot. Loads
    configuration (API keys, Telegram credentials, trading symbol) from
    environment variables, defines the strategy combinations to run, and
    starts the Bot's main loop.
"""

from dotenv import load_dotenv
from src.bot import Bot
import os

from src.strategy.strategieRSI import StrategieRSI
from src.strategy.strategieMACD import StrategieMACD
from src.strategy.strategyMFI import StrategyMFI
from src.strategy.strategyEMA import StrategieEMA
from src.strategy.strategyStochastic import StrategieStochastic
from src.strategy.strategieOBV import StrategyOBV
from src.strategy.strategyADX import StrategieADX
from src.strategy.strategyDonchian import StrategyDonchian
from src.strategy.strategieBollinger import StrategieBollinger

load_dotenv()

apiKey = os.getenv('KRAKEN_API_KEY')
secretKey = os.getenv('KRAKEN_SECRET_KEY')

telegramChatId = os.getenv('TELEGRAM_CHAT_ID')
telegramToken = os.getenv('TELEGRAM_TOKEN')

symbol = os.getenv('SYMBOL', 'TAO/USD:USD')

if __name__ == '__main__':
    combos = {'MACDxRSIxMFI' : [StrategieMACD,StrategieRSI,StrategyMFI],
              'EMAxStochxOBV' :[StrategieEMA,StrategieStochastic,StrategyOBV],
              'MACDxRSIxADX' : [StrategieMACD,StrategieRSI,StrategieADX],
              'DonchianxADXxMFI' : [StrategyDonchian,StrategieADX,StrategyMFI],
              'BollingerxRSIxMFI' : [StrategieBollinger,StrategieRSI,StrategyMFI]
              }
    bot = Bot(apiKey, secretKey, telegramToken, telegramChatId, symbol, combos=combos)
    bot.run()