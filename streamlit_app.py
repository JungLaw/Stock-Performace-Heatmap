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
from typing import Dict

# Add src to path for imports
src_path = Path(__file__).parent / "src"
sys.path.insert(0, str(src_path))

# Import our modules
from calculations.performance import DatabaseIntegratedPerformanceCalculator
from calculations.volume import DatabaseIntegratedVolumeCalculator
from calculations.technical import DatabaseIntegratedTechnicalCalculator
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
    if 'volume_calculator' not in st.session_state:
        st.session_state.volume_calculator = DatabaseIntegratedVolumeCalculator()
    if 'technical_calculator' not in st.session_state:
        st.session_state.technical_calculator = DatabaseIntegratedTechnicalCalculator()
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
    
    # Page selection for navigation
    if 'selected_page' not in st.session_state:
        st.session_state.selected_page = 'performance_heatmaps'  # Default to existing heatmaps
    
    # Analysis mode selection
    if 'selected_analysis_mode' not in st.session_state:
        st.session_state.selected_analysis_mode = 'price'  # Default to price performance
    
    # Volume analysis data storage (separate from price performance)
    if 'volume_data' not in st.session_state:
        st.session_state.volume_data = None
    if 'volume_last_update' not in st.session_state:
        st.session_state.volume_last_update = None

    # Filtering state (Step 3: Future-ready for additions)
    if 'country_visible_tickers' not in st.session_state:
        st.session_state.country_visible_tickers = []  # Will be populated on first run
    if 'sector_visible_tickers' not in st.session_state:
        st.session_state.sector_visible_tickers = []   # Will be populated on first run
    if 'custom_visible_tickers' not in st.session_state:
        st.session_state.custom_visible_tickers = []   # Will be populated on first run

def is_bucket_ticker(ticker: str) -> bool:
    """
    Check if ticker exists in any of the three buckets (COUNTRY/SECTOR/CUSTOM)
    
    Args:
        ticker: Stock ticker symbol (uppercase)
        
    Returns:
        True if ticker is in any bucket, False otherwise
    """
    # Get all bucket tickers
    all_bucket_tickers = []
    
    # COUNTRY_ETFS
    for item in ASSET_GROUPS.get('country', []):
        if isinstance(item, tuple):
            all_bucket_tickers.append(item[0])  # (ticker, display_name)
        else:
            all_bucket_tickers.append(item)     # Just ticker
    
    # SECTOR_ETFS
    for item in ASSET_GROUPS.get('sector', []):
        if isinstance(item, tuple):
            all_bucket_tickers.append(item[0])
        else:
            all_bucket_tickers.append(item)
    
    # CUSTOM_DEFAULT
    for item in CUSTOM_DEFAULT:
        if isinstance(item, tuple):
            all_bucket_tickers.append(item[0])
        else:
            all_bucket_tickers.append(item)
    
    return ticker.upper() in [t.upper() for t in all_bucket_tickers]

def is_final_data_available_for_date(target_date: datetime) -> bool:
    """
    Check if final data is available for a given date
    Only save to database if data is from last completed trading day or earlier
    
    Args:
        target_date: The date to check
        
    Returns:
        True if final data is available (target_date <= last completed trading day)
    """
    from calculations.performance import get_last_completed_trading_day
    
    last_complete_day = get_last_completed_trading_day()
    
    # Convert both to date objects for comparison
    if isinstance(last_complete_day, datetime):
        last_complete_day = last_complete_day.date()
    
    if isinstance(target_date, datetime):
        target_date_only = target_date.date()
    else:
        target_date_only = target_date
    
    # Final data is available if target date is on or before last completed trading day
    return target_date_only <= last_complete_day

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

    # STEP 0: Analysis Mode Selection
    st.sidebar.markdown("---")
    st.sidebar.subheader("📈 Analysis Mode")
    
    st.session_state.selected_analysis_mode = st.sidebar.radio(
        "Choose analysis type:",
        options=['price', 'volume'],
        format_func=lambda x: {
            'price': '💰 Price Performance',
            'volume': '📊 Volume Performance'
        }[x],
        index=['price', 'volume'].index(st.session_state.selected_analysis_mode),
        key='analysis_mode_selection'
    )

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
    
    # Time Period Selection - conditional based on analysis mode
    st.sidebar.subheader("⏰ Time Period")
    
    if st.session_state.selected_analysis_mode == 'price':
        period_options = {
            "1 Day": "1d",
            "1 Week": "1w", 
            "1 Month": "1m",
            "3 Months": "3m",
            "6 Months": "6m",
            "Year to Date": "ytd",
            "1 Year": "1y"
        }
        period_label = "Compare against:"
    else:  # volume mode
        period_options = {
            "10 Days": "10d",
            "1 Week": "1w",
            "1 Month": "1m", 
            "60 Days": "60d"
        }
        period_label = "Volume benchmark period:"
    
    selected_period_name = st.sidebar.selectbox(
        period_label,
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
        'database_save': bucket_save_to_db,  # ← NOW USES BUCKET-SPECIFIC TOGGLE
        'analysis_mode': st.session_state.selected_analysis_mode
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

def fetch_volume_data(tickers, period, save_to_db: bool = True):
    """Fetch volume data with progress tracking and database usage reporting"""
    with st.spinner(f"Fetching volume data for {len(tickers)} tickers..."):
        # Create progress bar
        progress_bar = st.progress(0)
        status_text = st.empty()
        
        volume_calculator = st.session_state.volume_calculator
        
        # Use the group calculation method for better efficiency
        status_text.text(f"Processing {len(tickers)} tickers using database-first approach...")
        
        try:
            volume_data = volume_calculator.calculate_volume_performance_for_group(tickers, period)
            
            # Show database usage statistics
            valid_count = len([v for v in volume_data if not v.get('error', False)])
            error_count = len([v for v in volume_data if v.get('error', False)])
            database_usage = len([v for v in volume_data if v.get('data_source') == 'database'])
            
            progress_bar.progress(1.0)
            status_text.empty()
            
            # Display efficiency information
            if database_usage > 0:
                cache_rate = database_usage / valid_count * 100 if valid_count > 0 else 0
                st.success(
                    f"✅ Volume data fetched successfully! "
                    f"Database cache used for {database_usage}/{valid_count} tickers "
                    f"({cache_rate:.0f}% cache hit rate)"
                )
            else:
                st.info("ℹ️ Volume data fetched from yfinance (no database cache available)")
            
        except Exception as e:
            st.error(f"Error fetching volume data: {str(e)}")
            volume_data = []
        
        # Clear progress indicators
        progress_bar.empty()
        status_text.empty()
        
        return volume_data

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
            # Handle both price and volume data structures
            if 'percentage_change' in best:
                performance_value = best['percentage_change']
            elif 'volume_change' in best:
                performance_value = best['volume_change']
            else:
                performance_value = 0.0
            
            st.success(
                f"🏆 Best: **{best['ticker']}** "
                f"({performance_value:+.2f}%)"
            )
        
        with col2:
            worst = stats['worst_performer']
            # Handle both price and volume data structures
            if 'percentage_change' in worst:
                performance_value = worst['percentage_change']
            elif 'volume_change' in worst:
                performance_value = worst['volume_change']
            else:
                performance_value = 0.0
            
            st.error(
                f"📉 Worst: **{worst['ticker']}** "
                f"({performance_value:+.2f}%)"
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

def generate_ma_comment(ticker, period, ma_type, current_price, ma_value, price_vs_ma):
    """Generate contextual comment for moving average"""
    # Determine if price is above or below MA
    if price_vs_ma > 0:
        direction = "above"
        fall_pct = abs((ma_value - current_price) / current_price * 100)
        comment = f"{ticker} is {price_vs_ma:+.1f}% above its {period}D {ma_type}. It has to fall {fall_pct:.1f}% to reach it."
    else:
        direction = "below"
        rise_pct = abs((ma_value - current_price) / current_price * 100)
        comment = f"{ticker} is {price_vs_ma:.1f}% below its {period}D {ma_type}. It has to rise {rise_pct:.1f}% to reach it."
    
    return comment

def display_technical_indicators_cards(indicators_data):
    """Display technical indicators in card-based layout similar to Investing.com"""
    if not indicators_data:
        st.warning("No technical indicators data available")
        return
    
    # Define indicator display order and formatting
    indicator_configs = {
        'rsi_14': {
            'name': 'RSI (14)',
            'format': '{:.2f}',
            'description': 'Relative Strength Index'
        },
        'macd': {
            'name': 'MACD (12,26)',
            'format': '{:.3f}',
            'description': 'Moving Average Convergence Divergence'
        },
        'stochastic': {
            'name': 'STOCH (9,6)',
            'format': '{:.2f}',
            'description': 'Stochastic Oscillator'
        },
        'adx': {
            'name': 'ADX (14)',
            'format': '{:.2f}',
            'description': 'Average Directional Index'
        },
        'elder_ray': {
            'name': 'Bull/Bear Power',
            'format': '{:.3f}',
            'description': 'Elder-ray System'
        },
        'atr_14': {
            'name': 'ATR (14)',
            'format': '{:.2f}',
            'description': 'Average True Range'
        },
        'williams_r': {
            'name': 'Williams %R',
            'format': '{:.2f}',
            'description': 'Williams Percent Range'
        },
        'cci_14': {
            'name': 'CCI (14)',
            'format': '{:.2f}',
            'description': 'Commodity Channel Index'
        },
        'ultimate_osc': {
            'name': 'Ultimate Osc',
            'format': '{:.2f}',
            'description': 'Ultimate Oscillator'
        },
        'roc_12': {
            'name': 'ROC (12)',
            'format': '{:.2f}',
            'description': 'Rate of Change'
        }
    }
    
    # Create responsive grid layout - 3 columns for 10 indicators
    cols = st.columns(3)
    
    col_index = 0
    for indicator_key, config in indicator_configs.items():
        if indicator_key in indicators_data:
            indicator = indicators_data[indicator_key]
            
            with cols[col_index % 3]:
                _display_indicator_card(
                    indicator_key,
                    config,
                    indicator
                )
            
            col_index += 1

def _display_indicator_card(indicator_key, config, indicator_data):
    """Display individual technical indicator card"""
    
    # Extract signal information
    signal_info = indicator_data.get('signal', {})
    signal = signal_info.get('signal', 'N/A')
    description = signal_info.get('description', '')
    
    # Get indicator value(s)
    if indicator_key == 'macd':
        value = indicator_data.get('value', 0)
        signal_line = indicator_data.get('signal_line', 0)
        display_value = f"{value:.3f} / {signal_line:.3f}"
    elif indicator_key == 'stochastic':
        k_value = indicator_data.get('k', 0)
        d_value = indicator_data.get('d', 0)
        display_value = f"%K: {k_value:.2f}, %D: {d_value:.2f}"
    elif indicator_key == 'adx':
        adx_value = indicator_data.get('value', 0)
        plus_di = indicator_data.get('plus_di', 0)
        minus_di = indicator_data.get('minus_di', 0)
        display_value = f"{adx_value:.2f} (+DI: {plus_di:.2f}, -DI: {minus_di:.2f})"
    elif indicator_key == 'elder_ray':
        bull_power = indicator_data.get('bull_power', 0)
        bear_power = indicator_data.get('bear_power', 0)
        display_value = f"Bull: {bull_power:.3f}, Bear: {bear_power:.3f}"
    else:
        value = indicator_data.get('value', 0)
        # Handle None values gracefully
        if value is None:
            display_value = "N/A"
        else:
            display_value = config['format'].format(value)
    
    # Determine signal color
    signal_colors = {
        'Buy': '🟢',
        'Strong Buy': '🟢',
        'Sell': '🔴', 
        'Strong Sell': '🔴',
        'Neutral': '⚪',
        'N/A': '⚫'
    }
    
    signal_color = signal_colors.get(signal, '⚪')
    
    # Generate contextual comment
    comment = _generate_indicator_comment(indicator_key, indicator_data, signal_info)
    
    # Create card using container
    with st.container():
        st.markdown(f"""
        <div style="
            border: 1px solid #ddd;
            border-radius: 8px;
            padding: 16px;
            margin-bottom: 12px;
            background-color: #fafafa;
        ">
            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 8px;">
                <h4 style="margin: 0; color: #333;">{config['name']}</h4>
                <span style="font-size: 18px;">{signal_color}</span>
            </div>
            <div style="margin-bottom: 8px;">
                <strong style="font-size: 18px; color: #333;">{display_value}</strong>
            </div>
            <div style="margin-bottom: 8px;">
                <span style="
                    background-color: {'#d4edda' if 'Buy' in signal else '#f8d7da' if 'Sell' in signal else '#e2e3e5'};
                    color: {'#155724' if 'Buy' in signal else '#721c24' if 'Sell' in signal else '#383d41'};
                    padding: 4px 8px;
                    border-radius: 4px;
                    font-size: 12px;
                    font-weight: bold;
                ">{signal}</span>
            </div>
            <div style="font-size: 14px; color: #666; line-height: 1.4;">
                {comment}
            </div>
        </div>
        """, unsafe_allow_html=True)

def _generate_indicator_comment(indicator_key, indicator_data, signal_info):
    """Generate contextual comments for technical indicators using signal_info to avoid duplication"""
    
    signal = signal_info.get('signal', 'N/A')
    description = signal_info.get('description', '')
    
    if indicator_key == 'rsi_14':
        value = indicator_data.get('value', 0)
        # Use signal_info description and add contextual value information
        base_comment = description or f"RSI signal: {signal}"
        return f"RSI at {value:.1f}. {base_comment}"
    
    elif indicator_key == 'macd':
        value = indicator_data.get('value', 0)
        signal_line = indicator_data.get('signal_line', 0)
        base_comment = description or f"MACD signal: {signal}"
        return f"MACD at {value:.3f} (Signal: {signal_line:.3f}). {base_comment}"
    
    elif indicator_key == 'stochastic':
        k_value = indicator_data.get('k', 0)
        d_value = indicator_data.get('d', 0)
        base_comment = description or f"Stochastic signal: {signal}"
        return f"Stochastic %K: {k_value:.1f}, %D: {d_value:.1f}. {base_comment}"
    
    elif indicator_key == 'adx':
        adx_value = indicator_data.get('value', 0)
        plus_di = indicator_data.get('plus_di', 0)
        minus_di = indicator_data.get('minus_di', 0)
        base_comment = description or f"ADX signal: {signal}"
        return f"ADX: {adx_value:.1f} (+DI: {plus_di:.1f}, -DI: {minus_di:.1f}). {base_comment}"
    
    elif indicator_key == 'elder_ray':
        bull_power = indicator_data.get('bull_power', 0)
        bear_power = indicator_data.get('bear_power', 0)
        base_comment = description or f"Elder Ray signal: {signal}"
        return f"Bull Power: {bull_power:.3f}, Bear Power: {bear_power:.3f}. {base_comment}"
    
    elif indicator_key == 'atr_14':
        value = indicator_data.get('value', 0)
        return f"ATR at {value:.2f} measures current volatility. Higher values indicate increased price movement potential."
    
    elif indicator_key == 'williams_r':
        value = indicator_data.get('value', 0)
        base_comment = description or f"Williams %R signal: {signal}"
        return f"Williams %R at {value:.1f}. {base_comment}"
    
    elif indicator_key == 'cci_14':
        value = indicator_data.get('value', 0)
        base_comment = description or f"CCI signal: {signal}"
        return f"CCI at {value:.1f}. {base_comment}"
    
    elif indicator_key == 'ultimate_osc':
        value = indicator_data.get('value', 0)
        base_comment = description or f"Ultimate Oscillator signal: {signal}"
        return f"Ultimate Oscillator at {value:.1f}. {base_comment}"
    
    elif indicator_key == 'roc_12':
        value = indicator_data.get('value', 0)
        base_comment = description or f"ROC signal: {signal}"
        return f"ROC at {value:.2f}%. {base_comment}"
    
    # Fallback to signal description
    return description or f"{signal} signal detected."

def display_moving_averages_table(ma_data):
    """Display professional moving averages table with color coding and comments"""
    if not ma_data or ma_data.get('error'):
        st.error(f"Error loading moving averages: {ma_data.get('message', 'Unknown error')}")
        return
    
    # Extract data
    ticker = ma_data['ticker']
    current_price = ma_data['current_price']
    calc_date = ma_data['calculation_date']
    periods_data = ma_data['periods']
    
    # Display current price header
    st.caption(f"Current Price: ${current_price:.2f} ({calc_date})")
    
    # Prepare table data
    table_rows = []
    periods = [5, 9, 10, 20, 21, 50, 100, 200]
    
    for period in periods:
        period_key = f'MA{period}'
        if period_key not in periods_data:
            continue
        
        sma_data = periods_data[period_key]['sma']
        ema_data = periods_data[period_key]['ema']
        
        # Generate comments for both SMA and EMA
        sma_comment = generate_ma_comment(ticker, period, 'SMA', current_price, 
                                         sma_data['value'], sma_data['price_vs_ma'])
        ema_comment = generate_ma_comment(ticker, period, 'EMA', current_price,
                                         ema_data['value'], ema_data['price_vs_ma'])
        
        # Column order: Period | SMA | P0/SMA | SMA/P0 | Signal | Comments | EMA | P0/EMA | EMA/P0 | Signal | Comments
        row = {
            'Period': f'MA{period}',
            'SMA': f"${sma_data['value']:.2f}",
            'P0/SMA': f"{sma_data['price_vs_ma']:+.1f}%",
            'SMA/P0': f"{sma_data['ma_vs_price']:+.1f}%",
            'SMA_Signal': sma_data['signal'],
            'SMA_Comments': sma_comment,
            'EMA': f"${ema_data['value']:.2f}",
            'P0/EMA': f"{ema_data['price_vs_ma']:+.1f}%",
            'EMA/P0': f"{ema_data['ma_vs_price']:+.1f}%",
            'EMA_Signal': ema_data['signal'],
            'EMA_Comments': ema_comment
        }
        table_rows.append(row)
    
    # Create DataFrame
    df = pd.DataFrame(table_rows)
    
    # Apply styling with proper function for row-wise styling
    def style_row(row):
        """Apply color to signal cells"""
        styles = [''] * len(row)
        
        # Find signal column indices
        cols = list(row.index)
        if 'SMA_Signal' in cols:
            sma_signal_idx = cols.index('SMA_Signal')
            if row['SMA_Signal'] == 'Buy':
                styles[sma_signal_idx] = 'background-color: #d4edda; color: #155724; font-weight: bold'
            elif row['SMA_Signal'] == 'Sell':
                styles[sma_signal_idx] = 'background-color: #f8d7da; color: #721c24; font-weight: bold'
            else:  # Neutral
                styles[sma_signal_idx] = 'background-color: #f8f9fa; color: #6c757d; font-weight: bold'
        
        if 'EMA_Signal' in cols:
            ema_signal_idx = cols.index('EMA_Signal')
            if row['EMA_Signal'] == 'Buy':
                styles[ema_signal_idx] = 'background-color: #d4edda; color: #155724; font-weight: bold'
            elif row['EMA_Signal'] == 'Sell':
                styles[ema_signal_idx] = 'background-color: #f8d7da; color: #721c24; font-weight: bold'
            else:  # Neutral
                styles[ema_signal_idx] = 'background-color: #f8f9fa; color: #6c757d; font-weight: bold'
        
        return styles
    
    # Apply styling
    styled_df = df.style.apply(style_row, axis=1).set_properties(**{
        'text-align': 'left',
        'font-size': '14px',
        'padding': '8px'
    }).set_table_styles([
        {'selector': 'th', 'props': [('background-color', '#f8f9fa'), 
                                      ('font-weight', 'bold'),
                                      ('text-align', 'left'),
                                      ('padding', '10px')]}
    ])
    
    # Display table
    st.dataframe(
        styled_df,
        column_config={
            'Period': st.column_config.TextColumn('Period', width='small'),
            'SMA': st.column_config.TextColumn('SMA', width='small'),
            'P0/SMA': st.column_config.TextColumn('P0/SMA', width='small'),
            'SMA/P0': st.column_config.TextColumn('SMA/P0', width='small'),
            'SMA_Signal': st.column_config.TextColumn('Signal', width='small'),
            'SMA_Comments': st.column_config.TextColumn('Comments', width='large'),
            'EMA': st.column_config.TextColumn('EMA', width='small'),
            'P0/EMA': st.column_config.TextColumn('P0/EMA', width='small'),
            'EMA/P0': st.column_config.TextColumn('EMA/P0', width='small'),
            'EMA_Signal': st.column_config.TextColumn('Signal', width='small'),
            'EMA_Comments': st.column_config.TextColumn('Comments', width='large')
        },
        hide_index=True,
        use_container_width=True
    )

def display_pivot_points(ticker: str, pivot_data: Dict, current_price: float) -> None:
    """
    Display pivot points analysis - All 4 pivot types side-by-side
    
    Args:
        ticker: Stock ticker symbol
        pivot_data: Dictionary with pivot calculations (classic, fibonacci, camarilla, woodys)
        current_price: Current stock price
    """
    if pivot_data.get('error'):
        st.error(f"Error calculating pivot points: {pivot_data.get('message', 'Unknown error')}")
        return
    
    # Display calculation metadata
    st.caption(f"Calculated using {pivot_data.get('ohlc_date', 'N/A')} OHLC data (previous trading day)")
    
    # Extract all pivot types
    classic = pivot_data.get('classic')
    fibonacci = pivot_data.get('fibonacci')
    camarilla = pivot_data.get('camarilla')
    woodys = pivot_data.get('woodys')
    
    # Check if we have at least one pivot type
    if not any([classic, fibonacci, camarilla, woodys]):
        st.warning("No pivot data available")
        return
    
    # Build DataFrame for side-by-side display
    pivot_levels = ['R3', 'R2', 'R1', 'Pivot', 'S1', 'S2', 'S3']
    pivot_keys = ['r3', 'r2', 'r1', 'pivot', 's1', 's2', 's3']
    
    table_data = []
    for level_name, level_key in zip(pivot_levels, pivot_keys):
        row = {'Level': level_name}
        
        # Add Classic
        if classic and level_key in classic:
            row['Classic'] = f"${classic[level_key]:.2f}"
        else:
            row['Classic'] = "N/A"
        
        # Add Fibonacci
        if fibonacci and level_key in fibonacci:
            row['Fibonacci'] = f"${fibonacci[level_key]:.2f}"
        else:
            row['Fibonacci'] = "N/A"
        
        # Add Camarilla
        if camarilla and level_key in camarilla:
            row['Camarilla'] = f"${camarilla[level_key]:.2f}"
        else:
            row['Camarilla'] = "N/A"
        
        # Add Woody's
        if woodys and level_key in woodys:
            row["Woody's"] = f"${woodys[level_key]:.2f}"
        else:
            row["Woody's"] = "N/A"
        
        table_data.append(row)
    
    # Create DataFrame
    df = pd.DataFrame(table_data)
    
    # Display as styled table
    st.dataframe(
        df,
        hide_index=True,
        use_container_width=True,
        column_config={
            "Level": st.column_config.TextColumn("Level", width="small"),
            "Classic": st.column_config.TextColumn("Classic", width="medium"),
            "Fibonacci": st.column_config.TextColumn("Fibonacci", width="medium"),
            "Camarilla": st.column_config.TextColumn("Camarilla", width="medium"),
            "Woody's": st.column_config.TextColumn("Woody's", width="medium")
        }
    )
    
    st.caption(f"Current Price: ${current_price:.2f}")

def display_data_table(performance_data):
    """Display detailed data table for both price and volume data"""
    if not performance_data:
        return
    
    # Filter valid data and create DataFrame
    valid_data = [p for p in performance_data if not p.get('error', False)]
    
    if not valid_data:
        st.warning("No valid data to display in table")
        return
    
    # Detect data type and create appropriate DataFrame
    if valid_data and 'percentage_change' in valid_data[0]:
        # Price performance data
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
            
    elif valid_data and 'volume_change' in valid_data[0]:
        # Volume performance data
        df_display = pd.DataFrame([
            {
                'Ticker': p['ticker'],
                'Current Volume': f"{p['current_volume']:,}" if p['current_volume'] else "N/A",
                'Benchmark Average': f"{p['benchmark_average']:,.0f}" if p['benchmark_average'] else "N/A",
                'Volume Change': f"{p['volume_change']:+.2f}%" if p['volume_change'] is not None else "N/A",
                'Benchmark Period': p.get('benchmark_label', p.get('benchmark_period', 'N/A'))
            }
            for p in valid_data
        ])
        # Sort by volume change (descending)
        df_display = df_display.sort_values('Volume Change', key=lambda x: 
            pd.to_numeric(x.str.rstrip('%'), errors='coerce'), ascending=False)
    else:
        # Unknown data structure
        st.warning("Unknown data format - cannot display table")
        return
    
    st.dataframe(
        df_display,
        use_container_width=True,
        hide_index=True
    )

def show_technical_analysis_dashboard():
    """Dashboard 1: Single Stock Technical Analysis"""
    st.title("🎯 Technical Analysis Dashboard")
    
    # Description
    st.markdown("""
    Comprehensive technical analysis for individual stocks with moving averages,
    technical indicators, and signal analysis.
    """)
    
    # Ticker input section
    st.subheader("📊 Stock Selection")
    
    col1, col2, col3 = st.columns([3, 2, 1])
    
    with col1:
        ticker = st.text_input(
            "Enter Stock Symbol:",
            value="NVDA",
            placeholder="e.g., AAPL, MSFT, GOOGL",
            help="Enter any valid stock ticker symbol"
        ).upper().strip()
    
    with col2:
        # Save to database checkbox (only for non-bucket tickers)
        save_to_db_checkbox = st.checkbox(
            "Save to database (Tracker)",
            value=False,
            help="Check to permanently track this ticker with daily updates. Bucket tickers (Country/Sector/Custom) are always saved.",
            key="ta_save_to_db_checkbox"
        )
    
    with col3:
        analyze_button = st.button(
            "🔍 Analyze",
            type="primary",
            use_container_width=True
        )
    
    if ticker and (analyze_button or 'current_ticker' not in st.session_state or st.session_state.current_ticker != ticker):
        # Store current ticker for persistence
        st.session_state.current_ticker = ticker
        
        # Determine if we should save to database
        is_bucket = is_bucket_ticker(ticker)
        
        # Bucket tickers always save, non-bucket tickers respect checkbox
        should_save_to_db = is_bucket or save_to_db_checkbox
        
        # Show info message about save behavior
        if is_bucket:
            st.info(f"ℹ️ {ticker} is a bucket ticker and will be automatically tracked with daily updates.")
        elif save_to_db_checkbox:
            st.info(f"ℹ️ {ticker} will be added to tracking list with daily updates.")
        else:
            st.info(f"ℹ️ {ticker} analysis is session-only. Check 'Save to database' to track permanently.")
        
        # Fetch technical analysis data
        with st.spinner(f"Analyzing {ticker}..."):
            try:
                technical_calculator = st.session_state.technical_calculator
                
                # Calculate comprehensive technical analysis with save_to_db control
                analysis_data = technical_calculator.calculate_comprehensive_analysis(
                    ticker, 
                    save_to_db=should_save_to_db
                )
                
                if not analysis_data.get('error'):
                    # Store in session state
                    st.session_state.technical_analysis_data = analysis_data
                    st.session_state.technical_analysis_ticker = ticker
                    st.session_state.technical_analysis_timestamp = datetime.now()
                    
                    # Also calculate 52-week analysis on initial analysis
                    extremes_result = technical_calculator.calculate_52_week_analysis(ticker)
                    if extremes_result.get('success'):
                        st.session_state.price_extremes_data = extremes_result['periods']
                    
                    st.success(f"✅ Analysis complete for {ticker}")
                else:
                    st.error(f"❌ Error analyzing {ticker}: {analysis_data.get('message', 'Unknown error')}")
                    return
                    
            except Exception as e:
                st.error(f"❌ Error analyzing {ticker}: {str(e)}")
                return
    
    # Display analysis if available
    if ('technical_analysis_data' in st.session_state and 
        'technical_analysis_ticker' in st.session_state and
        st.session_state.technical_analysis_ticker == ticker):
        
        data = st.session_state.technical_analysis_data
        
        # Show timestamp
        if 'technical_analysis_timestamp' in st.session_state:
            timestamp = st.session_state.technical_analysis_timestamp
            st.caption(f"Analysis generated: {timestamp.strftime('%Y-%m-%d %H:%M:%S')}")
        
        st.markdown("---")
        
        # PLACEHOLDER: Display technical analysis components
        # These will be implemented in subsequent steps
        
        # Moving Averages Table
        st.subheader("📈 Moving Averages Analysis")
        if 'moving_averages' in data:
            display_moving_averages_table(data['moving_averages'])
        
        # Technical Indicators Table  
        st.subheader("📊 Technical Indicators")
        if 'technical_indicators' in data:
            display_technical_indicators_cards(data['technical_indicators'])
        else:
            st.warning("Technical indicators data not available")
        
        # 52-Week High Analysis
        st.subheader("📊 52-Week High Analysis")
        
        # Get current price for display
        current_price = data.get('current_price', 0)
        timestamp_str = datetime.now().strftime('%m/%d/%Y, %I:%M %p')
        
        # Display current price
        st.markdown(f"**Current Price:** ${current_price:.2f} ({timestamp_str})")
        st.markdown("---")
        
        # Display 52-week analysis table if data available
        if 'price_extremes_data' in st.session_state and st.session_state.price_extremes_data:
            periods_data = st.session_state.price_extremes_data
            
            # Create display table with restructured columns
            table_rows = []
            period_order = ['52w', '52w_close', '6m', '3m', '1m', 'ytd']
            period_labels = {
                '52w': '52W',
                '52w_close': '52W (Close)',
                '6m': '6M',
                '3m': '3M',
                '1m': '1M',
                'ytd': 'YTD'
            }
            
            for period in period_order:
                if period in periods_data:
                    p_data = periods_data[period]
                    
                    # Calculate current vs levels
                    vs_high = ((current_price - p_data['high_price']) / p_data['high_price']) * 100
                    vs_5pct = ((current_price - p_data['level_minus_5pct']) / p_data['level_minus_5pct']) * 100
                    vs_10pct = ((current_price - p_data['level_minus_10pct']) / p_data['level_minus_10pct']) * 100
                    vs_15pct = ((current_price - p_data['level_minus_15pct']) / p_data['level_minus_15pct']) * 100
                    vs_20pct = ((current_price - p_data['level_minus_20pct']) / p_data['level_minus_20pct']) * 100
                    vs_33pct = ((current_price - p_data['level_minus_33pct']) / p_data['level_minus_33pct']) * 100
                    vs_low = ((current_price - p_data['low_price']) / p_data['low_price']) * 100
                    
                    row = {
                        'Period': period_labels[period],
                        'High': f"${p_data['high_price']:.2f}",
                        '% Chg (High)': f"{vs_high:+.1f}%",
                        '-5%': f"${p_data['level_minus_5pct']:.2f}",
                        '% Chg (-5%)': f"{vs_5pct:+.1f}%",
                        '-10%': f"${p_data['level_minus_10pct']:.2f}",
                        '% Chg (-10%)': f"{vs_10pct:+.1f}%",
                        '-15%': f"${p_data['level_minus_15pct']:.2f}",
                        '% Chg (-15%)': f"{vs_15pct:+.1f}%",
                        '-20%': f"${p_data['level_minus_20pct']:.2f}",
                        '% Chg (-20%)': f"{vs_20pct:+.1f}%",
                        '-33%': f"${p_data['level_minus_33pct']:.2f}",
                        '% Chg (-33%)': f"{vs_33pct:+.1f}%",
                        'Low': f"${p_data['low_price']:.2f}",
                        '% Chg (Low)': f"{vs_low:+.1f}%"
                    }
                    table_rows.append(row)
            
            if table_rows:
                df = pd.DataFrame(table_rows)
                # TODO: Add styling for negative percentages (red color)
                st.dataframe(df, use_container_width=True, hide_index=True)
        
        # Custom input section BELOW table
        st.markdown("---")
        st.markdown("**Update 52W High** (optional)")
        
        col1, col2, col3 = st.columns([2, 2, 1])
        
        with col1:
            custom_52w_high = st.number_input(
                "Custom 52W high:",
                min_value=0.01,
                value=None,
                step=None,  # Removes +/- buttons
                format="%.2f",
                placeholder="e.g., 195.30",
                help="Enter intraday high exceeding 52W closing high",
                key="custom_52w_high_input"
            )
        
        with col2:
            custom_date = st.date_input(
                "Date of high:",
                value=None,
                help="Date when the custom high occurred",
                key="custom_52w_date_input"
            )
        
        with col3:
            st.markdown("<br>", unsafe_allow_html=True)  # Spacer for alignment
            if st.button("🔄 Update", key="update_52w", use_container_width=True):
                if custom_52w_high:
                    with st.spinner("Updating 52-week analysis..."):
                        extremes_result = st.session_state.technical_calculator.calculate_52_week_analysis(
                            ticker,
                            user_52w_high=custom_52w_high
                        )
                        
                        if extremes_result.get('error'):
                            st.error(f"❌ {extremes_result['message']}")
                        elif extremes_result.get('success'):
                            st.session_state.price_extremes_data = extremes_result['periods']
                            st.success("✅ 52-week analysis updated")
                            st.rerun()
                else:
                    st.warning("⚠️ Enter a custom high value first")
        
        # Pivot Points Analysis
        st.markdown("---")
        st.subheader("📍 Pivot Points Analysis")
        
        # Determine save_to_db setting (same logic as main analysis)
        is_bucket = is_bucket_ticker(ticker)
        should_save_to_db = is_bucket or st.session_state.get('ta_save_to_db_checkbox', False)
        
        # Calculate pivot points if not already cached in session
        if 'pivot_points_data' not in st.session_state or st.session_state.get('pivot_points_ticker') != ticker:
            with st.spinner("Calculating pivot points..."):
                try:
                    pivot_data = st.session_state.technical_calculator.calculate_pivot_points(
                        ticker=ticker,
                        target_date=None,  # Auto-detect previous trading day
                        save_to_db=should_save_to_db
                    )
                    st.session_state.pivot_points_data = pivot_data
                    st.session_state.pivot_points_ticker = ticker
                except Exception as e:
                    st.error(f"Error calculating pivot points: {str(e)}")
                    st.session_state.pivot_points_data = {'error': True, 'message': str(e)}
        
        # Display pivot points
        if 'pivot_points_data' in st.session_state:
            display_pivot_points(
                ticker=ticker,
                pivot_data=st.session_state.pivot_points_data,
                current_price=current_price
            )
        else:
            st.info("Pivot points data not available")
        
        # Rolling Heatmap
        st.subheader("🔥 Rolling Signal Heatmap")
        if 'rolling_signals' in data:
            # TODO: Implement 10-day rolling heatmap
            st.info("Rolling signal heatmap coming soon...")
            with st.expander("Raw Rolling Signals Data", expanded=False):
                st.json(data['rolling_signals'])
    
    elif ticker:
        st.info(f"👆 Click 'Analyze Stock' to get technical analysis for {ticker}")
    else:
        st.info("👆 Enter a stock ticker symbol above to get started")

def show_performance_heatmaps():
    """Original Performance Heatmaps Dashboard (Existing Functionality)"""
    # Create header
    create_header()
    
    # Create sidebar controls
    controls = create_sidebar_controls()
        
    # Check if we need to fetch new data - handle both price and volume modes
    if controls['analysis_mode'] == 'price':
        current_data = st.session_state.performance_data
        last_update = st.session_state.last_update
    else:  # volume mode
        current_data = st.session_state.volume_data
        last_update = st.session_state.volume_last_update
    
    ticker_count_changed = (
        current_data is not None and 
        len(controls['tickers']) != len([p for p in current_data if not p.get('error', False)])
    )

    should_fetch = (
        controls['refresh'] or 
        current_data is None or
        last_update is None or
        ticker_count_changed  # NEW: Refresh when ticker count changes
    )
    
    if should_fetch:
        if controls['analysis_mode'] == 'price':
            # Fetch price performance data
            performance_data = fetch_performance_data(
                controls['tickers'], 
                controls['period'],
                save_to_db=controls['database_save']
            )
            
            # Store in session state
            st.session_state.performance_data = performance_data
            st.session_state.last_update = datetime.now()
            current_data = performance_data
            
        else:  # volume mode
            # Fetch volume performance data
            volume_data = fetch_volume_data(
                controls['tickers'], 
                controls['period'],
                save_to_db=controls['database_save']
            )
            
            # Store in session state
            st.session_state.volume_data = volume_data
            st.session_state.volume_last_update = datetime.now()
            current_data = volume_data
        
        st.success(f"✅ Data updated successfully at {datetime.now().strftime('%H:%M:%S')}")
    else:
        # Use cached data based on analysis mode
        if controls['analysis_mode'] == 'price':
            current_data = st.session_state.performance_data
        else:
            current_data = st.session_state.volume_data
    
    if current_data:
        # Create heatmap title based on analysis mode
        if controls['analysis_mode'] == 'price':
            title = f"{controls['group_name']} - {controls['period_name']} Performance"
        else:  # volume mode
            title = f"{controls['group_name']} - Current Volume vs. {controls['period_name']} Avg."
        
        # Display summary statistics
        st.subheader("📊 Summary Statistics")
        display_summary_stats(current_data)
        
        st.markdown("---")
        
        # Display heatmap
        st.subheader("🗺️ Performance Heatmap")
        
        # Add baseline date info (only for price mode)
        if controls['analysis_mode'] == 'price':
            baseline_date = None
            if current_data:
                for item in current_data:
                    if not item.get('error', False):
                        period = item.get('period', '1d')
                        
                        # FIXED: Use proper trading day calculation for baseline date
                        from src.calculations.performance import get_baseline_date_for_display
                        baseline_date_str = get_baseline_date_for_display(period)
                        baseline_date = datetime.strptime(baseline_date_str, '%Y-%m-%d').strftime('%m/%d/%y')
                        break
            
            if baseline_date:
                st.caption(f"Baseline Date: {baseline_date}")
        
        display_heatmap(current_data, title, controls['group'])
        
        # Display data table
        with st.expander("📋 Detailed Data Table", expanded=False):
            display_data_table(current_data)
        
        # Show last update time based on analysis mode
        if controls['analysis_mode'] == 'price' and st.session_state.last_update:
            st.caption(f"Last updated: {st.session_state.last_update.strftime('%Y-%m-%d %H:%M:%S')}")
        elif controls['analysis_mode'] == 'volume' and st.session_state.volume_last_update:
            st.caption(f"Last updated: {st.session_state.volume_last_update.strftime('%Y-%m-%d %H:%M:%S')}")
    
    else:
        st.info("👆 Select your preferences in the sidebar and click 'Refresh Data' to get started!")

    # Footer
    st.markdown("---")
    st.markdown(
        "Built with ❤️ using Streamlit and Plotly | "
        "Data provided by Yahoo Finance via yfinance"
    )

def main():
    """Main application function with page navigation"""
    # Page config
    st.set_page_config(
        page_title="Stock Performance Dashboard",
        page_icon="📈",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    # Initialize session state
    initialize_session_state()
    
    # Background update: Pre-load technical indicators for CUSTOM_DEFAULT tickers
    if 'technical_background_updated' not in st.session_state:
        with st.spinner(f'Refreshing technical indicators for {len(CUSTOM_DEFAULT)} tickers...'):
            for ticker in CUSTOM_DEFAULT:
                try:
                    # Calculate latest indicators
                    st.session_state.tech_calculator.calculate_comprehensive_analysis(
                        ticker=ticker,
                        save_to_db=True
                    )
                    # Backfill 22-day history for rolling heatmap
                    st.session_state.tech_calculator.backfill_technical_indicators(
                        ticker=ticker,
                        days=22
                    )
                    # Calculate 52-week price extremes
                    st.session_state.tech_calculator.calculate_52_week_analysis(ticker)
                except Exception as e:
                    # Silent failure - don't break app load for individual ticker failures
                    pass
        st.session_state.technical_background_updated = True
    
    # Page navigation in sidebar
    st.sidebar.title("📊 Navigation")
    st.session_state.selected_page = st.sidebar.selectbox(
        "Choose Dashboard:",
        options=['performance_heatmaps', 'technical_analysis', 'stock_comparison'],
        format_func=lambda x: {
            'performance_heatmaps': '📈 Performance Heatmaps',
            'technical_analysis': '🎯 Technical Analysis',  
            'stock_comparison': '📋 Stock Comparison'
        }[x],
        index=['performance_heatmaps', 'technical_analysis', 'stock_comparison'].index(
            st.session_state.selected_page
        ),
        key='page_navigation'
    )
    
    # Route to appropriate dashboard
    if st.session_state.selected_page == 'performance_heatmaps':
        show_performance_heatmaps()
    elif st.session_state.selected_page == 'technical_analysis':
        show_technical_analysis_dashboard()
    elif st.session_state.selected_page == 'stock_comparison':
        # Placeholder for Dashboard 2
        st.title("📋 Stock Comparison Dashboard")
        st.info("Dashboard 2: Multi-stock technical comparison coming soon...")
        st.markdown("""
        This dashboard will allow you to:
        - Compare technical indicators across multiple stocks
        - Use the existing bucket system (Country/Sector/Custom)
        - Display technical heatmaps for comparative analysis
        """)

if __name__ == "__main__":
    main()
