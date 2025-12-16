"""
pandas-ta-classic Integration Validation
Test pandas-ta-classic with existing OHLCV data format
"""

import sys
from pathlib import Path
import pandas as pd
import sqlite3

# Add src to path for imports
src_path = Path(__file__).parent.parent / "src"
sys.path.insert(0, str(src_path))

def test_pandas_ta_integration():
    """Test pandas-ta-classic with existing database data"""
    print("PANDAS-TA-CLASSIC INTEGRATION VALIDATION")
    print("=" * 50)
    
    try:
        import pandas_ta_classic as ta
        print(f"SUCCESS: pandas-ta-classic version {ta.__version__} imported successfully")
    except ImportError as e:
        print(f"FAIL: Cannot import pandas-ta-classic: {e}")
        return False
    
    # Test with existing database data
    db_path = "data/stock_data.db"
    
    try:
        conn = sqlite3.connect(db_path)
        
        # Get NVDA data (should exist in your database)
        query = """
        SELECT Date, Open, High, Low, Close, Volume 
        FROM daily_prices 
        WHERE Ticker = 'NVDA' 
        ORDER BY Date DESC 
        LIMIT 50
        """
        
        df = pd.read_sql_query(query, conn)
        conn.close()
        
        if df.empty:
            print("FAIL: No NVDA data found in database")
            return False
            
        print(f"SUCCESS: Loaded {len(df)} NVDA records from database")
        print(f"Date range: {df['Date'].min()} to {df['Date'].max()}")
        
        # Test key technical indicators
        print("\nTesting Technical Indicators:")
        
        # RSI
        rsi = ta.rsi(df['Close'], length=14)
        latest_rsi = rsi.iloc[-1]
        print(f"  RSI (14): {latest_rsi:.2f}")
        
        # MACD
        macd_data = ta.macd(df['Close'])
        latest_macd = macd_data['MACD_12_26_9'].iloc[-1]
        print(f"  MACD: {latest_macd:.4f}")
        
        # Elder Ray Index (Bull/Bear Power)
        eri = ta.eri(df['High'], df['Low'], df['Close'])
        bull_power = eri['BULLP_13'].iloc[-1]
        bear_power = eri['BEARP_13'].iloc[-1]
        print(f"  Bull Power: {bull_power:.4f}")
        print(f"  Bear Power: {bear_power:.4f}")
        
        # ADX
        adx_data = ta.adx(df['High'], df['Low'], df['Close'])
        latest_adx = adx_data['ADX_14'].iloc[-1]
        plus_di = adx_data['DMP_14'].iloc[-1]
        minus_di = adx_data['DMN_14'].iloc[-1]
        print(f"  ADX: {latest_adx:.2f}, +DI: {plus_di:.2f}, -DI: {minus_di:.2f}")
        
        # Stochastic
        stoch = ta.stoch(df['High'], df['Low'], df['Close'])
        stoch_k = stoch['STOCHk_14_3_3'].iloc[-1]
        stoch_d = stoch['STOCHd_14_3_3'].iloc[-1]
        print(f"  Stochastic K: {stoch_k:.2f}, D: {stoch_d:.2f}")
        
        # Test crossover detection
        print("\nTesting Crossover Detection:")
        
        # Simple moving averages for crossover test
        sma50 = ta.sma(df['Close'], length=50)
        sma200 = ta.sma(df['Close'], length=200)
        
        # Golden cross condition (50 > 200)
        golden_cross = sma50 > sma200
        
        # Test tsignals for crossover detection
        signals = ta.tsignals(golden_cross, asbool=True)
        recent_entries = signals['TS_Entries'].iloc[-10:].sum()
        recent_exits = signals['TS_Exits'].iloc[-10:].sum()
        
        print(f"  Golden Cross signals (last 10 days): {recent_entries} entries, {recent_exits} exits")
        print(f"  Current state: {'Golden Cross' if golden_cross.iloc[-1] else 'Death Cross'}")
        
        print("\nSUCCESS: All pandas-ta-classic indicators working with existing data format!")
        return True
        
    except Exception as e:
        print(f"FAIL: Error testing pandas-ta-classic: {e}")
        return False

if __name__ == "__main__":
    test_pandas_ta_integration()
