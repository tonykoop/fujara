#!/usr/bin/env python3
"""Structural modal scaffold for the fujara wooden tube.

For each design-table row this writes capstone/modal/<tag>/modes.csv with the
five lowest non-rigid-body bending modes of the tube.

Implementation notes
--------------------
The handoff allows Wolfram or open-source FEM (FEniCS, mph for Comsol).
Neither is installed in the worktree's Python environment.  As a
substitute this script uses two complementary closed-form / scipy
solvers, both of which a future FEniCS/Wolfram run is expected to
reproduce:

  1. **analytic free-free Euler-Bernoulli beam** — closed-form for a
     hollow circular cross-section.  Lowest five non-rigid bending modes.
  2. **scipy 1D FE eigensolve** — assembles the standard cubic-Hermite
     stiffness/mass matrices for the same Euler-Bernoulli beam and solves
     the generalised eigenvalue problem.  This validates the analytic
     formula and stands in for a 3-D shell FEM until FEniCS or Wolfram
     is wired in.

The script is structured so that swapping in a richer solver requires
only replacing `compute_modes` — the I/O contract (one CSV per design
row, columns `mode_index, frequency_hz, source`) is stable.
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
    WOOD_DENSITY,
    WOOD_YOUNG_MODULUS,
    FujaraRow,
    default_capstone_rows,
    free_free_beam_modes,
    row_tag,
)


N_MODES = 5
N_ELEMENTS_DEFAULT = 80


def _hermite_element_matrices(L_e: float, EI: float, rho_A: float):
    """Return cubic-Hermite element K and M for one Euler-Bernoulli element."""
    K = (EI / L_e**3) * np.array(
        [
            [12.0,       6.0 * L_e,    -12.0,       6.0 * L_e],
            [6.0 * L_e,  4.0 * L_e**2, -6.0 * L_e,  2.0 * L_e**2],
            [-12.0,      -6.0 * L_e,    12.0,      -6.0 * L_e],
            [6.0 * L_e,  2.0 * L_e**2, -6.0 * L_e,  4.0 * L_e**2],
        ]
    )
    M = (rho_A * L_e / 420.0) * np.array(
        [
            [156.0,      22.0 * L_e,    54.0,     -13.0 * L_e],
            [22.0 * L_e, 4.0 * L_e**2,  13.0 * L_e, -3.0 * L_e**2],
            [54.0,       13.0 * L_e,    156.0,    -22.0 * L_e],
            [-13.0 * L_e, -3.0 * L_e**2, -22.0 * L_e, 4.0 * L_e**2],
        ]
    )
    return K, M


def fem_free_free_modes(
    row: FujaraRow,
    n_modes: int = N_MODES,
    n_elements: int = N_ELEMENTS_DEFAULT,
    young_modulus: float = WOOD_YOUNG_MODULUS,
    wood_density: float = WOOD_DENSITY,
) -> list[float]:
    """Hermite-element FEM eigensolve, free-free boundary, hollow circular section."""

    od = row.bore_diameter_m + 2.0 * row.wall_thickness_m
    id_ = row.bore_diameter_m
    moment_of_inertia = math.pi / 64.0 * (od**4 - id_**4)
    cross_section_area = math.pi / 4.0 * (od**2 - id_**2)
    EI = young_modulus * moment_of_inertia
    rho_A = wood_density * cross_section_area

    L_e = row.bore_length_m / n_elements
    n_nodes = n_elements + 1
    n_dof = 2 * n_nodes  # (w, theta) per node

    K = np.zeros((n_dof, n_dof))
    M = np.zeros((n_dof, n_dof))
    Ke, Me = _hermite_element_matrices(L_e, EI, rho_A)
    for e in range(n_elements):
        i = 2 * e
        K[i : i + 4, i : i + 4] += Ke
        M[i : i + 4, i : i + 4] += Me

    # Free-free: no constraints.  The eigensolve will return two zero (or
    # numerically tiny) rigid-body modes — drop them, then take the next
    # n_modes.
    eigvals, _ = eigh(K, M)
    omegas_sq = np.clip(eigvals, 0.0, None)
    freqs = np.sqrt(omegas_sq) / (2.0 * math.pi)
    freqs.sort()

    # Drop rigid-body modes — first two eigenvalues are ~0 for free-free.
    freqs = freqs[2:]
    return [float(f) for f in freqs[:n_modes]]


def compute_modes(row: FujaraRow) -> list[tuple[int, float, str]]:
    """Return [(mode_index, frequency_hz, source), ...] for one row."""
    analytic = free_free_beam_modes(row, n_modes=N_MODES)
    fem = fem_free_free_modes(row, n_modes=N_MODES)
    out: list[tuple[int, float, str]] = []
    for i, f in enumerate(analytic, start=1):
        out.append((i, f, "analytic_euler_bernoulli"))
    for i, f in enumerate(fem, start=1):
        out.append((i, f, "scipy_hermite_fem"))
    return out


def write_row_csv(row: FujaraRow, modes: list[tuple[int, float, str]], out_root: Path) -> Path:
    out_dir = out_root / row_tag(row)
    out_dir.mkdir(parents=True, exist_ok=True)
    path = out_dir / "modes.csv"
    with path.open("w", newline="") as fh:
        writer = csv.writer(fh, lineterminator="\n")
        writer.writerow(("mode_index", "frequency_hz", "source"))
        for idx, freq, src in modes:
            writer.writerow([idx, f"{freq:.4f}", src])
    return path


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--out-root",
        type=Path,
        default=HERE.parent / "modal",
        help="Root directory for capstone/modal/<tag>/modes.csv outputs.",
    )
    args = parser.parse_args()

    rows = default_capstone_rows()
    written: list[Path] = []
    for row in rows:
        modes = compute_modes(row)
        path = write_row_csv(row, modes, args.out_root)
        written.append(path)

    rel = HERE.parent.parent
    for path in written:
        print(f"wrote {path.relative_to(rel)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
