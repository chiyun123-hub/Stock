"""Render data/prediction_today.json + trend stats into a static GUI homepage."""
import json
import os
from datetime import date

from analyzer import load_data, calculate_sma
from common import load_sidebar_context, render_page
from predict_universe import TICKERS as TICKER_INFO

OUTPUT_PATH = os.path.join(os.path.dirname(__file__), "index.html")

EXTRA_CSS = """
  .card {
    max-width: 420px; margin: 0 0 44px; background: var(--card); border: 1px solid var(--border);
    border-radius: 20px; padding: 32px; box-shadow: 0 20px 60px rgba(0,0,0,0.4);
  }
  .ticker-row { display: flex; justify-content: space-between; align-items: center; margin-bottom: 24px; }
  .ticker { font-size: 28px; font-weight: 700; letter-spacing: 0.5px; }
  .date { color: var(--muted); font-size: 13px; }
  .decision-badge {
    display: flex; align-items: center; justify-content: center; gap: 12px;
    padding: 28px 0; border-radius: 16px; margin-bottom: 24px; font-size: 40px; font-weight: 800;
  }
  .decision-badge.up   { background: rgba(34,197,94,0.12); color: var(--up); }
  .decision-badge.down { background: rgba(239,68,68,0.12); color: var(--down); }
  .reasoning {
    color: var(--text); font-size: 14px; line-height: 1.6; background: #0e141b;
    border: 1px solid var(--border); border-radius: 12px; padding: 14px 16px; margin-bottom: 24px;
  }
  .stats { display: grid; grid-template-columns: 1fr 1fr; gap: 12px; margin-bottom: 20px; }
  .stat { background: #0e141b; border: 1px solid var(--border); border-radius: 10px; padding: 12px 14px; }
  .stat-label { color: var(--muted); font-size: 11px; text-transform: uppercase; letter-spacing: 0.5px; }
  .stat-value { font-size: 16px; font-weight: 600; margin-top: 4px; }
  .disclaimer { font-size: 11px; color: var(--muted); text-align: center; line-height: 1.5; }
  .section-title { font-size: 20px; font-weight: 700; margin: 0 0 16px; }
  .prediction-table { margin-bottom: 40px; border: 1px solid var(--border); border-radius: 16px; padding: 20px; }
  .prediction-table.up   { border-color: rgba(34,197,94,0.3); }
  .prediction-table.down { border-color: rgba(239,68,68,0.3); }
  .table-title { display: flex; align-items: center; gap: 8px; font-size: 18px; font-weight: 800; margin-bottom: 16px; }
  .table-title.up   { color: var(--up); }
  .table-title.down { color: var(--down); }
  .market-groups { display: grid; grid-template-columns: 1fr 1fr; gap: 24px; }
  @media (max-width: 720px) { .market-groups { grid-template-columns: 1fr; } }
  .col-title { display: flex; align-items: center; gap: 8px; font-size: 14px; font-weight: 700; margin-bottom: 12px; padding: 0 4px; color: var(--muted); }
  .stock-row {
    display: flex; justify-content: space-between; align-items: flex-start; gap: 12px;
    background: var(--card); border: 1px solid var(--border); border-radius: 12px;
    padding: 12px 16px; margin-bottom: 10px; text-decoration: none; color: inherit;
    transition: border-color 0.15s, transform 0.15s;
  }
  .stock-row:hover { border-color: var(--accent); transform: translateY(-1px); }
  .stock-main { display: flex; flex-direction: column; gap: 4px; flex: 1; }
  .stock-ticker { font-weight: 700; font-size: 15px; }
  .stock-ticker .market-badge {
    font-size: 10px; font-weight: 700; color: var(--muted);
    border: 1px solid var(--border); border-radius: 4px; padding: 1px 5px; margin-left: 6px;
  }
  .stock-reason { font-size: 12px; color: var(--muted); line-height: 1.4; }
  .stock-price { font-size: 13px; font-weight: 600; color: var(--text); white-space: nowrap; }
  .rank { color: var(--muted); font-size: 12px; margin-right: 8px; }
"""


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


def safe_name(ticker: str) -> str:
    return ticker.replace(".", "_").lower()


def render_rows(items: list[dict]) -> str:
    if not items:
        return '<div class="stock-reason">데이터 없음</div>'
    rows = []
    for i, item in enumerate(items, 1):
        name = item.get("name") or item["ticker"]
        market = item.get("market", "US")
        currency = item.get("currency", "$")
        label = name
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


def render_content(prediction: dict, stats: dict, universe: dict) -> str:
    is_up = prediction["decision"] == "UP"
    ticker_href = f"stocks/{safe_name(prediction['ticker'])}.html"
    return f'''<div class="card">
      <div class="ticker-row">
        <a class="ticker" href="{ticker_href}" style="color:inherit;text-decoration:none;">{TICKER_INFO.get(prediction["ticker"], (prediction["ticker"],))[0]}</a>
        <div class="date">{prediction.get("date", date.today().isoformat())}</div>
      </div>
      <div class="decision-badge {"up" if is_up else "down"}">
        <span>{"▲" if is_up else "▼"}</span>
        <span>{prediction["decision"]}</span>
      </div>
      <div class="reasoning">{prediction.get("reasoning", "")}</div>
      <div class="stats">
        <div class="stat"><div class="stat-label">최근 종가</div><div class="stat-value">${stats['latest_close']:.2f}</div></div>
        <div class="stat"><div class="stat-label">20일 이동평균</div><div class="stat-value">${stats['sma_20']:.2f}</div></div>
        <div class="stat"><div class="stat-label">5일 변동률</div><div class="stat-value">{stats['change_5d']:+.2f}%</div></div>
        <div class="stat"><div class="stat-label">5년 범위</div><div class="stat-value">${stats['range_low']:.2f} - {stats['range_high']:.2f}</div></div>
      </div>
      <div class="disclaimer">이 예측은 AI가 과거 데이터를 기반으로 생성한 참고용 정보이며,<br>투자 자문이 아닙니다.</div>
    </div>

    <div class="section-title">국내·해외 대형주 스크리닝</div>

    <div class="prediction-table up">
      <div class="table-title up">▲ 상승 예상</div>
      <div class="market-groups">
        <div class="col">
          <div class="col-title">🇰🇷 국장 ({len(universe.get("up_kr", []))}/10)</div>
          {render_rows(universe.get("up_kr", []))}
        </div>
        <div class="col">
          <div class="col-title">🇺🇸 미장 ({len(universe.get("up_us", []))}/10)</div>
          {render_rows(universe.get("up_us", []))}
        </div>
      </div>
    </div>

    <div class="prediction-table down">
      <div class="table-title down">▼ 하락 예상</div>
      <div class="market-groups">
        <div class="col">
          <div class="col-title">🇰🇷 국장 ({len(universe.get("down_kr", []))}/10)</div>
          {render_rows(universe.get("down_kr", []))}
        </div>
        <div class="col">
          <div class="col-title">🇺🇸 미장 ({len(universe.get("down_us", []))}/10)</div>
          {render_rows(universe.get("down_us", []))}
        </div>
      </div>
    </div>

    <div class="disclaimer">스크리닝 결과는 20일 이동평균·최근 5일 수익률 기반 추세 판단이며, 투자 자문이 아닙니다.</div>'''


def main() -> None:
    prediction = load_prediction()
    stats = build_stats()
    universe = load_universe()
    ctx = load_sidebar_context()
    content = render_content(prediction, stats, universe)
    html = render_page("주식 예측 대시보드", "dashboard", content, EXTRA_CSS, **ctx)
    with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
        f.write(html)
    print(f"Wrote {OUTPUT_PATH}")


if __name__ == "__main__":
    main()
