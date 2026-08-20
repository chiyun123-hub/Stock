"""Build the "종목 예측" section: predictions.html lists every date we've
predicted, and predictions_{date}.html shows that date's tickers with
predicted direction + resolved accuracy (적중/오답/대기).
"""
import os
from collections import defaultdict

os.environ.setdefault("SSL_CERT_FILE", os.path.join(os.path.dirname(__file__), "..", ".certs", "combined_ca_bundle.pem"))
os.environ.setdefault("REQUESTS_CA_BUNDLE", os.environ["SSL_CERT_FILE"])

from dotenv import load_dotenv
from supabase import create_client

from check_accuracy import actual_direction
from common import load_sidebar_context, render_page

BASE_DIR = os.path.dirname(__file__)
LIST_OUTPUT = os.path.join(BASE_DIR, "predictions.html")
DETAIL_DIR = BASE_DIR  # predictions_{date}.html sits alongside index.html

LIST_CSS = """
  h1 { font-size: 24px; margin: 0 0 4px; }
  .sub { color: var(--muted); font-size: 13px; margin-bottom: 28px; }
  .date-list { list-style: none; margin: 0; padding: 0; }
  .date-item {
    display: flex; justify-content: space-between; align-items: center;
    background: var(--card); border: 1px solid var(--border); border-radius: 12px;
    padding: 16px 20px; margin-bottom: 12px; text-decoration: none; color: var(--text);
    transition: border-color 0.15s;
  }
  .date-item:hover { border-color: var(--accent); }
  .date-main { font-size: 15px; font-weight: 700; }
  .date-sub { font-size: 12px; color: var(--muted); margin-top: 2px; }
  .date-accuracy { font-size: 18px; font-weight: 800; color: var(--accent); }
  .date-accuracy.pending { color: var(--muted); font-size: 13px; font-weight: 600; }
  .empty { color: var(--muted); font-size: 14px; text-align: center; padding: 60px 0; }
"""

DETAIL_CSS = """
  h1 { font-size: 24px; margin: 0 0 4px; }
  .sub { color: var(--muted); font-size: 13px; margin-bottom: 28px; }
  table { width: 100%; border-collapse: collapse; font-size: 13px; }
  th, td { text-align: left; padding: 10px 12px; border-bottom: 1px solid var(--border); }
  th { color: var(--muted); font-weight: 600; font-size: 11px; text-transform: uppercase; }
  td a { color: var(--text); font-weight: 700; text-decoration: none; }
  td a:hover { color: var(--accent); }
  .badge { display: inline-block; padding: 2px 8px; border-radius: 6px; font-weight: 700; font-size: 11px; }
  .badge.up { background: rgba(34,197,94,0.15); color: var(--up); }
  .badge.down { background: rgba(239,68,68,0.15); color: var(--down); }
  .badge.pending { background: rgba(139,152,165,0.15); color: var(--muted); }
  .result-ok { color: var(--up); font-weight: 700; }
  .result-no { color: var(--down); font-weight: 700; }
  .result-pending { color: var(--muted); }
  .reason-cell { color: var(--muted); font-size: 12px; max-width: 320px; }
  .table-wrap { overflow-x: auto; }
"""


def safe_name(ticker: str) -> str:
    return ticker.replace(".", "_").lower()


def fetch_all_predictions() -> list[dict]:
    load_dotenv()
    client = create_client(os.getenv("SUPABASE_URL"), os.getenv("SUPABASE_KEY"))
    rows = client.table("predictions").select("date,ticker,prediction,reason").order("date", desc=True).execute().data
    return rows


def evaluate(rows: list[dict]) -> list[dict]:
    evaluated = []
    for row in rows:
        actual, pct = actual_direction(row["ticker"], row["date"])
        status = "pending"
        correct = None
        if actual is not None:
            correct = row["prediction"] == actual
            status = "correct" if correct else "wrong"
        evaluated.append({**row, "actual": actual, "change_pct": pct, "status": status, "correct": correct})
    return evaluated


def render_list_page(by_date: dict, ctx: dict) -> None:
    if not by_date:
        body = '<div class="empty">아직 저장된 예측 기록이 없습니다.</div>'
    else:
        items = []
        for d in sorted(by_date, reverse=True):
            rows = by_date[d]
            resolved = [r for r in rows if r["status"] != "pending"]
            correct = sum(1 for r in resolved if r["correct"])
            acc_html = (
                f'<div class="date-accuracy">{round(correct / len(resolved) * 100)}%</div>'
                if resolved else '<div class="date-accuracy pending">검증 대기</div>'
            )
            items.append(
                f'<a class="date-item" href="predictions_{d}.html">'
                f'<div><div class="date-main">{d}</div>'
                f'<div class="date-sub">{len(rows)}개 종목 예측 · {len(resolved)}개 검증 완료</div></div>'
                f'{acc_html}</a>'
            )
        body = f'<ul class="date-list">{"".join(items)}</ul>'

    content = f'''<h1>📊 종목 예측</h1>
    <div class="sub">날짜를 선택하면 그날 예측한 종목과 정확도를 볼 수 있습니다.</div>
    {body}'''
    html = render_page("종목 예측", "predictions", content, LIST_CSS, **ctx)
    with open(LIST_OUTPUT, "w", encoding="utf-8") as f:
        f.write(html)


def render_detail_page(d: str, rows: list[dict], ctx: dict) -> None:
    badge = lambda v: f'<span class="badge {"up" if v == "UP" else "down"}">{v}</span>' if v else '<span class="badge pending">-</span>'
    body_rows = []
    for r in sorted(rows, key=lambda x: x["ticker"]):
        if r["status"] == "pending":
            result = '<span class="result-pending">검증 대기</span>'
            actual_badge = badge(None)
            pct_text = "-"
        else:
            result = '<span class="result-ok">적중</span>' if r["correct"] else '<span class="result-no">오답</span>'
            actual_badge = badge(r["actual"])
            pct_text = f'{r["change_pct"]:+.2f}%'
        stock_link = f"stocks/{safe_name(r['ticker'])}.html"
        body_rows.append(
            f'<tr><td><a href="{stock_link}">{r["ticker"]}</a></td>'
            f'<td>{badge(r["prediction"])}</td><td>{actual_badge}</td>'
            f'<td>{pct_text}</td><td>{result}</td>'
            f'<td class="reason-cell">{r.get("reason") or ""}</td></tr>'
        )
    table = (
        '<div class="table-wrap"><table><thead><tr>'
        "<th>종목</th><th>예측</th><th>실제</th><th>등락률</th><th>결과</th><th>근거</th>"
        "</tr></thead><tbody>" + "\n".join(body_rows) + "</tbody></table></div>"
    )
    content = f'''<h1>📊 {d} 예측</h1>
    <div class="sub">이날 예측한 {len(rows)}개 종목의 방향과 실제 결과입니다.</div>
    {table}'''
    html = render_page(f"{d} 종목 예측", "predictions", content, DETAIL_CSS, **ctx)
    with open(os.path.join(DETAIL_DIR, f"predictions_{d}.html"), "w", encoding="utf-8") as f:
        f.write(html)


def main() -> None:
    rows = evaluate(fetch_all_predictions())
    by_date = defaultdict(list)
    for r in rows:
        by_date[r["date"]].append(r)

    ctx = load_sidebar_context()
    render_list_page(by_date, ctx)
    for d, day_rows in by_date.items():
        render_detail_page(d, day_rows, ctx)

    print(f"Wrote predictions.html + {len(by_date)} date detail pages")


if __name__ == "__main__":
    main()
