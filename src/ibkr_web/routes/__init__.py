"""Blueprint registration."""

from __future__ import annotations

from flask import Flask

from . import dashboard, orders, portfolio, scanner, watchlists


def register_blueprints(app: Flask) -> None:
    app.register_blueprint(dashboard.blueprint)
    app.register_blueprint(orders.blueprint)
    app.register_blueprint(portfolio.blueprint)
    app.register_blueprint(scanner.blueprint)
    app.register_blueprint(watchlists.blueprint)
