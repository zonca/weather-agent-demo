"""Flag suspicious readings, such as sensor glitches."""


def flag_outliers(readings, field="temperature_c", low=-60.0, high=60.0):
    """Return the readings whose ``field`` is outside ``[low, high]``."""
    return [
        r
        for r in readings
        if r[field] is not None and not (low <= r[field] <= high)
    ]
