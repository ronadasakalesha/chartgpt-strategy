import pandas as pd
import matplotlib.pyplot as plt

def analyze_trades(trades):

    initial_capital = 100000
    capital = initial_capital

    risk_per_trade_pct = 0.5   # 🔥 Controlled risk (0.5%)

    results = []
    equity_curve = []

    loss_streak = 0
    max_loss_streak = 3   # 🔥 Stop after 3 consecutive losses

    for t in trades:

        # 🔥 Skip trading if loss streak exceeded
        if loss_streak >= max_loss_streak:
            loss_streak = 0   # reset after skipping one cycle
            continue

        entry = t["entry"]
        exit_price = t["exit"]
        sl = t["sl"]

        # Risk amount
        risk_amount = capital * (risk_per_trade_pct / 100)

        risk_per_unit = abs(entry - sl)

        if risk_per_unit == 0:
            continue

        position_size = risk_amount / risk_per_unit

        # PnL calculation
        if t["type"] == "BUY":
            pnl = (exit_price - entry) * position_size
        else:
            pnl = (entry - exit_price) * position_size

        capital += pnl

        results.append(pnl)
        equity_curve.append(capital)

        # 🔥 Loss streak logic
        if pnl < 0:
            loss_streak += 1
        else:
            loss_streak = 0

    df = pd.DataFrame({
        "PnL": results,
        "Equity": equity_curve
    })

    total = len(df)
    wins = len(df[df["PnL"] > 0])
    losses = len(df[df["PnL"] <= 0])

    win_rate = (wins / total) * 100 if total > 0 else 0

    # Drawdown
    df["Peak"] = df["Equity"].cummax()
    df["Drawdown"] = df["Equity"] - df["Peak"]
    max_drawdown = df["Drawdown"].min()

    print("\n===== BACKTEST RESULT =====")
    print("Initial Capital:", initial_capital)
    print("Final Capital:", round(capital, 2))
    print("Total Trades:", total)
    print("Wins:", wins)
    print("Losses:", losses)
    print("Win Rate:", round(win_rate, 2), "%")
    print("Total Profit:", round(capital - initial_capital, 2))
    print("Max Drawdown:", round(max_drawdown, 2))

    # 📈 Equity Curve
    plt.figure()
    plt.plot(df["Equity"])
    plt.title("Equity Curve")
    plt.xlabel("Trades")
    plt.ylabel("Capital")
    plt.grid()
    plt.show()

    return df