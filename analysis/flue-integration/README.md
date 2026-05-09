# Flue integration variant study (fujara #2)

**Readiness:** L2 design comparison + first-pass 1-D Webster re-run.
**Physics gate:** met (re-uses the merged capstone PR #3 solver).
**Empirical gate:** deferred — no prototype data, no L4 claim.

## Question

The current G2 fujara build has three voicing parts above the labium:

- `G2FujaraTop` / `FujaraBottomG2` — the two halves of the split-blank
  body. Already carry the long fipple-ramp / flue-dam features
  (~349 mm / ~393 mm long) milled into their inside faces.
- `G2FujaraFlue` — a 31.75 mm × 53.975 mm cylindrical block plugged
  into the bore at the head joint. Carries the air duct + windway
  engagement.
- `G2FujaraFluePlug` — a removable wax-sealed plug for fine-tuning.

This study asks: **can the G2FujaraFlue block be eliminated and its
features rolled into G2FujaraTop + FujaraBottomG2?**

## Variants compared

| | Separate-flue (current G2) | Integrated-flue |
|---|---|---|
| Body parts above labium | top + bottom + flue block | top + bottom |
| Permanent glue joints in head | 3 (top↔bottom, top↔flue, bottom↔flue) | 1 (top↔bottom) |
| Flue plug retained? | yes (wax-sealed) | yes (wax-sealed) |
| Active resonator | labium → foot (unchanged) | labium → foot (unchanged) |
| Bore geometry below labium | unchanged | unchanged |

The flue plug stays in both variants — it is the user-facing voicing
adjustment, not a manufacturing artifact.

## Findings (TL;DR)

1. **Acoustically a wash.** The 1-D Webster solver reports
   `delta_modal = 0.000 Hz` and `delta_coupled = 0.000 Hz` across all
   five modes. Both variants share the same labium-to-foot length, the
   same bore ID, and the same wall geometry — the only inputs the 1-D
   model sees. See [acoustic-impact.md](acoustic-impact.md).

2. **Geometry is interchangeable.** The integrated variant absorbs the
   54 mm flue-block features as additional pocket cuts on the inside
   faces of the two body halves — the split-blank construction already
   exposes both faces to CNC. See
   [geometry-comparison.md](geometry-comparison.md).

3. **Manufacturing trades complexity for finality.** Integrated drops
   one part, two glue joints, and one alignment fixture. In exchange,
   the windway becomes irreplaceable once the body halves are glued —
   the separate-flue variant lets you swap a recut block without
   rebuilding the whole instrument. See
   [manufacturing-impact.md](manufacturing-impact.md).

4. **Recommendation:** integrated wins for production runs once the
   voicing literals stabilise. Separate wins during prototyping and
   for repair-friendliness. See [recommendation.md](recommendation.md).

## Reproduce

The cavity FEM re-runs the merged capstone solver against the same
A2 baseline (110 Hz, 50:1 aspect):

```
python3 analysis/flue-integration/scripts/integrated_flue_cavity.py
```

Outputs land in `analysis/flue-integration/data/`. The script imports
from `capstone/scripts/{fujara_design_math,acoustic_cavity_fem}.py` —
no solver code is duplicated.

## Files

- [README.md](README.md) — this overview
- [geometry-comparison.md](geometry-comparison.md) — side-by-side
  dimension table
- [acoustic-impact.md](acoustic-impact.md) — Webster re-run + sensitivity
- [manufacturing-impact.md](manufacturing-impact.md) — joinery, jig, tolerance
- [recommendation.md](recommendation.md) — when each variant wins
- `scripts/integrated_flue_cavity.py` — comparison driver
- `data/integrated-vs-separate.csv` — per-mode delta
- `data/sensitivity-end-correction.csv` — f0 vs ±2 mm end-correction shift

## Hardware-development gate

| Gate | Status | Evidence |
|---|---|---|
| Math | met | Reuses capstone closed-form geometry |
| Physics | met | 1-D Webster + wall-flex correction re-run |
| Empirical | deferred | Requires a prototype of the integrated variant |

The deferred empirical gate is the honest line. The 1-D model cannot
distinguish the two variants; promotion to L4 requires a built-and-blown
integrated-flue body and a comparison of measured f0, second-mode
purity, and overblow stability against the existing G2 build.
