"""
Stock Performance Heatmap Dashboard - Main Application

Run with: streamlit run streamlit_app.py
"""

import streamlit as st
import sys
from pathlib import Path

# Add src to path for imports
src_path = Path(__file__).parent / "src"
sys.path.insert(0, str(src_path))

def main():
    st.set_page_config(
        page_title="Stock Performance Heatmap Dashboard",
        page_icon=":chart_with_upwards_trend:",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    st.title(":chart_with_upwards_trend: Stock Performance Heatmap Dashboard")
    st.markdown("---")
    
    st.info(":construction: Dashboard under construction - migrated from stock-screener project")
    
    # Show migration status
    st.subheader("Migration Status")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Database", ":white_check_mark: Migrated", help="Historical stock data preserved")
    with col2:
        st.metric("Data Fetching", ":white_check_mark: Migrated", help="yfinance integration ready") 
    with col3:
        st.metric("Visualization", ":construction: In Progress", help="Heatmap under development")
        
    # Show database info
    st.subheader("Database Status")
    try:
        import sqlite3
        conn = sqlite3.connect('data/stock_data.db')
        cursor = conn.cursor()
        cursor.execute('SELECT COUNT(*) FROM daily_prices')
        record_count = cursor.fetchone()[0]
        cursor.execute('SELECT DISTINCT Ticker FROM daily_prices')
        tickers = sorted([row[0] for row in cursor.fetchall()])
        conn.close()
        
        st.success(f"Database contains {record_count} records for {len(tickers)} tickers")
        st.write("Tickers:", ", ".join(tickers))
    except Exception as e:
        st.error(f"Database connection error: {e}")

if __name__ == "__main__":
    main()
