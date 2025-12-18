import pandas as pd
import talib


def add_label(df_input: pd.DataFrame, open_col: str, close_col: str, label_col: str) -> pd.DataFrame:
    df = df_input.copy()
    # True if next candle's close is higher than current's
    # df[label_col] = (df[close_col].shift(-1) > df[close_col]).astype("Int64")
    df[label_col] = (df[close_col] > df[open_col]).shift(-1).astype("Int64")
    return df


def add_technical_indicators(
    df_input: pd.DataFrame,
    open_col: str,
    high_col: str,
    low_col: str,
    close_col: str,
    volume_col: str,
) -> pd.DataFrame:
    df = df_input.copy()

    df["rsi_14"] = talib.RSI(df[close_col], timeperiod=14)

    df["stoch_k"], df["stoch_d"] = talib.STOCH(
        df[high_col],
        df[low_col],
        df[close_col],
        fastk_period=14,
        slowk_period=3,
        slowd_period=3,
    )

    df["macd"], df["macd_signal"], df["macd_hist"] = talib.MACD(
        df[close_col],
        fastperiod=12,
        slowperiod=26,
        signalperiod=9,
    )

    df["sma_14"] = talib.SMA(df[close_col], timeperiod=14)
    # df["sma_50"] = talib.SMA(df[close_col], timeperiod=50)
    # df["sma_200"] = talib.SMA(df[close_col], timeperiod=200)
    # df["ema_14"] = talib.EMA(df[close_col], timeperiod=14)
    # df["ema_50"] = talib.EMA(df[close_col], timeperiod=50)
    # df["ema_200"] = talib.EMA(df[close_col], timeperiod=200)

    df["atr_14"] = talib.ATR(df[high_col], df[low_col], df[close_col], timeperiod=14)
    upper_bb, _, lower_bb = talib.BBANDS(df[close_col], timeperiod=20, nbdevup=2, nbdevdn=2)
    df["bb_20_upper"] = upper_bb
    df["bb_20_lower"] = lower_bb
    df["obv"] = talib.OBV(df[close_col], df[volume_col])
    df["obv_slope"] = df["obv"].diff(periods=10)

    return df


def flatten_windowed_data(X: pd.DataFrame, window_size: int) -> pd.DataFrame:
    X_windowed = []
    columns = X.columns
    for i in range(len(X) - window_size + 1):
        window = X.iloc[i : i + window_size][::-1].values.flatten()
        X_windowed.append(window)
    column_names = [f"{col}_t-{w}" for w in range(window_size) for col in columns]
    # preserve the timestamp index aligned with the end of each window
    index = X.index[window_size - 1 :]
    X_windowed_df = pd.DataFrame(X_windowed, columns=column_names, index=index)
    return X_windowed_df


def generate_column_names(base_cols, window_size):
    column_names = []
    for w in range(window_size):
        for col in base_cols:
            column_names.append(f"{col}_t-{w}")
    return column_names


def preprocess_data(path: str = "data/ALL.csv"):
    df = pd.read_csv(path, parse_dates=["timestamp"], index_col="timestamp")
    df = df.ffill()
    df = add_label(df, "nvda_open", "nvda_close", "y")
    df = add_technical_indicators(df, "nvda_open", "nvda_high", "nvda_low", "nvda_close", "nvda_volume")
    df = df.dropna()
    df.to_csv("data/processed_data.csv")


def get_df(window_size: int, path: str = "data/processed_data.csv"):
    df = pd.read_csv(path, parse_dates=["timestamp"], index_col="timestamp")
    X = df.drop(columns=["y"])
    y = df["y"]

    X_windowed = flatten_windowed_data(X, window_size=window_size)
    y_windowed = y[window_size - 1 :]
    X_train = X_windowed[:"2024-07-01 01:00:00"]
    X_val = X_windowed["2024-07-01 02:00:00":"2025-01-01 01:00:00"]
    X_test = X_windowed["2025-01-01 02:00:00":"2025-07-01 01:00:00"]
    y_train = y_windowed[:"2024-07-01 01:00:00"]
    y_val = y_windowed["2024-07-01 02:00:00":"2025-01-01 01:00:00"]
    y_test = y_windowed["2025-01-01 02:00:00":"2025-07-01 01:00:00"]
    return X_train, X_val, X_test, y_train, y_val, y_test
