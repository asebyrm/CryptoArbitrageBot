# 🪙 Crypto Arbitrage Bot

## Overview

This project implements a **high-frequency cryptocurrency arbitrage bot** that monitors price differences across multiple centralized exchanges and executes profitable trades automatically.

The goal of this bot is to detect and exploit temporary price inefficiencies between markets, allowing the user to profit from the differences in asset prices.

## ⚙️ Features

- **Multi-exchange support**: Works with major CEXs like Binance, KuCoin, Coinbase, and Crypto.com via [CCXT](https://github.com/ccxt/ccxt).
- **Real-time price monitoring** with millisecond-level polling.
- **Triangular and inter-exchange arbitrage detection**.
- **Transaction fee aware**: Calculates profit after deducting trading and transfer fees.
- **Asynchronous architecture** using Python `asyncio` for non-blocking operations.
- **Logging and trade history recording**.
- **Configurable thresholds** for minimum profit and asset volume.

## 🏗️ Architecture

```
┌──────────────────┐
│ Exchange Clients │ (via CCXT)
└──────────────────┘
         │
         ▼
┌─────────────────────┐
│ Price Fetcher (Live)│
└─────────────────────┘
         │
         ▼
┌─────────────────────┐
│ Arbitrage Detector  │
└─────────────────────┘
         │
         ▼
┌─────────────────────┐
│ Trade Executor       │
└─────────────────────┘
         │
         ▼
┌─────────────────────┐
│ Logger & Recorder   │
└─────────────────────┘
```

## 📦 Installation

```bash
git clone https://github.com/ahmetselim/crypto-arbitrage-bot.git
cd crypto-arbitrage-bot
pip install -r requirements.txt
```

## 🚀 Usage

Before starting, make sure to set your API keys in `exchange_controller.py` 
```bash
python main.py
```

## 🔐 Security Warning

> **Do not share your API keys or commit them to version control.**  


## 🧠 Future Improvements

- Web dashboard for monitoring
- Machine learning-based prediction for future inefficiencies
- Distributed architecture for faster polling
- Flashloan integration (if on-chain)

## 📜 License

MIT License.
