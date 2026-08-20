"""Render data/accuracy.json (from check_accuracy.py) into accuracy.html."""
import json
import os

BASE_DIR = os.path.dirname(__file__)
TEMPLATE_PATH = os.path.join(BASE_DIR, "accuracy_template.html")
OUTPUT_PATH = os.path.join(BASE_DIR, "accuracy.html")


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
    with open(TEMPLATE_PATH, encoding="utf-8") as f:
        template = f.read()

    accuracy_pct = data.get("accuracy_pct")
    replacements = {
        "{{ACCURACY_PCT}}": f"{accuracy_pct}%" if accuracy_pct is not None else "집계 전",
        "{{CORRECT}}": str(data.get("correct", 0)),
        "{{TOTAL}}": str(data.get("total_evaluated", 0)),
        "{{PENDING}}": str(data.get("pending", 0)),
        "{{TABLE}}": render_table(data.get("rows", [])),
    }
    for key, value in replacements.items():
        template = template.replace(key, value)

    with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
        f.write(template)
    print(f"Wrote {OUTPUT_PATH}")


if __name__ == "__main__":
    main()
