import sqlite3
import pandas as pd

DB_FILE = "stock_data.db"
TABLE_NAME = "daily_prices"

# Add this temporary code to see your current table structure
def check_table_schema():
    with sqlite3.connect(DB_FILE) as conn:
        cursor = conn.cursor()
        cursor.execute(f"PRAGMA table_info({TABLE_NAME})")
        columns = cursor.fetchall()
        print("Current table schema:")
        for col in columns:
            print(f"  {col}")

# Call this before setup_database()
check_table_schema()



# Check for duplicate entries
def check_for_duplicates():
    with sqlite3.connect(DB_FILE) as conn:
        query = f"SELECT Ticker, Date, COUNT(*) FROM {TABLE_NAME} GROUP BY Ticker, Date HAVING COUNT(*) > 1"
        duplicates = pd.read_sql_query(query, conn)
        if not duplicates.empty:
            print("Duplicate entries found:")
            print(duplicates)
        else:
            print("No duplicate entries found.")

check_for_duplicates()


# get the most recent date in the database
def get_most_recent_date(ticker_symbol):
    """
    Fetches the most recent date for a given ticker symbol from the database.
    
    Args:
        ticker_symbol (str): The stock ticker symbol to query.
    
    Returns:
        str: The most recent date in 'YYYY-MM-DD' format, or None if no data is found.
    """
    with sqlite3.connect(DB_FILE) as conn:
        query = f"""
        SELECT MAX(Date) AS MostRecentDate
        FROM {TABLE_NAME}
        WHERE Ticker = ?
        """
        result = pd.read_sql_query(query, conn, params=(ticker_symbol,))
        
        if result.empty or pd.isna(result['MostRecentDate'].iloc[0]):
            print(f"No data found for {ticker_symbol}.")
            return None
        
        return result['MostRecentDate'].iloc[0]



""""""
# Check data for specific date 
def get_stock_data_for_date(ticker_symbol, date):
    """
    Fetches stock data for a specific ticker symbol and date from the database.
    
    Args:
        ticker_symbol (str): The stock ticker symbol to query.
        date (str): The date in 'YYYY-MM-DD' format to query.
    
    Returns:
        pd.DataFrame: A DataFrame containing the stock data for the specified ticker and date.
    """
    with sqlite3.connect(DB_FILE) as conn:
        query = f"""
        SELECT * FROM {TABLE_NAME}
        WHERE Ticker = ? AND Date = ?
        """
        df = pd.read_sql_query(query, conn, params=(ticker_symbol, date))
        
        if df.empty:
            print(f"No data found for {ticker_symbol} on {date}.")
            return None
        
        return df
    
# Checks
get_stock_data_for_date("AAPL", "2023-12-31") # no data for this date
get_stock_data_for_date("AAPL", "2024-01-01") # no data for this date
get_stock_data_for_date("AAPL", "2024-12-31")
get_stock_data_for_date("AAPL", "2025-01-01")  # no data for this date

get_stock_data_for_date("AAPL", "2020-12-31")
get_stock_data_for_date("AAPL", "2021-01-01") # no data for this date
get_stock_data_for_date("AAPL", "2021-12-31")
get_stock_data_for_date("AAPL", "2022-01-01") # no data for this date
get_stock_data_for_date("AAPL", "2022-12-31") # no data for this date
get_stock_data_for_date("AAPL", "2023-01-01") # no data for this date

