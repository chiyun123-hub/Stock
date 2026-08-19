"""Backtest a trained direction model on a strictly held-out recent window."""
import argparse
import json
import pickle

import numpy as np
import pandas as pd

import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", "stock-model-training", "scripts"))
from build_features import build_features  # noqa: E402

FEATURE_COLS = ["ma5", "ma20", "volatility10", "return1"]


def main(csv_path: str, ticker: str, holdout_days: int) -> None:
    df = pd.read_csv(csv_path, index_col=0, parse_dates=True)
    feat = build_features(df)
    holdout = feat.iloc[-holdout_days:]

    with open(f"models/{ticker.lower()}_model.pkl", "rb") as f:
        model = pickle.load(f)

    preds = model.predict(holdout[FEATURE_COLS])
    direction_accuracy = float((preds == holdout["target_up"]).mean())

    strategy_returns = holdout["return1"].shift(-1).fillna(0) * np.where(preds == 1, 1, -1)
    cumulative_return = float((1 + strategy_returns).cumprod().iloc[-1] - 1)
    equity_curve = (1 + strategy_returns).cumprod()
    max_drawdown = float(((equity_curve / equity_curve.cummax()) - 1).min())

    result = {
        "ticker": ticker,
        "holdout_days": holdout_days,
        "direction_accuracy": direction_accuracy,
        "cumulative_return": cumulative_return,
        "max_drawdown": max_drawdown,
    }
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("csv_path")
    parser.add_argument("ticker")
    parser.add_argument("--holdout-days", type=int, default=60)
    args = parser.parse_args()
    main(args.csv_path, args.ticker, args.holdout_days)
