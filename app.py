"""Standalone Streamlit entry point for the Module 7 Question 1 application.

Run from this repository root with ``streamlit run app.py``.
"""
from __future__ import annotations

import sys
from pathlib import Path

_SRC = Path(__file__).resolve().parent / "src"
if str(_SRC) not in sys.path:
    sys.path.insert(0, str(_SRC))

from module7.webapp.pages import get_pages  # noqa: E402
from module7.webapp.registry import collect_pages  # noqa: E402
from module7.webapp.shell import render_app  # noqa: E402


def main() -> None:
    """Collect and render the Module 7 Question 1 pages."""
    render_app(collect_pages([get_pages]))


if __name__ == "__main__":
    main()
