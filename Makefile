.PHONY: bootstrap run test lint

bootstrap:
	uv venv .venv
	uv pip install -e .

run:
	uv run -- python -m ibkr_web

test:
	uv run -- pytest -q

lint:
	uv run -- ruff check src tests || true
