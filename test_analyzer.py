"""TDD tests for the prediction engine's analyzer module."""
import os

import pandas as pd

from analyzer import load_data, calculate_sma

CSV_PATH = "data/aapl_5y.csv"


def test_data_file_exists() -> None:
    assert os.path.exists(CSV_PATH)


def test_load_data_returns_dataframe() -> None:
    df = load_data(CSV_PATH)
    assert isinstance(df, pd.DataFrame)
    assert not df.empty
    assert "Close" in df.columns


def test_calculate_sma_20_correctness() -> None:
    df = load_data(CSV_PATH)
    result = calculate_sma(df, window=20)
    expected = df["Close"].rolling(20, min_periods=20).mean()
    pd.testing.assert_series_equal(result["SMA_20"], expected, check_names=False)


def test_calculate_sma_first_19_rows_nan() -> None:
    df = load_data(CSV_PATH)
    result = calculate_sma(df, window=20)
    assert result["SMA_20"].iloc[:19].isna().all()
    assert pd.notna(result["SMA_20"].iloc[19])
