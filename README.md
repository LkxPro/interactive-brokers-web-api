# Interactive Brokers Web API

## Video Walkthrough

https://www.youtube.com/watch?v=CRsH9TKveLo

## Requirements

* Docker Desktop - https://www.docker.com/products/docker-desktop/
* [uv](https://docs.astral.sh/uv/) for managing Python environments

> Quick install: `curl -LsSf https://astral.sh/uv/install.sh | sh`

## Clone the source code
```
git clone https://github.com/hackingthemarkets/interactive-brokers-web-api.git
```

## Bring up the container
```
docker-compose up
```

## Getting a command line prompt
```
docker exec -it ibkr bash
```

Inside the container, the helper script `start.sh` provisions the Flask environment with
`uv venv` and `uv pip install` before launching the dev server.

## Develop without Docker

You can work on the Flask application directly on your host machine.

1. Install [uv](https://docs.astral.sh/uv/) and ensure it is on your `PATH`.
2. Change into the project folder: `cd interactive-brokers-web-api/webapp`.
3. Create the environment: `uv venv .venv` (rerun only when you need a fresh environment).
4. Activate it: `. .venv/bin/activate` (macOS/Linux) or `.venv\\Scripts\\activate` (Windows PowerShell).
5. Install dependencies: `uv pip install -r requirements.txt`.
6. Start (or connect to) the Interactive Brokers Client Portal Gateway locally so it serves `https://localhost:5055`.
7. Export required variables (for example `export IBKR_ACCOUNT_ID=<your-account-id>`).
8. Launch the Flask server: `flask --app app run --debug -p 5056 -h 0.0.0.0`.

Refer to `scripts/rest_api_examples.py` for example REST calls while iterating on the UI.
