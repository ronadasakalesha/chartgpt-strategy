import pandas as pd

def analyze_trades(trades):
    pnls = []

    for t in trades:
        if t["type"] == "BUY":
            pnl = t["exit"] - t["entry"]
        else:
            pnl = t["entry"] - t["exit"]
        pnls.append(pnl)

    df = pd.DataFrame(pnls, columns=["PnL"])

    total = len(df)
    wins = len(df[df["PnL"] > 0])
    win_rate = (wins / total * 100) if total else 0

    print("Total Trades:", total)
    print("Win Rate:", round(win_rate, 2), "%")
    print("Total PnL:", df["PnL"].sum())

    return df
