#!/usr/bin/env python3
"""Run deterministic Module 7 geometry tests."""
from __future__ import annotations

import subprocess
import sys
from pathlib import Path


if __name__ == "__main__":
    root = Path(__file__).resolve().parents[1]
    raise SystemExit(subprocess.call([sys.executable, "-m", "pytest", "tests"], cwd=root))
