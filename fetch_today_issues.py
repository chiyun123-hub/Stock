"""Fetch a handful of headlines for the homepage sidebar ("오늘의 이슈").
Caches to data/today_issues.json for the day so repeated site rebuilds
don't re-trigger Yahoo RSS rate limiting.
"""
import json
import os
from datetime import date

os.environ.setdefault("SSL_CERT_FILE", os.path.join(os.path.dirname(__file__), ".certs", "combined_ca_bundle.pem"))
os.environ.setdefault("REQUESTS_CA_BUNDLE", os.environ["SSL_CERT_FILE"])

from predict import fetch_news

ISSUE_TICKERS = ["AAPL", "005930.KS"]
CACHE_PATH = "data/today_issues.json"


def load_cache() -> dict | None:
    if not os.path.exists(CACHE_PATH):
        return None
    with open(CACHE_PATH, encoding="utf-8") as f:
        cache = json.load(f)
    return cache if cache.get("date") == date.today().isoformat() else None


def fetch_and_cache() -> dict:
    cached = load_cache()
    if cached is not None:
        return cached

    headlines = []
    for ticker in ISSUE_TICKERS:
        headlines.extend(fetch_news(ticker, limit=5))

    result = {"date": date.today().isoformat(), "headlines": headlines[:10]}
    os.makedirs("data", exist_ok=True)
    with open(CACHE_PATH, "w", encoding="utf-8") as f:
        json.dump(result, f, indent=2, ensure_ascii=False)
    return result


if __name__ == "__main__":
    issues = fetch_and_cache()
    print(f"{len(issues['headlines'])} headlines cached for {issues['date']}")
