"""Upsert a local OHLCV CSV into the supabase market_data table."""
import argparse
import os
import sys

import pandas as pd
from dotenv import load_dotenv
from supabase import create_client


def main(csv_path: str, ticker: str) -> None:
    load_dotenv()
    url = os.environ.get("SUPABASE_URL")
    key = os.environ.get("SUPABASE_KEY")
    if not url or not key:
        print("SUPABASE_URL/SUPABASE_KEY not set in .env — skipping supabase upsert.")
        sys.exit(0)

    df = pd.read_csv(csv_path)
    df = df.rename(columns={c: c.lower() for c in df.columns})
    rows = df.to_dict(orient="records")
    for row in rows:
        row["ticker"] = ticker

    client = create_client(url, key)
    client.table("market_data").upsert(rows, on_conflict="ticker,date").execute()
    print(f"Upserted {len(rows)} rows for {ticker}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("csv_path")
    parser.add_argument("ticker")
    args = parser.parse_args()
    main(args.csv_path, args.ticker)
