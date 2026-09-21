# Trading Bot

Author: Tao Serveaux

## Purpose

This project is an automated cryptocurrency trading bot for **Kraken
Futures**. It watches a trading pair's candlestick data, evaluates several
technical-analysis strategies in parallel, and opens or closes leveraged
long/short positions automatically based on the signals they produce. It can
run against the real exchange or in a built-in **paper trading** (simulated)
mode, and it reports on its activity through Telegram.

The goal is to test and run multiple independent "strategy combinations" at
once, each with its own risk budget, position tracking and performance
statistics, so different indicator setups can be compared over time without
interfering with one another.

## Features

- **Kraken Futures connectivity** via `ccxt`, with leverage control, balance
  lookup, and market order execution with attached take-profit/stop-loss.
- **Paper trading mode**: simulates orders and PnL locally using real market
  prices, without sending any order to the exchange — useful for testing
  strategies risk-free.
- **Nine technical indicator strategies**, each returning a `long` / `short`
  / `hold` signal:
  - Bollinger Bands
  - MACD
  - On-Balance Volume (OBV)
  - RSI
  - ADX
  - Donchian Channels
  - EMA crossover
  - Money Flow Index (MFI)
  - Stochastic Oscillator
- **Combined strategies**: several indicators are grouped into named
  "combos" (e.g. `MACDxRSIxMFI`), and a combo only triggers a trade when
  enough of its indicators agree (configurable voting threshold).
- **Risk management**: each combo has its own cash allocation, a
  configurable percentage of capital risked per trade, and a maximum
  fraction of capital that can be engaged at once.
- **Automatic take-profit / stop-loss** on every opened position.
- **Telegram notifications** when a trade is opened, when it is closed, and
  when an error occurs.
- **Telegram commands** (via a separate process) to query performance
  statistics on demand: `/stats` (all combos) or `/stats <comboName>`
  (a specific combo).
- **Persistent statistics** per symbol and per combo (total trades, total
  profit, winrate, best/worst trade), saved to JSON files under `data/`.
- **Resilient main loop**: automatically handles exchange timeouts and rate
  limiting without crashing.

## Project structure

```
main.py                    Entry point: starts the trading bot
mainTelegram.py             Entry point: starts the Telegram command listener
requirements.txt            Python dependencies

src/
  bot.py                    Main trading loop orchestration (Bot class)

  core/
    exchange.py              Kraken Futures client wrapper (real trading)
    paperExchange.py         Simulated exchange for paper trading
    dataFeed.py               Candle (OHLCV) data fetching
    orderManager.py           Opens/closes positions based on signals

  strategy/
    baseStrategie.py          Abstract base class for all strategies
    combinedStrategy.py       Aggregates multiple strategies into a signal
    strategieRSI.py            RSI strategy
    strategieMACD.py           MACD strategy
    strategieOBV.py            OBV strategy
    strategieBollinger.py      Bollinger Bands strategy
    strategyADX.py             ADX strategy
    strategyDonchian.py        Donchian Channels strategy
    strategyEMA.py              EMA crossover strategy
    strategyMFI.py              MFI strategy
    strategyStochastic.py       Stochastic Oscillator strategy

  risk/
    riskManager.py            Capital allocation and exposure limits

  utils/
    notifier.py                Telegram trade/error notifications
    stats.py                   Performance statistics tracking/persistence
    telegramService.py         Telegram command polling and stats replies

data/                        JSON files with saved per-symbol/per-combo stats
```

## Setup

1. Install dependencies:

   ```
   pip install -r requirements.txt
   ```

2. Create a `.env` file at the project root with:

   ```
   KRAKEN_API_KEY=your_kraken_api_key
   KRAKEN_SECRET_KEY=your_kraken_secret_key
   TELEGRAM_TOKEN=your_telegram_bot_token
   TELEGRAM_CHAT_ID=your_telegram_chat_id
   SYMBOL=TAO/USD:USD   # optional, defaults to TAO/USD:USD
   ```

## Usage

Run the trading bot (paper mode by default):

```
python main.py
```

Run the Telegram command listener (in a separate process) to receive
`/stats` replies:

```
python mainTelegram.py
```

## Disclaimer

This bot trades with real funds when paper mode is disabled. Cryptocurrency
and leveraged futures trading carries a substantial risk of loss. Use at
your own risk, start with paper mode, and never trade with money you cannot
afford to lose.
