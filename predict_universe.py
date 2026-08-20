"""Run the prediction engine across a fixed universe of large-cap tickers
(US + Korea) and split the results into UP / DOWN lists
(data/predictions_universe.json).
News headlines are skipped here (trend-only) to avoid RSS rate limiting
across dozens of sequential requests.
"""
import json
import os
import time

os.environ.setdefault("SSL_CERT_FILE", os.path.join(os.path.dirname(__file__), ".certs", "combined_ca_bundle.pem"))
os.environ.setdefault("REQUESTS_CA_BUNDLE", os.environ["SSL_CERT_FILE"])
os.environ.setdefault("CURL_CA_BUNDLE", os.environ["SSL_CERT_FILE"])

import yfinance as yf
from dotenv import load_dotenv

from analyzer import load_data, calculate_sma
from predict import summarize_trend, call_gemini

# ticker -> (display name, market, currency symbol)
# Names use plain, readable casing (e.g. "Nvidia" not "NVDA"/"NVIDIA") since
# these are shown to users instead of raw ticker codes.
US_TICKERS = {
    "AAPL": ("Apple", "US", "$"), "MSFT": ("Microsoft", "US", "$"),
    "GOOGL": ("Alphabet", "US", "$"), "AMZN": ("Amazon", "US", "$"),
    "NVDA": ("Nvidia", "US", "$"), "META": ("Meta", "US", "$"),
    "TSLA": ("Tesla", "US", "$"), "JPM": ("JPMorgan", "US", "$"),
    "V": ("Visa", "US", "$"), "WMT": ("Walmart", "US", "$"),
    "UNH": ("UnitedHealth", "US", "$"), "XOM": ("Exxon Mobil", "US", "$"),
    "JNJ": ("Johnson & Johnson", "US", "$"), "PG": ("Procter & Gamble", "US", "$"),
    "MA": ("Mastercard", "US", "$"), "HD": ("Home Depot", "US", "$"),
    "CVX": ("Chevron", "US", "$"), "ABBV": ("AbbVie", "US", "$"),
    "KO": ("Coca-Cola", "US", "$"), "PEP": ("PepsiCo", "US", "$"),
    "NFLX": ("Netflix", "US", "$"), "DIS": ("Disney", "US", "$"),
    "INTC": ("Intel", "US", "$"), "AMD": ("AMD", "US", "$"),
    "BA": ("Boeing", "US", "$"), "NKE": ("Nike", "US", "$"),
}
KR_TICKERS = {
    "005930.KS": ("삼성전자", "KR", "₩"), "000660.KS": ("SK하이닉스", "KR", "₩"),
    "035420.KS": ("NAVER", "KR", "₩"), "035720.KS": ("카카오", "KR", "₩"),
    "051910.KS": ("LG화학", "KR", "₩"), "006400.KS": ("삼성SDI", "KR", "₩"),
    "207940.KS": ("삼성바이오로직스", "KR", "₩"), "005380.KS": ("현대차", "KR", "₩"),
    "000270.KS": ("기아", "KR", "₩"), "105560.KS": ("KB금융", "KR", "₩"),
    "055550.KS": ("신한지주", "KR", "₩"), "012330.KS": ("현대모비스", "KR", "₩"),
    "096770.KS": ("SK이노베이션", "KR", "₩"), "066570.KS": ("LG전자", "KR", "₩"),
    "003670.KS": ("포스코퓨처엠", "KR", "₩"), "086790.KS": ("하나금융지주", "KR", "₩"),
    "015760.KS": ("한국전력", "KR", "₩"), "032830.KS": ("삼성생명", "KR", "₩"),
    "009150.KS": ("삼성전기", "KR", "₩"), "047050.KS": ("포스코인터내셔널", "KR", "₩"),
}
TICKERS = {**US_TICKERS, **KR_TICKERS}


def ensure_data(ticker: str, period: str = "1y") -> str:
    safe_name = ticker.replace(".", "_").lower()
    path = f"data/{safe_name}_{period}.csv"
    if not os.path.exists(path):
        os.makedirs("data", exist_ok=True)
        df = yf.download(ticker, period=period, interval="1d")
        df.to_csv(path)
    return path


def build_prompt_trend_only(ticker: str, name: str, trend_summary: str) -> str:
    return (
        "You are a stock trend classifier. Based on the trend data below for "
        f"{name} ({ticker}), respond with exactly one word, UP or DOWN, on the "
        "first line, then a one-sentence reason (in Korean) on the second line.\n\n"
        f"Trend summary:\n{trend_summary}"
    )


def predict_one(ticker: str, name: str, market: str, currency: str) -> dict:
    path = ensure_data(ticker)
    df = load_data(path)
    trend_summary = summarize_trend(df)
    prompt = build_prompt_trend_only(ticker, name, trend_summary)
    decision = call_gemini(prompt)
    latest_close = float(calculate_sma(df)["Close"].iloc[-1])
    return {
        "ticker": ticker,
        "name": name,
        "market": market,
        "currency": currency,
        "latest_close": round(latest_close, 2),
        **decision,
    }


def main() -> None:
    load_dotenv()
    results = []
    for ticker, (name, market, currency) in TICKERS.items():
        try:
            result = predict_one(ticker, name, market, currency)
            print(f"{ticker} ({name}): {result['decision']}")
            results.append(result)
        except Exception as e:
            print(f"{ticker}: FAILED ({e})")
        time.sleep(5)  # free-tier Gemini quota is 15 requests/minute

    up = [r for r in results if r["decision"] == "UP"][:10]
    down = [r for r in results if r["decision"] == "DOWN"][:10]

    os.makedirs("data", exist_ok=True)
    with open("data/predictions_universe.json", "w", encoding="utf-8") as f:
        json.dump(
            {"up": up, "down": down, "all": results, "failed_count": len(TICKERS) - len(results)},
            f, indent=2, ensure_ascii=False,
        )

    print(f"UP: {len(up)}, DOWN: {len(down)}, total tracked: {len(results)}")


if __name__ == "__main__":
    main()
