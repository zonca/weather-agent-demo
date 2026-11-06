# stationdata

Small tools to analyze readings from a weather station: load the CSV files the
station produces, convert units, compute daily statistics and flag sensor glitches.

## Install

```bash
git clone https://github.com/zonca/weather-agent-demo
cd weather-agent-demo
pip install -e .
```

## Quickstart

```python
from stationdata import load_csv, daily_stats, flag_outliers

readings = load_csv("data/station_2026-09.csv")

for day, s in daily_stats(readings).items():
    print(day, round(s["mean"], 1), s["min"], s["max"])

print(len(flag_outliers(readings)), "suspicious readings")
```

## Data format

CSV with the columns `time` (ISO 8601), `temperature_c` and `humidity` (percent).
Missing readings are empty or `NA`.
