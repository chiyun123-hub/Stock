"""Download historical OHLCV data for one ticker via yfinance and save to data/."""
import argparse
import os

import yfinance as yf


def fetch(ticker: str, period: str, interval: str) -> str:
    os.makedirs("data", exist_ok=True)
    df = yf.download(ticker, period=period, interval=interval)
    path = f"data/{ticker.lower()}_{period}.csv"
    df.to_csv(path)
    return path


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("ticker")
    parser.add_argument("--period", default="5y")
    parser.add_argument("--interval", default="1d")
    args = parser.parse_args()

    saved_path = fetch(args.ticker, args.period, args.interval)
    print(f"Saved {saved_path}")
