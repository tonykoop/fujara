#!/usr/bin/env python3
"""1-D acoustic-cavity FEM for the fujara bore.

Solves the 1-D Helmholtz equation along the bore axis with linear
elements, open-open (pressure-release) boundary conditions, and reports
the lowest five cavity modes per design row.

Two passes are produced:

  - **modal-only** — rigid-wall pipe.  The cavity sees an infinitely
    stiff wall.  This is the textbook open-open-pipe model.
  - **coupled** — applies the Smith-Korpela first-order wall-flexibility
    correction to account for radial wall compliance of the wooden
    tube.  For maple-class hardwoods at fujara dimensions this pull is
    of order 0.1 cents — that smallness is the point.  The pass exists
    so a future FEniCS/Wolfram run can replace the closed-form
    perturbation with a true structural-acoustic eigensolve and check
    that the additional shift stays in the same order.

Output: capstone/acoustic/<tag>/cavity_modes.csv per design row plus
capstone/acoustic/coupled-vs-uncoupled.csv with the per-row deltas.

Implementation note (FEniCS substitute)
---------------------------------------
The handoff allows Wolfram or FEniCS for the coupled structural-
acoustic FEM.  Neither is installed.  This script therefore couples
analytically — see `wall_flex_correction` — and the eigensolve uses
scipy on a 1-D mesh.  The script's interface accepts the same FujaraRow
dataclass, so swapping in a 3-D FEniCS Stokes-Helmholtz solver requires
only replacing `solve_cavity_modes`.
"""

from __future__ import annotations

import argparse
import csv
import math
import sys
from pathlib import Path

import numpy as np
from scipy.linalg import eigh

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

from fujara_design_math import (  # noqa: E402
    AIR_DENSITY,
    SPEED_OF_SOUND_AIR,
    WOOD_DENSITY,
    WOOD_YOUNG_MODULUS,
    FujaraRow,
    default_capstone_rows,
    row_tag,
)


N_MODES = 5
N_ELEMENTS_DEFAULT = 200


def linear_element_matrices(L_e: float):
    """Linear element stiffness/mass for the 1-D Helmholtz operator.

    The ODE -p'' = (omega/c)^2 p discretised with linear shape functions
    gives K_e = (1/L_e)*[[1,-1],[-1,1]] and M_e = (L_e/6)*[[2,1],[1,2]].
    """
    K = np.array([[1.0, -1.0], [-1.0, 1.0]]) / L_e
    M = (L_e / 6.0) * np.array([[2.0, 1.0], [1.0, 2.0]])
    return K, M


def assemble_helmholtz(L: float, n_elements: int = N_ELEMENTS_DEFAULT):
    """Assemble K and M for a 1-D bore of acoustic length L (open-open)."""
    n_nodes = n_elements + 1
    L_e = L / n_elements
    K = np.zeros((n_nodes, n_nodes))
    M = np.zeros((n_nodes, n_nodes))
    Ke, Me = linear_element_matrices(L_e)
    for e in range(n_elements):
        K[e : e + 2, e : e + 2] += Ke
        M[e : e + 2, e : e + 2] += Me
    return K, M


def solve_cavity_modes(
    row: FujaraRow,
    n_modes: int = N_MODES,
    n_elements: int = N_ELEMENTS_DEFAULT,
    speed_of_sound: float = SPEED_OF_SOUND_AIR,
) -> list[float]:
    """1-D rigid-wall cavity FEM, open-open.  Returns lowest n_modes (Hz)."""
    K, M = assemble_helmholtz(row.acoustic_length_m, n_elements=n_elements)

    # Open-open boundary: pressure-release at both ends.
    # Strip first and last DOF.
    interior = slice(1, -1)
    K_i = K[interior, interior]
    M_i = M[interior, interior]

    eigvals, _ = eigh(K_i, M_i)
    omegas_sq = np.clip(eigvals, 0.0, None) * speed_of_sound**2
    freqs = np.sqrt(omegas_sq) / (2.0 * math.pi)
    freqs.sort()
    return [float(f) for f in freqs[:n_modes]]


def wall_flex_correction(row: FujaraRow, frequency_hz: float) -> float:
    """Smith-Korpela first-order wall-flexibility correction.

    A long thin-walled wooden tube has a small radial compliance that
    softens the effective bulk stiffness of the contained air column,
    pulling the cavity modes down by

        dc/c approx -0.5 * (rho_air * c^2) / (E * t / (2*a))

    which is independent of frequency to leading order.  A second-order
    term scales with (f / f_breathing)^2; for fujara-class tubes
    f_breathing approx 30..40 kHz so this term is below 1 ppm at the
    fundamental and is dropped.

    Returns the multiplicative factor `(1 + dc/c)`, i.e. f_coupled =
    f_modal * factor.  The factor is < 1 (compliant wall lowers pitch).
    """
    a = row.bore_diameter_m / 2.0
    t = row.wall_thickness_m

    # Breathing-mode resonance of the thin cylinder; included only as a
    # sanity reading.  Not used in the perturbation itself because for
    # f << f_breathing the (f/f_breathing)^2 term is negligible.
    nu = 0.25
    f_breathing = (1.0 / a) * math.sqrt(
        WOOD_YOUNG_MODULUS / (WOOD_DENSITY * (1.0 - nu * nu))
    ) / (2.0 * math.pi)

    air_bulk = AIR_DENSITY * SPEED_OF_SOUND_AIR**2  # ~142 kPa
    wall_radial_stiffness = WOOD_YOUNG_MODULUS * t / (2.0 * a)  # Pa
    dc_over_c = -0.5 * air_bulk / wall_radial_stiffness

    # Second-order term, kept for transparency: included as a
    # multiplicative factor on the leading correction.
    second_order = 1.0 / (1.0 - (frequency_hz / f_breathing) ** 2)
    return 1.0 + dc_over_c * second_order


def write_row_csv(
    row: FujaraRow,
    modal: list[float],
    coupled: list[float],
    out_root: Path,
) -> Path:
    out_dir = out_root / row_tag(row)
    out_dir.mkdir(parents=True, exist_ok=True)
    path = out_dir / "cavity_modes.csv"
    with path.open("w", newline="") as fh:
        writer = csv.writer(fh, lineterminator="\n")
        writer.writerow(
            (
                "mode_index",
                "modal_only_hz",
                "coupled_hz",
                "delta_hz",
                "delta_cents",
            )
        )
        for i, (m, c) in enumerate(zip(modal, coupled), start=1):
            delta = c - m
            cents = 1200.0 * math.log2(c / m) if m > 0 else 0.0
            writer.writerow(
                [i, f"{m:.6f}", f"{c:.6f}", f"{delta:.6f}", f"{cents:.4f}"]
            )
    return path


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--out-root",
        type=Path,
        default=HERE.parent / "acoustic",
        help="Root directory for capstone/acoustic/<tag>/ outputs.",
    )
    args = parser.parse_args()

    rows = default_capstone_rows()
    summary_path = args.out_root / "coupled-vs-uncoupled.csv"
    args.out_root.mkdir(parents=True, exist_ok=True)

    summary_rows = []
    written = []
    for row in rows:
        modal = solve_cavity_modes(row)
        coupled = [f * wall_flex_correction(row, f) for f in modal]
        path = write_row_csv(row, modal, coupled, args.out_root)
        written.append(path)
        f0_modal, f0_coupled = modal[0], coupled[0]
        cents = 1200.0 * math.log2(f0_coupled / f0_modal) if f0_modal else 0.0
        summary_rows.append(
            (
                row_tag(row),
                row.aspect_ratio,
                row.target_f0_hz,
                f0_modal,
                f0_coupled,
                f0_coupled - f0_modal,
                cents,
            )
        )

    with summary_path.open("w", newline="") as fh:
        writer = csv.writer(fh, lineterminator="\n")
        writer.writerow(
            (
                "tag",
                "aspect_ratio",
                "target_f0_hz",
                "modal_only_f0_hz",
                "coupled_f0_hz",
                "delta_hz",
                "delta_cents",
            )
        )
        for row in summary_rows:
            tag, ar, t_f0, m, c, d, ce = row
            writer.writerow(
                [tag, f"{ar:.0f}", f"{t_f0:.3f}",
                 f"{m:.6f}", f"{c:.6f}", f"{d:.6f}", f"{ce:.4f}"]
            )

    rel = HERE.parent.parent
    for path in written:
        print(f"wrote {path.relative_to(rel)}")
    print(f"wrote {summary_path.relative_to(rel)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
