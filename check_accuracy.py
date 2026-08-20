"""Compare past predictions stored in Supabase against what the price
actually did on the next trading day, and save a summary + per-row detail
to data/accuracy.json for the "예측 정확도" page.
"""
import json
import os
from datetime import date

os.environ.setdefault("SSL_CERT_FILE", os.path.join(os.path.dirname(__file__), ".certs", "combined_ca_bundle.pem"))
os.environ.setdefault("REQUESTS_CA_BUNDLE", os.environ["SSL_CERT_FILE"])

import pandas as pd
from dotenv import load_dotenv
from supabase import create_client

from analyzer import load_data


def safe_name(ticker: str) -> str:
    return ticker.replace(".", "_").lower()


def find_csv(ticker: str) -> str | None:
    for period in ("1y", "5y"):
        path = f"data/{safe_name(ticker)}_{period}.csv"
        if os.path.exists(path):
            return path
    return None


def actual_direction(ticker: str, pred_date: str) -> tuple[str | None, float | None]:
    """Return ('UP'/'DOWN', % change) from pred_date's close to the next
    trading day's close in the cached CSV, or (None, None) if not available."""
    csv_path = find_csv(ticker)
    if not csv_path:
        return None, None
    df = load_data(csv_path)
    idx = df.index[df.index == pd.Timestamp(pred_date)]
    if len(idx) == 0:
        return None, None
    pos = df.index.get_loc(idx[0])
    if pos + 1 >= len(df):
        return None, None  # next trading day not fetched yet
    today_close = float(df["Close"].iloc[pos])
    next_close = float(df["Close"].iloc[pos + 1])
    pct = (next_close / today_close - 1) * 100
    return ("UP" if next_close >= today_close else "DOWN"), pct


def main() -> None:
    load_dotenv()
    client = create_client(os.getenv("SUPABASE_URL"), os.getenv("SUPABASE_KEY"))
    rows = client.table("predictions").select("date,ticker,prediction,reason").order("date").execute().data

    evaluated = []
    for row in rows:
        actual, pct = actual_direction(row["ticker"], row["date"])
        if actual is None:
            continue
        evaluated.append({
            "date": row["date"],
            "ticker": row["ticker"],
            "predicted": row["prediction"],
            "actual": actual,
            "change_pct": round(pct, 2),
            "correct": row["prediction"] == actual,
        })

    total = len(evaluated)
    correct = sum(1 for e in evaluated if e["correct"])
    accuracy = round(correct / total * 100, 1) if total else None

    result = {
        "generated_at": date.today().isoformat(),
        "total_evaluated": total,
        "correct": correct,
        "accuracy_pct": accuracy,
        "pending": len(rows) - total,
        "rows": evaluated,
    }
    with open("data/accuracy.json", "w", encoding="utf-8") as f:
        json.dump(result, f, indent=2, ensure_ascii=False)

    print(f"Evaluated {total}/{len(rows)} predictions - accuracy: {accuracy}%")


if __name__ == "__main__":
    main()
