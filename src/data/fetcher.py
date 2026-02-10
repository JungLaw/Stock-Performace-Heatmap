"""
Stock Data Fetcher - Enhanced from original main.py

Handles fetching historical and real-time stock data from yfinance
and populating the SQLite database.
"""

import sqlite3
import pandas as pd
import yfinance as yf
from datetime import date
import os

# --- Configuration for Initial Data Population ---
#DB_FILE = "../../data/stock_data.db"
# Resolve database path relative to project root
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
DB_FILE = os.path.join(PROJECT_ROOT, "data", "stock_data.db")

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




# --- New Robust Data Fetching with Validation ---

def validate_fetch_parameters(tickers, start_date, end_date):
    """
    Validates input parameters for data fetching.
    
    Args:
        tickers (list or str): Stock ticker symbol(s) to fetch.
        start_date (str): Start date in 'YYYY-MM-DD' format.
        end_date (str): End date in 'YYYY-MM-DD' format.
    
    Raises:
        ValueError: If any parameter is invalid.
    """
    # Normalize tickers to list
    if isinstance(tickers, str):
        tickers = [tickers]
    
    if not tickers or not all(isinstance(t, str) and t.strip() for t in tickers):
        raise ValueError("Tickers must be non-empty strings. Received: {tickers}")
    
    # Validate date formats
    from datetime import datetime
    try:
        start_dt = datetime.strptime(start_date, '%Y-%m-%d')
        end_dt = datetime.strptime(end_date, '%Y-%m-%d')
    except ValueError as e:
        raise ValueError(f"Dates must be in 'YYYY-MM-DD' format. Error: {e}")
    
    # Validate date range logic
    if start_dt > end_dt:
        raise ValueError(f"start_date ({start_date}) cannot be after end_date ({end_date})")
    
    return [t.upper() for t in tickers]


def check_database_coverage(tickers, start_date, end_date):
    """
    Checks what date ranges already exist in the database for given tickers.
    Reports overlaps and suggests corrected date ranges.
    
    Args:
        tickers (list): Stock ticker symbols to check.
        start_date (str): Requested start date in 'YYYY-MM-DD' format.
        end_date (str): Requested end date in 'YYYY-MM-DD' format.
    
    Returns:
        dict: Coverage information with overlap details and suggested date ranges.
    """
    coverage = {}
    
    with sqlite3.connect(DB_FILE) as conn:
        for ticker in tickers:
            query = f"""
            SELECT MIN(Date) AS min_date, MAX(Date) AS max_date, COUNT(*) AS record_count
            FROM {TABLE_NAME}
            WHERE Ticker = ?
            """
            result = pd.read_sql_query(query, conn, params=(ticker,))
            
            if not result.empty and pd.notna(result['min_date'].iloc[0]):
                min_date = result['min_date'].iloc[0]
                max_date = result['max_date'].iloc[0]
                record_count = int(result['record_count'].iloc[0])
                
                # Check for overlaps
                overlap_start = max(start_date, min_date)
                overlap_end = min(end_date, max_date)
                has_overlap = overlap_start <= overlap_end
                
                coverage[ticker] = {
                    'exists_in_db': True,
                    'db_min_date': min_date,
                    'db_max_date': max_date,
                    'record_count': record_count,
                    'has_overlap': has_overlap,
                    'overlap_start': overlap_start if has_overlap else None,
                    'overlap_end': overlap_end if has_overlap else None,
                }
            else:
                coverage[ticker] = {
                    'exists_in_db': False,
                    'db_min_date': None,
                    'db_max_date': None,
                    'record_count': 0,
                    'has_overlap': False,
                    'overlap_start': None,
                    'overlap_end': None,
                }
    
    return coverage


def print_coverage_report(coverage, requested_start, requested_end):
    """
    Prints a user-friendly report of database coverage and overlaps.
    Suggests alternative date ranges if overlaps are detected.
    
    Args:
        coverage (dict): Output from check_database_coverage().
        requested_start (str): Requested start date.
        requested_end (str): Requested end date.
    
    Returns:
        bool: True if any overlaps exist, False otherwise.
    """
    print("\n" + "="*80)
    print("DATABASE COVERAGE REPORT")
    print("="*80)
    
    any_overlaps = False
    
    for ticker, info in coverage.items():
        print(f"\n{ticker}:")
        
        if not info['exists_in_db']:
            print(f"  ✓ No existing data. Safe to fetch {requested_start} to {requested_end}.")
        else:
            print(f"  Existing data range: {info['db_min_date']} to {info['db_max_date']} ({info['record_count']} records)")
            
            if info['has_overlap']:
                any_overlaps = True
                print(f"  ⚠ OVERLAP DETECTED: {info['overlap_start']} to {info['overlap_end']}")
                print(f"    Data for {ticker} already exists for the following dates:")
                print(f"    {info['overlap_start']} to {info['overlap_end']}")
                print(f"\n    To avoid duplicates, use one of these options:")
                print(f"      Option A: Fetch data AFTER existing data")
                print(f"                ({info['db_max_date']} to {requested_end})")
                print(f"      Option B: Fetch data BEFORE existing data")
                print(f"                ({requested_start} to {info['db_min_date']})")
                print(f"      Option C: Use replace_existing_data=True to overwrite existing data")
            else:
                print(f"  ✓ No overlap. Safe to fetch {requested_start} to {requested_end}.")
    
    if any_overlaps:
        print("\n" + "-"*80)
        print("If you'd rather overwrite existing data instead of modifying the date range,")
        print("set the `replace_existing_data` parameter to True.")
        print("-"*80)
    
    print("="*80 + "\n")
    return any_overlaps


def fetch_and_populate_data(tickers, start_date, end_date, replace_existing_data=False):
    """
    Robustly fetches historical stock data from yfinance for a date range
    and populates the SQLite database. Checks for overlaps and offers safe defaults.
    
    Args:
        tickers (list or str): Stock ticker symbol(s) to fetch (e.g., ["AAPL", "MSFT"] or "AAPL").
        start_date (str): Start date in 'YYYY-MM-DD' format.
        end_date (str): End date in 'YYYY-MM-DD' format.
        replace_existing_data (bool): If True, will overwrite existing data for overlapping dates.
                                      If False (default), will skip overlapping records.
    
    Returns:
        dict: Summary of the operation (records inserted, skipped, errors, etc.)
    """
    print(f"\n{'='*80}")
    print("FETCH AND POPULATE DATA")
    print(f"{'='*80}\n")
    
    # Step 1: Validate input parameters
    try:
        tickers = validate_fetch_parameters(tickers, start_date, end_date)
        print(f"✓ Input validation passed")
        print(f"  Tickers: {tickers}")
        print(f"  Date range: {start_date} to {end_date}")
    except ValueError as e:
        print(f"✗ Input validation failed: {e}")
        return {'success': False, 'error': str(e)}
    
    # Step 2: Check database coverage for overlaps
    coverage = check_database_coverage(tickers, start_date, end_date)
    has_overlaps = print_coverage_report(coverage, start_date, end_date)
    
    # Step 3: Handle overlaps
    if has_overlaps and not replace_existing_data:
        print("⚠ WARNING: Overlapping data detected and replace_existing_data=False.")
        print("   Proceeding with SKIP mode (overlapping records will not be inserted).\n")
    
    if has_overlaps and replace_existing_data:
        print("⚠ WARNING: replace_existing_data=True.")
        print("   Overlapping records will be REPLACED with new data.\n")
    
    # Step 4: Fetch and populate data
    summary = {
        'success': True,
        'tickers_processed': 0,
        'total_records_inserted': 0,
        'total_records_skipped': 0,
        'tickers_failed': [],
        'errors': [],
    }
    
    with sqlite3.connect(DB_FILE) as conn:
        for ticker in tickers:
            try:
                print(f"Fetching data for {ticker} from {start_date} to {end_date}...")
                
                # Download data from yfinance
                data = yf.download(ticker, start=start_date, end=end_date, auto_adjust=False)
                
                # CHECK 1: Verify data was returned
                if data.empty:
                    print(f"  ⚠ WARNING: No data returned for {ticker}.")
                    summary['tickers_failed'].append(ticker)
                    continue
                
                # Clean and format the data
                cleaned_data = preprocess_data_for_db(data, ticker)
                
                # CHECK 2: Verify cleaned data is not empty
                if cleaned_data.empty:
                    print(f"  ⚠ WARNING: Data cleaning resulted in empty DataFrame for {ticker}.")
                    summary['tickers_failed'].append(ticker)
                    continue
                
                # CHECK 3: Validate required columns exist
                required_cols = ['Ticker', 'Date', 'Open', 'High', 'Low', 'Close', 'Adj Close', 'Volume']
                missing_cols = [col for col in required_cols if col not in cleaned_data.columns]
                if missing_cols:
                    raise ValueError(f"Missing required columns: {missing_cols}")
                
                # CHECK 4: Validate data types
                try:
                    cleaned_data['Open'] = pd.to_numeric(cleaned_data['Open'], errors='coerce')
                    cleaned_data['High'] = pd.to_numeric(cleaned_data['High'], errors='coerce')
                    cleaned_data['Low'] = pd.to_numeric(cleaned_data['Low'], errors='coerce')
                    cleaned_data['Close'] = pd.to_numeric(cleaned_data['Close'], errors='coerce')
                    cleaned_data['Adj Close'] = pd.to_numeric(cleaned_data['Adj Close'], errors='coerce')
                    cleaned_data['Volume'] = pd.to_numeric(cleaned_data['Volume'], errors='coerce')
                    
                    if cleaned_data[['Open', 'High', 'Low', 'Close', 'Adj Close', 'Volume']].isna().any().any():
                        raise ValueError("Data contains NaN values after type conversion")
                except Exception as e:
                    raise ValueError(f"Data type validation failed: {e}")
                
                # CHECK 5: Handle duplicates or overlaps
                if replace_existing_data:
                    # Delete existing records for this ticker in the date range
                    delete_query = f"""
                    DELETE FROM {TABLE_NAME}
                    WHERE Ticker = ? AND Date BETWEEN ? AND ?
                    """
                    cursor = conn.cursor()
                    cursor.execute(delete_query, (ticker, start_date, end_date))
                    conn.commit()
                    print(f"  Deleted existing records for {ticker} in date range {start_date} to {end_date}.")
                    records_inserted = len(cleaned_data)
                else:
                    # Use INSERT OR IGNORE to skip duplicates
                    cursor = conn.cursor()
                    for idx, row in cleaned_data.iterrows():
                        try:
                            insert_query = f"""
                            INSERT INTO {TABLE_NAME} (Ticker, Date, Open, High, Low, Close, "Adj Close", Volume)
                            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                            """
                            cursor.execute(insert_query, (
                                row['Ticker'], row['Date'], row['Open'], row['High'],
                                row['Low'], row['Close'], row['Adj Close'], row['Volume']
                            ))
                        except sqlite3.IntegrityError:
                            # Duplicate key - skip it
                            summary['total_records_skipped'] += 1
                    conn.commit()
                    records_inserted = len(cleaned_data) - summary['total_records_skipped']
                
                if replace_existing_data:
                    # Insert all records
                    cleaned_data.to_sql(TABLE_NAME, conn, if_exists='append', index=False)
                    records_inserted = len(cleaned_data)
                
                summary['tickers_processed'] += 1
                summary['total_records_inserted'] += records_inserted
                
                print(f"  ✓ Successfully saved {records_inserted} records for {ticker}.")
                
            except Exception as e:
                print(f"  ✗ ERROR: Failed to process data for {ticker}. Reason: {e}")
                summary['tickers_failed'].append(ticker)
                summary['errors'].append({'ticker': ticker, 'error': str(e)})
    
    # Print summary
    print(f"\n{'='*80}")
    print("OPERATION SUMMARY")
    print(f"{'='*80}")
    print(f"Tickers processed: {summary['tickers_processed']}/{len(tickers)}")
    print(f"Total records inserted: {summary['total_records_inserted']}")
    if summary['total_records_skipped'] > 0:
        print(f"Total records skipped (duplicates): {summary['total_records_skipped']}")
    if summary['tickers_failed']:
        print(f"Tickers failed: {summary['tickers_failed']}")
    if summary['errors']:
        print(f"Errors encountered:")
        for err in summary['errors']:
            print(f"  - {err['ticker']}: {err['error']}")
    print(f"{'='*80}\n")
    
    return summary


if __name__ == "__main__":
    # 1. Create the database and table schema
    setup_database()
    
    # 2. Populate it with the 2024 historical data
    #populate_initial_data()
    
    # 3. Update existing ticker with additinal historical data
    fetch_and_populate_data(["META"], "2018-01-01", "2020-01-01", replace_existing_data=False)
    #fetch_and_populate_data(tickers=["AAPL", "AMZN", "GOOGL"], start_date="2018-01-01", end_date="2020-01-01", replace_existing_data=False)
    #fetch_and_populate_data(tickers=["MSFT" , "NVDA", "SPY", "QQQ"], start_date="2018-01-01", end_date="2020-01-01", replace_existing_data=False)
    #fetch_and_populate_data(tickers=["MU"], start_date="2018-01-01", end_date="2023-08-27", replace_existing_data=False)
    #fetch_and_populate_data(tickers=["TSM"], start_date="2018-01-01", end_date="2023-08-23", replace_existing_data=False)
    #fetch_and_populate_data(tickers=["BABA", "ONEQ"], start_date="2018-01-01", end_date="2024-07-31", replace_existing_data=False)
