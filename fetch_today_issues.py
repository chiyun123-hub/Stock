"""Fetch key headlines (with clickable article links) for every predicted
ticker, translate them to Korean, and cache to data/today_issues.json for
the homepage sidebar ("오늘의 이슈").

Each Google News RSS link is decoded to its real destination URL and
HTTP-validated (up to 4 attempts) before being included, so broken /
removed articles don't end up on the site.
"""
import json
import os
import time
from datetime import date

os.environ.setdefault("SSL_CERT_FILE", os.path.join(os.path.dirname(__file__), ".certs", "combined_ca_bundle.pem"))
os.environ.setdefault("REQUESTS_CA_BUNDLE", os.environ["SSL_CERT_FILE"])
os.environ.setdefault("CURL_CA_BUNDLE", os.environ["SSL_CERT_FILE"])

import requests
from dotenv import load_dotenv
from googlenewsdecoder import gnewsdecoder

from predict import fetch_news_with_links, summarize_headlines_ko, translate_titles_to_korean

CACHE_PATH = "data/today_issues.json"
HEADLINES_PER_TICKER = 1
MAX_TICKERS = 20
LINK_VALIDATION_ATTEMPTS = 4


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


def resolve_and_validate(google_link: str, attempts: int = LINK_VALIDATION_ATTEMPTS) -> str | None:
    """Decode the real article URL from a Google News RSS link, then confirm
    it actually loads (retrying up to `attempts` times). Returns None if the
    link can't be resolved or never returns a valid page."""
    real_url = None
    for _ in range(attempts):
        try:
            decoded = gnewsdecoder(google_link, interval=1)
            if decoded.get("status"):
                real_url = decoded["decoded_url"]
                break
        except Exception:
            pass
    if not real_url:
        return None

    for _ in range(attempts):
        try:
            resp = requests.get(real_url, timeout=10, allow_redirects=True)
            if resp.status_code < 400:
                return real_url
        except requests.exceptions.RequestException:
            pass
    return None


def fetch_and_cache(force: bool = False) -> dict:
    cached = load_cache()
    if cached is not None and not force:
        return cached

    load_dotenv()
    candidates = []
    for ticker, name in predicted_tickers():
        candidates.extend(fetch_news_with_links(ticker, name=name, limit=HEADLINES_PER_TICKER))
        time.sleep(0.5)  # be gentle with the RSS endpoint

    items = []
    for item in candidates:
        real_url = resolve_and_validate(item["link"])
        if real_url is None:
            print(f"Dropping unreachable link for {item['ticker']}: {item['title'][:60]}")
            continue
        item["link"] = real_url
        items.append(item)

    titles_kr = translate_titles_to_korean([it["title"] for it in items])
    for item, title_kr in zip(items, titles_kr):
        item["title_kr"] = title_kr

    summaries = summarize_headlines_ko(titles_kr, max_chars=300)
    for item, summary in zip(items, summaries):
        item["summary"] = summary

    result = {"date": date.today().isoformat(), "headlines": items}
    os.makedirs("data", exist_ok=True)
    with open(CACHE_PATH, "w", encoding="utf-8") as f:
        json.dump(result, f, indent=2, ensure_ascii=False)
    return result


if __name__ == "__main__":
    issues = fetch_and_cache(force=True)
    print(f"{len(issues['headlines'])} headlines cached for {issues['date']}")
