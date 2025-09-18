from __future__ import annotations

import pytest

from ibkr_web.app import create_app
from ibkr_web.config import AppConfig


class StubClient:
    def __init__(self) -> None:
        self._orders: list[dict[str, str]] = []

    def get_accounts(self) -> list[dict[str, str]]:
        return [{"id": "U123", "accountId": "U123"}]

    def get_account_summary(self, account_id: str) -> dict[str, str]:
        return {"account": account_id, "nav": "100000"}

    def search_contracts(self, symbol: str, name: bool = True, sec_type: str | None = None):
        return [{"symbol": symbol, "conid": 1}]

    def get_contract_details(self, conids):
        return {"secdef": [{"conid": conids[0]}]}

    def get_market_data_history(self, conid, *, period: str, bar: str):
        return {"symbol": conid, "bars": []}

    def get_orders(self):
        return self._orders

    def place_order(self, account_id: str, order):
        self._orders.append(order)
        return {"status": "ok"}

    def cancel_order(self, account_id: str, order_id: str):
        return {"status": "cancelled", "order_id": order_id}

    def get_positions(self, account_id: str):
        return []

    def get_watchlists(self):
        return {"data": {"user_lists": []}}

    def get_watchlist(self, watchlist_id: int):
        return {"id": watchlist_id, "rows": []}

    def delete_watchlist(self, watchlist_id: int):
        return {"status": "deleted"}

    def create_watchlist(self, payload):
        return payload

    def get_scanner_params(self):
        return {
            "instrument_list": [],
            "filter_list": [],
            "scan_type_list": [],
            "location_tree": [],
        }

    def run_scanner(self, payload):
        return {"data": []}

    def close(self) -> None:
        pass


@pytest.fixture()
def stub_client() -> StubClient:
    return StubClient()


@pytest.fixture()
def app(stub_client: StubClient):
    cfg = AppConfig(
        base_api_url="https://localhost:5055/v1/api",
        account_id="U123",
        verify=False,
        request_timeout=5,
    )
    application = create_app(config=cfg, client=stub_client)
    application.config.update(TESTING=True)
    return application


@pytest.fixture()
def client(app):
    return app.test_client()
