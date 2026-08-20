"""Generate a detail page (with a price chart) for every screened ticker,
and for the single featured prediction. Written to site_predict/stocks/.
"""
import json
import os
from datetime import date

from analyzer import load_data, calculate_sma
from chart import line_chart_svg, period_return

BASE_DIR = os.path.dirname(__file__)
TEMPLATE_PATH = os.path.join(BASE_DIR, "stock_template.html")
OUTPUT_DIR = os.path.join(BASE_DIR, "stocks")


def safe_name(ticker: str) -> str:
    return ticker.replace(".", "_").lower()


def find_csv(ticker: str) -> str | None:
    for period in ("1y", "5y"):
        path = f"data/{safe_name(ticker)}_{period}.csv"
        if os.path.exists(path):
            return path
    return None


def build_page(item: dict) -> str:
    ticker = item["ticker"]
    market = item.get("market", "US")
    currency = item.get("currency", "$")
    name = item.get("name", "")
    decision = item["decision"]
    is_up = decision == "UP"
    color = "#22c55e" if is_up else "#ef4444"

    csv_path = find_csv(ticker)

    def fmt_pct(v: float | None) -> str:
        if v is None:
            return "N/A"
        cls = "pct-up" if v >= 0 else "pct-down"
        return f'<span class="{cls}">{v:+.2f}%</span>'

    if csv_path:
        df = calculate_sma(load_data(csv_path), window=20)
        close = df["Close"]
        chart_svg = line_chart_svg(close, color, currency=currency)
        latest_close = float(close.iloc[-1])
        sma_20 = float(df["SMA_20"].iloc[-1])
        change_5d = (close.iloc[-1] / close.iloc[-6] - 1) * 100 if len(close) > 6 else float("nan")
        range_text = f"{close.min():,.2f} - {close.max():,.2f}"
        change_1m = fmt_pct(period_return(close, 21))
        change_3m = fmt_pct(period_return(close, 63))
        change_6m = fmt_pct(period_return(close, 126))
        change_1y = fmt_pct(period_return(close, 252))
    else:
        chart_svg = '<div class="chart-empty">차트를 그릴 데이터가 없습니다.</div>'
        latest_close = item.get("latest_close", 0)
        sma_20 = float("nan")
        change_5d = float("nan")
        range_text = "N/A"
        change_1m = change_3m = change_6m = change_1y = "N/A"

    with open(TEMPLATE_PATH, encoding="utf-8") as f:
        template = f.read()

    replacements = {
        "{{TICKER}}": ticker,
        "{{MARKET}}": market,
        "{{NAME}}": name,
        "{{DATE}}": date.today().isoformat(),
        "{{DECISION}}": decision,
        "{{DECISION_CLASS}}": "up" if is_up else "down",
        "{{ARROW}}": "▲" if is_up else "▼",
        "{{REASONING}}": item.get("reasoning", ""),
        "{{CHART_SVG}}": chart_svg,
        "{{CURRENCY}}": currency,
        "{{LATEST_CLOSE}}": f"{latest_close:,.2f}",
        "{{SMA_20}}": f"{sma_20:,.2f}" if sma_20 == sma_20 else "N/A",
        "{{CHANGE_5D}}": fmt_pct(change_5d) if change_5d == change_5d else "N/A",
        "{{RANGE}}": range_text,
        "{{CHANGE_1M}}": change_1m,
        "{{CHANGE_3M}}": change_3m,
        "{{CHANGE_6M}}": change_6m,
        "{{CHANGE_1Y}}": change_1y,
    }
    for key, value in replacements.items():
        template = template.replace(key, str(value))
    return template


def main() -> None:
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    items = []
    universe_path = "data/predictions_universe.json"
    if os.path.exists(universe_path):
        with open(universe_path, encoding="utf-8") as f:
            universe = json.load(f)
        items.extend(universe.get("up", []))
        items.extend(universe.get("down", []))

    featured_path = "data/prediction_today.json"
    if os.path.exists(featured_path):
        with open(featured_path, encoding="utf-8") as f:
            featured = json.load(f)
        items.append({"market": "US", "currency": "$", "name": "", **featured})

    written = 0
    for item in items:
        html = build_page(item)
        out_path = os.path.join(OUTPUT_DIR, f"{safe_name(item['ticker'])}.html")
        with open(out_path, "w", encoding="utf-8") as f:
            f.write(html)
        written += 1

    print(f"Wrote {written} stock detail pages to {OUTPUT_DIR}")


if __name__ == "__main__":
    main()
