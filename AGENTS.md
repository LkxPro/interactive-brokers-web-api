# Repository Guidelines

## Project Structure & Module Organization
The Flask application resides in `src/ibkr_web/`, with `app.py` providing the entry point and feature blueprints under `routes/`. Service integrations with the Interactive Brokers gateway live in `services/`, while reusable filters and CLI utilities sit in `filters.py` and `cli/`. HTML templates live in `templates/`, mirroring blueprint names such as `dashboard.html`. Shared configuration defaults are defined in `config.py`. Pytest suites belong under `tests/`, organized to match the runtime package (e.g., `tests/routes/test_orders.py`). The gateway helper script (`clientportal_gateway.sh`) and configuration (`conf.yaml`) stay at the repo root.

## Build, Test, and Development Commands
- `make bootstrap` — create `.venv` via `uv` and install editable dependencies.
- `make run` — start the development server (`uv run -- python -m ibkr_web`) on port 5056.
- `uv run -- pytest -q` or `make test` — execute the test suite.
- `clientportal_gateway.sh download | run | clean` — manage the Client Portal Gateway lifecycle.
- `uv run -- ibkr-rest accounts` — invoke the Typer CLI for quick API checks.

Run commands from the repository root; no `cd` required.

## Coding Style & Naming Conventions
Follow PEP 8 with four-space indentation, `snake_case` for functions and variables, and `CamelCase` for classes. Keep blueprint modules cohesive: route handlers and their service helpers should share a directory. Templates mirror route names and avoid inline logic beyond simple Jinja filters. `ruff` and `black` are available via `make lint`; note any new tooling in `README.md`.

## Testing Guidelines
Write pytest cases in `tests/`, naming files `test_<feature>.py`. Stub HTTP calls with `responses` or `requests-mock` to avoid hitting the live gateway. Ensure new features include positive, negative, and edge-path coverage before submitting a PR.

## Commit & Pull Request Guidelines
Use imperative, concise commit subjects describing one logical change (e.g., “add account balances route”). Reference issue IDs in the commit body when applicable. PRs should state user impact, outline backend/frontend changes, list manual validation steps, and attach screenshots or cURL samples for UI/API updates. Call out new environment variables or certificate steps for reviewers.

## Security & Configuration Tips
Store broker credentials in `.env` or a secrets manager; never commit them. Set `IBKR_VERIFY_SSL=1` once a trusted cert is installed and document the process. Scrub logs for sensitive identifiers before merging.
