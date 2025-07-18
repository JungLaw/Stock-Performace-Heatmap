"""
SQL Delete by Date Range Utility

Safely delete records from the stock database within a specified date range.
Useful for cleaning up incomplete or incorrect data.
"""

import sqlite3
from pathlib import Path

def delete_records_by_date_range(start_date: str, end_date: str, db_path: str = "../data/stock_data.db"):
    """
    Delete records from daily_prices table within the specified date range
    
    Args:
        start_date: Start date in YYYY-MM-DD format (inclusive)
        end_date: End date in YYYY-MM-DD format (inclusive)
        db_path: Path to the database file (relative to scripts directory)
    """
    # Resolve the database path
    script_dir = Path(__file__).parent
    full_db_path = (script_dir / db_path).resolve()
    
    if not full_db_path.exists():
        print(f"❌ Database file not found: {full_db_path}")
        return
    
    print(f"🗄️ Connecting to database: {full_db_path}")
    
    try:
        conn = sqlite3.connect(str(full_db_path))
        cursor = conn.cursor()
        
        # First, check what will be deleted
        cursor.execute(
            "SELECT COUNT(*) FROM daily_prices WHERE Date >= ? AND Date <= ?", 
            (start_date, end_date)
        )
        count = cursor.fetchone()[0]
        
        if count == 0:
            print(f"ℹ️ No records found in date range {start_date} to {end_date}")
            return
        
        print(f"📊 Found {count} records to delete from {start_date} to {end_date}")
        
        # Show sample of what will be deleted
        cursor.execute(
            "SELECT DISTINCT Ticker, Date FROM daily_prices WHERE Date >= ? AND Date <= ? ORDER BY Date, Ticker LIMIT 10", 
            (start_date, end_date)
        )
        sample = cursor.fetchall()
        print("📋 Sample records to delete:")
        for ticker, date in sample:
            print(f"   - {ticker}: {date}")
        
        if count > 10:
            print(f"   ... and {count - 10} more records")
        
        # Confirm deletion
        response = input(f"\n⚠️ Delete {count} records? (y/N): ").strip().lower()
        if response != 'y':
            print("❌ Deletion cancelled")
            return
        
        # Execute the deletion
        cursor.execute(
            "DELETE FROM daily_prices WHERE Date >= ? AND Date <= ?", 
            (start_date, end_date)
        )
        deleted = cursor.rowcount
        conn.commit()
        
        print(f"✅ Successfully deleted {deleted} records from {start_date} to {end_date}")
        
    except Exception as e:
        print(f"❌ Error: {e}")
    finally:
        conn.close()

if __name__ == "__main__":
    # Default: Clean up the problematic date range from the database issue
    delete_records_by_date_range("2025-07-14", "2025-07-17")
