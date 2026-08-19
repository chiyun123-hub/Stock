"""Upsert data/prediction_today.json into the Supabase `predictions` table."""
import json
import os
from datetime import date, datetime

# Trust the corporate TLS-inspection root cert (see .certs/combined_ca_bundle.pem)
_CA_BUNDLE = os.path.join(os.path.dirname(__file__), ".certs", "combined_ca_bundle.pem")
os.environ["SSL_CERT_FILE"] = _CA_BUNDLE
os.environ["REQUESTS_CA_BUNDLE"] = _CA_BUNDLE

from dotenv import load_dotenv
from supabase import create_client


def load_latest_prediction(path: str = "data/prediction_today.json") -> dict:
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def to_row(prediction: dict) -> dict:
    """Map predict.py's output shape to the predictions table columns."""
    return {
        "date": prediction.get("date", date.today().isoformat()),
        "ticker": prediction["ticker"],
        "prediction": prediction["decision"],
        "reason": prediction.get("reasoning", ""),
        "created_at": datetime.utcnow().isoformat(),
    }


def _client():
    load_dotenv()
    url = os.getenv("SUPABASE_URL")
    key = os.getenv("SUPABASE_KEY")
    if not url or not key:
        print("SUPABASE_URL/SUPABASE_KEY not set in .env — skipping sync.")
        return None
    return create_client(url, key)


def sync(path: str = "data/prediction_today.json") -> dict | None:
    client = _client()
    if client is None:
        return None

    prediction = load_latest_prediction(path)
    row = to_row(prediction)

    client.table("predictions").upsert(row, on_conflict="date,ticker").execute()
    print(f"Synced prediction for {row['ticker']} ({row['date']}) to Supabase.")
    return row


def sync_universe(path: str = "data/predictions_universe.json") -> int:
    """Upsert every ticker from predict_universe.py's UP/DOWN screening."""
    client = _client()
    if client is None:
        return 0

    with open(path, encoding="utf-8") as f:
        universe = json.load(f)

    today = date.today().isoformat()
    now = datetime.utcnow().isoformat()
    rows = [
        {
            "date": today,
            "ticker": item["ticker"],
            "prediction": item["decision"],
            "reason": item.get("reasoning", ""),
            "created_at": now,
        }
        for item in universe.get("up", []) + universe.get("down", [])
    ]
    if not rows:
        return 0

    client.table("predictions").upsert(rows, on_conflict="date,ticker").execute()
    print(f"Synced {len(rows)} universe predictions to Supabase.")
    return len(rows)


if __name__ == "__main__":
    sync()
    sync_universe()
