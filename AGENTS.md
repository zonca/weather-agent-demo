# AGENTS.md

`stationdata`: a tiny, stdlib-only Python package for loading weather-station
CSVs and computing daily stats / unit conversions / outlier flags. No runtime
dependencies.

## Setup and commands

- This is a `src/` layout package (`src/stationdata/`), installed in editable
  mode already. Use the checked-in virtualenv: `.venv/bin/python`.
- The venv has no `pip` (created by `uv`). Reinstall after packaging changes
  with `uv pip install -e . --python .venv/bin/python`; do not try
  `.venv/bin/pip` or `python -m pip`.
- There is no linter, formatter, or CI yet. `pytest` is installed; run
  `.venv/bin/python -m pytest` before claiming a task is done. Tests live in
  `tests/` and use small hand-written inputs; also exercise the package
  directly against `data/station_2026-09.csv`.
- Python >= 3.10 (`pyproject.toml`); the venv runs 3.13.

## Rules

- Standard library only. Ask before adding any dependency (runtime or dev).
- Do not commit unless asked. When asked, make small commits, one logical
  change per commit.
- Use the `gh` CLI for GitHub operations (issues, PRs, releases, etc.).
- Use `gog` for Google Drive operations (uploading, listing, downloading
  files).

## Gotchas

- The README quickstart imports `load_readings`, which does not exist. The real
  public name is `load_csv` (see `src/stationdata/__init__.py`); it lives in
  `io.py`. Keep `__init__.py` `__all__` in sync with any rename.
- Missing readings are `""` or `NA` in CSV and become `None` in memory.
  `daily_stats` and `weekly_stats` ignore `None` values when computing
  `mean`, `min` and `max`; every consumer must still handle `None` (see
  `flag_outliers`). A day with no valid readings raises `ValueError`, and
  `weekly_stats` propagates it for any week containing such a day.
- Data file `data/station_2026-09.csv` is 720 hourly rows for 2026-09-01..30
  with columns `time` (ISO 8601), `temperature_c`, `humidity` (percent).
