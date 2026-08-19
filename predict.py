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

NEWS_RSS_URL = "https://feeds.finance.yahoo.com/rss/2.0/headline"


def fetch_news(ticker: str, limit: int = 10) -> list[str]:
    """Fetch latest headlines for a ticker via Yahoo Finance RSS (no API key needed).

    Returns an empty list on rate limiting / network failure so the pipeline
    can still produce a trend-only prediction instead of crashing.
    """
    try:
        resp = requests.get(NEWS_RSS_URL, params={"s": ticker, "region": "US", "lang": "en-US"})
        resp.raise_for_status()
    except requests.exceptions.RequestException as e:
        print(f"News fetch failed ({e}); continuing without headlines.")
        return []
    root = ET.fromstring(resp.text)
    titles = [item.findtext("title") for item in root.iter("item")]
    return [t for t in titles if t][:limit]


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
