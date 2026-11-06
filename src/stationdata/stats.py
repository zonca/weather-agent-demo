"""Daily and weekly statistics of station readings."""

from collections import defaultdict


def daily_stats(readings, field="temperature_c"):
    """Compute mean, min and max of ``field`` for each day.

    Returns a dict mapping a ``datetime.date`` to a dict with keys
    ``mean``, ``min`` and ``max``.
    """
    by_day = defaultdict(list)
    for r in readings:
        by_day[r["time"].date()].append(r[field])

    stats = {}
    for day, values in sorted(by_day.items()):
        valid = [v for v in values if v is not None]
        stats[day] = {
            "mean": sum(valid) / len(values),
            "min": min(valid),
            "max": max(valid),
        }
    return stats


def weekly_stats(readings, field="temperature_c"):
    """Compute mean, min and max of ``field`` for each ISO week.

    Returns a dict mapping a ``"YYYY-Www"`` string to a dict with keys
    ``mean``, ``min`` and ``max``. Weeks run Monday to Sunday; ``mean``
    weights each reading equally, matching ``daily_stats``.
    """
    by_week = defaultdict(list)
    for r in readings:
        iso = r["time"].isocalendar()
        by_week[f"{iso.year}-W{iso.week:02d}"].append(r)

    stats = {}
    for week, week_readings in sorted(by_week.items()):
        days = daily_stats(week_readings, field)
        per_day = defaultdict(int)
        for r in week_readings:
            per_day[r["time"].date()] += 1
        stats[week] = {
            "mean": sum(
                days[day]["mean"] * per_day[day] for day in days
            ) / len(week_readings),
            "min": min(s["min"] for s in days.values()),
            "max": max(s["max"] for s in days.values()),
        }
    return stats
