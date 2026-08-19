"""Minimal analyzer: load OHLCV data and compute simple moving averages."""
import pandas as pd


def load_data(path: str) -> pd.DataFrame:
    # yfinance CSVs have 2 extra header rows (Ticker, Date label); skip them
    df = pd.read_csv(path, index_col=0, skiprows=[1, 2])
    df.index = pd.to_datetime(df.index, format="%Y-%m-%d")
    df.index.name = "Date"
    for col in df.columns:
        df[col] = pd.to_numeric(df[col], errors="coerce")
    # Drop trailing rows for a still-open trading session (Close not yet reported)
    return df.dropna(subset=["Close"])


def calculate_sma(df: pd.DataFrame, window: int = 20) -> pd.DataFrame:
    out = df.copy()
    out[f"SMA_{window}"] = out["Close"].rolling(window, min_periods=window).mean()
    return out
