# Simple Moving Average Trading Bot

An automated Python script that fetches market data, generates trading signals using an SMA Crossover strategy, and logs the execution history into a local SQLite database.

## Features
* Automated data fetching from Yahoo Finance via yfinance.
* Flattens multi-index structures to ensure data stability.
* Calculates 10-day (fast) and 50-day (slow) moving averages using numpy.
* Logs ticker, execution date, current price, and trading signals in sqlite3.

## Requirements
Install the required dependencies before running the script:
```bash
pip install yfinance numpy
```

## Usage
Run the script to analyze the default asset (TSLA):
```bash
python trading_algorithm.py
```

## Strategy Logic
* Buy Signal: Fast SMA (10 days) is greater than Slow SMA (50 days).
* Sell Signal: Fast SMA (10 days) is lower than Slow SMA (50 days).
* Neutral Signal: Both moving averages are equal.

## Database Schema
Logs are stored locally in 'finance_data.db' under the 'history' table:
* ticker (TEXT)
* date (TEXT)
* current_price (REAL)
* signal (TEXT)

## Disclaimer
This project is for educational purposes only. It does not constitute financial or investment advice. Use at your own risk.
