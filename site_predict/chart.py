"""Render an interactive SVG line chart (date x-axis, price y-axis, hover
tooltip) from a pandas Close-price series, plus an optional predicted-price
point for the next trading day.
"""
import json
import re

import pandas as pd


def _nice_ticks(lo: float, hi: float, count: int = 5) -> list[float]:
    step = (hi - lo) / max(count - 1, 1) or 1.0
    return [lo + step * i for i in range(count)]


def naive_predicted_price(close: pd.Series, lookback: int = 5) -> float:
    """Extrapolate next-day price from the average daily return over `lookback` days.

    This is a simple, transparent technical estimate (not the AI's UP/DOWN
    call) — shown on the chart as a reference point, not investment advice.
    """
    series = close.dropna()
    returns = series.pct_change().tail(lookback)
    avg_daily_return = float(returns.mean()) if len(returns) else 0.0
    return float(series.iloc[-1]) * (1 + avg_daily_return)


def interactive_chart_html(close: pd.Series, currency: str, color: str,
                            chart_id: str, predicted_price: float | None = None,
                            width: int = 680, height: int = 320) -> str:
    series = close.dropna()
    if len(series) < 2:
        return '<div class="chart-empty">차트를 그릴 데이터가 부족합니다.</div>'

    dates = [d.strftime("%Y-%m-%d") for d in series.index]
    values = series.tolist()
    n = len(values)

    has_pred = predicted_price is not None
    all_values = values + ([predicted_price] if has_pred else [])
    lo, hi = min(all_values), max(all_values)
    span = (hi - lo) or 1.0
    lo -= span * 0.05
    hi += span * 0.05
    span = hi - lo

    pad_l, pad_r, pad_t, pad_b = 64, 20, 16, 32
    inner_w = width - pad_l - pad_r
    inner_h = height - pad_t - pad_b
    total_points = n + (1 if has_pred else 0)
    last_i = total_points - 1

    def x(i: int) -> float:
        return pad_l + inner_w * i / last_i

    def y(v: float) -> float:
        return pad_t + inner_h - inner_h * (v - lo) / span

    points = " ".join(f"{x(i):.1f},{y(v):.1f}" for i, v in enumerate(values))

    # y-axis gridlines + labels
    y_ticks = _nice_ticks(lo, hi, 5)
    y_axis_svg = "\n".join(
        f'<line x1="{pad_l}" y1="{y(t):.1f}" x2="{width - pad_r}" y2="{y(t):.1f}" '
        f'stroke="#232b35" stroke-width="1"></line>'
        f'<text x="{pad_l - 8}" y="{y(t) + 4:.1f}" fill="#8b98a5" font-size="11" text-anchor="end">'
        f'{currency}{t:,.0f}</text>'
        for t in y_ticks
    )

    # x-axis: ~5 evenly spaced date labels (actual-data indices only)
    x_tick_idx = sorted(set(round(i) for i in [k * (n - 1) / 4 for k in range(5)]))
    x_axis_svg = "\n".join(
        f'<text x="{x(i):.1f}" y="{height - 8}" fill="#8b98a5" font-size="11" '
        f'text-anchor="middle">{dates[i]}</text>'
        for i in x_tick_idx
    )

    pred_svg = ""
    if has_pred:
        pred_x, pred_y = x(n), y(predicted_price)
        last_x, last_y = x(n - 1), y(values[-1])
        pred_svg = (
            f'<line x1="{last_x:.1f}" y1="{last_y:.1f}" x2="{pred_x:.1f}" y2="{pred_y:.1f}" '
            f'stroke="{color}" stroke-width="2" stroke-dasharray="4,4"></line>'
            f'<circle cx="{pred_x:.1f}" cy="{pred_y:.1f}" r="5" fill="{color}" '
            f'stroke="#0b0f14" stroke-width="2"></circle>'
            f'<text x="{pred_x:.1f}" y="{pred_y - 12:.1f}" fill="{color}" font-size="12" '
            f'font-weight="700" text-anchor="middle">예측 {currency}{predicted_price:,.2f}</text>'
        )

    # Data embedded for the hover handler (dates + prices, predicted point appended)
    chart_dates = dates + (["예측 (다음 거래일)"] if has_pred else [])
    chart_values = values + ([predicted_price] if has_pred else [])
    data_json = json.dumps({"dates": chart_dates, "values": chart_values, "currency": currency})
    safe_id = re.sub(r"[^a-zA-Z0-9_]", "_", chart_id)

    return f'''<div class="chart-container" id="chart-{safe_id}">
  <svg viewBox="0 0 {width} {height}" class="price-chart" data-width="{width}" data-height="{height}">
    {y_axis_svg}
    {x_axis_svg}
    <polyline points="{points}" fill="none" stroke="{color}" stroke-width="2"></polyline>
    {pred_svg}
    <line class="hover-line" x1="0" y1="{pad_t}" x2="0" y2="{height - pad_b}" stroke="#8b98a5" stroke-width="1" style="display:none"></line>
    <circle class="hover-dot" r="4" fill="{color}" stroke="#0b0f14" stroke-width="2" style="display:none"></circle>
    <rect class="hover-capture" x="{pad_l}" y="{pad_t}" width="{inner_w}" height="{inner_h}" fill="transparent"></rect>
  </svg>
  <div class="chart-tooltip" style="display:none"></div>
  <script type="application/json" class="chart-data">{data_json}</script>
</div>
<script>
(function() {{
  const root = document.getElementById("chart-{safe_id}");
  const svg = root.querySelector("svg");
  const capture = root.querySelector(".hover-capture");
  const hoverLine = root.querySelector(".hover-line");
  const hoverDot = root.querySelector(".hover-dot");
  const tooltip = root.querySelector(".chart-tooltip");
  const data = JSON.parse(root.querySelector(".chart-data").textContent);
  const padL = {pad_l}, padR = {pad_r}, padT = {pad_t}, padB = {pad_b};
  const W = {width}, H = {height};
  const lo = {lo}, hi = {hi};
  const lastI = {last_i};

  function priceToY(v) {{
    return padT + (H - padT - padB) - (H - padT - padB) * (v - lo) / (hi - lo);
  }}

  function handleMove(evt) {{
    const rect = svg.getBoundingClientRect();
    const scale = W / rect.width;
    const svgX = (evt.clientX - rect.left) * scale;
    const ratio = Math.min(Math.max((svgX - padL) / (W - padL - padR), 0), 1);
    const idx = Math.round(ratio * lastI);
    const clamped = Math.min(Math.max(idx, 0), data.values.length - 1);
    const px = padL + (W - padL - padR) * clamped / lastI;
    const py = priceToY(data.values[clamped]);

    hoverLine.setAttribute("x1", px);
    hoverLine.setAttribute("x2", px);
    hoverLine.style.display = "block";
    hoverDot.setAttribute("cx", px);
    hoverDot.setAttribute("cy", py);
    hoverDot.style.display = "block";

    tooltip.style.display = "block";
    tooltip.innerHTML = data.dates[clamped] + "<br><strong>" + data.currency +
      data.values[clamped].toLocaleString(undefined, {{minimumFractionDigits: 2, maximumFractionDigits: 2}}) + "</strong>";
    const wrapRect = root.getBoundingClientRect();
    const cursorX = evt.clientX - wrapRect.left;
    tooltip.style.left = Math.min(cursorX + 12, wrapRect.width - 130) + "px";
    tooltip.style.top = "8px";
  }}

  capture.addEventListener("mousemove", handleMove);
  capture.addEventListener("mouseleave", function() {{
    hoverLine.style.display = "none";
    hoverDot.style.display = "none";
    tooltip.style.display = "none";
  }});
}})();
</script>'''


def period_return(close: pd.Series, days: int) -> float | None:
    """% change over the last `days` trading rows (None if not enough history)."""
    series = close.dropna()
    if len(series) <= days:
        return None
    return float((series.iloc[-1] / series.iloc[-1 - days] - 1) * 100)
