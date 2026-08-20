"""Render data/accuracy.json (from check_accuracy.py) into accuracy.html."""
import json
import os

from common import load_sidebar_context, render_page

OUTPUT_PATH = os.path.join(os.path.dirname(__file__), "accuracy.html")

EXTRA_CSS = """
  h1 { font-size: 24px; margin: 0 0 4px; }
  .sub { color: var(--muted); font-size: 13px; margin-bottom: 28px; }
  .summary { display: grid; grid-template-columns: repeat(3, 1fr); gap: 12px; margin-bottom: 28px; }
  .summary-card { background: var(--card); border: 1px solid var(--border); border-radius: 14px; padding: 20px; text-align: center; }
  .summary-label { font-size: 12px; color: var(--muted); margin-bottom: 6px; }
  .summary-value { font-size: 28px; font-weight: 800; }
  .summary-value.accent { color: var(--accent); }
  table { width: 100%; border-collapse: collapse; font-size: 13px; }
  th, td { text-align: left; padding: 10px 12px; border-bottom: 1px solid var(--border); }
  th { color: var(--muted); font-weight: 600; font-size: 11px; text-transform: uppercase; }
  .badge { display: inline-block; padding: 2px 8px; border-radius: 6px; font-weight: 700; font-size: 11px; }
  .badge.up { background: rgba(34,197,94,0.15); color: var(--up); }
  .badge.down { background: rgba(239,68,68,0.15); color: var(--down); }
  .result-ok { color: var(--up); font-weight: 700; }
  .result-no { color: var(--down); font-weight: 700; }
  .empty { color: var(--muted); font-size: 14px; text-align: center; padding: 60px 0; }
  .note { font-size: 12px; color: var(--muted); margin-top: 20px; line-height: 1.6; }
  .table-wrap { overflow-x: auto; }
"""


def load_accuracy(path: str = "data/accuracy.json") -> dict:
    if not os.path.exists(path):
        return {}
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def render_table(rows: list[dict]) -> str:
    if not rows:
        return '<div class="empty">아직 검증 가능한 예측이 없습니다. 다음 거래일 데이터가 쌓이면 표시됩니다.</div>'
    body = []
    for r in sorted(rows, key=lambda x: x["date"], reverse=True):
        badge = lambda v: f'<span class="badge {"up" if v == "UP" else "down"}">{v}</span>'
        result = '<span class="result-ok">적중</span>' if r["correct"] else '<span class="result-no">오답</span>'
        body.append(
            f'<tr><td>{r["date"]}</td><td>{r["ticker"]}</td>'
            f'<td>{badge(r["predicted"])}</td><td>{badge(r["actual"])}</td>'
            f'<td>{r["change_pct"]:+.2f}%</td><td>{result}</td></tr>'
        )
    return (
        '<div class="table-wrap"><table><thead><tr>'
        "<th>날짜</th><th>종목</th><th>예측</th><th>실제</th><th>등락률</th><th>결과</th>"
        "</tr></thead><tbody>" + "\n".join(body) + "</tbody></table></div>"
    )


def main() -> None:
    data = load_accuracy()
    ctx = load_sidebar_context()
    accuracy_pct = data.get("accuracy_pct")
    content = f'''<h1>🎯 예측 정확도</h1>
    <div class="sub">AI가 UP/DOWN으로 예측한 다음 거래일, 실제 주가가 그 방향으로 움직였는지 검증합니다.</div>

    <div class="summary">
      <div class="summary-card">
        <div class="summary-label">전체 정확도</div>
        <div class="summary-value accent">{f"{accuracy_pct}%" if accuracy_pct is not None else "집계 전"}</div>
      </div>
      <div class="summary-card">
        <div class="summary-label">적중 / 검증 완료</div>
        <div class="summary-value">{data.get("correct", 0)} / {data.get("total_evaluated", 0)}</div>
      </div>
      <div class="summary-card">
        <div class="summary-label">검증 대기 (다음 거래일 미확정)</div>
        <div class="summary-value">{data.get("pending", 0)}</div>
      </div>
    </div>

    {render_table(data.get("rows", []))}

    <div class="note">
      정확도는 예측일 종가 대비 다음 거래일 종가의 실제 등락 방향과 AI의 UP/DOWN 판단을 비교해 계산합니다.
      다음 거래일 데이터가 아직 수집되지 않은 예측은 "검증 대기"로 분류되며 정확도 계산에서 제외됩니다.
      이 페이지는 투자 자문이 아니라 예측 시스템 자체의 성능 추적용입니다.
    </div>'''
    html = render_page("예측 정확도", "accuracy", content, EXTRA_CSS, **ctx)
    with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
        f.write(html)
    print(f"Wrote {OUTPUT_PATH}")


if __name__ == "__main__":
    main()
