"""Portfolio views."""

from __future__ import annotations

from flask import Blueprint, current_app, render_template

from ..dependencies import get_account_id, get_ibkr_client
from ..services.ibkr_client import IBKRClientError

blueprint = Blueprint("portfolio", __name__)


@blueprint.route("/portfolio")
def portfolio() -> str:
    client = get_ibkr_client()

    try:
        account_id = get_account_id()
    except RuntimeError as exc:
        current_app.logger.exception("Account ID not configured: %s", exc)
        positions = []
    else:
        try:
            positions = client.get_positions(account_id)
        except IBKRClientError:
            positions = []

    return render_template("portfolio.html", positions=positions)
