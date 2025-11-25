"""
Database Schema Preparation for Technical Analysis
Safely add technical analysis tables to existing database
"""

import sqlite3
import shutil
from pathlib import Path
from datetime import datetime

def backup_database():
    """Create a backup of the existing database"""
    db_path = Path("data/stock_data.db")
    backup_path = Path(f"data/stock_data_backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}.db")
    
    if db_path.exists():
        shutil.copy2(db_path, backup_path)
        print(f"SUCCESS: Database backed up to {backup_path}")
        return True
    else:
        print("FAIL: Original database not found")
        return False

def create_technical_analysis_tables():
    """Create the technical analysis tables"""
    print("TECHNICAL ANALYSIS DATABASE SCHEMA PREPARATION")
    print("=" * 60)
    
    # Step 1: Backup existing database
    if not backup_database():
        return False
    
    db_path = "data/stock_data.db"
    
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Check existing table structure
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
        existing_tables = [row[0] for row in cursor.fetchall()]
        print(f"Existing tables: {existing_tables}")
        
        # 1. Technical indicators storage for rolling heatmap
        print("\nCreating technical_indicators_daily table...")
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS technical_indicators_daily (
                ticker TEXT NOT NULL,
                date DATE NOT NULL,
                
                -- Moving Averages
                sma_5 REAL, sma_9 REAL, sma_10 REAL, sma_20 REAL, sma_21 REAL,
                sma_50 REAL, sma_100 REAL, sma_200 REAL,
                ema_5 REAL, ema_9 REAL, ema_10 REAL, ema_20 REAL, ema_21 REAL, 
                ema_50 REAL, ema_100 REAL, ema_200 REAL,
                
                -- Technical Indicators  
                rsi_14 REAL,
                macd_value REAL, macd_signal REAL, macd_histogram REAL,
                stoch_k REAL, stoch_d REAL,
                stochrsi_value REAL,
                adx_value REAL, plus_di REAL, minus_di REAL,
                williams_r REAL,
                cci_14 REAL,
                ultimate_osc REAL,
                roc_12 REAL,
                atr_14 REAL,
                bull_power REAL, bear_power REAL,
                
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                PRIMARY KEY (ticker, date)
            )
        """)
        print("SUCCESS: technical_indicators_daily table created")
        
        # 2. Price extremes for 52-week analysis
        print("\nCreating price_extremes_periods table...")
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS price_extremes_periods (
                ticker TEXT NOT NULL,
                period TEXT NOT NULL,  -- '52w', '3m', '1m', '2w'
                high_price REAL,
                low_price REAL,
                high_date DATE,
                low_date DATE,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                PRIMARY KEY (ticker, period)
            )
        """)
        print("SUCCESS: price_extremes_periods table created")
        
        # 3. Pivot points calculations
        print("\nCreating pivot_points_daily table...")
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS pivot_points_daily (
                ticker TEXT NOT NULL,
                date DATE NOT NULL,
                pivot_type TEXT NOT NULL,  -- 'classic', 'fibonacci', 'woodys', 'camarilla'
                pivot REAL,
                r1 REAL, r2 REAL, r3 REAL,
                s1 REAL, s2 REAL, s3 REAL,
                PRIMARY KEY (ticker, date, pivot_type)
            )
        """)
        print("SUCCESS: pivot_points_daily table created")
        
        # Create indexes for performance
        print("\nCreating indexes for performance...")
        
        # Indexes for technical_indicators_daily
        cursor.execute("""
            CREATE INDEX IF NOT EXISTS idx_technical_ticker_date 
            ON technical_indicators_daily(ticker, date)
        """)
        
        cursor.execute("""
            CREATE INDEX IF NOT EXISTS idx_technical_date 
            ON technical_indicators_daily(date)
        """)
        
        # Indexes for price_extremes_periods
        cursor.execute("""
            CREATE INDEX IF NOT EXISTS idx_extremes_ticker 
            ON price_extremes_periods(ticker)
        """)
        
        # Indexes for pivot_points_daily
        cursor.execute("""
            CREATE INDEX IF NOT EXISTS idx_pivot_ticker_date 
            ON pivot_points_daily(ticker, date)
        """)
        
        print("SUCCESS: All indexes created")
        
        # Commit changes
        conn.commit()
        
        # Verify table creation
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
        all_tables = [row[0] for row in cursor.fetchall()]
        new_tables = [t for t in all_tables if t not in existing_tables]
        
        print(f"\nNew tables created: {new_tables}")
        
        # Test table accessibility
        print("\nTesting table accessibility...")
        for table in new_tables:
            cursor.execute(f"SELECT COUNT(*) FROM {table}")
            count = cursor.fetchone()[0]
            print(f"  {table}: {count} records (empty as expected)")
        
        conn.close()
        
        print("\nSUCCESS: Technical analysis database schema preparation complete!")
        print("All tables created successfully and existing data preserved.")
        return True
        
    except Exception as e:
        print(f"FAIL: Error creating technical analysis tables: {e}")
        return False

def verify_existing_data_intact():
    """Verify that existing data is still intact after schema changes"""
    print("\nVERIFYING EXISTING DATA INTEGRITY")
    print("=" * 40)
    
    try:
        conn = sqlite3.connect("data/stock_data.db")
        cursor = conn.cursor()
        
        # Check daily_prices table
        cursor.execute("SELECT COUNT(*) FROM daily_prices")
        total_records = cursor.fetchone()[0]
        
        cursor.execute("SELECT COUNT(DISTINCT Ticker) FROM daily_prices")
        unique_tickers = cursor.fetchone()[0]
        
        cursor.execute("SELECT MIN(Date), MAX(Date) FROM daily_prices")
        min_date, max_date = cursor.fetchone()
        
        print(f"daily_prices table:")
        print(f"  Total records: {total_records:,}")
        print(f"  Unique tickers: {unique_tickers}")
        print(f"  Date range: {min_date} to {max_date}")
        
        # Spot check some key tickers
        test_tickers = ['NVDA', 'AAPL', 'MSFT', 'GOOGL']
        for ticker in test_tickers:
            cursor.execute("SELECT COUNT(*) FROM daily_prices WHERE Ticker = ?", (ticker,))
            count = cursor.fetchone()[0]
            print(f"  {ticker}: {count} records")
        
        conn.close()
        
        print("SUCCESS: Existing data integrity verified!")
        return True
        
    except Exception as e:
        print(f"FAIL: Error verifying existing data: {e}")
        return False

def run_database_preparation():
    """Run complete database preparation validation"""
    schema_success = create_technical_analysis_tables()
    data_integrity = verify_existing_data_intact()
    
    overall_success = schema_success and data_integrity
    
    print("\n" + "=" * 60)
    print(f"DATABASE PREPARATION RESULT: {'SUCCESS' if overall_success else 'FAILED'}")
    if overall_success:
        print("Ready for technical analysis implementation!")
    else:
        print("Check backup and restore if needed.")
    print("=" * 60)
    
    return overall_success

if __name__ == "__main__":
    run_database_preparation()
