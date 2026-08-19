"""Build look-ahead-safe features from an OHLCV dataframe."""
import pandas as pd


def build_features(df: pd.DataFrame) -> pd.DataFrame:
    out = df.copy()
    out["ma5"] = out["Close"].rolling(5).mean()
    out["ma20"] = out["Close"].rolling(20).mean()
    out["volatility10"] = out["Close"].pct_change().rolling(10).std()
    out["return1"] = out["Close"].pct_change()
    out["target_next_close"] = out["Close"].shift(-1)
    out["target_up"] = (out["target_next_close"] > out["Close"]).astype(int)
    return out.dropna()
