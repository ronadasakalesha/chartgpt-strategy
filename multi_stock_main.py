from data.data_loader import fetch_data
from strategy.advanced_strategy import apply_strategy
from backtest.backtester import analyze_trades

stocks = [
    "RELIANCE.NS",
    "TCS.NS",
    "INFY.NS",
    "HDFCBANK.NS",
    "ICICIBANK.NS"
]

all_trades = []

for stock in stocks:
    print(f"\nProcessing {stock}...")

    df = fetch_data(stock)
    trades = apply_strategy(df)

    for t in trades:
        t["symbol"] = stock

    all_trades.extend(trades)

# Final analysis
analyze_trades(all_trades)