"""Application factory for the IBKR web UI."""

from __future__ import annotations

from pathlib import Path
from typing import Optional

from flask import Flask

from .config import AppConfig
from .filters import register_filters
from .routes import register_blueprints
from .services.ibkr_client import IBKRClient

try:  # pragma: no cover - optional dependency during runtime only
    from dotenv import load_dotenv
except ImportError:  # pragma: no cover - we fall back silently
    load_dotenv = None


def create_app(config: Optional[AppConfig] = None, client: Optional[IBKRClient] = None) -> Flask:
    """Create and configure the Flask application."""
    templates_path = Path(__file__).resolve().parent / "templates"
    app = Flask(__name__, template_folder=str(templates_path))

    if load_dotenv is not None:
        load_dotenv()

    runtime_config = config or AppConfig.from_env()

    app.config.update(
        IBKR_BASE_URL=runtime_config.base_api_url,
        IBKR_ACCOUNT_ID=runtime_config.account_id,
        IBKR_VERIFY=runtime_config.verify,
        IBKR_REQUEST_TIMEOUT=runtime_config.request_timeout,
    )

    ibkr_client = client or IBKRClient(
        runtime_config.base_api_url,
        verify=runtime_config.verify,
        timeout=runtime_config.request_timeout,
    )
    app.extensions["ibkr_client"] = ibkr_client

    register_blueprints(app)
    register_filters(app)

    return app
