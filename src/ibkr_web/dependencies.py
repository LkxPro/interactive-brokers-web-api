"""Helpers for retrieving shared application extensions."""

from __future__ import annotations

from flask import current_app

from .services.ibkr_client import IBKRClient


def get_ibkr_client() -> IBKRClient:
    client: IBKRClient = current_app.extensions["ibkr_client"]
    return client


def get_account_id() -> str:
    account_id = current_app.config.get("IBKR_ACCOUNT_ID")
    if not account_id:
        raise RuntimeError("IBKR_ACCOUNT_ID is not configured. Set it via the environment or .env file.")
    return account_id
