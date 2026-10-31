# Calcifer



## Run the game

`./run`

## Local developemt

### Prerequisites

```
pip install --user pipenv
pipenv install --dev
```

### Run tests

`pipenv run pytest`

### Type check

`pipenv run mypy`

### Git hooks

Install the Ruff, mypy, and pytest pre-commit hooks:

`pipenv run pre-commit install`

To run the hooks against every file:

`pipenv run pre-commit run --all-files`

To generate an HTML coverage report:

`pipenv run pytest --cov --cov-report html:coverage_report`

To update snapshot files:

`pipenv run pytest --update-snapshots`