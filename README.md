# Interactive Brokers Web API

A structured Flask application and supporting utilities for working with the
Interactive Brokers Client Portal Gateway, packaged for an easy host-based
workflow.

## Prerequisites

- Python 3.11+
- [uv](https://docs.astral.sh/uv/) on your `PATH` (for virtualenv + command
  execution)
- Interactive Brokers Client Portal Gateway credentials

## Gateway Setup

Use the provided helper script to download and run the official gateway from
Interactive Brokers:

```bash
# Download and extract the Client Portal files into ./gateway
./clientportal_gateway.sh download

# Start the gateway (leave this running in a dedicated terminal)
./clientportal_gateway.sh run
```

The script mirrors the steps previously handled in container setups: it fetches
`clientportal.gw.zip`, unpacks it into `./gateway`, and copies the bundled
`conf.yaml` into the correct location. Use `./clientportal_gateway.sh clean`
if you need to remove the downloaded artifacts.

## Application Environment

1. Create a virtual environment and install dependencies from the project root:
   ```bash
   uv venv .venv
   uv pip install -e .
   ```
2. Export the required environment variables (or copy `.env.example` to `.env`
   and rely on `python-dotenv`):
   ```bash
   export IBKR_BASE_URL=https://localhost:5055/v1/api
   export IBKR_ACCOUNT_ID=<your-account-id>
   export IBKR_VERIFY_SSL=0  # enable once you trust/install the cert
   ```
3. Launch the Flask development server without changing directories:
   ```bash
   uv run -- python -m ibkr_web
   ```
   The UI is available at `http://localhost:5056` by default.

## Project Layout

```
interactive-brokers-web-api/
├── src/ibkr_web/        # Flask app factory, blueprints, services, templates
├── clientportal_gateway.sh  # Helper to download and start the gateway
├── tests/               # Pytest-based unit tests
├── Makefile             # Common workflows (bootstrap, run, test, lint)
├── conf.yaml            # Gateway configuration copied during setup
└── .env.example         # Sample environment variables
```

Routes are organised into feature-specific blueprints under
`src/ibkr_web/routes/`, while HTTP calls to the IBKR gateway live in
`src/ibkr_web/services/ibkr_client.py`.

## Useful Commands

- `make bootstrap` — create the virtual environment and install dependencies.
- `make run` — start the Flask development server (`uv run -- python -m ibkr_web`).
- `make test` — execute the pytest suite (install via `uv pip install -e .[dev]`).
- `make lint` — run Ruff checks (optional).
- `uv run -- ibkr-rest accounts` — call the Typer CLI for quick REST queries.

All commands execute from the repository root—no need to `cd` into subfolders.

## Testing

Tests live under `tests/` and target both blueprints and the service layer using
stubbed API responses. Run them with:

```bash
uv run -- pytest -q
```

When adding new tests, mirror the runtime package structure inside `tests/` (e.g.
`tests/routes/test_orders.py`).

## Security Notes

- Provide `IBKR_CERT_PATH` when you have a trusted certificate and set
  `IBKR_VERIFY_SSL=1` to re-enable SSL verification.
- Keep broker credentials and session tokens in environment variables or secret
  stores—never commit them to the repository.
