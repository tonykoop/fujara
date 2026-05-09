# Manufacturing impact — separate vs integrated flue

## Joinery + glue strategy

### Separate-flue (current G2)

Three permanent joints in the head zone:

1. `G2FujaraTop ↔ FujaraBottomG2` — the body's split-blank glue line
   (full body length, ~1755 mm). Hide-glue or PVA, edge-to-edge with
   `c_glue_gap = 0.0762 mm` clearance.
2. `G2FujaraTop ↔ G2FujaraFlue` — radial glue between block OD and
   bore ID at the head zone, ~54 mm long. Same clearance.
3. `FujaraBottomG2 ↔ G2FujaraFlue` — same as (2), other half.

Plus one removable joint:

4. `G2FujaraFluePlug` ↔ flue block — wax-sealed,
   `c_wax_seal_fit = 0.0762 mm`. User-serviceable.

### Integrated-flue

One permanent joint in the head zone:

1. `G2FujaraTop ↔ FujaraBottomG2` — the body's split-blank glue line.
   **Unchanged** — already runs the full body length, the head zone's
   integrated windway features are just additional pocket cuts on the
   inside faces before glue-up.

Plus one removable joint, unchanged:

2. `G2FujaraFluePlug` ↔ pocket in top board — wax-sealed,
   `c_wax_seal_fit = 0.0762 mm`. User-serviceable.

**Net delta:** −2 permanent joints, same removable joint.

## Tolerance impact

### Separate: stack-up across three joints

The labium-to-bore-wall offset is what voices the instrument. In the
separate variant, it depends on:

- `g_body_ID` (bore diameter, master global)
- `flue_block_diameter = g_body_ID − c_glue_gap` (block OD)
- Labium edge cut on `G2FujaraTop` (literal sketch dim)
- Glue-line gap between block and bore (process variable)

Worst-case stack: ~0.15 mm (sum of the two `c_glue_gap` instances on
opposite sides of the block, plus mid-tolerance bias on the labium
literal). In practice this is recoverable by post-glue voicing
(scraping the labium, adjusting the plug).

### Integrated: stack-up across one joint

- `g_body_ID` (bore diameter, master global)
- Labium edge cut on `G2FujaraTop` (literal sketch dim)
- Top↔bottom glue line offset (one number)

Worst-case stack: ~0.05 mm. The flue-block radial glue gap drops out
because there is no separate flue block. **Tighter and less variable.**

This is the single strongest reason to integrate: the labium-to-bore
relationship gets simpler and more repeatable.

## Jig changes

### Glue-up jig

Separate: needs the body-half glue jig **and** a radial concentric jig
to seat the flue block to the bore at the right axial location while
the body halves register against each other. Two-stage glue-up
(seat block, then close body halves) or one-stage (everything at
once with the block held by a removable mandrel through the bore).

Integrated: needs only the body-half glue jig. The windway pockets on
the inside faces are CNC-cut before glue-up, no separate seating
operation.

**Net delta:** drop the radial concentric jig.

### CNC tool paths

Separate: three SLDPRT files mean three CAM setups (top board, bottom
board, flue block). The flue block is small enough to be batched
several-up on a single sheet.

Integrated: two SLDPRT files (top board, bottom board), each with the
windway pocket added to its existing inside-face program. **Top
board's program grows** by the windway slot + breath duct + flue
engagement step (three additional cuts, ~3 minutes of machine time
on a typical hobby CNC). **Bottom board's program grows** by the
optional matching engagement step (or stays flat — a flat windway
floor works acoustically).

**Net delta:** lose one CAM setup (the flue block), grow two existing
programs slightly. Wall-clock saving is on the order of one block
batch's setup time.

### Voicing fixture

Both variants use the same final voicing fixture: the assembled body
clamped at the foot with a microphone at the labium and the flue plug
in place. No change.

## Repair-friendliness

This is where separate **wins**.

| Failure mode | Separate | Integrated |
|---|---|---|
| Cracked flue block | swap block (~$5 stock) | rebuild whole body |
| Bad labium cut on flue side | replace flue block | replace top board → rebuild body |
| Tone-hole misposition | replace top board → rebuild body | same |
| Wax plug worn | re-cut plug (both variants) | re-cut plug |

The integrated variant ties windway integrity to body integrity.
A broken windway means the whole instrument goes back to billet.
This is the price of the cleaner tolerance stack.

## Sourcing impact

| Stock | Separate | Integrated |
|---|---|---|
| Body boards | 2 × 71" × 2.25" × 1.125" | 2 × 71" × 2.25" × 1.125" |
| Flue block | 1 × 32mm × 60mm hardwood | — |
| Flue plug | 1 × 13mm × 50mm hardwood | 1 × 13mm × 50mm hardwood |

Drops one ~$5 hardwood block per instrument. Negligible against the
~$60 board cost.

## Process change risk

The integrated variant requires the windway pocket to be cut into the
inside face of `G2FujaraTop` **before** the bore is bored through. If
the bore operation goes second (typical), the windway pocket is
intersected by the bore — this is intended. If the bore goes first
(less typical), the windway pocket has to be milled on a curved
inside face, which is harder and less repeatable.

**Recommended order:** windway pocket → glue-up → bore. The
split-blank construction makes this natural — the windway is on a flat
face, the bore is the operation that creates the cylindrical inner
surface.

## Summary

| Aspect | Separate | Integrated | Winner |
|---|---|---|---|
| Permanent joints (head zone) | 3 | 1 | integrated |
| CAM setups | 3 | 2 | integrated |
| Tolerance stack at labium | ±0.15 mm | ±0.05 mm | integrated |
| Glue-up fixtures | 2 | 1 | integrated |
| Repair-friendly (windway-only failure) | yes | no | separate |
| Sourcing parts | 3 stock items | 2 stock items | integrated |
| Mass at finish | ~30 g extra | baseline | wash (negligible) |
