# Stock-Graphs

Interactive GUI application for stock price analysis with line charts and real-time data.

## Quick Start

```bash
pip install -r requirements.txt
python stock_graphs.py
```

## Features

- 🖥️ **Interactive GUI** - Clean, modern dark theme interface
- 📊 **Line Charts** - Professional stock price visualization
- 📈 **Price Analysis** - Current price, changes, percentage gains/losses
- ⏰ **Flexible Periods** - Predefined buttons + custom input
- 🎨 **Dark Theme** - Easy on the eyes, professional appearance
- 🔄 **Real-time Data** - Live stock data from Yahoo Finance

## Usage

1. **Run the app**: `python stock_graphs.py`
2. **Enter ticker**: Type stock symbol (e.g., AAPL, TSLA, SPY)
3. **Select period**: Click time period buttons or enter custom periods
4. **View chart**: Interactive line chart with price data
5. **Custom periods**: Use text box for specific timeframes

## Time Periods

**Button Options**: `YTD`, `1D`, `5D`, `1M`, `6M`, `1Y`, `5Y`, `Max`

**Custom Input**: Any `[number][unit]` format:
- `Y` = years (e.g., `21Y`, `3Y`)
- `M` = months (e.g., `3M`, `6M`) 
- `D` = days (e.g., `45D`, `30D`)

**Examples**: `21Y`, `3M`, `45D`, `21 years`, `6 months`, `30 days`

## Dependencies

- yfinance
- pandas  
- matplotlib
- numpy