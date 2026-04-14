from data.data_loader import fetch_data
from strategy.advanced_strategy import apply_strategy
from backtest.backtester import analyze_trades

if __name__ == "__main__":
    df = fetch_data("RELIANCE.NS")
    print(df.columns)
    trades = apply_strategy(df)
    analyze_trades(trades)
