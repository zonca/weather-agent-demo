"""Daily and weekly statistics of station readings."""

from collections import defaultdict


def _summarize(values):
    """Mean, min and max of a list of values, ignoring missing ones."""
    valid = [v for v in values if v is not None]
    return {
        "mean": sum(valid) / len(values),
        "min": min(valid),
        "max": max(valid),
    }


def daily_stats(readings, field="temperature_c"):
    """Compute mean, min and max of ``field`` for each day.

    Returns a dict mapping a ``datetime.date`` to a dict with keys
    ``mean``, ``min`` and ``max``. Missing values (``None``) are ignored.
    """
    values_by_day = defaultdict(list)
    for reading in readings:
        values_by_day[reading["time"].date()].append(reading[field])

    stats = {}
    for day, values in sorted(values_by_day.items()):
        if all(v is None for v in values):
            raise ValueError(f"no valid {field} readings for {day}")
        stats[day] = _summarize(values)
    return stats


def weekly_stats(readings, field="temperature_c"):
    """Compute mean, min and max of ``field`` for each ISO week.

    Returns a dict mapping a ``"YYYY-Www"`` string to a dict with keys
    ``mean``, ``min`` and ``max``. Weeks run Monday to Sunday; ``mean``
    weights each reading equally, matching ``daily_stats``.
    """
    by_week = defaultdict(list)
    for reading in readings:
        iso = reading["time"].isocalendar()
        by_week[f"{iso.year}-W{iso.week:02d}"].append(reading)

    stats = {}
    for week, week_readings in sorted(by_week.items()):
        days = daily_stats(week_readings, field)
        valid_per_day = defaultdict(int)
        for reading in week_readings:
            if reading[field] is not None:
                valid_per_day[reading["time"].date()] += 1
        stats[week] = {
            "mean": sum(
                days[day]["mean"] * valid_per_day[day] for day in days
            ) / sum(valid_per_day.values()),
            "min": min(s["min"] for s in days.values()),
            "max": max(s["max"] for s in days.values()),
        }
    return stats
