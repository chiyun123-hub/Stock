"""Render data/today_issues.json into a full-page news list (issues.html),
linked from the sidebar's "오늘의 이슈" item.
"""
import json
import os
from datetime import date

BASE_DIR = os.path.dirname(__file__)
TEMPLATE_PATH = os.path.join(BASE_DIR, "issues_template.html")
OUTPUT_PATH = os.path.join(BASE_DIR, "issues.html")


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
    with open(TEMPLATE_PATH, encoding="utf-8") as f:
        template = f.read()

    replacements = {
        "{{DATE}}": date.today().isoformat(),
        "{{COUNT}}": str(len(headlines)),
        "{{NEWS_LIST}}": render_list(headlines),
    }
    for key, value in replacements.items():
        template = template.replace(key, value)

    with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
        f.write(template)
    print(f"Wrote {OUTPUT_PATH}")


if __name__ == "__main__":
    main()
