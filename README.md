# ohutvarasto

[![CI](https://github.com/viivizz/ohutvarasto/actions/workflows/main.yml/badge.svg)](https://github.com/viivizz/ohutvarasto/actions)
[![codecov](https://codecov.io/github/viivizz/ohutvarasto/graph/badge.svg?token=DEBYWV4GWH)](https://codecov.io/github/viivizz/ohutvarasto)

## Installation

Install [uv](https://docs.astral.sh/uv/) and the project dependencies:

```bash
uv sync --dev
```

## Run the web application

```bash
uv run flask --app src/app run
```

Open `http://127.0.0.1:5000` in a browser.

## Run tests

```bash
uv run pytest
```
