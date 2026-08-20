"""Render data/today_issues.json into a full-page news list (issues.html),
linked from the sidebar's "오늘의 이슈" item.
"""
import json
import os

from analyzer import load_data, calculate_sma
from chart import naive_predicted_price
from common import load_sidebar_context, render_page
from predict_universe import TICKERS as TICKER_INFO

OUTPUT_PATH = os.path.join(os.path.dirname(__file__), "issues.html")

EXTRA_CSS = """
  h1 { font-size: 24px; margin: 0 0 4px; }
  .sub { color: var(--muted); font-size: 13px; margin-bottom: 28px; }
  .news-list { list-style: none; margin: 0; padding: 0; }
  .news-item {
    display: flex; justify-content: space-between; align-items: flex-start; gap: 16px;
    background: var(--card); border: 1px solid var(--border); border-radius: 12px;
    padding: 16px 18px; margin-bottom: 12px; text-decoration: none; color: var(--text);
  }
  .news-item:hover { border-color: var(--accent); }
  .news-main { flex: 1; min-width: 0; }
  .news-ticker {
    display: inline-block; font-size: 11px; font-weight: 700; color: var(--accent);
    border: 1px solid var(--accent); border-radius: 4px; padding: 2px 6px; margin-right: 8px;
  }
  .news-title { font-size: 14px; line-height: 1.5; font-weight: 600; margin-bottom: 6px; }
  .news-summary { font-size: 12px; color: var(--muted); line-height: 1.5; }
  .news-price { flex-shrink: 0; text-align: right; min-width: 110px; }
  .news-price-now { font-size: 14px; font-weight: 700; }
  .news-price-target { font-size: 11px; color: var(--muted); margin-top: 2px; }
  .news-price-pct { font-size: 12px; font-weight: 700; margin-top: 4px; }
  .pct-up { color: var(--up); }
  .pct-down { color: var(--down); }
  .empty { color: var(--muted); font-size: 14px; text-align: center; padding: 60px 0; }
"""


def safe_name(ticker: str) -> str:
    return ticker.replace(".", "_").lower()


def display_name(ticker: str) -> str:
    return TICKER_INFO.get(ticker, (ticker,))[0]


def load_issues(path: str = "data/today_issues.json") -> list[dict]:
    if not os.path.exists(path):
        return []
    with open(path, encoding="utf-8") as f:
        return json.load(f).get("headlines", [])


def price_info(ticker: str) -> dict | None:
    """Latest close + naive next-day predicted price, for the price column."""
    currency = TICKER_INFO.get(ticker, (ticker, "US", "$"))[2]
    for period in ("1y", "5y"):
        path = f"data/{safe_name(ticker)}_{period}.csv"
        if os.path.exists(path):
            close = calculate_sma(load_data(path))["Close"]
            latest = float(close.iloc[-1])
            predicted = naive_predicted_price(close)
            pct = (predicted / latest - 1) * 100
            return {"currency": currency, "latest": latest, "predicted": predicted, "pct": pct}
    return None


def render_list(headlines: list[dict]) -> str:
    if not headlines:
        return '<div class="empty">지금은 표시할 뉴스가 없습니다. 잠시 후 다시 시도해주세요.</div>'
    items = []
    for h in headlines:
        info = price_info(h["ticker"])
        if info:
            pct_cls = "pct-up" if info["pct"] >= 0 else "pct-down"
            price_html = (
                '<div class="news-price">'
                f'<div class="news-price-now">{info["currency"]}{info["latest"]:,.2f}</div>'
                f'<div class="news-price-target">예측 {info["currency"]}{info["predicted"]:,.2f}</div>'
                f'<div class="news-price-pct {pct_cls}">{info["pct"]:+.2f}%</div>'
                "</div>"
            )
        else:
            price_html = '<div class="news-price"><div class="news-price-target">가격 정보 없음</div></div>'

        items.append(
            f'<a class="news-item" href="{h["link"]}" target="_blank" rel="noopener noreferrer">'
            '<div class="news-main">'
            f'<div class="news-title"><span class="news-ticker">{display_name(h["ticker"])}</span>{h.get("title_kr", h["title"])}</div>'
            + (f'<div class="news-summary">{h["summary"]}</div>' if h.get("summary") else "")
            + "</div>"
            + price_html
            + "</a>"
        )
    return f'<div class="news-list">{"".join(items)}</div>'


def main() -> None:
    headlines = load_issues()
    ctx = load_sidebar_context()
    content = f'''<h1>📰 오늘의 이슈</h1>
    <div class="sub">{ctx["date_str"]} · 예측 대상 종목 관련 뉴스 {len(headlines)}건 · 현재가 대비 다음 거래일 예측가 표시</div>
    {render_list(headlines)}'''
    html = render_page("오늘의 이슈", "issues", content, EXTRA_CSS, **ctx)
    with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
        f.write(html)
    print(f"Wrote {OUTPUT_PATH}")


if __name__ == "__main__":
    main()
