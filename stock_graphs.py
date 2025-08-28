import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.widgets as widgets
from matplotlib.patches import Rectangle
import numpy as np
from datetime import datetime, timedelta
import matplotlib.dates as mdates

class StockVisualizer:
    def __init__(self, ticker):
        self.ticker = ticker.upper()
        self.stock = yf.Ticker(self.ticker)
        self.current_period = '1Y'
        self.data = None
        
        # Set up the figure with dark theme
        plt.style.use('dark_background')
        self.fig = plt.figure(figsize=(12, 8), facecolor='#0d0d0d')
        self.fig.patch.set_facecolor('#0d0d0d')
        
        # Create main plot area
        self.ax = plt.subplot2grid((10, 1), (2, 0), rowspan=7, colspan=1)
        self.ax.set_facecolor('#0d0d0d')
        
        # Info display area - back to top
        self.info_ax = plt.subplot2grid((10, 1), (0, 0), rowspan=2, colspan=1)
        self.info_ax.axis('off')
        
        # Button area - moved below graph
        self.button_ax = plt.subplot2grid((10, 1), (9, 0), rowspan=1, colspan=1)
        self.button_ax.axis('off')
        
        # Custom input area - positioned in bottom right corner
        self.custom_ax = plt.axes([0.85, 0.02, 0.12, 0.04])
        self.custom_text = widgets.TextBox(self.custom_ax, 'Custom:', initial='')
        self.custom_text.on_submit(self.on_custom_submit)
        
        # Colors
        self.green = '#4CAF50'
        self.red = '#f44336'
        self.text_color = '#ffffff'
        self.grid_color = '#2a2a2a'
        self.button_color = '#1a1a1a'
        self.button_active = '#3a3a3a'
        
        # Initialize
        self.create_buttons()
        self.update_plot('1Y')
        
    def fetch_data(self, period):
        """Fetch historical data based on selected period"""
        end_date = datetime.now()
        
        period_map = {
            '1D': (end_date - timedelta(days=1), '5m'),
            '5D': (end_date - timedelta(days=5), '30m'),
            '1M': (end_date - timedelta(days=30), '1h'),
            '6M': (end_date - timedelta(days=180), '1d'),
            'YTD': (datetime(end_date.year, 1, 1), '1d'),
            '1Y': (end_date - timedelta(days=365), '1d'),
            '5Y': (end_date - timedelta(days=365*5), '1d'),
            'Max': (None, '1d')
        }
        
        # Handle custom periods
        if period not in period_map:
            # Parse custom period (e.g., "21Y", "3M", "45D")
            try:
                import re
                match = re.match(r'(\d+)([YMD])', period.upper())
                if match:
                    num = int(match.group(1))
                    unit = match.group(2)
                    
                    if unit == 'Y':
                        start_date = end_date - timedelta(days=365*num)
                    elif unit == 'M':
                        start_date = end_date - timedelta(days=30*num)
                    elif unit == 'D':
                        start_date = end_date - timedelta(days=num)
                    
                    # Determine appropriate interval
                    days_diff = (end_date - start_date).days
                    if days_diff <= 7:
                        interval = '5m'
                    elif days_diff <= 60:
                        interval = '1h'
                    else:
                        interval = '1d'
                    
                    self.data = self.stock.history(start=start_date, end=end_date, interval=interval)
                else:
                    # Default to 1 year if parsing fails
                    self.data = self.stock.history(period='1y')
            except:
                self.data = self.stock.history(period='1y')
        elif period == 'Max':
            self.data = self.stock.history(period='max')
        else:
            start_date, interval = period_map[period]
            if period in ['1D', '5D', '1M']:
                self.data = self.stock.history(start=start_date, end=end_date, interval=interval)
            else:
                self.data = self.stock.history(start=start_date, end=end_date)
        
        return self.data
    
    def create_buttons(self):
        """Create time period selector buttons"""
        periods = ['YTD', '1D', '5D', '1M', '6M', '1Y', '5Y', 'Max']
        button_width = 0.08
        spacing = 0.02
        total_width = len(periods) * button_width + (len(periods) - 1) * spacing
        start_x = 0.8 - total_width - 0.02  # 0.02 gap before custom box
        
        self.buttons = {}
        self.button_backgrounds = {}
        
        for i, period in enumerate(periods):
            x_pos = start_x + i * (button_width + spacing)
            
            # Create button background
            bg = Rectangle((x_pos - 0.005, 0.2), button_width + 0.01, 0.6,
                          transform=self.button_ax.transAxes,
                          facecolor=self.button_color,
                          edgecolor='none',
                          zorder=1)
            self.button_ax.add_patch(bg)
            self.button_backgrounds[period] = bg
            
            # Create button text
            button = self.button_ax.text(x_pos + button_width/2, 0.5, period,
                                       transform=self.button_ax.transAxes,
                                       ha='center', va='center',
                                       color=self.text_color,
                                       fontsize=10,
                                       weight='normal',
                                       zorder=2)
            self.buttons[period] = button
            
        # Highlight default period
        self.button_backgrounds['1Y'].set_facecolor(self.button_active)
        self.buttons['1Y'].set_weight('bold')
        
        # Set up click event
        self.fig.canvas.mpl_connect('button_press_event', self.on_click)
    
    def on_custom_submit(self, text):
        """Handle custom time period input"""
        if text.strip():
            # Parse the input - support formats like "21Y", "3M", "45D", "21 years", etc.
            import re
            text = text.strip().upper()
            
            # Try to match patterns
            patterns = [
                (r'(\d+)\s*Y(?:EARS?)?', 'Y'),
                (r'(\d+)\s*M(?:ONTHS?)?', 'M'),
                (r'(\d+)\s*D(?:AYS?)?', 'D'),
            ]
            
            for pattern, unit in patterns:
                match = re.search(pattern, text)
                if match:
                    num = match.group(1)
                    formatted_period = f"{num}{unit}"
                    self.update_plot(formatted_period)
                    break
    
    def on_click(self, event):
        """Handle button clicks"""
        if event.inaxes == self.button_ax:
            # Get click position
            for period, button in self.buttons.items():
                bbox = button.get_window_extent()
                if bbox.contains(event.x, event.y):
                    self.update_plot(period)
                    break
    
    def update_plot(self, period):
        """Update the plot with new time period"""
        self.current_period = period
        
        # Update button highlighting - only for standard periods
        standard_periods = ['YTD', '1D', '5D', '1M', '6M', '1Y', '5Y', 'Max']
        for p, bg in self.button_backgrounds.items():
            if p == period and period in standard_periods:
                bg.set_facecolor(self.button_active)
                self.buttons[p].set_weight('bold')
            else:
                bg.set_facecolor(self.button_color)
                self.buttons[p].set_weight('normal')
        
        # Fetch new data
        self.fetch_data(period)
        
        if self.data.empty:
            return
        
        # Clear and redraw
        self.ax.clear()
        self.info_ax.clear()
        self.info_ax.axis('off')
        
        # Plot the data
        dates = self.data.index
        prices = self.data['Close']
        
        # Determine if stock is up or down
        change = prices.iloc[-1] - prices.iloc[0]
        change_pct = (change / prices.iloc[0]) * 100
        line_color = self.green if change >= 0 else self.red
        
        # Plot the line
        self.ax.plot(dates, prices, color=line_color, linewidth=2.5, alpha=1.0)
        
        # Fill under the line
        self.ax.fill_between(dates, prices, alpha=0.2, color=line_color)
        
        # Style the plot
        self.ax.set_facecolor('#0d0d0d')  # Very dark background like the image
        self.ax.grid(True, color='#404040', alpha=0.5, linewidth=1.0)  # Thicker grid lines
        self.ax.spines['top'].set_visible(False)
        self.ax.spines['right'].set_visible(False)
        self.ax.spines['left'].set_color(self.grid_color)
        self.ax.spines['bottom'].set_color(self.grid_color)
        
        # Format x-axis based on period
        if period in ['1D', '5D']:
            self.ax.xaxis.set_major_formatter(mdates.DateFormatter('%H:%M'))
        elif period in ['1M', '6M', 'YTD', '1Y']:
            self.ax.xaxis.set_major_formatter(mdates.DateFormatter('%b %Y'))
        else:
            self.ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y'))
        
        # Rotate x labels
        plt.setp(self.ax.xaxis.get_majorticklabels(), rotation=0, ha='center')
        
        # Set y-axis limits with some padding
        y_min = prices.min() * 0.98
        y_max = prices.max() * 1.02
        self.ax.set_ylim(y_min, y_max)
        
        # Format y-axis (move to left)
        self.ax.yaxis.set_label_position('left')
        self.ax.yaxis.tick_left()
        
        # Update info display
        current_price = prices.iloc[-1]
        
        # Title
        self.info_ax.text(0.05, 0.8, f'{self.ticker}', 
                         transform=self.info_ax.transAxes,
                         color='#888888', fontsize=12)
        
        # Current price
        self.info_ax.text(0.05, 0.3, f'{current_price:.2f}',
                         transform=self.info_ax.transAxes,
                         color=self.text_color, fontsize=36, weight='bold')
        
        # Change info - format period display nicely
        period_display = period
        if period not in standard_periods:
            # Parse custom periods for display
            import re
            match = re.match(r'(\d+)([YMD])', period)
            if match:
                num = match.group(1)
                unit = match.group(2)
                unit_map = {'Y': 'year', 'M': 'month', 'D': 'day'}
                unit_name = unit_map.get(unit, '')
                if int(num) > 1:
                    unit_name += 's'
                period_display = f"{num} {unit_name}"
        
        change_sign = '+' if change >= 0 else ''
        self.info_ax.text(0.05, 0.0, f'{change_sign}{change:.2f} ({change_sign}{change_pct:.2f}%) past {period_display}',
                         transform=self.info_ax.transAxes,
                         color=line_color, fontsize=14)
        
        # Timestamp
        timestamp = datetime.now().strftime('%b %d, %I:%M %p %Z')
        self.info_ax.text(0.5, 0.0, timestamp,
                         transform=self.info_ax.transAxes,
                         color='#888888', fontsize=10)
        
        plt.tight_layout()
        self.fig.canvas.draw()
    
    def show(self):
        """Display the visualization"""
        plt.show()

# Example usage
if __name__ == "__main__":
    # Get ticker from user
    ticker = input("Enter stock ticker symbol (e.g., AAPL, GOOGL, SPY): ").strip()
    
    try:
        # Create and show visualization
        visualizer = StockVisualizer(ticker)
        
        print("\nInstructions:")
        print("- Click on time period buttons (1D, 5D, 1M, etc.)")
        print("- Use the 'Custom:' text box at bottom right for custom periods")
        print("  Examples: '21Y', '3M', '45D', '21 years', '6 months', '30 days'")
        print("- Close the window to exit\n")
        
        visualizer.show()
    except Exception as e:
        print(f"Error: {e}")
        print("Please make sure you have a valid ticker symbol and internet connection.")