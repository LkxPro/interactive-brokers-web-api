"""Compatibility wrapper for legacy imports.

This module exists so Docker and older tooling that import `webapp.app`
continue to function. The real application now lives in the `ibkr_web`
package.
"""

from ibkr_web.app import create_app

app = create_app()
