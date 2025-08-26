"""
Stock Performance Heatmap Dashboard - Main Application

An interactive heatmap for visualizing stock and ETF performance
across different time periods and asset groups.

Run with: streamlit run streamlit_app.py
"""

import streamlit as st
import sys
from pathlib import Path
from datetime import datetime
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime, timedelta

# Add src to path for imports
src_path = Path(__file__).parent / "src"
sys.path.insert(0, str(src_path))

# Import our modules
from calculations.performance import DatabaseIntegratedPerformanceCalculator
from visualization.heatmap import FinvizHeatmapGenerator, get_color_legend
from config.assets import ASSET_GROUPS, CUSTOM_DEFAULT

def initialize_session_state():
    """Initialize session state variables"""
    if 'performance_data' not in st.session_state:
        st.session_state.performance_data = None
    if 'last_update' not in st.session_state:
        st.session_state.last_update = None
    if 'calculator' not in st.session_state:
        st.session_state.calculator = DatabaseIntegratedPerformanceCalculator()
    if 'heatmap_generator' not in st.session_state:
        st.session_state.heatmap_generator = FinvizHeatmapGenerator()
    
    # Three-level ticker management session state variables
    if 'selected_country_etfs' not in st.session_state:
        st.session_state.selected_country_etfs = []
    if 'selected_sector_etfs' not in st.session_state:
        st.session_state.selected_sector_etfs = []
    if 'session_custom_tickers' not in st.session_state:
        st.session_state.session_custom_tickers = []
    if 'permanent_country_additions' not in st.session_state:
        st.session_state.permanent_country_additions = []
    if 'permanent_sector_additions' not in st.session_state:
        st.session_state.permanent_sector_additions = []
    
    # Database and performance settings
    if 'save_custom_to_database' not in st.session_state:
        st.session_state.save_custom_to_database = True
    if 'custom_ticker_limit' not in st.session_state:
        st.session_state.custom_ticker_limit = 10

    if 'selected_bucket' not in st.session_state:
        st.session_state.selected_bucket = 'custom'  # Default to custom bucket

    # Filtering state (Step 3: Future-ready for additions)
    if 'country_visible_tickers' not in st.session_state:
        st.session_state.country_visible_tickers = []  # Will be populated on first run
    if 'sector_visible_tickers' not in st.session_state:
        st.session_state.sector_visible_tickers = []   # Will be populated on first run
    if 'custom_visible_tickers' not in st.session_state:
        st.session_state.custom_visible_tickers = []   # Will be populated on first run

def create_level1_predefined_selection():
    """Level 1: Predefined ticker selection with checkboxes"""
    from config.assets import COUNTRY_ETFS, SECTOR_ETFS, get_tickers_only
    
    st.sidebar.subheader("📋 Level 1: Predefined Assets")
    
    # Country ETFs Section
    with st.sidebar.expander("🌍 Country ETFs (52 available)", expanded=False):
        # Select All/Deselect All for Country ETFs
        col1, col2 = st.columns(2)
        with col1:
            if st.button("Select All Countries", key="select_all_countries"):
                st.session_state.selected_country_etfs = get_tickers_only(COUNTRY_ETFS)
        with col2:
            if st.button("Deselect All Countries", key="deselect_all_countries"):
                st.session_state.selected_country_etfs = []
        
        # Search filter for countries
        country_search = st.text_input(
            "Search countries:",
            key="country_search",
            placeholder="Type to filter..."
        )
        
        # Filter country ETFs based on search
        filtered_countries = COUNTRY_ETFS
        if country_search:
            filtered_countries = [
                (ticker, name) for ticker, name in COUNTRY_ETFS
                if country_search.lower() in name.lower() or country_search.lower() in ticker.lower()
            ]
        
        # Create checkboxes for country ETFs
        for ticker, display_name in filtered_countries:
            is_selected = ticker in st.session_state.selected_country_etfs
            if st.checkbox(
                f"{display_name} ({ticker})",
                value=is_selected,
                key=f"country_{ticker}"
            ):
                if ticker not in st.session_state.selected_country_etfs:
                    st.session_state.selected_country_etfs.append(ticker)
            else:
                if ticker in st.session_state.selected_country_etfs:
                    st.session_state.selected_country_etfs.remove(ticker)
        
        # Show selection count
        st.caption(f"Selected: {len(st.session_state.selected_country_etfs)} countries")
    
    # Sector ETFs Section
    with st.sidebar.expander("🏭 Sector ETFs (30 available)", expanded=False):
        # Select All/Deselect All for Sector ETFs
        col1, col2 = st.columns(2)
        with col1:
            if st.button("Select All Sectors", key="select_all_sectors"):
                st.session_state.selected_sector_etfs = get_tickers_only(SECTOR_ETFS)
        with col2:
            if st.button("Deselect All Sectors", key="deselect_all_sectors"):
                st.session_state.selected_sector_etfs = []
        
        # Search filter for sectors
        sector_search = st.text_input(
            "Search sectors:",
            key="sector_search",
            placeholder="Type to filter..."
        )
        
        # Filter sector ETFs based on search
        filtered_sectors = SECTOR_ETFS
        if sector_search:
            filtered_sectors = [
                (ticker, name) for ticker, name in SECTOR_ETFS
                if sector_search.lower() in name.lower() or sector_search.lower() in ticker.lower()
            ]
        
        # Create checkboxes for sector ETFs
        for ticker, display_name in filtered_sectors:
            is_selected = ticker in st.session_state.selected_sector_etfs
            if st.checkbox(
                f"{display_name} ({ticker})",
                value=is_selected,
                key=f"sector_{ticker}"
            ):
                if ticker not in st.session_state.selected_sector_etfs:
                    st.session_state.selected_sector_etfs.append(ticker)
            else:
                if ticker in st.session_state.selected_sector_etfs:
                    st.session_state.selected_sector_etfs.remove(ticker)
        
        # Show selection count
        st.caption(f"Selected: {len(st.session_state.selected_sector_etfs)} sectors")

def create_level2_permanent_expansion():
    """Level 2: Add new tickers to permanent predefined lists"""
    st.sidebar.subheader("➕ Level 2: Expand Permanent Lists")
    
    # Add to Country ETFs
    with st.sidebar.expander("🌍 Add New Country ETF", expanded=False):
        new_country_ticker = st.text_input(
            "Country ETF Ticker:",
            key="new_country_ticker",
            placeholder="e.g., EWK"
        ).upper().strip()
        
        new_country_name = st.text_input(
            "Display Name:",
            key="new_country_name",
            placeholder="e.g., Belgium"
        ).strip()
        
        if st.button("Add Country ETF", key="add_country_etf"):
            if new_country_ticker and new_country_name:
                # Check if already exists
                existing_tickers = [item[0] for item in st.session_state.permanent_country_additions]
                if new_country_ticker not in existing_tickers:
                    st.session_state.permanent_country_additions.append((new_country_ticker, new_country_name))
                    # Auto-select the newly added ticker
                    if new_country_ticker not in st.session_state.selected_country_etfs:
                        st.session_state.selected_country_etfs.append(new_country_ticker)
                    st.success(f"✅ Added {new_country_name} ({new_country_ticker}) to country ETFs")
                else:
                    st.warning(f"⚠️ {new_country_ticker} already exists in your additions")
            else:
                st.error("❌ Please enter both ticker and display name")
        
        # Show current permanent additions
        if st.session_state.permanent_country_additions:
            st.caption("Your additions:")
            for ticker, name in st.session_state.permanent_country_additions:
                st.caption(f"• {name} ({ticker})")
    
    # Add to Sector ETFs
    with st.sidebar.expander("🏭 Add New Sector ETF", expanded=False):
        new_sector_ticker = st.text_input(
            "Sector ETF Ticker:",
            key="new_sector_ticker",
            placeholder="e.g., JETS"
        ).upper().strip()
        
        new_sector_name = st.text_input(
            "Display Name:",
            key="new_sector_name",
            placeholder="e.g., Airlines"
        ).strip()
        
        if st.button("Add Sector ETF", key="add_sector_etf"):
            if new_sector_ticker and new_sector_name:
                # Check if already exists
                existing_tickers = [item[0] for item in st.session_state.permanent_sector_additions]
                if new_sector_ticker not in existing_tickers:
                    st.session_state.permanent_sector_additions.append((new_sector_ticker, new_sector_name))
                    # Auto-select the newly added ticker
                    if new_sector_ticker not in st.session_state.selected_sector_etfs:
                        st.session_state.selected_sector_etfs.append(new_sector_ticker)
                    st.success(f"✅ Added {new_sector_name} ({new_sector_ticker}) to sector ETFs")
                else:
                    st.warning(f"⚠️ {new_sector_ticker} already exists in your additions")
            else:
                st.error("❌ Please enter both ticker and display name")
        
        # Show current permanent additions
        if st.session_state.permanent_sector_additions:
            st.caption("Your additions:")
            for ticker, name in st.session_state.permanent_sector_additions:
                st.caption(f"• {name} ({ticker})")

def create_level3_session_custom():
    """Level 3: Session-only custom tickers with configurable limit"""
    st.sidebar.subheader("🎯 Level 3: Session Custom Tickers")
    
    # Configurable ticker limit
    st.session_state.custom_ticker_limit = st.sidebar.slider(
        "Max custom tickers:",
        min_value=5,
        max_value=50,
        value=st.session_state.custom_ticker_limit,
        help="Higher limits may slow analysis"
    )
    
    # Performance warning
    if st.session_state.custom_ticker_limit > 20:
        st.sidebar.warning("⚠️ Large ticker counts may slow analysis")
    
    # Add ticker(s) - unified input for single or multiple
    ticker_input = st.sidebar.text_area(
        "Add Ticker(s):",
        key="custom_ticker_input",
        placeholder="Single: TSLA\nMultiple: AAPL, MSFT, GOOGL\n(comma or line separated)",
        height=80
    )
    
    if st.sidebar.button("Add Ticker(s)", key="add_custom_tickers"):
        if ticker_input.strip():
            # Parse input (reuse bulk parsing logic)
            parsed_tickers = []
            for line in ticker_input.replace(',', '\n').split('\n'):
                ticker = line.strip().upper()
                if ticker and ticker not in parsed_tickers:
                    parsed_tickers.append(ticker)
            
            # Add tickers respecting limit
            added_count = 0
            current_count = len(st.session_state.session_custom_tickers)
            
            for ticker in parsed_tickers:
                if current_count + added_count < st.session_state.custom_ticker_limit:
                    if ticker not in st.session_state.session_custom_tickers:
                        st.session_state.session_custom_tickers.append(ticker)
                        added_count += 1
                else:
                    break
            
            if added_count > 0:
                st.success(f"✅ Added {added_count} ticker{'s' if added_count != 1 else ''}")
            if added_count < len(parsed_tickers):
                remaining = len(parsed_tickers) - added_count
                st.warning(f"⚠️ {remaining} ticker{'s' if remaining != 1 else ''} skipped (limit reached)")
        else:
            st.error("❌ Enter at least one ticker symbol")
    
    # Display current custom tickers with remove functionality
    if st.session_state.session_custom_tickers:
        st.sidebar.write("**Current custom tickers:**")
        
        # Show count
        count = len(st.session_state.session_custom_tickers)
        limit = st.session_state.custom_ticker_limit
        st.sidebar.caption(f"Selected: {count}/{limit} tickers")
        
        # Tag-style display with remove buttons
        tickers_to_remove = []
        for i, ticker in enumerate(st.session_state.session_custom_tickers):
            col1, col2 = st.sidebar.columns([3, 1])
            with col1:
                st.write(f"🏷️ {ticker}")
            with col2:
                if st.button("❌", key=f"remove_custom_{i}", help=f"Remove {ticker}"):
                    tickers_to_remove.append(ticker)
        
        # Remove tickers (done after iteration to avoid modification during iteration)
        for ticker in tickers_to_remove:
            st.session_state.session_custom_tickers.remove(ticker)
            st.success(f"✅ Removed {ticker}")
            st.rerun()
        
        # Clear all button
        if st.sidebar.button("🗑️ Clear All Custom", key="clear_all_custom"):
            st.session_state.session_custom_tickers = []
            st.success("✅ Cleared all custom tickers")
            st.rerun()
    
    # Database save toggle
    st.sidebar.markdown("---")
    st.session_state.save_custom_to_database = st.sidebar.checkbox(
        "💾 Save custom tickers to database",
        value=st.session_state.save_custom_to_database,
        help="When checked, custom ticker data will be permanently cached for faster future access"
    )


def create_sidebar_controls():
    """Create sidebar controls for bucket-based ticker management"""
    st.sidebar.title("⚙️ Dashboard Controls")

    # STEP 1: Bucket Selection
    st.sidebar.markdown("---")
    st.sidebar.subheader("📊 Select Analysis Bucket")

    st.session_state.selected_bucket = st.sidebar.radio(
        "Choose your analysis focus:",
        options=['country', 'sector', 'custom'],
        format_func=lambda x: {
            'country': '🌍 Country ETFs',
            'sector': '🏭 Sector ETFs', 
            'custom': '🎯 Custom Stocks'
        }[x],
        index=['country', 'sector', 'custom'].index(st.session_state.selected_bucket),
        key='bucket_selection'
    )

    # Show current selection
    bucket_names = {
        'country': 'Country ETFs',
        'sector': 'Sector ETFs',
        'custom': 'Custom Stocks'
    }
    st.sidebar.info(f"Currently analyzing: **{bucket_names[st.session_state.selected_bucket]}**")

    # STEP 3 & 4: Filter and Add Tickers for Selected Bucket
    st.sidebar.markdown("---")
    st.sidebar.subheader(f"🔧 Modify/Filter {bucket_names[st.session_state.selected_bucket]}")
    
    # Import needed functions
    from config.assets import COUNTRY_ETFS, SECTOR_ETFS, get_tickers_only
    
    # Initialize bucket_save_to_db variable
    bucket_save_to_db = True  # Default value
    
    if st.session_state.selected_bucket == 'country':
        # Initialize visible tickers if empty
        all_country_tickers = get_tickers_only(COUNTRY_ETFS)
        if not st.session_state.country_visible_tickers:
            st.session_state.country_visible_tickers = all_country_tickers.copy()
        
        # Country ETF filtering
        with st.sidebar.expander("📋 Show/Hide Country ETFs", expanded=False):
            for ticker, display_name in COUNTRY_ETFS:
                is_visible = ticker in st.session_state.country_visible_tickers
                if st.checkbox(
                    f"{display_name} ({ticker})",
                    value=is_visible,
                    key=f"filter_country_{ticker}"
                ):
                    if ticker not in st.session_state.country_visible_tickers:
                        st.session_state.country_visible_tickers.append(ticker)
                else:
                    if ticker in st.session_state.country_visible_tickers:
                        st.session_state.country_visible_tickers.remove(ticker)
            
            st.caption(f"Showing: {len(st.session_state.country_visible_tickers)}/{len(all_country_tickers)} country ETFs")
        
        # Add new Country ETF
        with st.sidebar.expander("➕ Add New Country ETF", expanded=False):
            new_country_ticker = st.text_input(
                "Country ETF Ticker:",
                key="new_country_ticker_step4",
                placeholder="e.g., EWK"
            ).upper().strip()
            
            new_country_name = st.text_input(
                "Display Name:",
                key="new_country_name_step4", 
                placeholder="e.g., Belgium"
            ).strip()
            
            # FIXED: Capture the bucket-specific toggle value
            bucket_save_to_db = st.checkbox(
                "💾 Save to database",
                value=True,
                key="save_country_to_db",
                help="Save historical data for faster future access"
            )
            
            if st.button("Add Country ETF", key="add_country_step4"):
                if new_country_ticker and new_country_name:
                    if new_country_ticker not in st.session_state.country_visible_tickers:
                        st.session_state.country_visible_tickers.append(new_country_ticker)
                        st.success(f"✅ Added {new_country_name} ({new_country_ticker}) to country ETFs")
                    else:
                        st.warning(f"⚠️ {new_country_ticker} already in your list")
                else:
                    st.error("❌ Please enter both ticker and display name")
    
    elif st.session_state.selected_bucket == 'sector':
        # Initialize visible tickers if empty
        all_sector_tickers = get_tickers_only(SECTOR_ETFS)
        if not st.session_state.sector_visible_tickers:
            st.session_state.sector_visible_tickers = all_sector_tickers.copy()
        
        # Sector ETF filtering
        with st.sidebar.expander("📋 Show/Hide Sector ETFs", expanded=False):
            for ticker, display_name in SECTOR_ETFS:
                is_visible = ticker in st.session_state.sector_visible_tickers
                if st.checkbox(
                    f"{display_name} ({ticker})",
                    value=is_visible,
                    key=f"filter_sector_{ticker}"
                ):
                    if ticker not in st.session_state.sector_visible_tickers:
                        st.session_state.sector_visible_tickers.append(ticker)
                else:
                    if ticker in st.session_state.sector_visible_tickers:
                        st.session_state.sector_visible_tickers.remove(ticker)
            
            st.caption(f"Showing: {len(st.session_state.sector_visible_tickers)}/{len(all_sector_tickers)} sector ETFs")
        
        # Add new Sector ETF
        with st.sidebar.expander("➕ Add New Sector ETF", expanded=False):
            new_sector_ticker = st.text_input(
                "Sector ETF Ticker:",
                key="new_sector_ticker_step4",
                placeholder="e.g., JETS"
            ).upper().strip()
            
            new_sector_name = st.text_input(
                "Display Name:",
                key="new_sector_name_step4",
                placeholder="e.g., Airlines"
            ).strip()
            
            # FIXED: Capture the bucket-specific toggle value
            bucket_save_to_db = st.checkbox(
                "💾 Save to database",
                value=True,
                key="save_sector_to_db",
                help="Save historical data for faster future access"
            )
            
            if st.button("Add Sector ETF", key="add_sector_step4"):
                if new_sector_ticker and new_sector_name:
                    if new_sector_ticker not in st.session_state.sector_visible_tickers:
                        st.session_state.sector_visible_tickers.append(new_sector_ticker)
                        st.success(f"✅ Added {new_sector_name} ({new_sector_ticker}) to sector ETFs")
                    else:
                        st.warning(f"⚠️ {new_sector_ticker} already in your list")
                else:
                    st.error("❌ Please enter both ticker and display name")
    
    else:  # custom bucket
        # Initialize visible tickers if empty
        if not st.session_state.custom_visible_tickers:
            st.session_state.custom_visible_tickers = list(CUSTOM_DEFAULT)
        
        # Custom stock filtering
        with st.sidebar.expander("📋 Show/Hide Custom Stocks", expanded=True):
            for ticker in CUSTOM_DEFAULT:
                is_visible = ticker in st.session_state.custom_visible_tickers
                if st.checkbox(
                    f"{ticker}",
                    value=is_visible,
                    key=f"filter_custom_{ticker}"
                ):
                    if ticker not in st.session_state.custom_visible_tickers:
                        st.session_state.custom_visible_tickers.append(ticker)
                else:
                    if ticker in st.session_state.custom_visible_tickers:
                        st.session_state.custom_visible_tickers.remove(ticker)
            
            st.caption(f"Showing: {len(st.session_state.custom_visible_tickers)}/{len(CUSTOM_DEFAULT)} custom stocks")
        
        # Add new Custom Stocks
        with st.sidebar.expander("➕ Add Custom Stocks", expanded=False):
            ticker_input = st.text_area(
                "Add Ticker(s):",
                key="custom_ticker_input_step4",
                placeholder="Single: TSLA\nMultiple: AAPL, MSFT, GOOGL\n(comma or line separated)",
                height=80
            )
            
            # FIXED: Capture the bucket-specific toggle value
            bucket_save_to_db = st.checkbox(
                "💾 Save to database",
                value=st.session_state.save_custom_to_database,
                key="save_custom_to_db_step4",
                help="Save historical data for faster future access"
            )
            
            if st.button("Add Ticker(s)", key="add_custom_step4"):
                if ticker_input.strip():
                    # Parse input
                    parsed_tickers = []
                    for line in ticker_input.replace(',', '\n').split('\n'):
                        ticker = line.strip().upper()
                        if ticker and ticker not in parsed_tickers:
                            parsed_tickers.append(ticker)
                    
                    # Add tickers
                    added_count = 0
                    for ticker in parsed_tickers:
                        if ticker not in st.session_state.custom_visible_tickers:
                            st.session_state.custom_visible_tickers.append(ticker)
                            added_count += 1
                    
                    if added_count > 0:
                        st.success(f"✅ Added {added_count} ticker{'s' if added_count != 1 else ''}")
                    if added_count < len(parsed_tickers):
                        skipped = len(parsed_tickers) - added_count
                        st.info(f"ℹ️ {skipped} ticker{'s' if skipped != 1 else ''} already in list")
                else:
                    st.error("❌ Enter at least one ticker symbol")

    # Ticker Aggregation Based on Selected Bucket
    st.sidebar.markdown("---")
    
    # Get final tickers based on bucket selection
    if st.session_state.selected_bucket == 'country':
        final_tickers = st.session_state.country_visible_tickers.copy()
    elif st.session_state.selected_bucket == 'sector':
        final_tickers = st.session_state.sector_visible_tickers.copy()
    else:  # custom bucket
        final_tickers = st.session_state.custom_visible_tickers.copy()
    
    # Remove duplicates while preserving order
    seen = set()
    deduplicated_tickers = []
    for ticker in final_tickers:
        if ticker not in seen:
            seen.add(ticker)
            deduplicated_tickers.append(ticker)
    
    final_tickers = deduplicated_tickers
    
    # Display current selection summary
    st.sidebar.success(f"✅ Total selected: {len(final_tickers)} tickers")
    st.sidebar.caption(f"Bucket: {bucket_names[st.session_state.selected_bucket]}")
    
    # Show preview
    preview_tickers = final_tickers[:5]
    preview_text = ", ".join(preview_tickers)
    if len(final_tickers) > 5:
        preview_text += f" +{len(final_tickers) - 5} more"
    st.sidebar.caption(f"Preview: {preview_text}")
    
    # Use bucket selection for asset group and title
    asset_group = st.session_state.selected_bucket
    
    bucket_titles = {
        'country': f"Country ETFs ({len(final_tickers)} tickers)",
        'sector': f"Sector ETFs ({len(final_tickers)} tickers)", 
        'custom': f"Custom Stocks ({len(final_tickers)} tickers)"
    }
    group_name = bucket_titles[st.session_state.selected_bucket]
    
    # Time Period Selection
    st.sidebar.subheader("⏰ Time Period")
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
    st.sidebar.subheader("🔄 Data Refresh")
    refresh_button = st.sidebar.button(
        "🔄 Refresh Data",
        help="Fetch latest market data",
        use_container_width=True
    )
    
    # FIXED: Return the actual bucket-specific database toggle value
    return {
        'group': asset_group,
        'group_name': group_name,
        'tickers': final_tickers,
        'period': selected_period,
        'period_name': selected_period_name,
        'refresh': refresh_button,
        'database_save': bucket_save_to_db  # ← NOW USES BUCKET-SPECIFIC TOGGLE
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

def fetch_performance_data(tickers, period, save_to_db: bool = True):
    """Fetch performance data with progress tracking and database usage reporting"""
    with st.spinner(f"Fetching data for {len(tickers)} tickers..."):
        # Create progress bar
        progress_bar = st.progress(0)
        status_text = st.empty()
        
        calculator = st.session_state.calculator
        
        # Use the group calculation method for better efficiency
        status_text.text(f"Processing {len(tickers)} tickers using database-first approach...")
        
        try:
            performance_data = calculator.calculate_performance_for_group(tickers, period, save_to_db=save_to_db)
            
            # Show database usage statistics
            summary = calculator.get_performance_summary(performance_data)
            
            progress_bar.progress(1.0)
            status_text.empty()
            
            # Display efficiency information
            if summary['database_usage'] > 0:
                st.success(
                    f"✅ Data fetched successfully! "
                    f"Database cache used for {summary['database_usage']}/{summary['valid_count']} tickers "
                    f"({summary['database_usage']/summary['valid_count']*100:.0f}% cache hit rate)"
                )
            else:
                st.info("ℹ️ Data fetched from yfinance (no database cache available)")
            
        except Exception as e:
            st.error(f"Error fetching performance data: {str(e)}")
            performance_data = []
        
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

def display_heatmap(performance_data, title, asset_group=None):
    """Display the main heatmap visualization"""
    generator = st.session_state.heatmap_generator
    
    # Create heatmap with asset group information
    fig = generator.create_treemap(
        performance_data=performance_data,
        title=title,
        width=1200,
        height=700,
        asset_group=asset_group
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
        
    # Check if we need to fetch new data (STEP 3: Include filter changes)
    ticker_count_changed = (
        st.session_state.performance_data is not None and 
        len(controls['tickers']) != len([p for p in st.session_state.performance_data if not p.get('error', False)])
    )

    should_fetch = (
        controls['refresh'] or 
        st.session_state.performance_data is None or
        (st.session_state.last_update is None) or
        ticker_count_changed  # NEW: Refresh when ticker count changes
    )
    
    if should_fetch:
        # Fetch performance data
        performance_data = fetch_performance_data(
            controls['tickers'], 
            controls['period'],
            save_to_db=controls['database_save']
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
        
        # Add baseline date info
        baseline_date = None
        if performance_data:
            for item in performance_data:
                if not item.get('error', False):
                    period = item.get('period', '1d')
                    
                    # FIXED: Use proper trading day calculation for baseline date
                    from src.calculations.performance import get_baseline_date_for_display
                    baseline_date_str = get_baseline_date_for_display(period)
                    baseline_date = datetime.strptime(baseline_date_str, '%Y-%m-%d').strftime('%m/%d/%y')
                    break
        
        if baseline_date:
            st.caption(f"Baseline Date: {baseline_date}")
        
        display_heatmap(performance_data, title, controls['group'])
        
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
