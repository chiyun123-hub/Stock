"""Fetch key headlines (with clickable article links) for every predicted
ticker, translate them to Korean, and cache to data/today_issues.json for
the homepage sidebar ("오늘의 이슈").
"""
import json
import os
import time
from datetime import date

os.environ.setdefault("SSL_CERT_FILE", os.path.join(os.path.dirname(__file__), ".certs", "combined_ca_bundle.pem"))
os.environ.setdefault("REQUESTS_CA_BUNDLE", os.environ["SSL_CERT_FILE"])

from dotenv import load_dotenv

from predict import fetch_news_with_links, translate_titles_to_korean

CACHE_PATH = "data/today_issues.json"
HEADLINES_PER_TICKER = 2
MAX_TICKERS = 10


def load_cache() -> dict | None:
    if not os.path.exists(CACHE_PATH):
        return None
    with open(CACHE_PATH, encoding="utf-8") as f:
        cache = json.load(f)
    return cache if cache.get("date") == date.today().isoformat() else None


def predicted_tickers(path: str = "data/predictions_universe.json") -> list[tuple[str, str]]:
    if not os.path.exists(path):
        return []
    with open(path, encoding="utf-8") as f:
        universe = json.load(f)
    items = universe.get("up", []) + universe.get("down", [])
    return [(item["ticker"], item.get("name", "")) for item in items][:MAX_TICKERS]


def fetch_and_cache(force: bool = False) -> dict:
    cached = load_cache()
    if cached is not None and not force:
        return cached

    load_dotenv()
    items = []
    for ticker, name in predicted_tickers():
        items.extend(fetch_news_with_links(ticker, name=name, limit=HEADLINES_PER_TICKER))
        time.sleep(0.5)  # be gentle with the RSS endpoint

    titles_kr = translate_titles_to_korean([it["title"] for it in items])
    for item, title_kr in zip(items, titles_kr):
        item["title_kr"] = title_kr

    result = {"date": date.today().isoformat(), "headlines": items}
    os.makedirs("data", exist_ok=True)
    with open(CACHE_PATH, "w", encoding="utf-8") as f:
        json.dump(result, f, indent=2, ensure_ascii=False)
    return result


if __name__ == "__main__":
    issues = fetch_and_cache(force=True)
    print(f"{len(issues['headlines'])} headlines cached for {issues['date']}")
