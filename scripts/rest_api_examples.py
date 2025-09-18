"""Legacy entry point kept for backwards compatibility.

Run ``ibkr-rest --help`` for the modern Typer-based CLI that replaces this
script. Invoking this module still executes the same CLI for convenience.
"""

from ibkr_web.cli import main


if __name__ == "__main__":  # pragma: no cover - convenience entry point
    main()
