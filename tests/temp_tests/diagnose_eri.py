"""
Quick diagnostic to check Elder Ray Index column names
"""

import sys
from pathlib import Path
import pandas as pd
import sqlite3

# Add src to path for imports
src_path = Path(__file__).parent.parent / "src"
sys.path.insert(0, str(src_path))

try:
    import pandas_ta_classic as ta
    
    # Get sample data
    conn = sqlite3.connect("data/stock_data.db")
    query = """
    SELECT Date, Open, High, Low, Close, Volume 
    FROM daily_prices 
    WHERE Ticker = 'NVDA' 
    ORDER BY Date DESC 
    LIMIT 50
    """
    df = pd.read_sql_query(query, conn)
    conn.close()
    
    # Test Elder Ray Index
    print("Testing Elder Ray Index column names:")
    eri = ta.eri(df['High'], df['Low'], df['Close'])
    print("ERI columns:", eri.columns.tolist())
    print("Sample values:")
    print(eri.tail(3))
    
except Exception as e:
    print(f"Error: {e}")
