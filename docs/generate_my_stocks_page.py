"""Build my_stocks.html: a client-side (localStorage) holdings tracker.

Since this is a static site (no login/backend), holdings are saved in the
browser's localStorage — private to that browser/device, no server needed.
Every time the page loads, it compares each holding's ticker against
today's AI prediction and shows a persistent red "매도 신호" banner for
any holding predicted DOWN. There is no push-notification channel on a
static GitHub Pages site, so the alert is an on-page banner shown on
every visit rather than a background/email/SMS push.
"""
import json
import os

from analyzer import load_data, calculate_sma
from chart import naive_predicted_price
from common import load_sidebar_context, render_page
from predict_universe import TICKERS as TICKER_INFO

OUTPUT_PATH = os.path.join(os.path.dirname(__file__), "my_stocks.html")

EXTRA_CSS = """
  h1 { font-size: 24px; margin: 0 0 4px; }
  .sub { color: var(--muted); font-size: 13px; margin-bottom: 24px; line-height: 1.6; }
  .alert-banner {
    display: none; background: rgba(239,68,68,0.12); border: 1px solid var(--down);
    color: var(--down); border-radius: 12px; padding: 14px 18px; margin-bottom: 20px;
    font-size: 14px; font-weight: 700;
  }
  .add-form {
    display: flex; gap: 10px; flex-wrap: wrap; align-items: flex-end;
    background: var(--card); border: 1px solid var(--border); border-radius: 12px;
    padding: 16px; margin-bottom: 24px;
  }
  .add-form label { display: flex; flex-direction: column; font-size: 11px; color: var(--muted); gap: 4px; }
  .add-form select, .add-form input {
    background: #0e141b; border: 1px solid var(--border); color: var(--text);
    border-radius: 8px; padding: 8px 10px; font-size: 13px; font-family: inherit;
  }
  .add-form button {
    background: var(--accent); border: none; color: #fff; font-weight: 700;
    border-radius: 8px; padding: 9px 18px; font-size: 13px; cursor: pointer; font-family: inherit;
  }
  .holdings { display: flex; flex-direction: column; gap: 10px; }
  .holding-row {
    display: flex; justify-content: space-between; align-items: center; gap: 16px;
    background: var(--card); border: 1px solid var(--border); border-radius: 12px; padding: 14px 18px;
  }
  .holding-row.sell-signal { border-color: var(--down); background: rgba(239,68,68,0.06); }
  .holding-name { font-weight: 700; font-size: 15px; }
  .holding-meta { font-size: 12px; color: var(--muted); margin-top: 2px; }
  .holding-pl { text-align: right; }
  .holding-pl-pct { font-size: 16px; font-weight: 800; }
  .holding-decision { font-size: 11px; font-weight: 700; padding: 2px 8px; border-radius: 6px; margin-top: 4px; display: inline-block; }
  .holding-decision.up { background: rgba(34,197,94,0.15); color: var(--up); }
  .holding-decision.down { background: rgba(239,68,68,0.15); color: var(--down); }
  .remove-btn {
    background: none; border: 1px solid var(--border); color: var(--muted);
    border-radius: 6px; padding: 4px 10px; font-size: 11px; cursor: pointer; font-family: inherit;
  }
  .remove-btn:hover { border-color: var(--down); color: var(--down); }
  .pct-up { color: var(--up); }
  .pct-down { color: var(--down); }
  .empty { color: var(--muted); font-size: 14px; text-align: center; padding: 40px 0; }
"""


def safe_name(ticker: str) -> str:
    return ticker.replace(".", "_").lower()


def build_ticker_data() -> dict:
    """{ticker: {name, market, currency, latest, predicted, decision, reasoning}}
    for every ticker we track, so 내 주식 can look up any of them, not just
    today's top-10/top-10 screening picks."""
    universe_path = "data/predictions_universe.json"
    all_results = {}
    if os.path.exists(universe_path):
        with open(universe_path, encoding="utf-8") as f:
            universe = json.load(f)
        for item in universe.get("all") or (universe.get("up", []) + universe.get("down", [])):
            all_results[item["ticker"]] = item

    data = {}
    for ticker, (name, market, currency) in TICKER_INFO.items():
        result = all_results.get(ticker)
        latest = predicted = None
        for period in ("1y", "5y"):
            path = f"data/{safe_name(ticker)}_{period}.csv"
            if os.path.exists(path):
                close = calculate_sma(load_data(path))["Close"]
                latest = float(close.iloc[-1])
                predicted = naive_predicted_price(close)
                break
        data[ticker] = {
            "name": name, "market": market, "currency": currency,
            "latest": latest, "predicted": predicted,
            "decision": result["decision"] if result else None,
            "reasoning": result.get("reasoning", "") if result else "",
        }
    return data


def render_options() -> str:
    return "\n".join(
        f'<option value="{ticker}">{name} ({ticker})</option>'
        for ticker, (name, _, _) in sorted(TICKER_INFO.items(), key=lambda kv: kv[1][0])
    )


SCRIPT = """
<script>
(function() {
  const TICKER_DATA = __TICKER_DATA_JSON__;
  const STORAGE_KEY = "myStocksV1";

  function loadHoldings() {
    try { return JSON.parse(localStorage.getItem(STORAGE_KEY)) || []; }
    catch (e) { return []; }
  }
  function saveHoldings(list) {
    localStorage.setItem(STORAGE_KEY, JSON.stringify(list));
  }

  function render() {
    const holdings = loadHoldings();
    const container = document.getElementById("holdings-list");
    const banner = document.getElementById("alert-banner");

    if (holdings.length === 0) {
      container.innerHTML = '<div class="empty">아직 등록한 종목이 없습니다. 위에서 매수한 종목과 매수가를 추가해보세요.</div>';
      banner.style.display = "none";
      return;
    }

    const sellSignals = [];
    container.innerHTML = holdings.map((h, idx) => {
      const info = TICKER_DATA[h.ticker] || {};
      const currency = info.currency || "$";
      const current = info.latest;
      const plPct = current ? ((current - h.buyPrice) / h.buyPrice * 100) : null;
      const isDown = info.decision === "DOWN";
      if (isDown) sellSignals.push(info.name || h.ticker);

      const plHtml = plPct !== null
        ? `<div class="holding-pl-pct ${plPct >= 0 ? 'pct-up' : 'pct-down'}">${plPct >= 0 ? '+' : ''}${plPct.toFixed(2)}%</div>`
        : '<div class="holding-pl-pct">-</div>';
      const decisionHtml = info.decision
        ? `<span class="holding-decision ${info.decision === 'UP' ? 'up' : 'down'}">${info.decision === 'UP' ? '▲ 상승 예측' : '▼ 하락 예측 · 매도 검토'}</span>`
        : '<span class="holding-decision">예측 대기</span>';

      return `<div class="holding-row ${isDown ? 'sell-signal' : ''}">
        <div>
          <div class="holding-name">${info.name || h.ticker}</div>
          <div class="holding-meta">매수가 ${currency}${h.buyPrice.toLocaleString()} · 현재가 ${current ? currency + current.toLocaleString(undefined, {minimumFractionDigits:2, maximumFractionDigits:2}) : '조회 불가'}</div>
          <div class="holding-meta">${info.reasoning || ''}</div>
          ${decisionHtml}
        </div>
        <div class="holding-pl">
          ${plHtml}
          <button class="remove-btn" data-idx="${idx}">삭제</button>
        </div>
      </div>`;
    }).join("");

    container.querySelectorAll(".remove-btn").forEach(btn => {
      btn.addEventListener("click", () => {
        const list = loadHoldings();
        list.splice(parseInt(btn.dataset.idx, 10), 1);
        saveHoldings(list);
        render();
      });
    });

    if (sellSignals.length > 0) {
      banner.style.display = "block";
      banner.textContent = `⚠ 매도 신호: ${sellSignals.join(", ")} — 오늘 하락 예측되었습니다. 매도를 검토해보세요.`;
    } else {
      banner.style.display = "none";
    }
  }

  document.getElementById("add-form").addEventListener("submit", function(e) {
    e.preventDefault();
    const ticker = document.getElementById("ticker-select").value;
    const buyPrice = parseFloat(document.getElementById("buy-price").value);
    if (!ticker || !buyPrice || buyPrice <= 0) return;
    const list = loadHoldings();
    list.push({ ticker, buyPrice, addedAt: new Date().toISOString() });
    saveHoldings(list);
    document.getElementById("buy-price").value = "";
    render();
  });

  render();
})();
</script>
"""


def main() -> None:
    ticker_data = build_ticker_data()
    ctx = load_sidebar_context()

    content = f'''<h1>💼 내 주식</h1>
    <div class="sub">
      매수한 종목과 매수가를 등록하면, 오늘의 AI 예측과 비교해 하락 예측 시 매도 신호를 보여드립니다.<br>
      데이터는 이 브라우저에만 저장됩니다(로그인/서버 없음) — 다른 기기에서는 다시 등록해야 합니다.<br>
      정적 사이트 특성상 실시간 푸시 알림은 지원하지 않으며, 이 페이지를 열 때마다 최신 신호를 확인할 수 있습니다.
      추적 가능한 종목은 현재 스크리닝 대상 46개로 제한됩니다.
    </div>

    <div class="alert-banner" id="alert-banner"></div>

    <form class="add-form" id="add-form">
      <label>종목
        <select id="ticker-select">{render_options()}</select>
      </label>
      <label>매수가
        <input type="number" id="buy-price" step="0.01" min="0" placeholder="예: 262500" required>
      </label>
      <button type="submit">추가</button>
    </form>

    <div class="holdings" id="holdings-list"></div>
    {SCRIPT.replace("__TICKER_DATA_JSON__", json.dumps(ticker_data, ensure_ascii=False))}'''

    html = render_page("내 주식", "my_stocks", content, EXTRA_CSS, **ctx)
    with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
        f.write(html)
    print(f"Wrote {OUTPUT_PATH}")


if __name__ == "__main__":
    main()
