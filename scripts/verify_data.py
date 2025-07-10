# verify.py
import sqlite3
import pandas as pd

DB_FILE = "stock_data.db"

with sqlite3.connect(DB_FILE) as conn:
    # Check which tickers were added
    tickers_in_db = pd.read_sql("SELECT DISTINCT Ticker FROM daily_prices", conn)
    print("Tickers in database:")
    print(tickers_in_db)
    
    print("-" * 30)

    # Check the total number of records
    record_count = pd.read_sql("SELECT COUNT(*) FROM daily_prices", conn)
    print(f"Total records in database: {record_count.iloc[0,0]}")