"""Application configuration helpers."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Optional, Union
import os


def _env_bool(name: str, default: bool = False) -> bool:
    """Return a boolean for an environment variable."""
    value = os.getenv(name)
    if value is None:
        return default
    return value.lower() in {"1", "true", "t", "yes", "y", "on"}


@dataclass
class AppConfig:
    """Holds runtime configuration derived from the environment."""

    base_api_url: str = "https://localhost:5055/v1/api"
    account_id: Optional[str] = None
    verify: Union[bool, str] = False
    request_timeout: int = 10

    @classmethod
    def from_env(cls) -> "AppConfig":
        base_api_url = os.getenv("IBKR_BASE_URL", cls.base_api_url)
        account_id = os.getenv("IBKR_ACCOUNT_ID")
        cert_path = os.getenv("IBKR_CERT_PATH")
        verify_ssl = _env_bool("IBKR_VERIFY_SSL", default=False)

        if cert_path:
            verify: Union[bool, str] = cert_path
        else:
            verify = verify_ssl

        timeout_env = os.getenv("IBKR_REQUEST_TIMEOUT")
        try:
            timeout = int(timeout_env) if timeout_env else cls.request_timeout
        except ValueError:
            timeout = cls.request_timeout

        return cls(
            base_api_url=base_api_url.rstrip("/"),
            account_id=account_id,
            verify=verify,
            request_timeout=timeout,
        )
