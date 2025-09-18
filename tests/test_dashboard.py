from __future__ import annotations


def test_dashboard_page(client):
    response = client.get("/")
    assert response.status_code == 200
    assert b"dashboard" in response.data.lower()


def test_lookup_endpoint(client):
    response = client.get("/lookup", query_string={"symbol": "AAPL"})
    assert response.status_code == 200
