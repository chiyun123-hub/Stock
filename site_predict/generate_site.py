"""Render data/prediction_today.json + trend stats into a static GUI homepage."""
import json
import os
from datetime import date

from analyzer import load_data, calculate_sma

TEMPLATE_PATH = os.path.join(os.path.dirname(__file__), "template.html")
OUTPUT_PATH = os.path.join(os.path.dirname(__file__), "index.html")


def load_prediction(path: str = "data/prediction_today.json") -> dict:
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def build_stats(csv_path: str = "data/aapl_5y.csv") -> dict:
    df = calculate_sma(load_data(csv_path), window=20)
    close = df["Close"]
    return {
        "latest_close": round(float(close.iloc[-1]), 2),
        "sma_20": round(float(df["SMA_20"].iloc[-1]), 2),
        "change_5d": round(float((close.iloc[-1] / close.iloc[-6] - 1) * 100), 2),
        "range_low": round(float(close.min()), 2),
        "range_high": round(float(close.max()), 2),
    }


def load_universe(path: str = "data/predictions_universe.json") -> dict:
    if not os.path.exists(path):
        return {"up": [], "down": []}
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def load_issues(path: str = "data/today_issues.json") -> list[dict]:
    if not os.path.exists(path):
        return []
    with open(path, encoding="utf-8") as f:
        return json.load(f).get("headlines", [])


def render_issues(headlines: list[dict]) -> str:
    if not headlines:
        return '<div class="issue-empty">뉴스 소스 요청 제한으로 지금은 표시할 이슈가 없습니다.</div>'
    items = "\n".join(
        f'<li class="issue-item"><a href="{h["link"]}" target="_blank" rel="noopener noreferrer">'
        f'<span class="issue-ticker">{h["ticker"]}</span>{h.get("title_kr", h["title"])}</a></li>'
        for h in headlines
    )
    return f'<ul class="issue-list">{items}</ul>'


def safe_name(ticker: str) -> str:
    return ticker.replace(".", "_").lower()


def render_rows(items: list[dict]) -> str:
    if not items:
        return '<div class="stock-reason">데이터 없음</div>'
    rows = []
    for i, item in enumerate(items, 1):
        name = item.get("name", "")
        market = item.get("market", "US")
        currency = item.get("currency", "$")
        label = f'{item["ticker"]}{f" · {name}" if name else ""}'
        href = f"stocks/{safe_name(item['ticker'])}.html"
        rows.append(
            f'<a class="stock-row" href="{href}">'
            '<div class="stock-main">'
            f'<div class="stock-ticker"><span class="rank">{i}</span>{label}'
            f'<span class="market-badge">{market}</span></div>'
            f'<div class="stock-reason">{item.get("reasoning", "")}</div>'
            "</div>"
            f'<div class="stock-price">{currency}{item.get("latest_close", 0):,.2f}</div>'
            "</a>"
        )
    return "\n".join(rows)


def render(prediction: dict, stats: dict, universe: dict) -> str:
    with open(TEMPLATE_PATH, encoding="utf-8") as f:
        template = f.read()

    is_up = prediction["decision"] == "UP"
    ticker_href = f"stocks/{safe_name(prediction['ticker'])}.html"
    replacements = {
        "{{TICKER}}": prediction["ticker"],
        "{{TICKER_HREF}}": ticker_href,
        "{{DECISION}}": prediction["decision"],
        "{{DECISION_CLASS}}": "up" if is_up else "down",
        "{{ARROW}}": "▲" if is_up else "▼",
        "{{REASONING}}": prediction.get("reasoning", ""),
        "{{DATE}}": prediction.get("date", date.today().isoformat()),
        "{{LATEST_CLOSE}}": f"{stats['latest_close']:.2f}",
        "{{SMA_20}}": f"{stats['sma_20']:.2f}",
        "{{CHANGE_5D}}": f"{stats['change_5d']:+.2f}%",
        "{{RANGE}}": f"{stats['range_low']:.2f} - {stats['range_high']:.2f}",
        "{{UP_COUNT}}": str(len(universe.get("up", []))),
        "{{DOWN_COUNT}}": str(len(universe.get("down", []))),
        "{{UP_ROWS}}": render_rows(universe.get("up", [])),
        "{{DOWN_ROWS}}": render_rows(universe.get("down", [])),
        "{{ISSUE_LIST}}": render_issues(load_issues()),
    }
    for key, value in replacements.items():
        template = template.replace(key, str(value))
    return template


def main() -> None:
    prediction = load_prediction()
    stats = build_stats()
    universe = load_universe()
    html = render(prediction, stats, universe)
    with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
        f.write(html)
    print(f"Wrote {OUTPUT_PATH}")


if __name__ == "__main__":
    main()
