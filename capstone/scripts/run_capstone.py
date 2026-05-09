#!/usr/bin/env python3
"""End-to-end capstone driver.

Runs the design table, structural modal solve, acoustic cavity solve,
and figure rendering in one shot.  Use this for reproducibility — the
PR's "Validation run" line cites the SHA256 of this script's emitted
artefacts (see capstone/REPRODUCIBILITY.md).
"""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent

STEPS = (
    "generate_design_table.py",
    "modal_fem.py",
    "acoustic_cavity_fem.py",
    "make_figures.py",
)


def main() -> int:
    for step in STEPS:
        path = HERE / step
        print(f"\n=== {step} ===")
        result = subprocess.run([sys.executable, str(path)], check=False)
        if result.returncode != 0:
            print(f"step {step} failed with exit {result.returncode}")
            return result.returncode
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
