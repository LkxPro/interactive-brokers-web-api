"""Entry point for running the development server with ``python -m ibkr_web``."""

from __future__ import annotations

import os

from .app import create_app


def main() -> None:
    host = os.getenv("IBKR_WEB_HOST", "0.0.0.0")
    port = int(os.getenv("IBKR_WEB_PORT", "5056"))
    debug = os.getenv("IBKR_WEB_DEBUG", "1") not in {"0", "false", "no"}

    app = create_app()
    app.run(host=host, port=port, debug=debug)


if __name__ == "__main__":  # pragma: no cover - convenience entry point
    main()
