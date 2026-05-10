# Recommendation — when each variant wins

## Headline

**Integrate the flue once the voicing literals stabilise.** Keep the
separate-flue construction for prototyping, voicing R&D, and any
single-build instrument where the flue might need to come back out.

## When integrated wins

- **Production runs** of a known-good design (the voicing literals in
  `Fujara-Master-Inputs.csv` rows 36–43 don't move between units).
- **Tighter tolerance stack** at the labium (±0.05 mm vs ±0.15 mm)
  matters — e.g., a key where overblow purity is marginal and you need
  the labium-to-bore relationship to be repeatable across copies.
- **Fewer parts to source and machine** — drops one CAM setup and one
  glue-up jig per instrument.
- **Cleaner-looking head joint** — no visible block-to-bore glue line
  inside the breath passage, which some players notice on the
  mirror-side of the windway.

## When separate wins

- **Prototyping a new key.** The flue block is the cheapest thing to
  re-cut when the windway geometry needs another pass. A new block is
  ~30 minutes of CNC; a new body is two days.
- **Voicing literal research.** While the eight voicing literals
  (`fipple_*`, `flue_depth_*`, `flue_dam`) are still being
  calibrated, having the flue as a swappable part is what makes the
  empirical loop fast.
- **One-off instruments** where the player may want a re-voicing in a
  few years. A separate block can be replaced; an integrated windway
  cannot.
- **Repair scenarios.** Anything that cracks, splits, or wears in the
  windway zone is recoverable on the separate variant; the integrated
  variant means rebuild-from-billet.

## Decision rule for the build queue

```
If the design is being re-tested AND/OR voicing-literal headroom is unproven:
    build separate-flue
Else if the design is calibrated AND the build is one of N copies:
    build integrated-flue
```

Concrete instantiation against the current capstone matrix:

| Build target | Variant | Reason |
|---|---|---|
| First A2 prototype with the L:D=50 capstone numbers | separate | first-of-key, voicing literals untested at this aspect |
| Second copy of the same A2 once the first voices clean | integrated | tighter labium stack-up, fewer joints |
| Capstone L:D sweep (45/50/55/60) | separate | each row is an unproven point in the design space |
| D2 / F2 / A2-60in / G2-69in production runs | integrated | all four are calibrated keys in the design table |

## Hardware-development gate triggers

- **Promote integrated to L4** only after a built integrated prototype
  measures within ±5 cents of f0 and within ±2 cents of the second
  mode against a separate-flue twin built from the same boards. This
  is the empirical gate the 1-D model cannot supply.
- **Demote** if the integrated build shows a windway-stability issue
  (jet flutter, uneven overblow) that the separate variant doesn't.
  The retreat path is straightforward: re-bore the body and seat a
  separately-machined flue block. The split-blank construction means
  the body itself isn't lost.

## Open questions for the next round

1. **Plug pocket geometry.** `G2FujaraFluePlug` currently seats into
   `G2FujaraFlue`'s engagement step. In the integrated variant, the
   plug pocket has to be machined into one or both body boards. Does
   the engagement step survive as a single-board pocket, or does it
   need to be split across both boards' inside faces?
2. **Mid-board windway floor.** The acoustic comparison assumed a
   flat windway floor on the bottom board. If a matching pocket on
   the bottom board is preferred (for symmetric jet behaviour), what
   does that cost in CNC time?
3. **Glue-line position vs windway.** The split-blank glue line runs
   the full body length, including across the windway zone. Does the
   glue line cross the windway slot? If so, the slot's edges
   straddle a glue joint, which is a potential failure plane. The
   alternative is to widen the windway pocket on the top board only,
   so the slot lives entirely above the glue line — which is the
   geometry assumed in the current analysis.

These three are the right questions for an L4 prototype to answer.
None of them is a blocker — the L2-L3 case for integration is solid.
