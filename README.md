# Interactive Brokers Web API

A structured Flask application and supporting utilities for working with the
Interactive Brokers Client Portal Gateway.

## Quick Start (Host Machine)

1. Install [uv](https://docs.astral.sh/uv/) and ensure it is on your `PATH`.
2. From the repository root run:
   ```bash
   uv venv .venv
   uv pip install -e .
   ```
3. Copy `.env.example` to `.env` (or export the variables manually) and set at
   minimum `IBKR_ACCOUNT_ID` and `IBKR_BASE_URL`. Defaults point at
   `https://localhost:5055/v1/api` with SSL verification disabled.
4. Start the development server without changing directories:
   ```bash
   uv run -- python -m ibkr_web
   ```
   The app runs at `http://localhost:5056` by default.

Use the Typer-based CLI for quick API calls:
```bash
uv run -- ibkr-rest accounts
uv run -- ibkr-rest marketdata 208813720 --period 30d --bar 1d
```

## Project Layout

```
interactive-brokers-web-api/
├── src/ibkr_web/        # Flask app factory, blueprints, services, templates
├── scripts/             # Legacy scripts (now thin wrappers around Typer CLI)
├── tests/               # Pytest-based unit tests
├── Makefile             # Common workflows (bootstrap, run, test, lint)
├── start.sh             # Container entrypoint (runs gateway + Flask app)
└── docker-compose.yml   # Optional Docker orchestration
```

Routes are organised into feature-specific blueprints under
`src/ibkr_web/routes/`, while HTTP calls to the IBKR gateway live in
`src/ibkr_web/services/ibkr_client.py`.

## Development Commands

- `make bootstrap` — create the virtual environment and install dependencies.
- `make run` — start the Flask development server (`uv run -- python -m ibkr_web`).
- `make test` — execute the pytest suite.
- `make lint` — run Ruff (optional, install via `uv pip install -e .[dev]`).

All commands run from the repository root. The Flask CLI is configured with the
application factory (`ibkr_web.app:create_app`), so any of the usual
`flask ...` commands work without `cd` steps.

## Testing

Tests live under `tests/` and target the blueprints and service layer with
`requests-mock`. Run them via:
```bash
uv run -- pytest -q
```

When adding new tests, mirror the runtime package structure inside `tests/`
(e.g. `tests/routes/test_orders.py`).

## Docker (Optional)

Docker remains available for end-to-end validation and to run the official IBKR
Client Portal Gateway alongside the Flask app:

```bash
docker-compose up
```

Inside the container the updated `start.sh` script provisions the virtualenv,
installs this project in editable mode, and launches the Flask server on
port `5056`.

## CLI Reference

The Typer CLI exposed via `ibkr-rest` offers quick interactions with the
gateway:

- `ibkr-rest accounts`
- `ibkr-rest orders`
- `ibkr-rest marketdata <conid> [--period 5d] [--bar 1d]`

Extend `src/ibkr_web/cli/__init__.py` with additional commands and the script
will pick them up automatically.

## Security Notes

- Provide `IBKR_CERT_PATH` when you have a trusted certificate and set
  `IBKR_VERIFY_SSL=1` to re-enable SSL verification.
- Keep broker credentials and session tokens in environment variables or secret
  stores. Never commit them to the repository.
