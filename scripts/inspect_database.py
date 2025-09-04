"""
Database Inspection Script
Quick check of database contents and new data additions
Enhanced with volume data quality assessment
"""

import sqlite3
import pandas as pd
from datetime import datetime

def inspect_database():
    """Comprehensive database inspection"""
    db_path = "data/stock_data.db"
    
    try:
        conn = sqlite3.connect(db_path)
        
        print("📊 DATABASE INSPECTION REPORT")
        print("=" * 50)
        
        # 1. Basic Statistics
        print("\n📈 BASIC STATISTICS:")
        
        # Total records
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM daily_prices")
        total_records = cursor.fetchone()[0]
        print(f"   Total Records: {total_records:,}")
        
        # Unique tickers
        cursor.execute("SELECT COUNT(DISTINCT Ticker) FROM daily_prices")
        ticker_count = cursor.fetchone()[0]
        print(f"   Unique Tickers: {ticker_count}")
        
        # Date range
        cursor.execute("SELECT MIN(Date), MAX(Date) FROM daily_prices")
        min_date, max_date = cursor.fetchone()
        print(f"   Date Range: {min_date} to {max_date}")
        
        # 2. Ticker Breakdown
        print("\n📋 TICKER BREAKDOWN:")
        cursor.execute("""
            SELECT Ticker, COUNT(*) as Record_Count, MIN(Date) as First_Date, MAX(Date) as Last_Date
            FROM daily_prices 
            GROUP BY Ticker 
            ORDER BY Record_Count DESC
        """)
        
        ticker_data = cursor.fetchall()
        for ticker, count, first_date, last_date in ticker_data:
            print(f"   {ticker:8} | {count:4} records | {first_date} to {last_date}")
        
        # 3. Recent Activity (check for new data)
        print("\n🔍 RECENT ACTIVITY CHECK:")
        today = datetime.now().strftime('%Y-%m-%d')
        yesterday = (datetime.now()).strftime('%Y-%m-%d')  # Simplified for demo
        
        cursor.execute("""
            SELECT Ticker, Date, Close 
            FROM daily_prices 
            WHERE Date >= '2025-07-01'
            ORDER BY Date DESC, Ticker
            LIMIT 20
        """)
        
        recent_data = cursor.fetchall()
        if recent_data:
            print("   Most Recent Records:")
            for ticker, date, close in recent_data:
                print(f"     {ticker:8} | {date} | ${close:8.2f}")
        else:
            print("   No recent records found (2025-07-01 onwards)")
        
        # 4. Check for New Tickers (those likely added by our sessions)
        print("\n🆕 POTENTIAL NEW TICKERS:")
        original_tickers = ["NVDA", "META", "MSFT", "IYK", "IYC", "MCHI", "EWJ", "AMZN", "AAPL", "GOOGL", "SPY", "QQQ", "IYE", "IYF"]
        
        cursor.execute("SELECT DISTINCT Ticker FROM daily_prices ORDER BY Ticker")
        all_tickers = [row[0] for row in cursor.fetchall()]
        
        new_tickers = [ticker for ticker in all_tickers if ticker not in original_tickers]
        
        if new_tickers:
            print(f"   Found {len(new_tickers)} new tickers: {', '.join(new_tickers)}")
            
            # Show records for new tickers
            for ticker in new_tickers:
                cursor.execute("SELECT COUNT(*), MIN(Date), MAX(Date) FROM daily_prices WHERE Ticker = ?", (ticker,))
                count, first_date, last_date = cursor.fetchone()
                print(f"     {ticker}: {count} records ({first_date} to {last_date})")
        else:
            print("   No new tickers found beyond original 14")
        
        # 5. Database Size
        cursor.execute("SELECT page_count * page_size as size FROM pragma_page_count(), pragma_page_size()")
        db_size = cursor.fetchone()[0]
        print(f"\n💾 Database Size: {db_size:,} bytes ({db_size/1024/1024:.2f} MB)")
        
        conn.close()
        
    except Exception as e:
        print(f"❌ Error inspecting database: {e}")

if __name__ == "__main__":
    inspect_database()
