"""Render an inline SVG line chart (with axis labels + % change annotations)
from a pandas Close-price series and its DatetimeIndex.
"""
import pandas as pd


def line_chart_svg(close: pd.Series, color: str, currency: str = "$",
                    width: int = 640, height: int = 280) -> str:
    series = close.dropna()
    values = series.tolist()
    dates = series.index
    if len(values) < 2:
        return '<div class="chart-empty">차트를 그릴 데이터가 부족합니다.</div>'

    pad_l, pad_r, pad_t, pad_b = 16, 16, 36, 28
    chart_h = height - pad_t - pad_b
    lo, hi = min(values), max(values)
    span = (hi - lo) or 1.0
    n = len(values)

    def x(i: int) -> float:
        return pad_l + (width - pad_l - pad_r) * i / (n - 1)

    def y(v: float) -> float:
        return pad_t + chart_h - chart_h * (v - lo) / span

    points = " ".join(f"{x(i):.1f},{y(v):.1f}" for i, v in enumerate(values))
    area_points = f"{x(0):.1f},{pad_t + chart_h} " + points + f" {x(n - 1):.1f},{pad_t + chart_h}"

    start_price, end_price = values[0], values[-1]
    total_pct = (end_price / start_price - 1) * 100 if start_price else 0.0
    pct_sign = "+" if total_pct >= 0 else ""
    start_label = f"{dates[0].strftime('%Y-%m-%d')}  {currency}{start_price:,.2f}"
    end_label = f"{dates[-1].strftime('%Y-%m-%d')}  {currency}{end_price:,.2f}"

    return f'''<svg viewBox="0 0 {width} {height}" class="price-chart" xmlns="http://www.w3.org/2000/svg">
  <text x="{pad_l}" y="20" fill="#8b98a5" font-size="12">{start_label}</text>
  <text x="{width - pad_r}" y="20" fill="{color}" font-size="14" font-weight="700" text-anchor="end">{pct_sign}{total_pct:.2f}%</text>
  <polygon points="{area_points}" fill="{color}" opacity="0.12"></polygon>
  <polyline points="{points}" fill="none" stroke="{color}" stroke-width="2"></polyline>
  <circle cx="{x(0):.1f}" cy="{y(start_price):.1f}" r="3" fill="{color}"></circle>
  <circle cx="{x(n - 1):.1f}" cy="{y(end_price):.1f}" r="3" fill="{color}"></circle>
  <text x="{width - pad_r}" y="{height - 8}" fill="#8b98a5" font-size="12" text-anchor="end">{end_label}</text>
  <text x="{pad_l}" y="{height - 8}" fill="#8b98a5" font-size="12">최고 {currency}{hi:,.2f} · 최저 {currency}{lo:,.2f}</text>
</svg>'''


def period_return(close: pd.Series, days: int) -> float | None:
    """% change over the last `days` trading rows (None if not enough history)."""
    series = close.dropna()
    if len(series) <= days:
        return None
    return float((series.iloc[-1] / series.iloc[-1 - days] - 1) * 100)
