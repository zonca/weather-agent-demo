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
- There is no test suite, linter, formatter, or CI yet. `pytest` is installed;
  run `.venv/bin/python -m pytest` before claiming a task is done. Since it
  collects nothing today, also exercise the package directly against
  `data/station_2026-09.csv`.
- Python >= 3.10 (`pyproject.toml`); the venv runs 3.13.

## Rules

- Standard library only. Ask before adding any dependency (runtime or dev).
- Do not commit unless asked. When asked, make small commits, one logical
  change per commit.
- Use the `gh` CLI for GitHub operations (issues, PRs, releases, etc.).

## Gotchas

- The README quickstart imports `load_readings`, which does not exist. The real
  public name is `load_csv` (see `src/stationdata/__init__.py`); it lives in
  `io.py`. Keep `__init__.py` `__all__` in sync with any rename.
- `daily_stats` (`stats.py`) divides by `len(values)`, i.e. the count
  *including* `None` readings, while `min`/`max` use only valid values. The
  sample data contains missing readings, so reported means are skewed low.
  Do not "simplify" this without deciding the intended missing-data semantics;
  a day with all-missing values raises `ValueError` from `min()`.
- Missing readings are `""` or `NA` in CSV and become `None` in memory; every
  consumer must handle `None` (see `flag_outliers`).
- Data file `data/station_2026-09.csv` is 720 hourly rows for 2026-09-01..30
  with columns `time` (ISO 8601), `temperature_c`, `humidity` (percent).
