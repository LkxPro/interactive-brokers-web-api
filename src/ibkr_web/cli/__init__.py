"""Command line interfaces for the IBKR web tools."""

from __future__ import annotations

import json
from typing import Any, Optional

import typer

from ..config import AppConfig
from ..services.ibkr_client import IBKRClient

cli = typer.Typer(help="Utilities for querying the Interactive Brokers Client Portal API")


def _get_client(config: Optional[AppConfig] = None) -> tuple[AppConfig, IBKRClient]:
    app_config = config or AppConfig.from_env()
    client = IBKRClient(
        app_config.base_api_url,
        verify=app_config.verify,
        timeout=app_config.request_timeout,
    )
    return app_config, client


def _echo(data: Any) -> None:
    typer.echo(json.dumps(data, indent=2, sort_keys=True, default=str))


@cli.command()
def accounts() -> None:
    """Print the list of accounts that the current session can access."""
    _, client = _get_client()
    try:
        _echo(client.get_accounts())
    finally:
        client.close()


@cli.command()
def orders() -> None:
    """Print open orders for the configured session."""
    _, client = _get_client()
    try:
        _echo(client.get_orders())
    finally:
        client.close()


@cli.command()
def marketdata(conid: str, period: str = "5d", bar: str = "1d") -> None:
    """Fetch historical market data for a contract id."""
    _, client = _get_client()
    try:
        _echo(client.get_market_data_history(conid, period=period, bar=bar))
    finally:
        client.close()


def main() -> None:  # pragma: no cover - thin wrapper for console_scripts
    cli()
