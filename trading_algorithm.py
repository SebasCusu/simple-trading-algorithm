import datetime
import sqlite3
import numpy as np
import yfinance as yf

# Database setup
conn = sqlite3.connect("finance_data.db")
cur = conn.cursor()

# Create history table
cur.execute(
    """
    CREATE TABLE IF NOT EXISTS history (
        ticker TEXT,
        date TEXT,
        current_price REAL,
        signal TEXT
    )
    """
)

def download_data(ticker):
    """
    Download market data and calculate moving averages.
    """
    data = yf.download(ticker, period="6mo", progress=False)

    if data.empty:
        print(f"Error: No data available for ticker {ticker}")
        return None

    close_prices = data["Close"].to_numpy().flatten()
    
    # Take the last 100 prices available
    prices_array = close_prices[-100:]
    
    # The last element in the array is the most recent price
    current_price = float(prices_array[-1])

    # Calculate Simple Moving Averages (SMA) using the clean numpy array
    fast_sma = np.mean(prices_array[-10:])
    slow_sma = np.mean(prices_array[-50:])

    return current_price, fast_sma, slow_sma

# Run strategy
tickers = ["AAPL","TSLA","MSFT","NFLX","NVDA","SPCX"]
for ticker in tickers:

    result = download_data(ticker)

    if result is None:
        continue

    current_price, fast_sma, slow_sma = result

        # Trading logic
    if fast_sma > slow_sma:
        signal = "Buy"
    elif fast_sma < slow_sma:
        signal = "Sell"
    else:
        signal = "Neutral"

    today = datetime.datetime.now().strftime("%Y-%m-%d")

    # Save result
    cur.execute(
            "INSERT INTO history VALUES (?, ?, ?, ?)",
            (ticker, today, current_price, signal),
        )
    conn.commit()

    # Show history
cur.execute("SELECT * FROM history")
saved_data = cur.fetchall()

print("\nHistory")
for row in saved_data:
    print(row)

conn.close()