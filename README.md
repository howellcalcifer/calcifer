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

To generate an HTML coverage report:

`pipenv run pytest --cov --cov-report html:coverage_report`

To update snapshot files:

`pipenv run pytest --update-snapshots`