"""Daily statistics of station readings."""

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
