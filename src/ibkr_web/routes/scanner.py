"""Market scanner routes."""

from __future__ import annotations

from flask import Blueprint, render_template, request

from ..dependencies import get_ibkr_client
from ..services.ibkr_client import IBKRClientError

blueprint = Blueprint("scanner", __name__)


@blueprint.route("/scanner")
def scanner() -> str:
    client = get_ibkr_client()

    try:
        params = client.get_scanner_params()
    except IBKRClientError:
        params = {
            "instrument_list": [],
            "filter_list": [],
            "scan_type_list": [],
            "location_tree": [],
        }

    scanner_map: dict[str, dict] = {}
    filter_map: dict[str, dict] = {}

    for item in params.get("instrument_list", []):
        scanner_map[item["type"]] = {
            "display_name": item.get("display_name"),
            "filters": item.get("filters", []),
            "sorts": [],
        }

    for item in params.get("filter_list", []):
        filter_map[item.get("group")] = {
            "display_name": item.get("display_name"),
            "type": item.get("type"),
            "code": item.get("code"),
        }

    for item in params.get("scan_type_list", []):
        for instrument in item.get("instruments", []):
            scanner_map.setdefault(instrument, {}).setdefault("sorts", []).append(
                {
                    "name": item.get("display_name"),
                    "code": item.get("code"),
                }
            )

    for item in params.get("location_tree", []):
        scanner_map.setdefault(item.get("type"), {}).setdefault("locations", item.get("locations", []))

    submitted = request.args.get("submitted", "")
    selected_instrument = request.args.get("instrument", "")
    location = request.args.get("location", "")
    sort = request.args.get("sort", "")
    scan_results: dict | list = []
    filter_code = request.args.get("filter", "")
    filter_value = request.args.get("filter_value", "")

    if submitted and selected_instrument and location and sort:
        payload = {
            "instrument": selected_instrument,
            "location": location,
            "type": sort,
            "filter": [],
        }
        if filter_code and filter_value:
            payload["filter"].append({"code": filter_code, "value": filter_value})

        try:
            scan_results = client.run_scanner(payload)
        except IBKRClientError:
            scan_results = []

    return render_template(
        "scanner.html",
        params=params,
        scanner_map=scanner_map,
        filter_map=filter_map,
        scan_results=scan_results,
    )
