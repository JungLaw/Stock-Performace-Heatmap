"""
Stock Performance Heatmap Dashboard - Main Application

A Finviz-style interactive heatmap for visualizing stock and ETF performance
across different time periods and asset groups.

Run with: streamlit run streamlit_app.py
"""

import streamlit as st
import sys
from pathlib import Path
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime

# Add src to path for imports
src_path = Path(__file__).parent / "src"
sys.path.insert(0, str(src_path))

# Import our modules
from calculations.performance import PerformanceCalculator
from visualization.heatmap import FinvizHeatmapGenerator, get_color_legend
from config.assets import ASSET_GROUPS

def initialize_session_state():
    """Initialize session state variables"""
    if 'performance_data' not in st.session_state:
        st.session_state.performance_data = None
    if 'last_update' not in st.session_state:
        st.session_state.last_update = None
    if 'calculator' not in st.session_state:
        st.session_state.calculator = PerformanceCalculator()
    if 'heatmap_generator' not in st.session_state:
        st.session_state.heatmap_generator = FinvizHeatmapGenerator()

def create_sidebar_controls():
    """Create sidebar controls for user interaction"""
    st.sidebar.title("⚙️ Dashboard Controls")
    
    # Asset Group Selection
    st.sidebar.subheader("Asset Group")
    asset_group_options = {
        "Custom Tickers": "custom",
        "Country ETFs": "country", 
        "Sector ETFs": "sector"
    }
    
    selected_group_name = st.sidebar.selectbox(
        "Choose asset group:",
        options=list(asset_group_options.keys()),
        index=0
    )
    selected_group = asset_group_options[selected_group_name]
    
    # Get tickers for selected group
    group_config = ASSET_GROUPS[selected_group]
    default_tickers = group_config["tickers"]
    
    # Custom ticker input if custom group selected
    if selected_group == "custom":
        st.sidebar.subheader("Custom Tickers")
        ticker_input = st.sidebar.text_area(
            "Enter tickers (one per line or comma-separated):",
            value="\\n".join(default_tickers[:5]),  # Show first 5 as default
            height=150,
            help="Enter stock tickers separated by commas or new lines"
        )
        
        # Parse ticker input
        if ticker_input.strip():
            # Split by both newlines and commas, then clean
            tickers = []
            for line in ticker_input.replace(',', '\\n').split('\\n'):
                line = line.strip().upper()
                if line:
                    tickers.append(line)
            selected_tickers = tickers[:10]  # Limit to 10 for performance
        else:
            selected_tickers = default_tickers[:5]
    else:
        selected_tickers = default_tickers
        st.sidebar.info(f"Using {len(selected_tickers)} {group_config['name'].lower()}")
    
    # Time Period Selection
    st.sidebar.subheader("Time Period")
    period_options = {
        "1 Day": "1d",
        "1 Week": "1w", 
        "1 Month": "1m",
        "3 Months": "3m",
        "6 Months": "6m",
        "Year to Date": "ytd",
        "1 Year": "1y"
    }
    
    selected_period_name = st.sidebar.selectbox(
        "Compare against:",
        options=list(period_options.keys()),
        index=0
    )
    selected_period = period_options[selected_period_name]
    
    # Refresh button
    st.sidebar.subheader("Data Refresh")
    refresh_button = st.sidebar.button(
        "🔄 Refresh Data",
        help="Fetch latest market data",
        use_container_width=True
    )
    
    return {
        'group': selected_group,
        'group_name': selected_group_name,
        'tickers': selected_tickers,
        'period': selected_period,
        'period_name': selected_period_name,
        'refresh': refresh_button
    }

def create_header():
    """Create the main header section"""
    st.title("📈 Stock Performance Heatmap Dashboard")
    
    # Description
    st.markdown("""
    Interactive financial heatmap inspired by Finviz, showing price performance 
    across different time periods. Select asset groups and time periods from the sidebar.
    """)
    
    # Color legend
    with st.expander("🎨 Color Legend", expanded=False):
        legend_data = get_color_legend()
        
        cols = st.columns(len(legend_data))
        for i, (description, color) in enumerate(legend_data.items()):
            with cols[i]:
                st.markdown(
                    f'<div style="background-color: {color}; padding: 10px; '
                    f'border-radius: 5px; text-align: center; color: white; '
                    f'font-weight: bold; margin: 2px;">{description}</div>',
                    unsafe_allow_html=True
                )

def fetch_performance_data(tickers, period):
    """Fetch performance data with progress tracking"""
    with st.spinner(f"Fetching data for {len(tickers)} tickers..."):
        # Create progress bar
        progress_bar = st.progress(0)
        status_text = st.empty()
        
        calculator = st.session_state.calculator
        performance_data = []
        
        for i, ticker in enumerate(tickers):
            status_text.text(f"Processing {ticker}... ({i+1}/{len(tickers)})")
            
            try:
                data = calculator.calculate_performance_for_ticker(ticker, period)
                performance_data.append(data)
            except Exception as e:
                st.warning(f"Error processing {ticker}: {str(e)}")
                # Add error entry
                performance_data.append({
                    'ticker': ticker,
                    'current_price': None,
                    'historical_price': None,
                    'percentage_change': 0.0,
                    'absolute_change': 0.0,
                    'period': period,
                    'error': True
                })
            
            # Update progress
            progress_bar.progress((i + 1) / len(tickers))
        
        # Clear progress indicators
        progress_bar.empty()
        status_text.empty()
        
        return performance_data

def display_summary_stats(performance_data):
    """Display summary statistics"""
    generator = st.session_state.heatmap_generator
    stats = generator.create_summary_stats(performance_data)
    
    # Main metrics row
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            "Total Tickers", 
            stats['total_tickers'],
            help="Number of tickers analyzed"
        )
    
    with col2:
        st.metric(
            "Valid Data", 
            stats['valid_data'],
            help="Tickers with successful data fetch"
        )
    
    with col3:
        avg_perf = stats['avg_performance']
        st.metric(
            "Average Performance",
            f"{avg_perf:+.2f}%",
            help="Average percentage change across all tickers"
        )
    
    with col4:
        pos_count = stats['positive_count']
        neg_count = stats['negative_count']
        if pos_count + neg_count > 0:
            pos_ratio = pos_count / (pos_count + neg_count) * 100
            st.metric(
                "Positive %",
                f"{pos_ratio:.1f}%",
                help="Percentage of tickers with positive performance"
            )
        else:
            st.metric("Positive %", "N/A")
    
    # Best/Worst performers
    if stats['best_performer'] and stats['worst_performer']:
        col1, col2 = st.columns(2)
        
        with col1:
            best = stats['best_performer']
            st.success(
                f"🏆 Best: **{best['ticker']}** "
                f"({best['percentage_change']:+.2f}%)"
            )
        
        with col2:
            worst = stats['worst_performer']
            st.error(
                f"📉 Worst: **{worst['ticker']}** "
                f"({worst['percentage_change']:+.2f}%)"
            )

def display_heatmap(performance_data, title):
    """Display the main heatmap visualization"""
    generator = st.session_state.heatmap_generator
    
    # Create heatmap
    fig = generator.create_treemap(
        performance_data=performance_data,
        title=title,
        width=1200,
        height=700
    )
    
    # Display with full width
    st.plotly_chart(fig, use_container_width=True)

def display_data_table(performance_data):
    """Display detailed data table"""
    if not performance_data:
        return
    
    # Filter valid data and create DataFrame
    valid_data = [p for p in performance_data if not p.get('error', False)]
    
    if not valid_data:
        st.warning("No valid data to display in table")
        return
    
    # Create display DataFrame
    df_display = pd.DataFrame([
        {
            'Ticker': p['ticker'],
            'Current Price': f"${p['current_price']:.2f}" if p['current_price'] else "N/A",
            'Historical Price': f"${p['historical_price']:.2f}" if p['historical_price'] else "N/A",
            'Absolute Change': f"${p['absolute_change']:+.2f}" if p['absolute_change'] else "N/A",
            'Percentage Change': f"{p['percentage_change']:+.2f}%" if p['percentage_change'] is not None else "N/A",
            'Period': p.get('period_label', p.get('period', 'N/A'))
        }
        for p in valid_data
    ])
    
    # Sort by percentage change (descending)
    df_display = df_display.sort_values('Percentage Change', key=lambda x: 
        pd.to_numeric(x.str.rstrip('%'), errors='coerce'), ascending=False)
    
    st.dataframe(
        df_display,
        use_container_width=True,
        hide_index=True
    )

def main():
    """Main application function"""
    # Page config
    st.set_page_config(
        page_title="Stock Performance Heatmap Dashboard",
        page_icon="📈",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    # Initialize session state
    initialize_session_state()
    
    # Create header
    create_header()
    
    # Create sidebar controls
    controls = create_sidebar_controls()
    
    # Check if we need to fetch new data
    should_fetch = (
        controls['refresh'] or 
        st.session_state.performance_data is None or
        (st.session_state.last_update is None)
    )
    
    if should_fetch:
        # Fetch performance data
        performance_data = fetch_performance_data(
            controls['tickers'], 
            controls['period']
        )
        
        # Store in session state
        st.session_state.performance_data = performance_data
        st.session_state.last_update = datetime.now()
        
        st.success(f"✅ Data updated successfully at {st.session_state.last_update.strftime('%H:%M:%S')}")
    else:
        performance_data = st.session_state.performance_data
    
    if performance_data:
        # Create heatmap title
        title = f"{controls['group_name']} - {controls['period_name']} Performance"
        
        # Display summary statistics
        st.subheader("📊 Summary Statistics")
        display_summary_stats(performance_data)
        
        st.markdown("---")
        
        # Display heatmap
        st.subheader("🗺️ Performance Heatmap")
        display_heatmap(performance_data, title)
        
        # Display data table
        with st.expander("📋 Detailed Data Table", expanded=False):
            display_data_table(performance_data)
        
        # Show last update time
        if st.session_state.last_update:
            st.caption(f"Last updated: {st.session_state.last_update.strftime('%Y-%m-%d %H:%M:%S')}")
    
    else:
        st.info("👆 Select your preferences in the sidebar and click 'Refresh Data' to get started!")

    # Footer
    st.markdown("---")
    st.markdown(
        "Built with ❤️ using Streamlit and Plotly | "
        "Data provided by Yahoo Finance via yfinance"
    )

if __name__ == "__main__":
    main()
