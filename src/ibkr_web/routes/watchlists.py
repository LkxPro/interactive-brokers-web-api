"""Watchlist routes."""

from __future__ import annotations

import time

from flask import Blueprint, redirect, render_template, request, url_for

from ..dependencies import get_ibkr_client
from ..services.ibkr_client import IBKRClientError

blueprint = Blueprint("watchlists", __name__)


@blueprint.route("/watchlists")
def watchlists() -> str:
    client = get_ibkr_client()

    try:
        response = client.get_watchlists()
    except IBKRClientError:
        response = {}

    data = response.get("data", {}) if isinstance(response, dict) else {}
    watchlists_data = data.get("user_lists", []) if isinstance(data, dict) else []

    return render_template("watchlists.html", watchlists=watchlists_data)


@blueprint.route("/watchlists/<int:watchlist_id>")
def watchlist_detail(watchlist_id: int) -> str:
    client = get_ibkr_client()

    try:
        watchlist = client.get_watchlist(watchlist_id)
    except IBKRClientError:
        watchlist = {}

    return render_template("watchlist.html", watchlist=watchlist)


@blueprint.route("/watchlists/<int:watchlist_id>/delete")
def watchlist_delete(watchlist_id: int):
    client = get_ibkr_client()

    try:
        client.delete_watchlist(watchlist_id)
    except IBKRClientError:
        pass

    return redirect(url_for("watchlists.watchlists"))


@blueprint.route("/watchlists/create", methods=["POST"])
def create_watchlist():
    client = get_ibkr_client()
    data = request.get_json(force=True)

    name = data.get("name", "")
    symbols = [symbol.strip() for symbol in data.get("symbols", "").split(",") if symbol.strip()]

    rows = []
    for symbol in symbols:
        try:
            result = client.search_contracts(symbol, sec_type="STK")
        except IBKRClientError:
            result = []
        if result:
            contract_id = result[0].get("conid")
            if contract_id:
                rows.append({"C": contract_id})

    payload = {
        "id": int(time.time()),
        "name": name,
        "rows": rows,
    }

    try:
        client.create_watchlist(payload)
    except IBKRClientError:
        pass

    return redirect(url_for("watchlists.watchlists"))
