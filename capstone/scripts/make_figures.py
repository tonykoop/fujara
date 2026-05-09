#!/usr/bin/env python3
"""Render the comparison plots embedded in capstone-deck.md.

Produces:
  capstone/figures/aspect-ratio-geometry.png
  capstone/figures/structural-modes.png
  capstone/figures/cavity-modes.png
  capstone/figures/coupled-vs-modal.png
"""

from __future__ import annotations

import csv
import sys
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

from fujara_design_math import (  # noqa: E402
    analytic_pipe_modes,
    default_capstone_rows,
    free_free_beam_modes,
    row_tag,
)


FIG_ROOT = HERE.parent / "figures"
MODAL_ROOT = HERE.parent / "modal"
ACOUSTIC_ROOT = HERE.parent / "acoustic"


def _load_modes_csv(path: Path) -> list[dict]:
    with path.open() as fh:
        return list(csv.DictReader(fh))


def plot_geometry(rows):
    fig, ax = plt.subplots(figsize=(7, 4))
    ratios = [r.aspect_ratio for r in rows]
    bore_in = [r.bore_diameter_in for r in rows]
    wall_in = [r.wall_thickness_in for r in rows]
    length_in = [r.bore_length_in for r in rows]

    ax.plot(ratios, bore_in, "o-", label="bore D (in)")
    ax.plot(ratios, wall_in, "s-", label="wall t (in)")
    ax2 = ax.twinx()
    ax2.plot(ratios, length_in, "^--", color="tab:gray", label="bore L (in)")
    ax2.set_ylabel("bore length L (in)")
    ax.set_xlabel("aspect ratio L:D")
    ax.set_ylabel("D, t (in)")
    ax.set_title("A2 fujara — geometry vs aspect ratio")
    lines, labels = ax.get_legend_handles_labels()
    lines2, labels2 = ax2.get_legend_handles_labels()
    ax.legend(lines + lines2, labels + labels2, loc="center right")
    ax.grid(True, alpha=0.3)
    fig.tight_layout()
    out = FIG_ROOT / "aspect-ratio-geometry.png"
    fig.savefig(out, dpi=140)
    plt.close(fig)
    return out


def plot_structural(rows):
    fig, ax = plt.subplots(figsize=(7, 4))
    ratios = [r.aspect_ratio for r in rows]
    for mode in range(5):
        analytic = [free_free_beam_modes(r, n_modes=5)[mode] for r in rows]
        ax.plot(ratios, analytic, "o-", label=f"mode {mode + 1}")
    ax.set_xlabel("aspect ratio L:D")
    ax.set_ylabel("structural mode frequency (Hz)")
    ax.set_title("Free-free Euler-Bernoulli bending modes (wooden tube)")
    ax.legend(loc="best", ncol=2)
    ax.grid(True, alpha=0.3)
    fig.tight_layout()
    out = FIG_ROOT / "structural-modes.png"
    fig.savefig(out, dpi=140)
    plt.close(fig)
    return out


def plot_cavity(rows):
    fig, ax = plt.subplots(figsize=(7, 4))
    ratios = [r.aspect_ratio for r in rows]
    for mode in range(5):
        analytic = [analytic_pipe_modes(r, n_modes=5)[mode] for r in rows]
        ax.plot(ratios, analytic, "o-", label=f"mode {mode + 1}")
    ax.set_xlabel("aspect ratio L:D")
    ax.set_ylabel("cavity mode frequency (Hz)")
    ax.set_title("Open-open cavity modes (rigid wall)")
    ax.legend(loc="best", ncol=2)
    ax.grid(True, alpha=0.3)
    fig.tight_layout()
    out = FIG_ROOT / "cavity-modes.png"
    fig.savefig(out, dpi=140)
    plt.close(fig)
    return out


def plot_coupled_vs_modal(rows):
    fig, ax = plt.subplots(figsize=(7, 4))
    ratios = [r.aspect_ratio for r in rows]

    # Read FEM cavity output and compute the coupled-vs-modal-only
    # delta in cents per mode, per row.
    cents_by_mode = [[] for _ in range(5)]
    for r in rows:
        path = ACOUSTIC_ROOT / row_tag(r) / "cavity_modes.csv"
        for record in _load_modes_csv(path):
            idx = int(record["mode_index"]) - 1
            if idx < 5:
                cents_by_mode[idx].append(float(record["delta_cents"]))

    for i, series in enumerate(cents_by_mode):
        if series:
            ax.plot(ratios, series, "o-", label=f"mode {i + 1}")
    ax.axhline(0, color="black", lw=0.6)
    ax.set_xlabel("aspect ratio L:D")
    ax.set_ylabel("coupled - modal-only (cents)")
    ax.set_title("Wall-flexibility pull (coupled vs rigid wall)")
    ax.legend(loc="best", ncol=2)
    ax.grid(True, alpha=0.3)
    fig.tight_layout()
    out = FIG_ROOT / "coupled-vs-modal.png"
    fig.savefig(out, dpi=140)
    plt.close(fig)
    return out


def main() -> int:
    FIG_ROOT.mkdir(parents=True, exist_ok=True)
    rows = default_capstone_rows()
    written = [
        plot_geometry(rows),
        plot_structural(rows),
        plot_cavity(rows),
        plot_coupled_vs_modal(rows),
    ]
    rel = HERE.parent.parent
    for path in written:
        print(f"wrote {path.relative_to(rel)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
