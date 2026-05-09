# Acoustic impact — separate vs integrated flue

## What the 1-D Webster solver says

Re-running `capstone/scripts/acoustic_cavity_fem.py` (merged in PR #3)
on both variants at the A2 / 50:1 baseline:

| Mode | Separate modal (Hz) | Integrated modal (Hz) | Δ (Hz) | Δ (cents) |
|---|---|---|---|---|
| 1 | 110.001131 | 110.001131 | 0.000000 | 0.0000 |
| 2 | 220.009047 | 220.009047 | 0.000000 | 0.0000 |
| 3 | 330.030535 | 330.030535 | 0.000000 | 0.0000 |
| 4 | 440.072381 | 440.072381 | 0.000000 | 0.0000 |
| 5 | 550.141372 | 550.141372 | 0.000000 | 0.0000 |

Wall-flex coupled values match identically too — same OD, ID, wall
thickness, so the Smith-Korpela perturbation is the same −0.05 cents
on both. Source: `data/integrated-vs-separate.csv`.

**The 1-D model cannot distinguish the two variants.** This is not a
bug — it is the model telling you correctly that the inputs it cares
about (acoustic length, cross-section, wall compliance) are identical
between variants. The flue block sits above the labium, outside the
resonating cavity; the labium-to-foot length is unchanged.

## Why the model is blind here

The 1-D Helmholtz cavity FEM in `acoustic_cavity_fem.py` discretises
the bore axis with linear elements between two pressure-release
boundaries (open foot, open labium). Its inputs reduce to:

1. `acoustic_length_m` — labium to foot, plus end corrections.
2. Effective speed of sound (= air sound speed × wall-flex factor).
3. Number of elements (mesh resolution).

None of those carry information about whether the head-zone occlusion
is one piece of wood or three. The flue block is geometrically
"upstream" of the labium boundary the solver imposes.

## Where the acoustic difference actually lives

Three second-order effects sit below the 1-D model's resolution:

### 1. Labium end correction

The end correction at the labium reflects the radiation impedance the
air column sees at the open boundary. It depends on:

- Aperture geometry (windway width × bore radius).
- Local wall stiffness right at the labium edge.
- 3-D flow geometry above the labium (the air jet's reflection back
  into the cavity).

The integrated variant has a windway milled into wood with no glue
joint at the labium edge; the separate variant has the windway
through a separately-glued block. **Plausible end-correction shift:
±2 mm per side.** Anything bigger would imply a different labium
position, which is a different design.

The sensitivity sweep (`data/sensitivity-end-correction.csv`):

| ΔL_eff (per side, mm) | f0 (Hz) | Δf0 (Hz) | Δf0 (cents) |
|---|---|---|---|
| −2.0 | 110.284 | +0.283 | +4.45 |
| −1.0 | 110.142 | +0.141 | +2.22 |
|  0.0 | 110.001 |  0.000 |  0.00 |
| +1.0 | 109.860 | −0.141 | −2.22 |
| +2.0 | 109.720 | −0.281 | −4.44 |

Bound: **±5 cents at the fundamental** for a ±2 mm end-correction
shift. That is well inside the voicing-literal tweak budget — the
fipple-height literal alone routinely moves f0 by tens of cents during
prototyping. Either variant lands in the voicing-tunable region.

### 2. Wall flexibility near the labium

The Smith-Korpela correction in `wall_flex_correction()` (already
merged) uses uniform wall properties along the bore. In the separate
variant, the head zone has the body wall + the flue block stacked
together → effectively higher local stiffness over the 54 mm head zone.
In the integrated variant, the head zone has only the body wall.

For wood at fujara dimensions the wall-flex factor is already only
−0.05 cents; the head-zone-only contribution is a fraction of that,
**below 0.05 cents**. Smaller than rounding noise on the 1-D solve.

### 3. Mode purity / overblow stability

Not captured by the linear eigenvalue model at all. A jet-driven flute
overblows cleanly when the higher modes are harmonically aligned and
the labium impedance is consistent across modes. Local
labium-zone construction can shift the impedance asymmetrically
between odd and even modes.

This is beyond what the L2-L3 study can measure. It is the empirical
gate.

## Honest summary

| Claim | Confidence |
|---|---|
| f0_modal is identical to within rounding | high — 1-D solver result |
| Labium end correction may shift ±2 mm | medium — geometric plausibility |
| f0 shift bounded at ±5 cents | high — sensitivity sweep |
| Mode purity / overblow may differ | unknown — needs prototype |
| Variant choice is acoustically a wash | high, conditional on voicing-literal re-trim |

The defensible L3 statement: **integration does not break the
acoustic design.** The voicing-literal re-trim that already happens
between any two prototypes is enough headroom to absorb any windway
geometry shift the integration introduces.

## Next-step instrumentation (if pursued)

A built integrated prototype should be measured against the existing
G2 build for:

1. f0 with all toneholes closed, microphone at 200 mm off the foot.
2. Second-mode purity (overblow octave): record amplitude vs played
   frequency stability over 5 seconds.
3. Spectral centroid of sustained low-G2 fundamental — a rough
   proxy for labium-jet stability.

Without those measurements, claim only L3.
