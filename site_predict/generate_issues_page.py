"""Render data/today_issues.json into a full-page news list (issues.html),
linked from the sidebar's "오늘의 이슈" item.
"""
import json
import os

from common import load_sidebar_context, render_page

OUTPUT_PATH = os.path.join(os.path.dirname(__file__), "issues.html")

EXTRA_CSS = """
  h1 { font-size: 24px; margin: 0 0 4px; }
  .sub { color: var(--muted); font-size: 13px; margin-bottom: 28px; }
  .news-list { list-style: none; margin: 0; padding: 0; }
  .news-item { background: var(--card); border: 1px solid var(--border); border-radius: 12px; padding: 16px 18px; margin-bottom: 12px; }
  .news-item a { color: var(--text); text-decoration: none; display: block; }
  .news-item a:hover { color: var(--accent); }
  .news-ticker {
    display: inline-block; font-size: 11px; font-weight: 700; color: var(--accent);
    border: 1px solid var(--accent); border-radius: 4px; padding: 2px 6px; margin-right: 8px;
  }
  .news-title { font-size: 14px; line-height: 1.5; }
  .empty { color: var(--muted); font-size: 14px; text-align: center; padding: 60px 0; }
"""


def load_issues(path: str = "data/today_issues.json") -> list[dict]:
    if not os.path.exists(path):
        return []
    with open(path, encoding="utf-8") as f:
        return json.load(f).get("headlines", [])


def render_list(headlines: list[dict]) -> str:
    if not headlines:
        return '<div class="empty">지금은 표시할 뉴스가 없습니다. 잠시 후 다시 시도해주세요.</div>'
    items = "\n".join(
        '<li class="news-item"><a href="{link}" target="_blank" rel="noopener noreferrer">'
        '<span class="news-ticker">{ticker}</span>'
        '<span class="news-title">{title}</span></a></li>'.format(
            link=h["link"], ticker=h["ticker"], title=h.get("title_kr", h["title"])
        )
        for h in headlines
    )
    return f'<ul class="news-list">{items}</ul>'


def main() -> None:
    headlines = load_issues()
    ctx = load_sidebar_context()
    content = f'''<h1>📰 오늘의 이슈</h1>
    <div class="sub">{ctx["date_str"]} · 예측 대상 종목 관련 뉴스 {len(headlines)}건</div>
    {render_list(headlines)}'''
    html = render_page("오늘의 이슈", "issues", content, EXTRA_CSS, **ctx)
    with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
        f.write(html)
    print(f"Wrote {OUTPUT_PATH}")


if __name__ == "__main__":
    main()
