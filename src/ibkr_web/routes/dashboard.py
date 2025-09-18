"""Dashboard and quote lookup routes."""

from __future__ import annotations

from flask import Blueprint, render_template, request

from ..dependencies import get_ibkr_client
from ..services.ibkr_client import IBKRClientError

blueprint = Blueprint("dashboard", __name__)


@blueprint.route("/")
def dashboard() -> str:
    client = get_ibkr_client()

    try:
        accounts = client.get_accounts()
    except IBKRClientError:
        return "Make sure you authenticate first then visit this page. <a href=\"https://localhost:5055\">Log in</a>", 503

    if not accounts:
        return render_template("dashboard.html", account=None, summary={})

    account = accounts[0]
    account_id = account.get("id")

    try:
        summary = client.get_account_summary(account_id)
    except IBKRClientError as exc:
        summary = {"error": str(exc)}

    return render_template("dashboard.html", account=account, summary=summary)


@blueprint.route("/lookup")
def lookup() -> str:
    client = get_ibkr_client()
    symbol = request.args.get("symbol")
    stocks: list[dict[str, str]] = []

    if symbol:
        try:
            stocks = client.search_contracts(symbol)
        except IBKRClientError:
            stocks = []

    return render_template("lookup.html", stocks=stocks)


@blueprint.route("/contract/<contract_id>/<period>")
def contract(contract_id: str, period: str = "5d", bar: str = "1d") -> str:
    client = get_ibkr_client()

    try:
        contract = client.get_contract_details([contract_id])["secdef"][0]
    except (KeyError, IndexError, IBKRClientError):
        contract = {}

    try:
        price_history = client.get_market_data_history(contract_id, period=period, bar=bar)
    except IBKRClientError:
        price_history = {}

    return render_template("contract.html", price_history=price_history, contract=contract)
