#!/usr/bin/env python3
"""Emit the L:D capstone design-table CSV.

Generates capstone/design-table/aspect-ratio-matrix.csv with one row per
aspect ratio (45 / 50 / 55 / 60) at the A2 fujara design fundamental.

Columns:
  aspect_ratio, target_f0_hz,
  bore_diameter_m, bore_diameter_in,
  bore_length_m,   bore_length_in,
  wall_thickness_m, wall_thickness_in,
  acoustic_length_m, end_correction_per_side_m,
  cavity_volume_m3,
  analytic_mode_1_hz, analytic_mode_2_hz, analytic_mode_3_hz,
  predicted_f0_hz
"""

from __future__ import annotations

import csv
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

from fujara_design_math import (  # noqa: E402
    analytic_pipe_modes,
    default_capstone_rows,
)


OUTPUT = (
    HERE.parent / "design-table" / "aspect-ratio-matrix.csv"
)


COLUMNS = (
    "aspect_ratio",
    "target_f0_hz",
    "bore_diameter_m",
    "bore_diameter_in",
    "bore_length_m",
    "bore_length_in",
    "wall_thickness_m",
    "wall_thickness_in",
    "acoustic_length_m",
    "end_correction_per_side_m",
    "cavity_volume_m3",
    "analytic_mode_1_hz",
    "analytic_mode_2_hz",
    "analytic_mode_3_hz",
    "predicted_f0_hz",
)


def main() -> int:
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    rows = default_capstone_rows()

    with OUTPUT.open("w", newline="") as fh:
        writer = csv.writer(fh, lineterminator="\n")
        writer.writerow(COLUMNS)
        for r in rows:
            modes = analytic_pipe_modes(r, n_modes=3)
            writer.writerow(
                [
                    f"{r.aspect_ratio:.0f}",
                    f"{r.target_f0_hz:.3f}",
                    f"{r.bore_diameter_m:.6f}",
                    f"{r.bore_diameter_in:.4f}",
                    f"{r.bore_length_m:.6f}",
                    f"{r.bore_length_in:.4f}",
                    f"{r.wall_thickness_m:.6f}",
                    f"{r.wall_thickness_in:.4f}",
                    f"{r.acoustic_length_m:.6f}",
                    f"{r.end_correction_per_side_m:.6f}",
                    f"{r.cavity_volume_m3:.6e}",
                    f"{modes[0]:.4f}",
                    f"{modes[1]:.4f}",
                    f"{modes[2]:.4f}",
                    # Predicted bass tone: by construction f0 = mode 1.
                    # Reported separately so a coupled FEM can overwrite it
                    # without touching the analytic-mode columns.
                    f"{modes[0]:.4f}",
                ]
            )

    print(f"wrote {OUTPUT.relative_to(HERE.parent.parent)} ({len(rows)} rows)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
