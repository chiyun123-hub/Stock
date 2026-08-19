"""TDD tests for predict.py. All network/API calls are mocked."""
import json
from unittest.mock import patch, MagicMock

import pandas as pd
import pytest

from predict import fetch_news, summarize_trend, save_prediction

SAMPLE_RSS = """<?xml version="1.0"?>
<rss><channel>
<item><title>Apple hits record high</title></item>
<item><title>Analysts raise AAPL price target</title></item>
</channel></rss>"""


@patch("predict.requests.get")
def test_fetch_news_returns_list_of_headlines(mock_get: MagicMock) -> None:
    mock_get.return_value.text = SAMPLE_RSS
    mock_get.return_value.raise_for_status = lambda: None

    headlines = fetch_news("AAPL")

    assert isinstance(headlines, list)
    assert len(headlines) == 2
    assert all(isinstance(h, str) for h in headlines)
    assert "Apple hits record high" in headlines


def test_summarize_trend_condenses_to_short_summary() -> None:
    dates = pd.date_range("2021-01-01", periods=1300, freq="D")
    df = pd.DataFrame({"Close": [100 + i * 0.01 for i in range(1300)]}, index=dates)

    summary = summarize_trend(df)

    assert isinstance(summary, str)
    lines = [line for line in summary.strip().splitlines() if line.strip()]
    assert 1 <= len(lines) <= 10


def test_save_prediction_writes_valid_json(tmp_path) -> None:
    result = {"ticker": "AAPL", "decision": "UP", "reasoning": "test"}
    path = tmp_path / "prediction_today.json"

    save_prediction(result, str(path))

    with open(path) as f:
        loaded = json.load(f)
    assert loaded == result
