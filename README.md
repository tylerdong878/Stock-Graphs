# Stock-Graphs

Interactive GUI application for stock price analysis with candlestick charts.

## Quick Start

```bash
pip install -r requirements.txt
python stock_graphs.py
```

## Features

- 🖥️ **Interactive GUI** - Clean, modern interface
- 📊 **Candlestick Charts** - Professional stock visualization
- 📈 **Price Analysis** - Start/end prices, changes, highs/lows
- ⏰ **Flexible Periods** - Dropdown + custom input
- 💾 **HTML Export** - Save and share charts
- 🎨 **Dark Theme** - Easy on the eyes

## Usage

1. **Run the app**: `python stock_graphs.py`
2. **Enter ticker**: Type stock symbol (e.g., AAPL, TSLA)
3. **Select period**: Choose from dropdown or enter custom
4. **Click Analyze**: View interactive chart and results
5. **Save HTML**: Export chart for sharing

## Periods

**Dropdown Options**: `1d`, `5d`, `1mo`, `3mo`, `6mo`, `1y`, `2y`, `5y`, `10y`, `20y`, `max`

**Custom Input**: Any `[number][unit]` format:
- `d` = days (e.g., `50d`)
- `mo` = months (e.g., `3mo`) 
- `y` = years (e.g., `2y`)

## Dependencies

- yfinance
- pandas  
- plotly
- numpy
- tkinter (built-in)