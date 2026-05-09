"""Shared math for the fujara L:D capstone study.

Closed-form physics + parametric design-table generation. Used by:
  - generate_design_table.py
  - modal_fem.py
  - acoustic_cavity_fem.py

Conventions:
  - SI throughout (metres, Hz, Pa, kg, kg/m^3).
  - Convenience inch conversions are produced only at I/O boundaries.
"""

from __future__ import annotations

import math
from dataclasses import dataclass


# Reference air properties at 20 C, 1 atm.
SPEED_OF_SOUND_AIR = 343.0          # m/s
AIR_DENSITY = 1.204                 # kg/m^3

# Reference structural properties for stave-glued temperate hardwood
# (values are an average of hard maple / black walnut / cherry — within +/-15%
#  of the species the existing fujara repo already documents).
WOOD_YOUNG_MODULUS = 11.5e9         # Pa  (longitudinal E, average hardwood)
WOOD_DENSITY = 705.0                # kg/m^3

# End correction at the open foot of the pipe (unflanged Levine-Schwinger
# small-radius limit).  Same magnitude is reused at the labium/sound-hole
# end as a first-cut symmetric model.
END_CORRECTION_COEFF = 0.6


# Free-free Euler-Bernoulli beam: roots of cos(beta*L)*cosh(beta*L) = 1.
# Lowest five non-rigid-body modes.
FREE_FREE_BETA_L = (
    4.73004074486270,
    7.85320462409584,
    10.99560783800167,
    14.13716549125746,
    17.27875965739948,
)


@dataclass(frozen=True)
class FujaraRow:
    """A single row of the L:D capstone design table."""

    aspect_ratio: float                 # L_phys / D
    target_f0_hz: float                 # design fundamental
    bore_diameter_m: float              # D, inner diameter
    wall_thickness_m: float             # t
    bore_length_m: float                # L_phys
    acoustic_length_m: float            # L_eff (with end corrections)
    cavity_volume_m3: float             # pi (D/2)^2 L_phys
    end_correction_per_side_m: float    # delta_L (one side)

    # Convenience mirrors in inches for shop-side reading.
    bore_diameter_in: float
    wall_thickness_in: float
    bore_length_in: float


def bore_diameter_for_aspect_ratio(
    target_f0_hz: float,
    aspect_ratio: float,
    speed_of_sound: float = SPEED_OF_SOUND_AIR,
    end_correction_coeff: float = END_CORRECTION_COEFF,
) -> float:
    """Solve for the bore diameter that produces target_f0_hz at the given L:D.

    Open-open pipe with symmetric end correction at both ends:
        L_eff = L_phys + 2 * (end_correction_coeff * a)
    where a = D / 2.  L_phys = aspect_ratio * D.  Solve:
        L_eff = D * (aspect_ratio + end_correction_coeff)
        L_eff = c / (2 * f0)
        =>  D = c / (2 * f0 * (aspect_ratio + end_correction_coeff))
    """
    return speed_of_sound / (
        2.0 * target_f0_hz * (aspect_ratio + end_correction_coeff)
    )


def design_row(
    target_f0_hz: float,
    aspect_ratio: float,
    wall_thickness_ratio: float = 0.22,
) -> FujaraRow:
    """Build one fujara design row.

    wall_thickness_ratio: t / D.  0.22 is the median across the existing
    fujara design table (D2..F#3 spans 21%..25%).
    """
    bore_d = bore_diameter_for_aspect_ratio(target_f0_hz, aspect_ratio)
    bore_l = aspect_ratio * bore_d
    a = bore_d / 2.0
    delta = END_CORRECTION_COEFF * a
    l_eff = bore_l + 2.0 * delta
    t = wall_thickness_ratio * bore_d
    volume = math.pi * a * a * bore_l

    return FujaraRow(
        aspect_ratio=aspect_ratio,
        target_f0_hz=target_f0_hz,
        bore_diameter_m=bore_d,
        wall_thickness_m=t,
        bore_length_m=bore_l,
        acoustic_length_m=l_eff,
        cavity_volume_m3=volume,
        end_correction_per_side_m=delta,
        bore_diameter_in=bore_d / 0.0254,
        wall_thickness_in=t / 0.0254,
        bore_length_in=bore_l / 0.0254,
    )


def analytic_pipe_modes(row: FujaraRow, n_modes: int = 5) -> list[float]:
    """First `n_modes` cavity modes of an open-open pipe (analytic).

    f_n = n * c / (2 * L_eff).  These are also the harmonic-series tones the
    fujara is designed to play by overblowing — the same eigenvalues the
    cavity FEM should reproduce.
    """
    base = SPEED_OF_SOUND_AIR / (2.0 * row.acoustic_length_m)
    return [(n + 1) * base for n in range(n_modes)]


def free_free_beam_modes(
    row: FujaraRow,
    n_modes: int = 5,
    young_modulus: float = WOOD_YOUNG_MODULUS,
    wood_density: float = WOOD_DENSITY,
) -> list[float]:
    """Lowest `n_modes` Euler-Bernoulli free-free bending modes of the wooden
    tube (rigid-body modes excluded).

    f_n = beta_n^2 / (2*pi) * sqrt(E*I / (rho*A))
    """
    od = row.bore_diameter_m + 2.0 * row.wall_thickness_m
    id_ = row.bore_diameter_m
    moment_of_inertia = math.pi / 64.0 * (od**4 - id_**4)
    cross_section_area = math.pi / 4.0 * (od**2 - id_**2)
    radical = math.sqrt(
        young_modulus * moment_of_inertia
        / (wood_density * cross_section_area)
    )
    L = row.bore_length_m
    return [
        ((bL / L) ** 2) / (2.0 * math.pi) * radical
        for bL in FREE_FREE_BETA_L[:n_modes]
    ]


# Standard four-row capstone matrix.
ASPECT_RATIOS = (45.0, 50.0, 55.0, 60.0)


# A2 (110 Hz, MIDI 45) is a popular Slovak fujara key — sits between the
# deepest (D2, ~73 Hz, 94" blank) and the smallest fujarka (F#3, ~185 Hz)
# documented in design-table/fujara-dimensions-parametric.xlsx, and lines
# up with the existing 1.25" bore + 50:1 baseline.
DEFAULT_TARGET_F0_HZ = 110.0


def default_capstone_rows() -> list[FujaraRow]:
    """Build the four canonical L:D rows at A2."""
    return [design_row(DEFAULT_TARGET_F0_HZ, ar) for ar in ASPECT_RATIOS]


def row_tag(row: FujaraRow) -> str:
    """Stable identifier `L<ratio>D<bore_in_mm>` for output filenames."""
    return f"L{int(round(row.aspect_ratio))}D{int(round(row.bore_diameter_m * 1000))}"
