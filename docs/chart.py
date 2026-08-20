"""Render a simple inline SVG line chart from a pandas Close-price series."""
import pandas as pd


def line_chart_svg(close: pd.Series, color: str, width: int = 640, height: int = 220) -> str:
    values = close.dropna().tolist()
    if len(values) < 2:
        return '<div class="chart-empty">차트를 그릴 데이터가 부족합니다.</div>'

    pad = 16
    lo, hi = min(values), max(values)
    span = (hi - lo) or 1.0
    n = len(values)

    def x(i: int) -> float:
        return pad + (width - 2 * pad) * i / (n - 1)

    def y(v: float) -> float:
        return height - pad - (height - 2 * pad) * (v - lo) / span

    points = " ".join(f"{x(i):.1f},{y(v):.1f}" for i, v in enumerate(values))
    area_points = f"{x(0):.1f},{height - pad} " + points + f" {x(n - 1):.1f},{height - pad}"

    return f'''<svg viewBox="0 0 {width} {height}" class="price-chart" xmlns="http://www.w3.org/2000/svg">
  <polygon points="{area_points}" fill="{color}" opacity="0.12"></polygon>
  <polyline points="{points}" fill="none" stroke="{color}" stroke-width="2"></polyline>
</svg>'''
