"""Tests for stationdata.stats.weekly_stats."""

from datetime import datetime

import pytest

from stationdata import weekly_stats


def _reading(day, hour, temperature_c):
    return {
        "time": datetime(2026, 9, day, hour),
        "temperature_c": temperature_c,
        "humidity": 50.0,
    }


def test_weekly_stats_normal_week():
    readings = [
        _reading(7, 0, 10.0),
        _reading(7, 12, 20.0),
        _reading(8, 0, 5.0),
        _reading(8, 12, 15.0),
    ]

    stats = weekly_stats(readings)

    assert stats == {"2026-W37": {"mean": 12.5, "min": 5.0, "max": 20.0}}


def test_weekly_stats_missing_readings_are_ignored():
    readings = [
        _reading(7, 0, 14.1),
        _reading(7, 1, None),
        _reading(7, 2, 24.5),
        _reading(7, 3, None),
        _reading(8, 0, 10.0),
        _reading(8, 1, 20.0),
    ]

    stats = weekly_stats(readings)["2026-W37"]

    assert stats["mean"] == pytest.approx(17.15)
    assert stats["min"] == 10.0
    assert stats["max"] == 24.5


def test_weekly_stats_all_missing_day_raises():
    # weekly_stats delegates to daily_stats, so an all-missing day inside a
    # week raises ValueError from min().
    readings = [
        _reading(7, 0, 10.0),
        _reading(7, 1, 20.0),
        _reading(8, 0, None),
        _reading(8, 1, None),
    ]

    with pytest.raises(ValueError):
        weekly_stats(readings)
