"""Render an interactive SVG line chart (date x-axis, price y-axis, hover
tooltip, period-range buttons) from a pandas Close-price series, plus an
optional predicted-price point for the next trading day.
"""
import json
import re

import pandas as pd

RANGE_OPTIONS = [
    ("1일", 2),
    ("3일", 3),
    ("1주", 5),
    ("1개월", 21),
    ("전체", None),
]


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
    safe_id = re.sub(r"[^a-zA-Z0-9_]", "_", chart_id)

    pad_l, pad_r, pad_t, pad_b = 64, 20, 16, 32
    data_json = json.dumps({
        "dates": dates,
        "values": values,
        "currency": currency,
        "predicted": predicted_price,
        "color": color,
        "width": width,
        "height": height,
        "padL": pad_l, "padR": pad_r, "padT": pad_t, "padB": pad_b,
    })

    range_buttons = "\n".join(
        f'<button type="button" class="range-btn{" active" if label == "전체" else ""}" '
        f'data-days="{days if days is not None else ""}">{label}</button>'
        for label, days in RANGE_OPTIONS
    )

    return f'''<div class="chart-container" id="chart-{safe_id}">
  <div class="range-buttons">{range_buttons}</div>
  <svg viewBox="0 0 {width} {height}" class="price-chart">
    <g class="y-axis"></g>
    <g class="x-axis"></g>
    <polyline class="price-line" points="" fill="none" stroke="{color}" stroke-width="2"></polyline>
    <g class="pred-marker"></g>
    <line class="hover-line" x1="0" y1="{pad_t}" x2="0" y2="{height - pad_b}" stroke="#8b98a5" stroke-width="1" style="display:none"></line>
    <circle class="hover-dot" r="4" fill="{color}" stroke="#0b0f14" stroke-width="2" style="display:none"></circle>
    <rect class="hover-capture" x="{pad_l}" y="{pad_t}" width="{width - pad_l - pad_r}" height="{height - pad_t - pad_b}" fill="transparent"></rect>
  </svg>
  <div class="chart-tooltip" style="display:none"></div>
  <script type="application/json" class="chart-data">{data_json}</script>
</div>
<script>
(function() {{
  const root = document.getElementById("chart-{safe_id}");
  const svg = root.querySelector("svg");
  const yAxis = root.querySelector(".y-axis");
  const xAxis = root.querySelector(".x-axis");
  const line = root.querySelector(".price-line");
  const predGroup = root.querySelector(".pred-marker");
  const capture = root.querySelector(".hover-capture");
  const hoverLine = root.querySelector(".hover-line");
  const hoverDot = root.querySelector(".hover-dot");
  const tooltip = root.querySelector(".chart-tooltip");
  const full = JSON.parse(root.querySelector(".chart-data").textContent);
  const {{ padL, padR, padT, padB, width: W, height: H, color }} = full;
  const innerW = W - padL - padR, innerH = H - padT - padB;

  let state = {{ dates: [], values: [], lo: 0, hi: 1, lastI: 1 }};

  function niceTicks(lo, hi, count) {{
    const step = (hi - lo) / Math.max(count - 1, 1) || 1;
    return Array.from({{length: count}}, (_, i) => lo + step * i);
  }}

  function svgEl(tag, attrs) {{
    const el = document.createElementNS("http://www.w3.org/2000/svg", tag);
    for (const k in attrs) el.setAttribute(k, attrs[k]);
    return el;
  }}

  function render(days) {{
    const n = full.values.length;
    const sliceStart = days ? Math.max(n - days, 0) : 0;
    const dates = full.dates.slice(sliceStart);
    const values = full.values.slice(sliceStart);
    const hasPred = full.predicted !== null && full.predicted !== undefined;
    const allValues = hasPred ? values.concat([full.predicted]) : values;
    let lo = Math.min(...allValues), hi = Math.max(...allValues);
    const span0 = (hi - lo) || 1;
    lo -= span0 * 0.05; hi += span0 * 0.05;
    const span = hi - lo;
    const lastI = values.length - 1 + (hasPred ? 1 : 0);

    state = {{ dates, values, lo, hi, lastI, hasPred, predicted: full.predicted }};

    const x = i => padL + innerW * i / Math.max(lastI, 1);
    const y = v => padT + innerH - innerH * (v - lo) / span;

    line.setAttribute("points", values.map((v, i) => x(i) + "," + y(v)).join(" "));

    yAxis.innerHTML = "";
    niceTicks(lo, hi, 5).forEach(t => {{
      yAxis.appendChild(svgEl("line", {{x1: padL, y1: y(t), x2: W - padR, y2: y(t), stroke: "#232b35", "stroke-width": 1}}));
      const label = svgEl("text", {{x: padL - 8, y: y(t) + 4, fill: "#8b98a5", "font-size": 11, "text-anchor": "end"}});
      label.textContent = full.currency + Math.round(t).toLocaleString();
      yAxis.appendChild(label);
    }});

    xAxis.innerHTML = "";
    const tickCount = Math.min(5, dates.length);
    const idxs = new Set();
    for (let k = 0; k < tickCount; k++) idxs.add(Math.round(k * (dates.length - 1) / Math.max(tickCount - 1, 1)));
    [...idxs].forEach(i => {{
      const label = svgEl("text", {{x: x(i), y: H - 8, fill: "#8b98a5", "font-size": 11, "text-anchor": "middle"}});
      label.textContent = dates[i];
      xAxis.appendChild(label);
    }});

    predGroup.innerHTML = "";
    if (hasPred) {{
      const lastX = x(values.length - 1), lastY = y(values[values.length - 1]);
      const predX = x(values.length), predY = y(full.predicted);
      predGroup.appendChild(svgEl("line", {{x1: lastX, y1: lastY, x2: predX, y2: predY, stroke: color, "stroke-width": 2, "stroke-dasharray": "4,4"}}));
      predGroup.appendChild(svgEl("circle", {{cx: predX, cy: predY, r: 5, fill: color, stroke: "#0b0f14", "stroke-width": 2}}));
      const label = svgEl("text", {{x: predX, y: predY - 12, fill: color, "font-size": 12, "font-weight": 700, "text-anchor": "middle"}});
      label.textContent = "예측 " + full.currency + full.predicted.toLocaleString(undefined, {{minimumFractionDigits: 2, maximumFractionDigits: 2}});
      predGroup.appendChild(label);
    }}
  }}

  function handleMove(evt) {{
    const rect = svg.getBoundingClientRect();
    const scale = W / rect.width;
    const svgX = (evt.clientX - rect.left) * scale;
    const ratio = Math.min(Math.max((svgX - padL) / innerW, 0), 1);
    const idx = Math.round(ratio * state.lastI);
    const displayValues = state.hasPred ? state.values.concat([state.predicted]) : state.values;
    const displayDates = state.hasPred ? state.dates.concat(["예측 (다음 거래일)"]) : state.dates;
    const clamped = Math.min(Math.max(idx, 0), displayValues.length - 1);
    const px = padL + innerW * clamped / Math.max(state.lastI, 1);
    const py = padT + innerH - innerH * (displayValues[clamped] - state.lo) / (state.hi - state.lo);

    hoverLine.setAttribute("x1", px); hoverLine.setAttribute("x2", px);
    hoverLine.style.display = "block";
    hoverDot.setAttribute("cx", px); hoverDot.setAttribute("cy", py);
    hoverDot.style.display = "block";

    tooltip.style.display = "block";
    tooltip.innerHTML = displayDates[clamped] + "<br><strong>" + full.currency +
      displayValues[clamped].toLocaleString(undefined, {{minimumFractionDigits: 2, maximumFractionDigits: 2}}) + "</strong>";
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

  root.querySelectorAll(".range-btn").forEach(btn => {{
    btn.addEventListener("click", function() {{
      root.querySelectorAll(".range-btn").forEach(b => b.classList.remove("active"));
      btn.classList.add("active");
      const days = btn.dataset.days ? parseInt(btn.dataset.days, 10) : null;
      render(days);
    }});
  }});

  render(null);
}})();
</script>'''


def period_return(close: pd.Series, days: int) -> float | None:
    """% change over the last `days` trading rows (None if not enough history)."""
    series = close.dropna()
    if len(series) <= days:
        return None
    return float((series.iloc[-1] / series.iloc[-1 - days] - 1) * 100)
