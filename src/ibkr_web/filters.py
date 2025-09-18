"""Template filter registrations."""

from __future__ import annotations

import time
from typing import Any

from flask import Flask


def register_filters(app: Flask) -> None:
    @app.template_filter("ctime")
    def _ctime_filter(value: Any) -> str:
        try:
            timestamp = float(value) / 1000.0
        except (TypeError, ValueError):
            return ""
        return time.ctime(timestamp)
