# Fujara Equations & Global Variables

Starter parametric scheme. Add globals via **Tools > Equations** in each part, then drive feature dims from them.

Conventions:
- All values in **mm** (SolidWorks accepts mm even when the part displays in inches).
- Names in `snake_case`.
- A leading `g_` marks a true design-master global (the small set you'd actually tune).
- A leading `c_` marks a fit-clearance constant (interference is negative).

---

## Tier 1 — Design master globals

These are the only numbers you change to retune the whole instrument. **Define identically in every part that uses them.** (Long-term: move to assembly-level externals or a master sketch — for now, sync by hand.)

| Global | Value (mm) | Value (in) | Used in |
|---|---|---|---|
| `g_body_OD` | 47.625 | 1.875 | top, bottom |
| `g_body_ID` | 31.75 | 1.250 | top, bottom (= 2 × bore radius) |
| `g_body_L_finished` | 1755.775 | 69.125 | top, bottom, assembly |
| `g_body_L_blank` | 1803.4 | 71.000 | top, bottom |
| `g_body_blank_W` | 57.15 | 2.250 | top, bottom |
| `g_mp_block_OD` | 28.575 | 1.125 | mouthpiece top + bottom block |
| `g_mp_block_ID` | 15.875 | 0.625 | mouthpiece top + bottom block |
| `g_mp_block_L_blank` | 735.584 | 28.960 | mouthpiece top + bottom block |
| `g_mp_block_blank_W` | 38.1 | 1.500 | mouthpiece top + bottom block |
| `g_mp_tube_OD` | 15.875 | 0.625 | mouthpiece (blow-tube part) |
| `g_mp_tube_ID` | 9.525 | 0.375 | mouthpiece, toptube |
| `g_dowel_OD` | 6.35 | 0.250 | top, bottom (matches 1/4" stock) |
| `g_thru_passage_OD` | 12.7 | 0.500 | flue, body bottom, mp blocks, fipple chamfer |

---

## Tier 2 — Fit / clearance constants

Define once in each part; same value everywhere. **Sign convention**: clearance is positive (hole is bigger), interference is negative.

| Constant | Value (mm) | Value (in) | Use case |
|---|---|---|---|
| `c_glue_gap` | 0.0762 | 0.003 | wood-on-wood permanent glued joints (body halves mating, breath connector glued in place) |
| `c_wax_seal_fit` | 0.0762 | 0.003 | removable parts sealed with beeswax (flue plug — pulls out for drying/cleaning) |
| `c_slip_fit` | 0.381 | 0.015 | non-sealed slip fit (ornament tubes in mounting holes) |
| `c_dowel_clearance` | 0.0 | 0.000 | dowel pin hole = pin OD (snug, glued) |
| `c_cork_interference` | -0.1524 | -0.006 | cork plug oversized vs bore — interference seal blocks horizontal air path, redirecting flow vertically through breath connector |

`c_glue_gap` and `c_wax_seal_fit` happen to share a value today but represent different design intent. Keep them separate so when you dial in the actual wax thickness through testing, you don't accidentally widen every glue joint in the instrument.

### Air flow path (for context — drives which fits matter)

Player → horizontal channel in body bottom → blocked by **cork** (interference seal) → vertical up through **breath connector** tube (glue-fit through both body halves) → into voicing area → through **flue plug** slot (0.040" height, wax-sealed, removable) → across the cutting edge of the flue chamfer (sound is produced here).

---

## Tier 3 — Per-part equations

Format: `"name" = expression`. Paste into **Tools > Equations** > Global Variables.

### G2FujaraTop.SLDPRT

```
"g_body_OD" = 47.625
"g_body_ID" = 31.75
"g_body_L_finished" = 1755.775
"g_body_L_blank" = 1803.4
"g_body_blank_W" = 57.15
"g_dowel_OD" = 6.35
"g_thru_passage_OD" = 12.7
"c_glue_gap" = 0.0762
"c_dowel_clearance" = 0
"board_thickness" = "g_body_blank_W" / 2
"blank_length" = "g_body_L_blank"
"blank_width" = "g_body_blank_W"
"bore_inner_radius" = "g_body_ID" / 2
"outer_diameter" = "g_body_OD"
"finished_length" = "g_body_L_finished"
"dowel_pin_diameter" = "g_dowel_OD" + "c_dowel_clearance"
```

Voicing (unique acoustic params — keep as literals, **not** globals):
```
"fipple_gap" = 10.16
"fipple_ramp" = 349.0659
"flue_dam" = 392.6991
"flue_depth" = 12.1285        ' Sketch5
"flue_depth" = 0.8382          ' Sketch8 — note same name, different sketch is fine
"fipple_height" = 0.254
"fipple_ramp_in" = 87.2665
```

Tuning (finger holes — these are the per-pitch numbers; each fujara key gets its own set):
```
"hole1_diameter" = 7.62
"hole2_diameter" = 7.62
"hole3_diameter" = 7.62
"fipple_to_hole1" = 1157.224
"fipple_to_hole2" = 1242.314
"fipple_to_hole3" = 1412.494
```

End cap groove (driven by OD — already correct in your model):
```
"groove_width" = 3.175
"groove_depth" = 6.35
"groove_location" = "g_body_OD"     ' confirms your IsDriven=TRUE
```

### FujaraBottomG2.SLDPRT

Same `g_*` and `c_*` block as top, plus:
```
"thickness" = "g_body_blank_W" / 2
"blank_length" = "g_body_L_blank"
"blank_width" = "g_body_blank_W"
"inner_bore_radius" = "g_body_ID" / 2
"outer_diameter" = "g_body_OD"
"finished_length" = "g_body_L_finished"
"dowel_pin_diameter" = "g_dowel_OD" + "c_dowel_clearance"
"mouthpiece_hole" = "g_thru_passage_OD" + "c_glue_gap"   ' so the 12.7 mp tube glues cleanly
```

> Recommendation: rename `thickness` → `board_thickness` here too, so the top/bottom CSV columns line up.

Mouthpiece tube mounting hole (already has slip fit — make it explicit):
```
"tube_diameter" = "g_mp_tube_OD" + "c_slip_fit"     ' = 15.875 + 0.381 = 16.256 ✓
"bracket_length" = 691.134
```

### G2Fujara_MouthpieceBottom.SLDPRT *(and Top — same equations both halves)*

```
"g_mp_block_OD" = 28.575
"g_mp_block_ID" = 15.875
"g_mp_block_L_blank" = 735.584
"g_mp_block_blank_W" = 38.1
"g_mp_tube_OD" = 15.875
"g_thru_passage_OD" = 12.7
"c_glue_gap" = 0.0762
"c_slip_fit" = 0.381

"thickness" = "g_mp_block_blank_W" / 2
"blank_length" = "g_mp_block_L_blank"
"blank_width" = "g_mp_block_blank_W"
"outer_diameter" = "g_mp_block_OD"
"inner_diameter" = "g_mp_block_ID" + "c_glue_gap"     ' tube OD 15.875, bore 15.952, glue film
"mouthpiece_through_hole" = "g_thru_passage_OD" + "c_glue_gap"
"mouthpiece_location" = 22.225
"counterbore_diameter" = "g_mp_tube_OD" + "c_slip_fit"   ' = 16.256
```

### mouthpiece.SLDPRT (the blow-tube)

```
"g_mp_tube_OD" = 15.875
"g_mp_tube_ID" = 9.525
"mouthpiece_outer_diameter" = "g_mp_tube_OD"
"mouthpiece_inner_diameter" = "g_mp_tube_ID"
"height@tube" = 50.8                 ' literal — overall tube length is its own design choice
"mouthpiece_curved_cut" = 21.4548
```

### Cork.SLDPRT

```
"g_mp_block_ID" = 15.875
"c_cork_interference" = -0.1524
"mid_diameter" = "g_mp_block_ID" - "c_cork_interference"   ' = 15.875 + 0.1524 = 16.027
"taper" = 122.173
"half_height" = 6.35
```

Subtracting a negative gives oversize. If that reads weirdly, flip the sign convention: define `c_cork_press = 0.1524` (always positive) and write `mid_diameter = g_mp_block_ID + c_cork_press`. Pick whichever stays cleaner in your head.

### G2FujaraFlue.SLDPRT (the voicing block)

```
"g_body_ID" = 31.75
"g_thru_passage_OD" = 12.7
"c_glue_gap" = 0.0762

"flue_block_diameter" = "g_body_ID" - "c_glue_gap"   ' = 31.674 — slips into bore with glue film
"flue_width" = "g_thru_passage_OD"
"duct_diameter" = "g_thru_passage_OD"
"flue_engagement" = 3.8862
"duct_location" = 22.225
```

### G2FujaraFluePlug.SLDPRT *(removable, wax-sealed — not glued)*

```
"g_thru_passage_OD" = 12.7
"c_wax_seal_fit" = 0.0762
"flue_plug_width" = "g_thru_passage_OD" - "c_wax_seal_fit"   ' = 12.6238 ✓
"flue_plug_length" = 53.975
"slot_radius" = 5.08
"slot_location" = 22.225
"airway_passage" = 9.525
"flue_height@slot" = 1.016    ' 0.040" — voicing-critical, no clearance, sealed with beeswax
```

The 0.040" slot height is the air-jet thickness — keep as a literal, this is a voicing-tuning parameter.

### toptube.SLDPRT / bottomtube.SLDPRT

These look like ornamental/structural tubes that slip into the mounting holes:
```
"g_mp_tube_OD" = 15.875
"g_mp_tube_ID" = 9.525
"tube_od" = "g_mp_tube_OD"
"tube_id" = "g_mp_tube_ID"
"height@tube" = 15.875       ' literal — could be a separate design global if these need to scale
```

### Assembly (Fujara_Assembly.SLDASM)

```
"g_body_L_finished" = 1755.775
"cut_to_length" = "g_body_L_finished"
```

The assembly sketch now carries the **voicing-aim measurement**:

```
true_sound_hole_to_splitting_edge_offset = 0.2354 mm = 0.0093"   ' IsDriven=TRUE
```

This is a **measured outcome**, not an input — SolidWorks computes it from the geometry. Don't try to drive it from a global; instead, watch it as a KPI. If you change anything in the flue plug, body alignment, or fipple geometry and this number drifts, you'll see it on the next macro run. The 0.0093" sits in the typical fujara voicing window (~0.005"–0.015") — leave it as the canary.

---

## What this buys you

- Change `g_body_L_finished` once — every `finished_length`, `cut_to_length`, etc. updates.
- Change `c_glue_gap` once — every glued joint adjusts together. Test-drive your fits without chasing 12 dims.
- The renamed `D1` dims (board_thickness, height@tube, etc.) become equation-driven, so they show up in the CSV as `IsLinked=TRUE` and the macro will print the formula in `EquationOrComment`.
- The dimensions that are *coincidentally* equal (the 12.7s that aren't all the same passage, the 15.875s that aren't all the tube OD) stay as literals — preserves design intent.

## Suggested next moves

1. Add the master `g_*` globals to `G2FujaraTop` first, drive its dims, save and rerun the macro. Confirm `IsLinked=TRUE` shows up where expected.
2. Repeat for the other parts.
3. Rename `thickness` → `board_thickness` on the bottom half + mouthpiece blocks for consistency.
4. Once it's all wired up, your `fujara-dimensions-parametric.xlsx` design table only needs to expose the `g_*` and `c_*` rows — everything else propagates.
