"""Order management routes."""

from __future__ import annotations

from flask import Blueprint, current_app, redirect, render_template, request, url_for

from ..dependencies import get_account_id, get_ibkr_client
from ..services.ibkr_client import IBKRClientError

blueprint = Blueprint("orders", __name__)


@blueprint.route("/orders")
def orders() -> str:
    client = get_ibkr_client()

    try:
        orders = client.get_orders()
    except IBKRClientError:
        orders = []

    return render_template("orders.html", orders=orders)


@blueprint.route("/order", methods=["POST"])
def place_order() -> str:
    client = get_ibkr_client()

    try:
        account_id = get_account_id()
    except RuntimeError as exc:
        current_app.logger.exception("Account ID not configured: %s", exc)
        return redirect(url_for("orders.orders"))

    def _to_int(value: str | None, default: int = 0) -> int:
        try:
            return int(value) if value is not None and value != "" else default
        except (TypeError, ValueError):
            return default

    def _to_float(value: str | None, default: float = 0.0) -> float:
        try:
            return float(value) if value is not None and value != "" else default
        except (TypeError, ValueError):
            return default

    order = {
        "conid": _to_int(request.form.get("contract_id")),
        "orderType": request.form.get("order_type", "LMT"),
        "price": _to_float(request.form.get("price")),
        "quantity": _to_int(request.form.get("quantity")),
        "side": request.form.get("side", "BUY"),
        "tif": request.form.get("tif", "GTC"),
    }

    try:
        client.place_order(account_id, order)
    except IBKRClientError as exc:
        current_app.logger.error("Failed to place order: %s", exc)

    return redirect(url_for("orders.orders"))


@blueprint.route("/orders/<order_id>/cancel")
def cancel_order(order_id: str):
    client = get_ibkr_client()

    try:
        account_id = get_account_id()
    except RuntimeError as exc:
        current_app.logger.exception("Account ID not configured: %s", exc)
        return redirect(url_for("orders.orders"))

    try:
        response = client.cancel_order(account_id, order_id)
    except IBKRClientError as exc:
        current_app.logger.error("Failed to cancel order %s: %s", order_id, exc)
        response = {"error": str(exc)}

    return response
