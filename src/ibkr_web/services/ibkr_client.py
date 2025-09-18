"""Thin wrapper around the Interactive Brokers Client Portal REST API."""

from __future__ import annotations

from typing import Any, Iterable, Optional
import logging

import requests
from requests import Response, Session
from requests.exceptions import RequestException
from requests.packages.urllib3.exceptions import InsecureRequestWarning  # type: ignore[attr-defined]

logger = logging.getLogger(__name__)


class IBKRClientError(RuntimeError):
    """Raised when the IBKR REST API call fails."""


class IBKRClient:
    """Client for talking to the IBKR REST API."""

    def __init__(
        self,
        base_url: str,
        *,
        verify: bool | str = False,
        timeout: int = 10,
        session: Optional[Session] = None,
    ) -> None:
        self.base_url = base_url.rstrip("/")
        self.timeout = timeout
        self.session = session or Session()
        self.session.verify = verify
        if verify is False:
            # We explicitly disable InsecureRequestWarning when verify is False.
            requests.packages.urllib3.disable_warnings(InsecureRequestWarning)  # type: ignore[attr-defined]

    def close(self) -> None:
        self.session.close()

    # Public helpers -----------------------------------------------------
    def get_accounts(self) -> list[dict[str, Any]]:
        return self._get_json("/portfolio/accounts")

    def get_account_summary(self, account_id: str) -> dict[str, Any]:
        return self._get_json(f"/portfolio/{account_id}/summary")

    def get_positions(self, account_id: str) -> list[dict[str, Any]]:
        return self._get_json(f"/portfolio/{account_id}/positions/0")

    def get_orders(self) -> list[dict[str, Any]]:
        response = self._get_json("/iserver/account/orders")
        return response.get("orders", []) if isinstance(response, dict) else []

    def place_order(self, account_id: str, order: dict[str, Any]) -> dict[str, Any]:
        payload = {"orders": [order]}
        return self._post_json(f"/iserver/account/{account_id}/orders", json=payload)

    def cancel_order(self, account_id: str, order_id: str) -> dict[str, Any]:
        return self._request("delete", f"/iserver/account/{account_id}/order/{order_id}")

    def search_contracts(self, symbol: str, name: bool = True, sec_type: Optional[str] = None) -> list[dict[str, Any]]:
        params = {"symbol": symbol, "name": str(name).lower()}
        if sec_type:
            params["secType"] = sec_type
        return self._get_json("/iserver/secdef/search", params=params)

    def get_contract_details(self, conids: Iterable[str | int]) -> dict[str, Any]:
        payload = {"conids": list(conids)}
        return self._post_json("/trsrv/secdef", json=payload)

    def get_market_data_history(self, conid: str | int, *, period: str, bar: str) -> dict[str, Any]:
        params = {"conid": conid, "period": period, "bar": bar}
        return self._get_json("/iserver/marketdata/history", params=params)

    def get_watchlists(self) -> dict[str, Any]:
        return self._get_json("/iserver/watchlists")

    def get_watchlist(self, watchlist_id: int) -> dict[str, Any]:
        params = {"id": watchlist_id}
        return self._get_json("/iserver/watchlist", params=params)

    def create_watchlist(self, payload: dict[str, Any]) -> dict[str, Any]:
        return self._post_json("/iserver/watchlist", json=payload)

    def delete_watchlist(self, watchlist_id: int) -> dict[str, Any]:
        params = {"id": watchlist_id}
        return self._request("delete", "/iserver/watchlist", params=params)

    def get_scanner_params(self) -> dict[str, Any]:
        return self._get_json("/iserver/scanner/params")

    def run_scanner(self, payload: dict[str, Any]) -> dict[str, Any]:
        return self._post_json("/iserver/scanner/run", json=payload)

    # Internal helpers --------------------------------------------------
    def _compose_url(self, path: str) -> str:
        if path.startswith("http://") or path.startswith("https://"):
            return path
        if not path.startswith("/"):
            path = f"/{path}"
        return f"{self.base_url}{path}"

    def _request(self, method: str, path: str, **kwargs: Any) -> Any:
        url = self._compose_url(path)
        try:
            response = self.session.request(method=method, url=url, timeout=self.timeout, **kwargs)
            response.raise_for_status()
        except RequestException as exc:  # pragma: no cover - we rewrap in custom error
            raise IBKRClientError(str(exc)) from exc

        return self._parse_response(response)

    def _get_json(self, path: str, params: Optional[dict[str, Any]] = None) -> Any:
        return self._request("get", path, params=params)

    def _post_json(self, path: str, json: Optional[dict[str, Any]] = None) -> Any:
        return self._request("post", path, json=json)

    @staticmethod
    def _parse_response(response: Response) -> Any:
        if not response.content:
            return {}
        content_type = response.headers.get("Content-Type", "")
        if "application/json" in content_type or response.text.startswith("{"):
            try:
                return response.json()
            except ValueError:
                logger.debug("Failed to decode JSON, returning raw text")
        return response.text
