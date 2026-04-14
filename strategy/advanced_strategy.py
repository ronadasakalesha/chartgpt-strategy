import pandas as pd

def add_indicators(df):
    df["EMA21"] = df["Close"].ewm(span=21).mean()
    df["EMA50"] = df["Close"].ewm(span=50).mean()

    df["Recent_High"] = df["High"].rolling(20).max().shift(1)
    df["Recent_Low"] = df["Low"].rolling(20).min().shift(1)

    return df

def apply_strategy(df):
    trades = []
    df = add_indicators(df)

    position = None
    waiting_for_confirmation = None

    for i in range(50, len(df)):
        row = df.iloc[i]

        if pd.isna(row["Recent_High"]) or pd.isna(row["Recent_Low"]):
            continue

        trend_strength = abs(float(row["EMA21"]) - float(row["EMA50"]))
        if trend_strength < 0.3:
            continue

        # Trap detection
        if waiting_for_confirmation is None and position is None:

            if (
                float(row["Low"]) < float(row["Recent_Low"]) and
                float(row["Close"]) > float(row["Recent_Low"]) and
                float(row["EMA21"]) > float(row["EMA50"])
            ):
                waiting_for_confirmation = "BUY"

            elif (
                float(row["High"]) > float(row["Recent_High"]) and
                float(row["Close"]) < float(row["Recent_High"]) and
                float(row["EMA21"]) < float(row["EMA50"])
            ):
                waiting_for_confirmation = "SELL"

        # Confirmation
        elif waiting_for_confirmation is not None and position is None:

            if waiting_for_confirmation == "BUY" and float(row["Close"]) > float(row["Open"]):

                # 🔥 STRUCTURE SL
                sl = min(df.iloc[i-5:i]["Low"])
                entry = float(row["Close"])
                risk = entry - sl
                tp = entry + (risk * 2)

                position = {
                    "type": "BUY",
                    "entry": entry,
                    "sl": sl,
                    "tp": tp,
                    "time": row["Datetime"]
                }
                waiting_for_confirmation = None

            elif waiting_for_confirmation == "SELL" and float(row["Close"]) < float(row["Open"]):

                sl = max(df.iloc[i-5:i]["High"])
                entry = float(row["Close"])
                risk = sl - entry
                tp = entry - (risk * 2)

                position = {
                    "type": "SELL",
                    "entry": entry,
                    "sl": sl,
                    "tp": tp,
                    "time": row["Datetime"]
                }
                waiting_for_confirmation = None

        # EXIT
        elif position is not None:

            if position["type"] == "BUY":
                if float(row["Close"]) <= position["sl"] or float(row["Close"]) >= position["tp"]:
                    trades.append({
                        **position,
                        "exit": float(row["Close"]),
                        "exit_time": row["Datetime"]
                    })
                    position = None

            elif position["type"] == "SELL":
                if float(row["Close"]) >= position["sl"] or float(row["Close"]) <= position["tp"]:
                    trades.append({
                        **position,
                        "exit": float(row["Close"]),
                        "exit_time": row["Datetime"]
                    })
                    position = None

    return trades