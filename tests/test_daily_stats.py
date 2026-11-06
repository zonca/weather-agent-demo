"""Tests for stationdata.stats.daily_stats."""

from datetime import date, datetime

import pytest

from stationdata import daily_stats


def _reading(day, hour, temperature_c):
    return {
        "time": datetime(2026, 9, day, hour),
        "temperature_c": temperature_c,
        "humidity": 50.0,
    }


def test_daily_stats_normal_days():
    readings = [
        _reading(1, 0, 10.0),
        _reading(1, 12, 20.0),
        _reading(2, 0, 5.0),
        _reading(2, 12, 15.0),
    ]

    stats = daily_stats(readings)

    assert stats == {
        date(2026, 9, 1): {"mean": 15.0, "min": 10.0, "max": 20.0},
        date(2026, 9, 2): {"mean": 10.0, "min": 5.0, "max": 15.0},
    }


def test_daily_stats_missing_readings_are_ignored():
    readings = [
        _reading(13, 0, 14.1),
        _reading(13, 1, None),
        _reading(13, 2, 24.5),
        _reading(13, 3, None),
    ]

    day = daily_stats(readings)[date(2026, 9, 13)]

    assert day["mean"] == pytest.approx(19.3)
    assert day["min"] == 14.1
    assert day["max"] == 24.5


def test_daily_stats_all_missing_day_raises():
    # Current behaviour: an all-missing day raises from min() on the empty
    # list of valid readings. The intended semantics are still undecided.
    readings = [_reading(3, 0, None), _reading(3, 1, None)]

    with pytest.raises(ValueError):
        daily_stats(readings)


def test_daily_mean_stays_within_min_and_max():
    readings = [
        _reading(13, 0, 14.1),
        _reading(13, 1, None),
        _reading(13, 2, 24.5),
        _reading(13, 3, None),
    ]

    day = daily_stats(readings)[date(2026, 9, 13)]

    assert day["min"] <= day["mean"] <= day["max"]
