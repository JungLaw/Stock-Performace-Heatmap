"""
Heatmap Visualization - Finviz-Style Treemap Implementation

This module creates interactive treemap visualizations using Plotly, 
styled to match Finviz professional standards with enhanced UX.
"""

import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import numpy as np
from typing import Dict, List, Optional, Tuple
import math


class FinvizHeatmapGenerator:
    """Generate Finviz-style heatmaps using Plotly treemaps"""
    
    # Finviz Professional Color Scheme
    FINVIZ_COLORS = {
        'strong_positive': '#00AA00',    # >3% gain
        'moderate_positive': '#33CC33',  # 1-3% gain  
        'slight_positive': '#66FF66',    # 0-1% gain
        'neutral': '#CCCCCC',            # ±0%
        'slight_negative': '#FF6666',    # 0 to -1% loss
        'moderate_negative': '#CC3333',  # -1 to -3% loss
        'strong_negative': '#AA0000'     # <-3% loss
    }
    
    # Performance thresholds for color mapping
    COLOR_THRESHOLDS = [
        (-float('inf'), -3.0, 'strong_negative'),
        (-3.0, -1.0, 'moderate_negative'),
        (-1.0, 0.0, 'slight_negative'),
        (0.0, 0.0, 'neutral'),
        (0.0, 1.0, 'slight_positive'),
        (1.0, 3.0, 'moderate_positive'),
        (3.0, float('inf'), 'strong_positive')
    ]
    
    def __init__(self):
        self.default_size = 100  # Default tile size when equal sizing
        
    def get_performance_color(self, percentage_change: float) -> str:
        """
        Map percentage change to Finviz color scheme
        
        Args:
            percentage_change: Performance percentage (-100 to +100)
            
        Returns:
            Hex color code
        """
        for min_val, max_val, color_key in self.COLOR_THRESHOLDS:
            if min_val <= percentage_change < max_val:
                return self.FINVIZ_COLORS[color_key]
        
        # Default to neutral for edge cases
        return self.FINVIZ_COLORS['neutral']
    
    def prepare_treemap_data(self, performance_data: List[Dict], 
                           sizing_method: str = 'equal',
                           asset_group: str = None) -> pd.DataFrame:
        """
        Prepare data for treemap visualization
        
        Args:
            performance_data: List of performance dictionaries from PerformanceCalculator
            sizing_method: 'equal' for uniform sizes, 'market_cap' for proportional (future)
            asset_group: Asset group name to determine display names ('country', 'sector', 'custom')
            
        Returns:
            DataFrame ready for Plotly treemap
        """
        # Import here to avoid circular imports
        from config.assets import get_display_name_for_ticker, should_use_display_names
        
        # Filter out error cases
        valid_data = [p for p in performance_data if not p.get('error', False)]
        
        if not valid_data:
            # Return empty DataFrame with expected structure
            return pd.DataFrame(columns=[
                'ticker', 'display_name', 'percentage_change', 'current_price', 'historical_price',
                'absolute_change', 'color', 'size', 'label', 'hover_text'
            ])
        
        df_data = []
        use_display_names = should_use_display_names(asset_group) if asset_group else False
        
        for item in valid_data:
            ticker = item['ticker']
            
            # Handle both price and volume data structures
            if 'percentage_change' in item:
                # Price performance data
                pct_change = item['percentage_change']
                current_value = item['current_price']
                historical_value = item['historical_price']
                absolute_change = item['absolute_change']
                period_label = item.get('period_label', 'N/A')
            elif 'volume_change' in item:
                # Volume performance data
                pct_change = item['volume_change']
                current_value = item['current_volume']
                historical_value = item['benchmark_average']
                absolute_change = current_value - historical_value if current_value and historical_value else 0
                period_label = item.get('benchmark_label', item.get('benchmark_period', 'N/A'))
            else:
                # Skip unknown data structure
                continue
            
            # Get display name based on asset group
            if use_display_names:
                display_name = get_display_name_for_ticker(ticker, asset_group)
            else:
                display_name = ticker
            
            # Color mapping
            color = self.get_performance_color(pct_change)
            
            # Size calculation (equal for now, market cap sizing later)
            size = self.default_size
            
            # Create display label (display name + percentage)
            if pct_change >= 0:
                label = f"{display_name}<br>+{pct_change:.2f}%"
            else:
                label = f"{display_name}<br>{pct_change:.2f}%"
            
            # Rich hover text (always show ticker in hover)
            hover_text = self._create_hover_text(item, display_name)
            
            df_data.append({
                'ticker': ticker,
                'display_name': display_name,
                'percentage_change': pct_change,
                'current_price': current_value,
                'historical_price': historical_value,
                'absolute_change': absolute_change,
                'color': color,
                'size': size,
                'label': label,
                'hover_text': hover_text,
                'period_label': period_label
            })
        
        return pd.DataFrame(df_data)
    
    def _create_hover_text(self, performance_item: Dict, display_name: str = None) -> str:
        """Create rich hover tooltip text for both price and volume data"""
        ticker = performance_item['ticker']
        
        # Handle both price and volume data structures
        if 'percentage_change' in performance_item:
            # Price performance data
            pct_change = performance_item['percentage_change']
            current_price = performance_item['current_price']
            historical_price = performance_item['historical_price']
            absolute_change = performance_item['absolute_change']
            period_label = performance_item.get('period_label', 'N/A')
            
            # Use display name if provided, otherwise use ticker
            title = display_name if display_name else ticker
            
            # Format prices and changes
            price_format = f"${current_price:.2f}" if current_price else "N/A"
            hist_price_format = f"${historical_price:.2f}" if historical_price else "N/A"
            abs_change_format = f"${absolute_change:+.2f}" if absolute_change else "N/A"
            pct_format = f"{pct_change:+.2f}%" if pct_change is not None else "N/A"
            
            # Create price hover text
            if display_name and display_name != ticker:
                hover_text = f"""<b>{title}</b><br>
<i>Ticker: {ticker}</i><br>
Current: {price_format}<br>
{period_label}: {hist_price_format}<br>
Change: {abs_change_format} ({pct_format})<br>
<extra></extra>"""
            else:
                hover_text = f"""<b>{title}</b><br>
Current: {price_format}<br>
{period_label}: {hist_price_format}<br>
Change: {abs_change_format} ({pct_format})<br>
<extra></extra>"""
                
        elif 'volume_change' in performance_item:
            # Volume performance data
            pct_change = performance_item['volume_change']
            current_volume = performance_item['current_volume']
            benchmark_average = performance_item['benchmark_average']
            benchmark_label = performance_item.get('benchmark_label', performance_item.get('benchmark_period', 'N/A'))
            
            # Use display name if provided, otherwise use ticker
            title = display_name if display_name else ticker
            
            # Format volume and changes
            volume_format = f"{current_volume:,}" if current_volume else "N/A"
            benchmark_format = f"{benchmark_average:,.0f}" if benchmark_average else "N/A"
            pct_format = f"{pct_change:+.2f}%" if pct_change is not None else "N/A"
            
            # Create volume hover text
            if display_name and display_name != ticker:
                hover_text = f"""<b>{title}</b><br>
<i>Ticker: {ticker}</i><br>
Current Volume: {volume_format}<br>
{benchmark_label} Avg: {benchmark_format}<br>
Volume Change: {pct_format}<br>
<extra></extra>"""
            else:
                hover_text = f"""<b>{title}</b><br>
Current Volume: {volume_format}<br>
{benchmark_label} Avg: {benchmark_format}<br>
Volume Change: {pct_format}<br>
<extra></extra>"""
        else:
            # Fallback for unknown data structure
            title = display_name if display_name else ticker
            hover_text = f"""<b>{title}</b><br>
Data unavailable<br>
<extra></extra>"""
        
        return hover_text
    
    def create_treemap(self, performance_data: List[Dict], 
                      title: str = "Stock Performance Heatmap",
                      sizing_method: str = 'equal',
                      width: int = 1200,
                      height: int = 800,
                      asset_group: str = None) -> go.Figure:
        """
        Create Finviz-style treemap visualization
        
        Args:
            performance_data: List of performance dictionaries
            title: Chart title
            sizing_method: Tile sizing method ('equal' or 'market_cap')
            width: Chart width in pixels
            height: Chart height in pixels
            asset_group: Asset group name for display name handling
            
        Returns:
            Plotly Figure object
        """
        # Prepare data
        df = self.prepare_treemap_data(performance_data, sizing_method, asset_group)
        
        if df.empty:
            # Create empty chart with message
            fig = go.Figure()
            fig.add_annotation(
                text="No data available",
                xref="paper", yref="paper",
                x=0.5, y=0.5,
                showarrow=False,
                font=dict(size=20, color="gray")
            )
            fig.update_layout(
                title=title,
                width=width,
                height=height
            )
            return fig
        
        # Create treemap
        fig = go.Figure(go.Treemap(
            labels=df['ticker'],
            values=df['size'],
            parents=[""] * len(df),  # All items at root level
            
            # Text and labeling
            text=df['label'],
            textinfo="text",
            textfont=dict(
                family="Arial, sans-serif",
                size=18,
                color="white"
            ),
            textposition="middle center",
            
            # Colors
            marker=dict(
                colors=df['color'],
                line=dict(
                    color="#E0E0E0",  # Border color
                    width=2
                )
            ),
            
            # Hover information
            hovertext=df['hover_text'],
            hoverinfo="text",
            hoverlabel=dict(
                bgcolor="rgba(0,0,0,0.8)",
                bordercolor="white",
                font=dict(color="white", size=14)
            ),
            
            # Layout and sizing
            pathbar=dict(visible=False),  # Hide pathbar for cleaner look
            maxdepth=1,  # Single level treemap
        ))
        
        # Update layout for Finviz-style appearance
        fig.update_layout(
            title=dict(
                text=title,
                font=dict(
                    family="Arial, sans-serif",
                    size=24,
                    color="#333333"
                ),
                x=0.5,  # Center the title
                pad=dict(t=20, b=20)
            ),
            
            # Remove margins for full-width display
            margin=dict(t=80, l=10, r=10, b=10),
            
            # Set dimensions
            width=width,
            height=height,
            
            # Background styling
            plot_bgcolor="#FFFFFF",
            paper_bgcolor="#F8F9FA",
            
            # Font defaults
            font=dict(
                family="Arial, sans-serif",
                color="#333333"
            )
        )
        
        return fig
    
    def create_summary_stats(self, performance_data: List[Dict]) -> Dict:
        """
        Create summary statistics for display - handles both price and volume data
        
        Args:
            performance_data: List of performance dictionaries (price or volume)
            
        Returns:
            Dictionary with summary statistics
        """
        valid_data = [p for p in performance_data if not p.get('error', False)]
        
        if not valid_data:
            return {
                'total_tickers': len(performance_data),
                'valid_data': 0,
                'avg_performance': 0.0,
                'positive_count': 0,
                'negative_count': 0,
                'neutral_count': 0,
                'best_performer': None,
                'worst_performer': None
            }
        
        # Detect data type and extract performance values
        if 'percentage_change' in valid_data[0]:
            # Price performance data
            percentages = [p['percentage_change'] for p in valid_data]
            best_performer = max(valid_data, key=lambda x: x['percentage_change'])
            worst_performer = min(valid_data, key=lambda x: x['percentage_change'])
        elif 'volume_change' in valid_data[0]:
            # Volume performance data
            percentages = [p['volume_change'] for p in valid_data]
            best_performer = max(valid_data, key=lambda x: x['volume_change'])
            worst_performer = min(valid_data, key=lambda x: x['volume_change'])
        else:
            # Fallback - unknown data structure
            return {
                'total_tickers': len(performance_data),
                'valid_data': 0,
                'avg_performance': 0.0,
                'positive_count': 0,
                'negative_count': 0,
                'neutral_count': 0,
                'best_performer': None,
                'worst_performer': None
            }
        
        positive_count = len([p for p in percentages if p > 0])
        negative_count = len([p for p in percentages if p < 0])
        neutral_count = len([p for p in percentages if p == 0])
        
        return {
            'total_tickers': len(performance_data),
            'valid_data': len(valid_data),
            'avg_performance': np.mean(percentages),
            'median_performance': np.median(percentages),
            'positive_count': positive_count,
            'negative_count': negative_count,
            'neutral_count': neutral_count,
            'best_performer': best_performer,
            'worst_performer': worst_performer
        }


# Convenience functions
def create_heatmap(performance_data: List[Dict], 
                  title: str = "Stock Performance Heatmap",
                  width: int = 1200, 
                  height: int = 800,
                  asset_group: str = None) -> go.Figure:
    """
    Quick function to create a heatmap visualization
    
    Args:
        performance_data: List of performance dictionaries
        title: Chart title
        width: Chart width
        height: Chart height
        asset_group: Asset group for display name handling
        
    Returns:
        Plotly Figure object
    """
    generator = FinvizHeatmapGenerator()
    return generator.create_treemap(performance_data, title, width=width, height=height, asset_group=asset_group)


def get_color_legend() -> Dict[str, str]:
    """
    Get the color legend for the heatmap
    
    Returns:
        Dictionary mapping color descriptions to hex codes
    """
    return {
        "Strong Gain (>3%)": FinvizHeatmapGenerator.FINVIZ_COLORS['strong_positive'],
        "Moderate Gain (1-3%)": FinvizHeatmapGenerator.FINVIZ_COLORS['moderate_positive'],
        "Slight Gain (0-1%)": FinvizHeatmapGenerator.FINVIZ_COLORS['slight_positive'],
        "Neutral (0%)": FinvizHeatmapGenerator.FINVIZ_COLORS['neutral'],
        "Slight Loss (0 to -1%)": FinvizHeatmapGenerator.FINVIZ_COLORS['slight_negative'],
        "Moderate Loss (-1 to -3%)": FinvizHeatmapGenerator.FINVIZ_COLORS['moderate_negative'],
        "Strong Loss (<-3%)": FinvizHeatmapGenerator.FINVIZ_COLORS['strong_negative']
    }


def create_color_legend_chart() -> go.Figure:
    """
    Create a small chart showing the color legend
    
    Returns:
        Plotly Figure object for color legend
    """
    legend_data = get_color_legend()
    
    # Create a simple bar chart as legend
    fig = go.Figure()
    
    x_pos = list(range(len(legend_data)))
    colors = list(legend_data.values())
    labels = list(legend_data.keys())
    
    fig.add_trace(go.Bar(
        x=x_pos,
        y=[1] * len(legend_data),
        marker_color=colors,
        text=labels,
        textposition='outside',
        textangle=45,
        showlegend=False,
        hoverinfo='skip'
    ))
    
    fig.update_layout(
        title="Color Legend",
        xaxis=dict(showticklabels=False, showgrid=False),
        yaxis=dict(showticklabels=False, showgrid=False),
        height=200,
        margin=dict(t=50, l=10, r=10, b=80),
        plot_bgcolor="white",
        paper_bgcolor="white"
    )
    
    return fig
