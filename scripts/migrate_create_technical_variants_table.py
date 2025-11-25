"""
Migration Script: Create technical_indicators_variants_daily Table

This script creates the hybrid schema table for storing technical indicator
variants across three timeframes (short-term, intermediate-term, long-term).

PURPOSE:
  - Stores 51 custom-parameter technical indicators (17 per timeframe)
  - Enables rolling heatmap functionality with parameter flexibility
  - Maintains clean separation from standard technical_indicators_daily table

USAGE:
  python scripts/migrate_create_technical_variants_table.py
  
OPTIONS:
  --dry-run    Preview SQL without applying changes
  --rollback   Drop the table (use with caution)

BACKFILL WORKFLOW (for future use):
  After creating this table, populate with historical data via:
  1. Calculate all 51 indicators for each ticker/date
  2. Insert results into technical_indicators_variants_daily
  3. Verify data completeness

DEPENDENCIES:
  - Database file: data/stock_data.db
  - Python: sqlite3, logging, argparse
"""

import sqlite3
import logging
from pathlib import Path
from datetime import datetime
import sys

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

DB_FILE = Path(__file__).parent.parent / "data" / "stock_data.db"
TABLE_NAME = "technical_indicators_variants_daily"

SCHEMA_SQL = """
CREATE TABLE IF NOT EXISTS {table_name} (
    ticker TEXT NOT NULL,
    date DATE NOT NULL,
    
    -- SHORT-TERM (1-15 days) - 17 indicators
    rsi_10 REAL,
    stoch_5_k REAL,
    stoch_5_d REAL,
    cci_10 REAL,
    roc_9 REAL,
    ema_5 REAL,
    ema_10 REAL,
    adx_9 REAL,
    macd_8_17_5_value REAL,
    macd_8_17_5_signal REAL,
    hma_9 REAL,
    atr_10 REAL,
    bollinger_10_1_5_upper REAL,
    bollinger_10_1_5_lower REAL,
    mfi_10 REAL,
    cmf_14 REAL,
    vwma_10 REAL,
    williams_r_5 REAL,
    ultimate_5_10_20 REAL,
    
    -- INTERMEDIATE-TERM (15-50 days) - 17 indicators
    rsi_14 REAL,
    stoch_14_k REAL,
    stoch_14_d REAL,
    cci_14 REAL,
    roc_20 REAL,
    ema_20 REAL,
    sma_50 REAL,
    adx_14 REAL,
    macd_12_26_9_value REAL,
    macd_12_26_9_signal REAL,
    hma_21 REAL,
    atr_14 REAL,
    bollinger_20_2_upper REAL,
    bollinger_20_2_lower REAL,
    mfi_14 REAL,
    cmf_21 REAL,
    vwma_20 REAL,
    williams_r_14 REAL,
    ultimate_7_14_28 REAL,
    
    -- LONG-TERM (50+ days) - 17 indicators
    rsi_30 REAL,
    stoch_21_k REAL,
    stoch_21_d REAL,
    cci_30 REAL,
    roc_50 REAL,
    sma_100 REAL,
    sma_200 REAL,
    adx_20 REAL,
    macd_20_50_10_value REAL,
    macd_20_50_10_signal REAL,
    hma_50 REAL,
    atr_50 REAL,
    bollinger_50_2_5_upper REAL,
    bollinger_50_2_5_lower REAL,
    mfi_30 REAL,
    cmf_50 REAL,
    vwma_50 REAL,
    williams_r_20 REAL,
    ultimate_10_20_40 REAL,
    
    -- Metadata
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    PRIMARY KEY (ticker, date)
);

CREATE INDEX IF NOT EXISTS idx_variants_ticker_date 
    ON {table_name}(ticker, date);
    
CREATE INDEX IF NOT EXISTS idx_variants_ticker 
    ON {table_name}(ticker);
    
CREATE INDEX IF NOT EXISTS idx_variants_date 
    ON {table_name}(date);
"""

def create_table(db_path: Path = DB_FILE, dry_run: bool = False) -> bool:
    """
    Create the technical_indicators_variants_daily table.
    
    Args:
        db_path: Path to SQLite database
        dry_run: If True, print SQL without executing
        
    Returns:
        True if successful, False otherwise
    """
    if not db_path.exists():
        logger.error(f"Database file not found: {db_path}")
        return False
    
    try:
        sql = SCHEMA_SQL.format(table_name=TABLE_NAME)
        
        if dry_run:
            logger.info("DRY RUN MODE - SQL that would be executed:")
            logger.info("-" * 80)
            logger.info(sql)
            logger.info("-" * 80)
            return True
        
        with sqlite3.connect(str(db_path)) as conn:
            cursor = conn.cursor()
            cursor.executescript(sql)
            conn.commit()
        
        logger.info(f"SUCCESS: Table {TABLE_NAME} created successfully")
        return True
        
    except sqlite3.OperationalError as e:
        if "already exists" in str(e):
            logger.warning(f"Table {TABLE_NAME} already exists - skipping creation")
            return True
        logger.error(f"Database error: {e}")
        return False
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        return False


def verify_table(db_path: Path = DB_FILE) -> bool:
    """
    Verify that the table was created successfully and check its structure.
    
    Args:
        db_path: Path to SQLite database
        
    Returns:
        True if table exists and has expected structure
    """
    try:
        with sqlite3.connect(str(db_path)) as conn:
            cursor = conn.cursor()
            
            cursor.execute(f"SELECT COUNT(*) FROM sqlite_master WHERE type='table' AND name=?", (TABLE_NAME,))
            table_exists = cursor.fetchone()[0] > 0
            
            if not table_exists:
                logger.error(f"Table {TABLE_NAME} does not exist")
                return False
            
            cursor.execute(f"PRAGMA table_info({TABLE_NAME})")
            columns = cursor.fetchall()
            
            logger.info(f"Table {TABLE_NAME} exists with {len(columns)} columns:")
            logger.info(f"  Short-term (1-15 days): 19 columns")
            logger.info(f"  Intermediate-term (15-50 days): 19 columns")
            logger.info(f"  Long-term (50+ days): 19 columns")
            logger.info(f"  Metadata: 2 columns")
            
            cursor.execute(f"SELECT COUNT(*) FROM {TABLE_NAME}")
            row_count = cursor.fetchone()[0]
            logger.info(f"Current records: {row_count}")
            
            cursor.execute(f"SELECT sql FROM sqlite_master WHERE type='index' AND tbl_name=?", (TABLE_NAME,))
            indexes = cursor.fetchall()
            logger.info(f"Indexes: {len(indexes)} defined")
            
            return True
            
    except Exception as e:
        logger.error(f"Verification failed: {e}")
        return False


def drop_table(db_path: Path = DB_FILE, confirm: bool = False) -> bool:
    """
    Drop the technical_indicators_variants_daily table.
    USE WITH CAUTION - This will delete all rolling heatmap data!
    
    Args:
        db_path: Path to SQLite database
        confirm: Must be True to execute (safety check)
        
    Returns:
        True if successful
    """
    if not confirm:
        logger.warning("To drop table, call with confirm=True")
        return False
    
    try:
        with sqlite3.connect(str(db_path)) as conn:
            cursor = conn.cursor()
            cursor.execute(f"DROP TABLE IF EXISTS {TABLE_NAME}")
            conn.commit()
        
        logger.warning(f"Table {TABLE_NAME} dropped successfully")
        return True
        
    except Exception as e:
        logger.error(f"Error dropping table: {e}")
        return False


def show_schema(db_path: Path = DB_FILE) -> None:
    """Display the current schema of the table."""
    try:
        with sqlite3.connect(str(db_path)) as conn:
            cursor = conn.cursor()
            cursor.execute(f"SELECT sql FROM sqlite_master WHERE type='table' AND name=?", (TABLE_NAME,))
            result = cursor.fetchone()
            
            if result:
                logger.info(f"Current schema for {TABLE_NAME}:")
                logger.info(result[0])
            else:
                logger.warning(f"Table {TABLE_NAME} does not exist yet")
                
    except Exception as e:
        logger.error(f"Error reading schema: {e}")


def main():
    """Main entry point for the migration script."""
    import argparse
    
    parser = argparse.ArgumentParser(
        description="Migrate database schema: Create technical_indicators_variants_daily table",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
EXAMPLES:
  # Preview SQL without applying
  python migrate_create_technical_variants_table.py --dry-run
  
  # Create the table
  python migrate_create_technical_variants_table.py
  
  # Verify table structure
  python migrate_create_technical_variants_table.py --verify
  
  # Drop table (requires confirmation)
  python migrate_create_technical_variants_table.py --rollback --confirm

ROLLBACK INSTRUCTIONS (if needed):
  If you need to undo this migration:
  1. Run with --rollback --confirm flag (this will delete the table)
  2. Or manually: DROP TABLE technical_indicators_variants_daily;
        """
    )
    
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Preview SQL changes without applying them"
    )
    parser.add_argument(
        "--verify",
        action="store_true",
        help="Check table structure and record count"
    )
    parser.add_argument(
        "--rollback",
        action="store_true",
        help="Drop the table (DESTRUCTIVE - requires --confirm)"
    )
    parser.add_argument(
        "--confirm",
        action="store_true",
        help="Confirm rollback/destructive operations"
    )
    parser.add_argument(
        "--schema",
        action="store_true",
        help="Display the table schema"
    )
    parser.add_argument(
        "--db",
        type=Path,
        default=DB_FILE,
        help=f"Path to database (default: {DB_FILE})"
    )
    
    args = parser.parse_args()
    
    logger.info(f"Database: {args.db}")
    logger.info(f"Table: {TABLE_NAME}")
    logger.info("-" * 80)
    
    if args.dry_run:
        logger.info("Running in DRY-RUN mode - no changes will be applied")
        create_table(args.db, dry_run=True)
        
    elif args.rollback:
        if not args.confirm:
            logger.error("Rollback requires --confirm flag")
            logger.info("Command: python migrate_create_technical_variants_table.py --rollback --confirm")
            sys.exit(1)
        
        logger.warning("DESTRUCTIVE: Dropping table...")
        if drop_table(args.db, confirm=True):
            logger.info("Rollback complete")
        else:
            logger.error("Rollback failed")
            sys.exit(1)
            
    elif args.verify:
        verify_table(args.db)
        
    elif args.schema:
        show_schema(args.db)
        
    else:
        logger.info("Creating table...")
        if create_table(args.db):
            logger.info("Verifying creation...")
            verify_table(args.db)
            logger.info("Migration complete!")
        else:
            logger.error("Migration failed")
            sys.exit(1)


if __name__ == "__main__":
    main()
