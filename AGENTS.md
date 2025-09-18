# Repository Guidelines

## Project Structure & Module Organization
The repo combines Docker orchestration with a Flask frontend. `docker-compose.yml`, `Dockerfile`, and `start.sh` spin up the Interactive Brokers gateway plus the web UI. Core API integrations live in `webapp/app.py`, while HTML templates are under `webapp/templates`. Use `scripts/rest_api_examples.py` as a reference when extending low-level REST calls, and stage any new utilities in `scripts/` before promoting them into the app. Keep future test files in `webapp/tests/` to mirror the runtime package.

## Build, Test, and Development Commands
Run `docker-compose up` from the repo root to build images and launch the gateway + web app stack. Attach to the running container with `docker exec -it ibkr bash` for interactive debugging. Inside the container, `./start.sh` provisions the virtualenv and launches `flask --app app run --debug -p 5056 -h 0.0.0.0`. For lightweight local edits outside Docker, activate `webapp/venv`, then install requirements with `pip install -r webapp/requirements.txt`.

## Coding Style & Naming Conventions
Follow PEP 8: four-space indentation, `snake_case` for functions and variables, and `CamelCase` for any future classes. Keep Flask routes and helper functions cohesive—group IBKR REST helpers near their route handlers. Jinja template files should mirror the route names (`dashboard.html`, `orders.html`, etc.) to simplify discovery. Run `ruff` or `black` if you introduce them, and capture the commands in the README before enforcing them.

## Testing Guidelines
Add automated coverage with `pytest`; place files under `webapp/tests/` using the `test_<feature>.py` naming scheme. Stub IBKR responses with `responses` or `requests-mock` to avoid hitting the live gateway in unit tests. Run `pytest webapp/tests -q` locally and in CI once available, and include fixtures for environment variables such as `IBKR_ACCOUNT_ID`.

## Commit & Pull Request Guidelines
Keep commits small, descriptive, and imperative (e.g., "add watchlist management", "update Dockerfile"). Reference issue IDs in the body when applicable. Pull requests should outline user impact, backend/frontend changes, and manual validation steps. Attach screenshots or cURL samples for UI or API updates, and mention any configuration changes (certificates, environment variables) reviewers must reproduce.

## Security & Configuration Tips
Store broker credentials in `.env` files or secrets managers; never commit them. The gateway uses self-signed certificates, so document any certificate installations instead of leaving `verify=False` in production-bound code. Review outgoing requests for personally identifiable information before adding logging or analytics.
