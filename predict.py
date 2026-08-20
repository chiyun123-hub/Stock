"""Core AI prediction engine: trend + news -> Claude -> UP/DOWN decision."""
import json
import os
import xml.etree.ElementTree as ET

# Trust the corporate TLS-inspection root cert (see .certs/combined_ca_bundle.pem)
_CA_BUNDLE = os.path.join(os.path.dirname(__file__), ".certs", "combined_ca_bundle.pem")
os.environ["SSL_CERT_FILE"] = _CA_BUNDLE
os.environ["REQUESTS_CA_BUNDLE"] = _CA_BUNDLE
os.environ["CURL_CA_BUNDLE"] = _CA_BUNDLE

import pandas as pd
import requests
from google import genai
from dotenv import load_dotenv

from analyzer import load_data, calculate_sma

NEWS_RSS_URL = "https://news.google.com/rss/search"


def _google_news_items(query: str) -> list:
    """Query Google News RSS (Korean locale) — no API key, far less rate limited
    than the Yahoo Finance RSS feed we used previously."""
    resp = requests.get(NEWS_RSS_URL, params={"q": query, "hl": "ko", "gl": "KR", "ceid": "KR:ko"})
    resp.raise_for_status()
    root = ET.fromstring(resp.text)
    return list(root.iter("item"))


def fetch_news(ticker: str, limit: int = 10) -> list[str]:
    """Fetch latest headlines for a ticker via Google News RSS (no API key needed).

    Returns an empty list on rate limiting / network failure so the pipeline
    can still produce a trend-only prediction instead of crashing.
    """
    try:
        items = _google_news_items(f"{ticker} stock")
    except requests.exceptions.RequestException as e:
        print(f"News fetch failed ({e}); continuing without headlines.")
        return []
    titles = [item.findtext("title") for item in items]
    return [t for t in titles if t][:limit]


def fetch_news_with_links(ticker: str, name: str = "", limit: int = 3) -> list[dict]:
    """Like fetch_news, but keeps each headline's article URL for click-through."""
    query = f"{name or ticker} 주식"
    try:
        items = _google_news_items(query)
    except requests.exceptions.RequestException as e:
        print(f"News fetch failed for {ticker} ({e}); skipping.")
        return []
    results = []
    for item in items:
        title = item.findtext("title")
        link = item.findtext("link")
        if title and link:
            results.append({"title": title, "link": link, "ticker": ticker})
    return results[:limit]


def summarize_trend(df: pd.DataFrame, window: int = 20) -> str:
    """Condense 5y of price data into a short trend summary (<=10 lines)."""
    df = calculate_sma(df, window=window)
    latest_close = df["Close"].iloc[-1]
    latest_sma = df[f"SMA_{window}"].iloc[-1]
    change_5d = (df["Close"].iloc[-1] / df["Close"].iloc[-6] - 1) * 100
    change_1y = (df["Close"].iloc[-1] / df["Close"].iloc[-252] - 1) * 100 if len(df) >= 252 else float("nan")
    trend = "above" if latest_close > latest_sma else "below"

    lines = [
        f"Latest close: {latest_close:.2f}",
        f"SMA_{window}: {latest_sma:.2f} (price is {trend} SMA)",
        f"5-day change: {change_5d:.2f}%",
        f"1-year change: {change_1y:.2f}%",
        f"5y range: {df['Close'].min():.2f} - {df['Close'].max():.2f}",
    ]
    return "\n".join(lines)


def build_prompt(trend_summary: str, headlines: list[str]) -> str:
    news_block = "\n".join(f"- {h}" for h in headlines) or "- (no recent headlines)"
    return (
        "You are a stock trend classifier. Based on the data below, "
        "respond with exactly one word, UP or DOWN, on the first line, "
        "then a one-sentence reason (in Korean) on the second line.\n\n"
        f"Trend summary:\n{trend_summary}\n\nRecent headlines:\n{news_block}"
    )


def call_gemini(prompt: str) -> dict:
    """Call the Gemini API and parse an UP/DOWN decision. Requires GEMINI_API_KEY in .env."""
    client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
    model = os.getenv("GEMINI_MODEL", "gemini-3.5-flash-lite")
    response = client.models.generate_content(model=model, contents=prompt)
    text = (response.text or "").strip()
    lines = text.splitlines()
    decision = lines[0].strip().upper() if lines else "UNKNOWN"
    reasoning = lines[1].strip() if len(lines) > 1 else ""
    return {"decision": decision, "reasoning": reasoning}


def translate_titles_to_korean(titles: list[str]) -> list[str]:
    """Batch-translate headlines to Korean in a single Gemini call (keeps order)."""
    if not titles:
        return []
    client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
    model = os.getenv("GEMINI_MODEL", "gemini-3.5-flash-lite")
    numbered = "\n".join(f"{i + 1}. {t}" for i, t in enumerate(titles))
    prompt = (
        "Translate each numbered news headline below into natural Korean. "
        "Reply with exactly the same numbering, one translated headline per line, "
        "no extra commentary.\n\n" + numbered
    )
    response = client.models.generate_content(model=model, contents=prompt)
    lines = [line.strip() for line in (response.text or "").splitlines() if line.strip()]
    translated = []
    for line in lines:
        text = line.split(".", 1)[1].strip() if "." in line[:4] else line
        translated.append(text)
    if len(translated) != len(titles):
        return titles  # fall back to originals if parsing mismatched
    return translated


def summarize_headlines_ko(titles: list[str], max_chars: int = 300) -> list[str]:
    """Batch-produce a <=max_chars Korean summary for each headline (one Gemini call).

    Since we only have the headline text (not the full article), this is a
    short, plausible-context summary rather than a summary of the full piece.
    """
    if not titles:
        return []
    client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
    model = os.getenv("GEMINI_MODEL", "gemini-3.5-flash-lite")
    numbered = "\n".join(f"{i + 1}. {t}" for i, t in enumerate(titles))
    prompt = (
        "For each numbered news headline below, write a Korean summary of what the "
        f"news is about, in {max_chars} characters or fewer. Reply with exactly the "
        "same numbering, one summary per line, no extra commentary.\n\n" + numbered
    )
    response = client.models.generate_content(model=model, contents=prompt)
    lines = [line.strip() for line in (response.text or "").splitlines() if line.strip()]
    summaries = []
    for line in lines:
        text = line.split(".", 1)[1].strip() if "." in line[:4] else line
        summaries.append(text[:max_chars])
    if len(summaries) != len(titles):
        return ["" for _ in titles]  # fall back to empty if parsing mismatched
    return summaries


def save_prediction(result: dict, path: str = "data/prediction_today.json") -> None:
    os.makedirs(os.path.dirname(path) or ".", exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(result, f, indent=2, ensure_ascii=False)


def predict(ticker: str = "AAPL", data_path: str = "data/aapl_5y.csv") -> dict:
    load_dotenv()
    df = load_data(data_path)
    trend_summary = summarize_trend(df)
    headlines = fetch_news(ticker)
    prompt = build_prompt(trend_summary, headlines)
    decision = call_gemini(prompt)
    result = {"ticker": ticker, **decision}
    save_prediction(result)
    return result


if __name__ == "__main__":
    predict()
