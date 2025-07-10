"""
Stock Data Fetcher - Enhanced from original main.py

Handles fetching historical and real-time stock data from yfinance
and populating the SQLite database.
"""

import sqlite3
import pandas as pd
import yfinance as yf
from datetime import date

# --- Configuration for Initial Data Population ---
DB_FILE = "../../data/stock_data.db"
TABLE_NAME = "daily_prices"
TICKERS_TO_POPULATE = ["NVDA", "META", "MSFT", "IYK", "IYC", "MCHI", "EWJ","AMZN", "AAPL", "GOOGL", "SPY", "QQQ", "IYE", "IYF"]
START_DATE = "2025-01-01"     # "2024-01-01"
# The yfinance 'end' date is exclusive, so to include 12/31, we set it to the next day.
END_DATE = "2025-05-30"       # outputs data thru 5/29/2025


# --- Reusable Functions from Previous Discussions ---
def setup_database():
    """Creates the SQLite database and the necessary table if they don't exist."""
    print("Setting up database...")
    with sqlite3.connect(DB_FILE) as conn:
        cursor = conn.cursor()
        cursor.execute(f"""
            CREATE TABLE IF NOT EXISTS {TABLE_NAME} (
                Ticker TEXT NOT NULL,
                Date TEXT NOT NULL,
                Open REAL NOT NULL,
                High REAL NOT NULL,
                Low REAL NOT NULL,
                Close REAL NOT NULL,
                "Adj Close" REAL NOT NULL,
                Volume INTEGER NOT NULL,
                PRIMARY KEY (Ticker, Date)
            )
        """)
        conn.commit()
    print("Database setup complete.")


def preprocess_data_for_db(df: pd.DataFrame, ticker_symbol: str) -> pd.DataFrame:
    """Prepares a DataFrame to match the database schema."""
    if df.empty:
        return df
        
    df.reset_index(inplace=True)
    df['Ticker'] = ticker_symbol
    
    # Fix MultiIndex columns - flatten them to simple column names
    if isinstance(df.columns, pd.MultiIndex):
        # For MultiIndex columns, take the first level (the main column name)
        ## "For each column tuple, take the first element if it exists and isn't empty, otherwise take the second element."
        df.columns = [col[0] if col[0] else col[1] for col in df.columns]
    
    db_columns = ['Ticker', 'Date', 'Open', 'High', 'Low', 'Close', 'Adj Close', 'Volume']
    for col in db_columns:
        if col not in df.columns:
            raise ValueError(f"Data for {ticker_symbol} is missing required column: '{col}'")
    
    df = df[db_columns]
    df['Date'] = pd.to_datetime(df['Date']).dt.strftime('%Y-%m-%d')
    return df



# --- Main Script Logic ---

def populate_initial_data():
    """
    Fetches historical data for a list of tickers for a specified
    date range and saves it to the database.
    """
    print(f"\nStarting initial data population for {len(TICKERS_TO_POPULATE)} tickers...")
    
    with sqlite3.connect(DB_FILE) as conn:
        for ticker in TICKERS_TO_POPULATE:
            try:
                print(f"  Fetching data for {ticker} from {START_DATE} to {END_DATE}...")
                
                # Download data from yfinance
                data = yf.download(ticker, start=START_DATE, end=END_DATE, auto_adjust=False)
                
                if data.empty:
                    print(f"  WARNING: No data returned for {ticker}.")
                    continue

                # Clean and format the data
                cleaned_data = preprocess_data_for_db(data, ticker)

                # DEBUG: Print DataFrame info
                print(f"  DEBUG - DataFrame shape: {cleaned_data.shape}")
                print(f"  DEBUG - DataFrame columns: {list(cleaned_data.columns)}")
                print(f"  DEBUG - DataFrame dtypes:\n{cleaned_data.dtypes}")
                print(f"  DEBUG - First few rows:\n{cleaned_data.head()}")
                print(f"  DEBUG - DataFrame index: {cleaned_data.index}")

                # Save the cleaned data to the database
                cleaned_data.to_sql(TABLE_NAME, conn, if_exists='append', index=False)
                
                print(f"  Successfully saved {len(cleaned_data)} records for {ticker}.")

            except Exception as e:
                print(f"  ERROR: Failed to process data for {ticker}. Reason: {e}")
    
    print("\nInitial data population complete.")




if __name__ == "__main__":
    # 1. Create the database and table schema
    setup_database()
    
    # 2. Populate it with the 2024 historical data
    populate_initial_data()


