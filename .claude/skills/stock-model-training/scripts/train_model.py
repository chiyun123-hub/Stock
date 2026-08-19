"""Train a direction-prediction model with a strict time-ordered split."""
import argparse
import json
import pickle

import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score

from build_features import build_features

FEATURE_COLS = ["ma5", "ma20", "volatility10", "return1"]


def main(csv_path: str, ticker: str, val_ratio: float) -> None:
    df = pd.read_csv(csv_path, index_col=0, parse_dates=True)
    feat = build_features(df)

    split = int(len(feat) * (1 - val_ratio))
    train, val = feat.iloc[:split], feat.iloc[split:]

    model = RandomForestClassifier(n_estimators=200, random_state=42)
    model.fit(train[FEATURE_COLS], train["target_up"])

    val_pred = model.predict(val[FEATURE_COLS])
    direction_accuracy = accuracy_score(val["target_up"], val_pred)

    with open(f"models/{ticker.lower()}_model.pkl", "wb") as f:
        pickle.dump(model, f)
    with open(f"models/{ticker.lower()}_features.json", "w") as f:
        json.dump({"features": FEATURE_COLS, "val_direction_accuracy": direction_accuracy}, f, indent=2)

    print(f"Validation direction accuracy: {direction_accuracy:.4f}")


if __name__ == "__main__":
    import os

    os.makedirs("models", exist_ok=True)
    parser = argparse.ArgumentParser()
    parser.add_argument("csv_path")
    parser.add_argument("ticker")
    parser.add_argument("--val-ratio", type=float, default=0.2)
    args = parser.parse_args()
    main(args.csv_path, args.ticker, args.val_ratio)
