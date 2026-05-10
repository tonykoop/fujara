#!/usr/bin/env python3
"""Re-run the capstone 1-D Webster cavity FEM on the integrated-flue variant.

Reuses `capstone/scripts/acoustic_cavity_fem.py` and
`capstone/scripts/fujara_design_math.py` from PR #3 — does NOT reimplement
the solver.

Two variants compared at the same A2 target (110 Hz):

  separate  — current G2 build: G2FujaraFlue is a 53.975 mm cylindrical
              block plugged into the bore above the labium. The
              resonating cavity is from the labium to the open foot.

  integrated — Flue_Top features cut directly into the inside faces of
              G2FujaraTop + FujaraBottomG2 before glue-up. No separate
              block. Same labium position, so same resonating cavity
              length to leading order.

The 1-D Webster equation with rigid walls cares only about acoustic
length and cross-section. Both variants share the same labium-to-foot
length and the same bore ID, so f0_modal is identical to within
rounding. The acoustic story is therefore in the second-order terms:

  - end_correction at the labium end (depends on local windway
    geometry — see SENSITIVITY_DELTA_L_M)
  - wall flexibility correction (identical: same OD, ID, wall thickness)

Output:
  data/integrated-vs-separate.csv  — per-mode delta table
  data/sensitivity-end-correction.csv — f0 sensitivity to ±2 mm shift
                                        in labium-end correction
"""

from __future__ import annotations

import csv
import math
import sys
from dataclasses import replace
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[3]
CAPSTONE_SCRIPTS = REPO_ROOT / "capstone" / "scripts"
sys.path.insert(0, str(CAPSTONE_SCRIPTS))

from fujara_design_math import (  # noqa: E402
    DEFAULT_TARGET_F0_HZ,
    FujaraRow,
    design_row,
)
from acoustic_cavity_fem import (  # noqa: E402
    solve_cavity_modes,
    wall_flex_correction,
)


# G2FujaraFlue cylindrical block axial length, from
# CAD/fujara-body/G2Fujara_Assembly.SLDASM_dimensions.csv (height@cylinder
# of G2FujaraFlue.Part = 53.975 mm = 2.125").
FLUE_BLOCK_AXIAL_LENGTH_M = 0.053975

# 50:1 baseline matches the existing single-config G2 build.
BASELINE_ASPECT_RATIO = 50.0

# Sensitivity sweep on labium-end correction. The integrated variant
# changes the local windway geometry (a milled slot in the wood face vs
# a duct through a separate block); a few-mm shift in the effective end
# correction is plausible without touching the resonating-length fix.
SENSITIVITY_DELTA_L_M = (-0.002, -0.001, 0.0, +0.001, +0.002)


def labium_to_foot_length_m(row: FujaraRow) -> float:
    """Resonating cavity length, labium to foot.

    For both variants this is the bore_length_m of the design row — the
    flue block sits ABOVE the labium and is acoustically outside the
    resonating cavity. Recorded explicitly here so the variants stay
    distinguishable when the cross-section assumption is later relaxed.
    """
    return row.bore_length_m


def integrated_acoustic_length_m(row: FujaraRow, delta_shift_m: float = 0.0) -> float:
    """Acoustic length for the integrated variant.

    Same labium-to-foot length as separate. End correction at the
    labium end carries an optional `delta_shift_m` perturbation to
    represent local windway-geometry differences.
    """
    return row.acoustic_length_m + 2.0 * delta_shift_m


def cents(f_target: float, f_ref: float) -> float:
    if f_ref <= 0 or f_target <= 0:
        return 0.0
    return 1200.0 * math.log2(f_target / f_ref)


def write_per_mode_comparison(
    row_sep: FujaraRow,
    row_int: FujaraRow,
    out_path: Path,
) -> None:
    modal_sep = solve_cavity_modes(row_sep)
    modal_int = solve_cavity_modes(row_int)
    coupled_sep = [f * wall_flex_correction(row_sep, f) for f in modal_sep]
    coupled_int = [f * wall_flex_correction(row_int, f) for f in modal_int]

    out_path.parent.mkdir(parents=True, exist_ok=True)
    with out_path.open("w", newline="") as fh:
        w = csv.writer(fh, lineterminator="\n")
        w.writerow(
            [
                "mode_index",
                "separate_modal_hz",
                "integrated_modal_hz",
                "delta_modal_hz",
                "delta_modal_cents",
                "separate_coupled_hz",
                "integrated_coupled_hz",
                "delta_coupled_hz",
                "delta_coupled_cents",
            ]
        )
        for i, (ms, mi, cs, ci) in enumerate(
            zip(modal_sep, modal_int, coupled_sep, coupled_int), start=1
        ):
            w.writerow(
                [
                    i,
                    f"{ms:.6f}",
                    f"{mi:.6f}",
                    f"{mi - ms:.6f}",
                    f"{cents(mi, ms):.4f}",
                    f"{cs:.6f}",
                    f"{ci:.6f}",
                    f"{ci - cs:.6f}",
                    f"{cents(ci, cs):.4f}",
                ]
            )


def write_end_correction_sensitivity(
    row: FujaraRow, out_path: Path
) -> None:
    """How much does f0 move if the integrated windway shifts the
    labium-end correction by a few mm?
    """
    f0_baseline = solve_cavity_modes(row)[0]
    out_path.parent.mkdir(parents=True, exist_ok=True)
    with out_path.open("w", newline="") as fh:
        w = csv.writer(fh, lineterminator="\n")
        w.writerow(
            [
                "delta_end_correction_m_per_side",
                "acoustic_length_m",
                "f0_modal_hz",
                "f0_delta_hz",
                "f0_delta_cents",
            ]
        )
        for d in SENSITIVITY_DELTA_L_M:
            row_perturbed = replace(
                row,
                acoustic_length_m=row.acoustic_length_m + 2.0 * d,
            )
            f0 = solve_cavity_modes(row_perturbed)[0]
            w.writerow(
                [
                    f"{d:+.4f}",
                    f"{row_perturbed.acoustic_length_m:.6f}",
                    f"{f0:.6f}",
                    f"{f0 - f0_baseline:.6f}",
                    f"{cents(f0, f0_baseline):.4f}",
                ]
            )


def main() -> int:
    out_dir = Path(__file__).resolve().parents[1] / "data"

    row_sep = design_row(DEFAULT_TARGET_F0_HZ, BASELINE_ASPECT_RATIO)
    # Integrated variant shares geometry to leading order; build a
    # separate FujaraRow so future variants can diverge.
    row_int = design_row(DEFAULT_TARGET_F0_HZ, BASELINE_ASPECT_RATIO)

    write_per_mode_comparison(
        row_sep,
        row_int,
        out_dir / "integrated-vs-separate.csv",
    )
    write_end_correction_sensitivity(
        row_sep,
        out_dir / "sensitivity-end-correction.csv",
    )

    print(f"baseline aspect ratio       : {BASELINE_ASPECT_RATIO}")
    print(f"baseline target f0          : {DEFAULT_TARGET_F0_HZ} Hz")
    print(f"bore diameter               : {row_sep.bore_diameter_m * 1000:.3f} mm")
    print(f"bore length (labium-to-foot): {labium_to_foot_length_m(row_sep) * 1000:.3f} mm")
    print(f"acoustic length             : {row_sep.acoustic_length_m * 1000:.3f} mm")
    print(f"flue block axial length     : {FLUE_BLOCK_AXIAL_LENGTH_M * 1000:.3f} mm")
    print(f"wrote {(out_dir / 'integrated-vs-separate.csv').relative_to(REPO_ROOT)}")
    print(
        f"wrote {(out_dir / 'sensitivity-end-correction.csv').relative_to(REPO_ROOT)}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
