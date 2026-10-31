# Calcifer



## Run the game

`./run`

Move with `go <direction>` or use `n`, `s`, `e`, `w`, `nw`, `ne`, `sw`, and `se` for the
corresponding cardinal and diagonal directions.

## Local developemt

### Prerequisites

Install uv, then install the Python version pinned by `.python-version` and the project dependencies:

```
uv python install
uv sync --locked
```

### Run tests

`uv run pytest`

### Type check

`uv run mypy`

### Git hooks

Install the Ruff, mypy, and pytest pre-commit hooks:

`uv run pre-commit install`

To run the hooks against every file:

`uv run pre-commit run --all-files`

To generate an HTML coverage report:

`uv run pytest --cov --cov-report html:coverage_report`

To update snapshot files:

`uv run pytest --update-snapshots`