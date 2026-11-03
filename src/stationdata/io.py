"""Read station readings from CSV files."""

import csv
from datetime import datetime


def _parse_value(text):
    """Return a float, or None when the reading is missing."""
    text = text.strip()
    if text == "" or text.upper() == "NA":
        return None
    return float(text)


def load_csv(path):
    """Load a station CSV file.

    The file has the columns ``time``, ``temperature_c`` and ``humidity``.
    Missing readings are empty or ``NA`` and are returned as ``None``.

    Returns a list of dicts with keys ``time`` (datetime), ``temperature_c``
    and ``humidity``.
    """
    readings = []
    with open(path, newline="") as f:
        for row in csv.DictReader(f):
            readings.append(
                {
                    "time": datetime.fromisoformat(row["time"]),
                    "temperature_c": _parse_value(row["temperature_c"]),
                    "humidity": _parse_value(row["humidity"]),
                }
            )
    return readings
