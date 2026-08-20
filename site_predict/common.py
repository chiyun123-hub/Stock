"""Shared sidebar + page-shell so every page (dashboard, issues, accuracy,
stock detail, predictions-by-date) renders the same persistent sidebar."""

BASE_CSS = """
  :root {
    --bg: #0b0f14; --card: #131a22; --border: #232b35;
    --text: #e8edf2; --muted: #8b98a5; --up: #22c55e; --down: #ef4444; --accent: #3b82f6;
  }
  * { box-sizing: border-box; }
  body {
    margin: 0; min-height: 100vh; background: var(--bg); color: var(--text);
    font-family: -apple-system, "Segoe UI", "Malgun Gothic", Pretendard, sans-serif;
  }
  .layout { display: flex; min-height: 100vh; }

  /* Sidebar */
  .sidebar { width: 280px; flex-shrink: 0; background: #0e141b; border-right: 1px solid var(--border); padding: 28px 20px; }
  .brand { font-size: 18px; font-weight: 800; margin-bottom: 4px; }
  .brand-sub { font-size: 12px; color: var(--muted); margin-bottom: 28px; }
  .sidebar-title { font-size: 13px; font-weight: 700; color: var(--muted); text-transform: uppercase; letter-spacing: 0.5px; margin-bottom: 12px; }
  .sidebar-nav { display: flex; flex-direction: column; gap: 8px; margin-bottom: 28px; }
  .sidebar-nav-item {
    display: flex; align-items: center; justify-content: space-between;
    background: var(--card); border: 1px solid var(--border); border-radius: 10px;
    padding: 10px 14px; font-size: 13px; font-weight: 600; color: var(--text);
    text-decoration: none; transition: border-color 0.15s;
  }
  .sidebar-nav-item:hover { border-color: var(--accent); }
  .sidebar-nav-item.active { border-color: var(--accent); background: #16202e; }
  .nav-badge { font-size: 11px; font-weight: 700; color: var(--muted); background: #0e141b; border-radius: 10px; padding: 2px 8px; }
  .sidebar-stat { background: var(--card); border: 1px solid var(--border); border-radius: 10px; padding: 12px 14px; margin-bottom: 10px; }
  .sidebar-stat-label { font-size: 11px; color: var(--muted); }
  .sidebar-stat-value { font-size: 15px; font-weight: 700; margin-top: 2px; }
  .sidebar-back { display: inline-block; margin-top: 8px; color: var(--muted); text-decoration: none; font-size: 13px; }
  .sidebar-back:hover { color: var(--text); }

  /* Main */
  .main { flex: 1; display: flex; justify-content: center; padding: 40px 32px 60px; }
  .main-inner { width: 100%; max-width: 900px; }

  @media (max-width: 720px) {
    .layout { flex-direction: column; }
    .sidebar { width: 100%; }
  }
"""


def render_sidebar(active: str, date_str: str, up_count: int, down_count: int,
                    issue_count: int, accuracy_badge: str, prefix: str = "") -> str:
    def cls(name: str) -> str:
        return "sidebar-nav-item active" if name == active else "sidebar-nav-item"

    return f'''<div class="sidebar">
    <div class="brand">📈 주식 예측 대시보드</div>
    <div class="brand-sub">{date_str} 기준 · AI 스크리닝</div>

    <div class="sidebar-title">메뉴</div>
    <nav class="sidebar-nav">
      <a class="{cls('issues')}" href="{prefix}issues.html">
        <span>📰 오늘의 이슈</span><span class="nav-badge">{issue_count}</span>
      </a>
      <a class="{cls('accuracy')}" href="{prefix}accuracy.html">
        <span>🎯 예측 정확도</span><span class="nav-badge">{accuracy_badge}</span>
      </a>
      <a class="{cls('predictions')}" href="{prefix}predictions.html">
        <span>📊 종목 예측</span>
      </a>
      <a class="{cls('my_stocks')}" href="{prefix}my_stocks.html">
        <span>💼 내 주식</span>
      </a>
    </nav>

    <div class="sidebar-title">요약</div>
    <div class="sidebar-stat">
      <div class="sidebar-stat-label">상승 예상</div>
      <div class="sidebar-stat-value" style="color:var(--up)">{up_count}종목</div>
    </div>
    <div class="sidebar-stat">
      <div class="sidebar-stat-label">하락 예상</div>
      <div class="sidebar-stat-value" style="color:var(--down)">{down_count}종목</div>
    </div>
    <a class="sidebar-back" href="{prefix}index.html">← 대시보드</a>
  </div>'''


def render_page(title: str, active: str, content_html: str, extra_css: str,
                 date_str: str, up_count: int, down_count: int, issue_count: int,
                 accuracy_badge: str, prefix: str = "") -> str:
    sidebar = render_sidebar(active, date_str, up_count, down_count, issue_count, accuracy_badge, prefix)
    return f'''<!DOCTYPE html>
<html lang="ko">
<head>
<meta charset="UTF-8">
<title>{title}</title>
<style>
{BASE_CSS}
{extra_css}
</style>
</head>
<body>
<div class="layout">
  {sidebar}
  <div class="main"><div class="main-inner">
    {content_html}
  </div></div>
</div>
</body>
</html>
'''


def load_sidebar_context(base_dir: str = ".") -> dict:
    """Common counts every page's sidebar needs (up/down/issues/accuracy)."""
    import json
    import os
    from datetime import date

    def read(path):
        full = os.path.join(base_dir, path)
        if not os.path.exists(full):
            return None
        with open(full, encoding="utf-8") as f:
            return json.load(f)

    universe = read("data/predictions_universe.json") or {"up": [], "down": []}
    issues = read("data/today_issues.json") or {"headlines": []}
    accuracy = read("data/accuracy.json") or {}

    return {
        "date_str": date.today().isoformat(),
        "up_count": len(universe.get("up", [])),
        "down_count": len(universe.get("down", [])),
        "issue_count": len(issues.get("headlines", [])),
        "accuracy_badge": f"{accuracy['accuracy_pct']}%" if accuracy.get("accuracy_pct") is not None else "집계 전",
    }
