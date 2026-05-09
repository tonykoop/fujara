# Geometry comparison — separate vs integrated flue

A2 baseline. Numbers source: `sw-reference/Fujara-Master-Inputs.csv`,
`CAD/fujara-body/G2Fujara_Assembly.SLDASM_dimensions.csv`,
`capstone/scripts/fujara_design_math.py`.

## Shared design parameters (both variants)

| Parameter | Value (mm) | Value (in) | Source |
|---|---|---|---|
| Target f0 | 110.000 Hz (A2) | — | capstone default |
| Bore ID `g_body_ID` | 31.750 | 1.250 | Master-Inputs §1 |
| Body OD `g_body_OD` | 47.625 | 1.875 | Master-Inputs §1 |
| Wall thickness | 7.938 | 0.313 | derived (OD−ID)/2 |
| Body length finished | 1755.775 | 69.125 | Master-Inputs §1 |
| Aspect ratio L:D | 50:1 | — | matches G2 single-config |
| Acoustic length L_eff | 1559.091 | 61.382 | capstone closed-form |

The 1-D Webster solver sees only these numbers. They are identical
between the two variants — that is why
`data/integrated-vs-separate.csv` reports zero delta on every mode.

## Separate-flue (current G2 build)

Parts that disappear or move under integration:

| Part | OD (mm) | Length (mm) | Volume (cm³)¹ | Mass (g)² | Disposition |
|---|---|---|---|---|---|
| `G2FujaraFlue` | 31.750 | 53.975 | 42.7 | 30.1 | **eliminated** in integrated |
| `G2FujaraFluePlug` | 12.624 | ~50³ | 6.3 | 4.4 | retained, unchanged |
| `G2FujaraTop` (top board) | 47.6 × 57.2 × 1803 | — | (no head-feature change) | — | gains windway pocket |
| `FujaraBottomG2` (bot board) | 47.6 × 57.2 × 1803 | — | (no head-feature change) | — | gains optional windway floor |

¹ Solid-cylinder volume; flue duct and windway cuts not subtracted.
² Hardwood density 705 kg/m³ (`fujara_design_math.WOOD_DENSITY`).
³ `G2FujaraFluePlug` axial length not in the master-inputs CSV; estimated from the
  flue-block depth that the plug seats into. Number is descriptive, not load-bearing.

### Flue-block features (from SW dimensions CSV)

| Feature | Value (mm) | Value (in) |
|---|---|---|
| `flue_block_diameter` | 31.750 | 1.250 |
| `flue_engagement` | 3.886 | 0.153 |
| `flue_width` (windway) | 12.700 | 0.500 |
| `duct_diameter` (breath passage) | 12.700 | 0.500 |
| `duct_location` (axial) | 22.225 | 0.875 |
| `height` (block axial length) | 53.975 | 2.125 |

These five features re-host onto the body top + bottom in the integrated
variant — see next section.

## Integrated-flue (proposed)

The split-blank body construction (`g_body_blank_W = 57.150`,
`board_thickness = 28.575`) means both head-end inside faces are flat
and CNC-accessible **before** glue-up. Migrating the flue features
into the boards is a tool-path change, not a new part.

### Re-hosting map

| Source feature (on `G2FujaraFlue`) | Destination | Implementation |
|---|---|---|
| `flue_block_diameter` | — | absorbed into existing bore (no separate diameter) |
| `flue_engagement` (3.886 mm) | both boards, head end | matched 3.886 mm step on inside face |
| `flue_width` (12.700 mm) | top board only | windway slot, milled into bore-side face |
| `duct_diameter` (12.700 mm) | top board only | breath passage, drilled axial |
| `duct_location` (22.225 mm) | top board only | axial datum from head-end |
| `height` (53.975 mm) | both boards | "head zone" length for windway features |

The bottom board has the option of either a flat windway floor or a
shallow matching pocket; both work acoustically (the 1-D model can't
distinguish), and a flat floor is one less feature.

### Voicing literals — unchanged

The eight voicing literals in `Fujara-Master-Inputs.csv` (rows 36–43)
all live on `G2FujaraTop` already. None move:

```
fipple_height       0.254 mm    (air-jet thickness above labium)
flue_height_slot    1.016 mm    (flue plug slot height)  ← on FluePlug
fipple_gap         10.160 mm
fipple_ramp       349.066 mm
flue_dam          392.699 mm
flue_depth_sketch5 12.129 mm
flue_depth_sketch8  0.838 mm
fipple_ramp_in     87.267 mm
```

`G2FujaraFluePlug` carries `flue_height_slot`. The plug is retained in
both variants — it is the user-facing voicing adjustment. Eliminating
it is a separate question from eliminating the flue **block**.

## Mass + part-count summary

| Metric | Separate | Integrated | Δ |
|---|---|---|---|
| Distinct head-zone parts | 3 (top, bottom, flue block) | 2 (top, bottom) | −1 |
| Permanent head-zone glue joints | 3 | 1 | −2 |
| Removable parts (flue plug) | 1 | 1 | 0 |
| Estimated head-zone mass⁴ | ~30 g (block alone) | ~0 g delta | −30 g |
| Total instrument mass | dominant from body boards (~1.2 kg) | same | negligible |

⁴ Mass delta is a rounding error against the 1.2 kg body. Not a real
factor in the recommendation.

## Cross-section profile (axial, A2 baseline)

```
Z (mm) along axis      separate-flue                 integrated-flue
─────────────────      ──────────────                ───────────────
0    (foot, open)      bore ID 31.75                 bore ID 31.75
…
~22  (mp port axis)    bore ID 31.75                 bore ID 31.75
…
1540 (labium)          bore ID 31.75                 bore ID 31.75
1540..1594             bore ID 31.75 occluded by     bore ID 31.75 with
(head zone, 54 mm)     flue block (windway 12.7      windway slot milled
                       wide cuts through block)      into top board only
>1594 (head closure)   wood (block + body wall)      wood (body wall + plug)
```

Below the labium: identical. Above the labium: same envelope, different
construction. The 1-D model sees only the resonating cavity (below the
labium); it returns identical f0. Whether the head-zone occlusion
geometry shifts the labium-end correction is the L3 question
[acoustic-impact.md](acoustic-impact.md) answers.
