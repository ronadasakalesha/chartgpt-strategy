import yfinance as yf

def fetch_data(symbol="RELIANCE.NS", interval="15m", period="60d"):
    df = yf.download(
        tickers=symbol,
        interval=interval,
        period=period,
        progress=False
    )

    # flatten columns if needed
    if hasattr(df.columns, "levels"):
        df.columns = df.columns.get_level_values(0)

    df.dropna(inplace=True)
    df.reset_index(inplace=True)

    return df