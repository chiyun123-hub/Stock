"""Generate a detail page (with a price chart) for every screened ticker,
and for the single featured prediction. Written to site_predict/stocks/.
"""
import json
import os
from datetime import date

from analyzer import load_data, calculate_sma
from chart import interactive_chart_html, naive_predicted_price, period_return
from common import load_sidebar_context, render_page

BASE_DIR = os.path.dirname(__file__)
CONTENT_TEMPLATE_PATH = os.path.join(BASE_DIR, "stock_content_template.html")
OUTPUT_DIR = os.path.join(BASE_DIR, "stocks")

EXTRA_CSS = """
  .card {
    background: var(--card); border: 1px solid var(--border); border-radius: 20px;
    padding: 32px; box-shadow: 0 20px 60px rgba(0,0,0,0.4); margin-bottom: 24px;
  }
  .ticker-row { display: flex; justify-content: space-between; align-items: baseline; margin-bottom: 4px; }
  .ticker { font-size: 26px; font-weight: 800; }
  .market-badge {
    font-size: 11px; font-weight: 700; color: var(--muted);
    border: 1px solid var(--border); border-radius: 4px; padding: 2px 6px; margin-left: 8px;
  }
  .name { color: var(--muted); font-size: 14px; margin-bottom: 20px; }
  .decision-badge {
    display: flex; align-items: center; justify-content: center; gap: 10px;
    padding: 22px 0; border-radius: 14px; margin-bottom: 20px; font-size: 32px; font-weight: 800;
  }
  .decision-badge.up   { background: rgba(34,197,94,0.12); color: var(--up); }
  .decision-badge.down { background: rgba(239,68,68,0.12); color: var(--down); }
  .reasoning {
    font-size: 14px; line-height: 1.6; background: #0e141b; border: 1px solid var(--border);
    border-radius: 12px; padding: 14px 16px; margin-bottom: 20px;
  }
  .chart-wrap { background: #0e141b; border: 1px solid var(--border); border-radius: 12px; padding: 16px; margin-bottom: 20px; }
  .chart-title { font-size: 12px; color: var(--muted); margin-bottom: 8px; }
  .range-buttons { display: flex; gap: 6px; margin-bottom: 10px; }
  .range-btn {
    background: #0e141b; border: 1px solid var(--border); color: var(--muted);
    font-size: 12px; font-weight: 600; padding: 5px 12px; border-radius: 8px;
    cursor: pointer; font-family: inherit;
  }
  .range-btn:hover { border-color: var(--accent); color: var(--text); }
  .range-btn.active { background: var(--accent); border-color: var(--accent); color: #fff; }
  .chart-container { position: relative; }
  .price-chart { width: 100%; height: auto; display: block; cursor: crosshair; }
  .chart-empty { font-size: 13px; color: var(--muted); text-align: center; padding: 40px 0; }
  .chart-tooltip {
    position: absolute; top: 8px; background: #1a2330; border: 1px solid var(--border);
    border-radius: 8px; padding: 6px 10px; font-size: 12px; line-height: 1.4;
    pointer-events: none; white-space: nowrap; z-index: 5;
  }
  .predicted-stat { border-color: var(--accent); }
  .stats { display: grid; grid-template-columns: 1fr 1fr; gap: 12px; }
  .stat { background: #0e141b; border: 1px solid var(--border); border-radius: 10px; padding: 12px 14px; }
  .stat-label { color: var(--muted); font-size: 11px; text-transform: uppercase; letter-spacing: 0.5px; }
  .period-title { font-size: 12px; color: var(--muted); margin: 20px 0 8px; }
  .period-stats { grid-template-columns: repeat(4, 1fr); margin-bottom: 20px; }
  .pct-up { color: var(--up); }
  .pct-down { color: var(--down); }
  .stat-value { font-size: 16px; font-weight: 600; margin-top: 4px; }
  .disclaimer { font-size: 11px; color: var(--muted); text-align: center; line-height: 1.5; }
"""


def safe_name(ticker: str) -> str:
    return ticker.replace(".", "_").lower()


def find_csv(ticker: str) -> str | None:
    for period in ("1y", "5y"):
        path = f"data/{safe_name(ticker)}_{period}.csv"
        if os.path.exists(path):
            return path
    return None


def build_page(item: dict, ctx: dict) -> str:
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
        predicted_price = naive_predicted_price(close)
        chart_svg = interactive_chart_html(
            close, currency, color, chart_id=safe_name(ticker), predicted_price=predicted_price
        )
        latest_close = float(close.iloc[-1])
        sma_20 = float(df["SMA_20"].iloc[-1])
        change_5d = (close.iloc[-1] / close.iloc[-6] - 1) * 100 if len(close) > 6 else float("nan")
        range_text = f"{close.min():,.2f} - {close.max():,.2f}"
        change_1m = fmt_pct(period_return(close, 21))
        change_3m = fmt_pct(period_return(close, 63))
        change_6m = fmt_pct(period_return(close, 126))
        change_1y = fmt_pct(period_return(close, 252))
        predicted_price_text = f"{currency}{predicted_price:,.2f}"
        predicted_change = (predicted_price / latest_close - 1) * 100
        predicted_change_text = fmt_pct(predicted_change)
    else:
        chart_svg = '<div class="chart-empty">차트를 그릴 데이터가 없습니다.</div>'
        latest_close = item.get("latest_close", 0)
        sma_20 = float("nan")
        change_5d = float("nan")
        range_text = "N/A"
        change_1m = change_3m = change_6m = change_1y = "N/A"
        predicted_price_text = "N/A"
        predicted_change_text = "N/A"

    with open(CONTENT_TEMPLATE_PATH, encoding="utf-8") as f:
        content = f.read()

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
        "{{PREDICTED_PRICE}}": predicted_price_text,
        "{{PREDICTED_CHANGE}}": predicted_change_text,
    }
    for key, value in replacements.items():
        content = content.replace(key, str(value))

    return render_page(f"{ticker} 예측 상세", "", content, EXTRA_CSS, prefix="../", **ctx)


def main() -> None:
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    ctx = load_sidebar_context()

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
        html = build_page(item, ctx)
        out_path = os.path.join(OUTPUT_DIR, f"{safe_name(item['ticker'])}.html")
        with open(out_path, "w", encoding="utf-8") as f:
            f.write(html)
        written += 1

    print(f"Wrote {written} stock detail pages to {OUTPUT_DIR}")


if __name__ == "__main__":
    main()
