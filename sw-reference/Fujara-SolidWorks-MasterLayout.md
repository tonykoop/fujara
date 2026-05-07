# Fujara SolidWorks MasterLayout

Reference doc for the Fujara assembly's parametric skeleton. Mirrors the
structure of `drone-flutes/sw-reference/Drone-Flutes-SolidWorks-MasterLayout.docx`
so the SW-reference docs across instruments stay legible as a series.

This doc is the design intent. The implementation lives in:

- `Fujara_Assembly.SLDASM` — the assembly that holds the MasterLayout part and the body/mouthpiece/voicing parts.
- `G2Fujara_MasterLayout.SLDPRT` *(to be added)* — the skeleton part. Holds the master sketch, every `g_*` and `c_*` global, every derived-global equation, and the linked-dim equations that map each downstream sketch dim to its global.
- `sw-reference/Fujara-Master-Inputs.csv` — flat list of globals (the human-edit surface).
- `sw-reference/Fujara-SW-Design-Table.csv` — SW-shaped design table (Insert > Tables > Design Table > From Existing File).
- `design-table/fujara_equations.md` — Tony's hand-written per-part equation block. This MasterLayout doc supersedes that file's per-part wiring with a centralized scheme; the old doc remains useful as the human-readable explanation of each per-part dim.
- `CAD/fujara-body/G2Fujara_Assembly.SLDASM_dimensions.csv` — output of `Extract_Dimensions.swp`. Used to validate SW state vs the design table.

## 1. Why MasterLayout

Tony's current Fujara assembly defines `g_*` globals **per part**, hand-synced. From the May 2026 macro dump, every part (G2FujaraTop, FujaraBottomG2, G2Fujara_MouthpieceTop/Bottom, etc.) has its own [Equation 0..N] block redefining the same `g_body_OD`, `g_body_L_finished`, etc. This works but has three real costs:

1. **Drift risk.** Editing `g_body_L_finished = 1755.775mm` in one part doesn't update the other part. Today there is one assembly config; the moment a second key is added, hand-syncing seven parts × N configurations becomes the dominant failure mode.
2. **Naming inconsistencies already in flight.** The current dump has `g_glue_glap` (typo for `c_glue_gap`) on G2FujaraTop, and `g_slip_fit` (should be `c_slip_fit`) on G2Fujara_MouthpieceBottom. These slip in because each part has a private copy.
3. **No design-table surface.** Without a master design table, switching keys means hand-editing seven equation blocks. With a MasterLayout part driven by a design-table xlsx, switching keys is one configuration click.

The MasterLayout pattern centralizes the skeleton in a dedicated SLDPRT and treats every other part as a downstream consumer. This is also exactly the pattern Tony has already proven on `TNG-000_TongueDrum` — that assembly's `TNG-000_MasterLayout` part holds 7 configurations × ~20 globals × ~140 sketch-linked dims with no hand-syncing.

## 2. Architecture

```
Fujara_Assembly.SLDASM
├── G2Fujara_MasterLayout.SLDPRT            ← skeleton part (NEW)
│   ├── Tools > Equations  (all g_* and c_* globals + derived globals)
│   ├── Embedded design table (drives globals per configuration)
│   └── Master sketches (Front plane, Top plane, Right plane)
│       ├── Sketch_Master_Profile           ← root: body envelope, OD/ID
│       ├── Plane_Mouthpiece_Origin         ← offset from foot
│       ├── Plane_Fipple                    ← offset from mouthpiece
│       ├── Plane_Window                    ← offset for labium
│       ├── Plane_HoleBand                  ← offset for finger holes
│       ├── Sketch_Mouthpiece_Block_Profile (pierces master)
│       ├── Sketch_Fipple_Profile            (pierces master)
│       ├── Sketch_Bore_Profile              (concentric on master OD)
│       ├── Sketch_Tone_Holes                (on Plane_HoleBand)
│       └── Sketch_Cork_Profile              (on Plane_Mouthpiece_Origin)
├── G2FujaraTop.SLDPRT                      ← consumes Sketch_Master_Profile + Sketch_Bore_Profile + Sketch_Tone_Holes
├── FujaraBottomG2.SLDPRT                   ← consumes Sketch_Master_Profile + Sketch_Bore_Profile (and mouthpiece-tube hole)
├── G2Fujara_MouthpieceTop.SLDPRT           ← consumes Sketch_Mouthpiece_Block_Profile
├── G2Fujara_MouthpieceBottom.SLDPRT        ← consumes Sketch_Mouthpiece_Block_Profile
├── G2FujaraFlue.SLDPRT                     ← consumes Sketch_Fipple_Profile (voicing block)
├── G2FujaraFluePlug.SLDPRT                 ← consumes Sketch_Fipple_Profile (removable, wax-sealed)
├── mouthpiece.SLDPRT                       ← blow-tube; consumes g_mp_tube_OD/ID
├── Cork.SLDPRT                             ← consumes g_mp_block_ID + c_cork_interference
├── toptube.SLDPRT, bottomtube.SLDPRT       ← ornamental tubes; consume g_mp_tube_OD/ID
└── 7815K833_Bronze Bushing-1               ← McMaster part; configuration-locked
```

The MasterLayout part holds **no solid features**. It is a skeleton — sketches and equations only. Body parts consume the skeleton's sketches via in-context references or **Insert > Part > "Locate part with Move/Copy Body"** with the `Convert Entities` propagation pattern.

The cleanest sketch-pull pattern for Tony's CNC-router workflow is **External Reference + Convert Entities** rather than full in-context modeling. This keeps the body parts editable in isolation when the assembly isn't open, and the macro CSV will surface external references via the linked-dim path.

## 3. The master sketch hierarchy

The master sketch sits on the Front plane and contains every driving dimension that defines the body envelope. Other sketches reference it via Convert Entities or Pierce relations. **Sketch_Master_Profile is the root; nothing bypasses it.**

```
Sketch_Master_Profile        (Front plane, root)
  ├── g_body_OD              outer profile diameter
  ├── g_body_ID              bore diameter
  ├── g_body_L_finished      finished body length (foot-to-mouthpiece-end)
  ├── g_body_L_blank         pre-cut blank length (oversized for trim)
  └── g_body_blank_W         blank board width (split-blank construction)
```

```
Plane_Foot                   (Front plane copy at z=0)
Plane_Mouthpiece_Origin      (Front plane offset by mp_origin_z)
Plane_Fipple                 (offset by fipple_origin_z from Plane_Mouthpiece_Origin)
Plane_Window                 (offset by window_z from Plane_Fipple)
Plane_HoleBand               (offset by hole1_z from Plane_Foot, holds the three finger-hole positions)
```

```
Sketch_Mouthpiece_Block_Profile   (on Plane_Mouthpiece_Origin)
  ├── g_mp_block_OD
  ├── g_mp_block_ID            (bore that holds the mouthpiece blow-tube + cork)
  ├── g_mp_block_L_blank
  └── g_mp_block_blank_W
```

```
Sketch_Bore_Profile          (concentric on master)
  └── bore_inner_radius = g_body_ID / 2
```

```
Sketch_Tone_Holes            (on Plane_HoleBand, per-key)
  ├── hole1_diameter          fixed acoustic dim per key
  ├── hole2_diameter
  ├── hole3_diameter
  ├── fipple_to_hole1
  ├── fipple_to_hole2
  └── fipple_to_hole3
```

```
Sketch_Fipple_Profile        (Plane_Fipple, voicing block)
  ├── flue_block_diameter = g_body_ID - c_glue_gap
  ├── flue_width = g_thru_passage_OD
  ├── duct_diameter = g_thru_passage_OD
  ├── flue_engagement
  └── duct_location
```

```
Sketch_Cork_Profile          (Plane_Mouthpiece_Origin)
  ├── mid_diameter = g_mp_block_ID + c_cork_press     (oversize, interference)
  ├── taper
  └── half_height
```

The two **voicing-critical** dimensions live as literals, not globals:

- `fipple_height = 0.254mm` (0.010") — the air-jet thickness above the labium.
- `flue_height@slot = 1.016mm` (0.040") — the flue plug slot height.

These tune by hand, prototype-by-prototype, and have no parametric scaling story. Keep them as literal sketch dimensions, not globals.

## 4. Design-table → global-equations chain

The flow is one-way:

```
Master_Inputs.csv (human-edit)
  ↓
Fujara-SW-Design-Table.csv → save-as .xlsx
  ↓
Insert > Tables > Design Table > From Existing File
  ↓
Embedded design table inside G2Fujara_MasterLayout.SLDPRT
  ↓
Tools > Equations  (globals get values from the active config row)
  ↓
Sketch dimensions (driven by =g_<name> equations)
  ↓
Downstream parts (consume master sketches via Convert Entities or external reference)
  ↓
Extract_Dimensions.swp output → ingest_dimension_csv.py validates SW vs Excel
```

A configuration switch in SW propagates through this chain in a single rebuild.

## 5. Tier 1 — Design master globals

These are the only numbers Tony hand-edits to retune the instrument across keys. **Defined once in the MasterLayout part.** All values stored in mm (SW canonical); inch readouts shown for shop reference.

| Global | Value (mm) | Value (in) | Role |
|---|---|---|---|
| `g_body_OD` | 47.625 | 1.875 | body outer profile |
| `g_body_ID` | 31.750 | 1.250 | bore diameter (= 2 × bore radius) |
| `g_body_L_finished` | 1755.775 | 69.125 | finished body length |
| `g_body_L_blank` | 1803.400 | 71.000 | pre-cut blank length |
| `g_body_blank_W` | 57.150 | 2.250 | blank board width |
| `g_mp_block_OD` | 28.575 | 1.125 | mouthpiece block outer profile |
| `g_mp_block_ID` | 15.875 | 0.625 | mouthpiece block bore (cork seat) |
| `g_mp_block_L_blank` | 735.584 | 28.960 | mouthpiece block blank length |
| `g_mp_block_blank_W` | 38.100 | 1.500 | mouthpiece block blank width |
| `g_mp_tube_OD` | 15.875 | 0.625 | blow-tube outer diameter |
| `g_mp_tube_ID` | 9.525 | 0.375 | blow-tube inner diameter |
| `g_dowel_OD` | 6.350 | 0.250 | alignment-dowel diameter (1/4" stock) |
| `g_thru_passage_OD` | 12.700 | 0.500 | breath-passage tube OD |
| `g_mp_origin_z` | 22.225 | 0.875 | mouthpiece block origin offset from foot |
| `g_fipple_to_hole1` | 1157.224 | 45.560 | finger-hole 1 distance from fipple |
| `g_fipple_to_hole2` | 1242.314 | 48.910 | finger-hole 2 distance from fipple |
| `g_fipple_to_hole3` | 1412.494 | 55.610 | finger-hole 3 distance from fipple |
| `g_hole_dia` | 7.620 | 0.300 | finger-hole diameter (uniform) |

The last four rows (`g_fipple_to_hole*`, `g_hole_dia`) were per-part literals in `fujara_equations.md`. Promoting them to tier-1 globals is a small change that buys per-key tuning at the design-table level — every fujara key needs its own hole positions, and putting them in the design table is the cleanest way to manage that.

## 6. Tier 2 — Fit / clearance constants

Defined once in the MasterLayout. **Sign convention**: clearance positive (hole bigger), interference negative.

| Constant | Value (mm) | Value (in) | Use case |
|---|---|---|---|
| `c_glue_gap` | 0.0762 | 0.003 | wood-on-wood permanent glued joints |
| `c_wax_seal_fit` | 0.0762 | 0.003 | removable parts sealed with beeswax (flue plug) |
| `c_slip_fit` | 0.381 | 0.015 | non-sealed slip fit (ornament tubes in mounting holes) |
| `c_dowel_clearance` | 0.000 | 0.000 | dowel-pin hole = pin OD (snug, glued) |
| `c_cork_press` | 0.1524 | 0.006 | cork plug oversize vs bore (interference seal) |

`c_glue_gap` and `c_wax_seal_fit` happen to share a value today but represent different design intent. Keep them separate — when wax thickness gets dialed in via testing, you don't want every glue joint moving with it.

`c_cork_press` flips the sign convention from `fujara_equations.md`'s `c_cork_interference = -0.1524`. Both work; the positive form reads more naturally in the cork's `mid_diameter = g_mp_block_ID + c_cork_press` equation.

### Inconsistencies to fix on first migration pass

The May 2026 macro dump shows two name drifts that should be repaired when the MasterLayout is wired:

| Where | Current | Should be |
|---|---|---|
| G2FujaraTop equation block | `g_glue_glap` | `c_glue_gap` |
| G2Fujara_MouthpieceBottom equation block | `g_slip_fit` | `c_slip_fit` |

These are typos that crept in from hand-syncing the per-part blocks. Once globals live in MasterLayout and downstream parts inherit, this category of drift disappears.

## 7. Tier 3 — Derived globals (computed from tier-1)

These live in MasterLayout's Tools > Equations panel as **equations**, not as design-table inputs. They're not values Tony tunes; they're values the geometry needs.

```
"board_thickness"          = "g_body_blank_W" / 2
"bore_inner_radius"        = "g_body_ID" / 2
"flue_block_diameter"      = "g_body_ID"  - "c_glue_gap"
"flue_plug_width"          = "g_thru_passage_OD" - "c_wax_seal_fit"
"mouthpiece_through_hole"  = "g_thru_passage_OD" + "c_glue_gap"
"mp_inner_diameter"        = "g_mp_block_ID"   + "c_glue_gap"
"mp_counterbore_diameter"  = "g_mp_tube_OD"    + "c_slip_fit"
"mp_tube_mount_diameter"   = "g_mp_tube_OD"    + "c_slip_fit"
"dowel_pin_diameter"       = "g_dowel_OD"      + "c_dowel_clearance"
"cork_mid_diameter"        = "g_mp_block_ID"   + "c_cork_press"
"mp_block_thickness"       = "g_mp_block_blank_W" / 2
```

## 8. Per-part inheritance — how each existing part references the master

The MasterLayout part does not export geometry. Downstream parts pull from it via two mechanisms:

1. **Sketch convert/pierce** — the body parts (G2FujaraTop, FujaraBottomG2) need the master's outer profile and bore. The cleanest path is **Insert > Part** with the MasterLayout part as the donor, then **Convert Entities** on `Sketch_Master_Profile` and `Sketch_Bore_Profile` into the body part's working sketches.
2. **Equation references** — for parts that don't need master sketch geometry but do need the global values (Cork.SLDPRT only needs `g_mp_block_ID` and `c_cork_press`), define each global in the part's own Tools > Equations panel as `"g_mp_block_ID" = 15.875mm` and pull it from the **same SW design table** that drives MasterLayout.

The second mechanism is what Tony's existing `fujara_equations.md` file documents. The MasterLayout doesn't replace it — it makes it stop being the source of truth. The new source of truth is the embedded design table inside MasterLayout, exported as `Fujara-SW-Design-Table.xlsx`.

### Per-part global subset (which globals each part actually consumes)

| Part | Tier-1 globals consumed | Derived dims it needs |
|---|---|---|
| `G2Fujara_MasterLayout` | all | all derived |
| `G2FujaraTop` | g_body_*, g_dowel_OD, c_dowel_clearance, c_glue_gap, g_fipple_to_hole*, g_hole_dia | board_thickness, bore_inner_radius, dowel_pin_diameter |
| `FujaraBottomG2` | g_body_*, g_dowel_OD, c_dowel_clearance, c_glue_gap, c_slip_fit, g_thru_passage_OD, g_mp_tube_OD | board_thickness, bore_inner_radius, dowel_pin_diameter, mp_tube_mount_diameter, mouthpiece_through_hole |
| `G2Fujara_MouthpieceTop` | g_mp_block_*, g_mp_tube_OD, g_thru_passage_OD, c_glue_gap, c_slip_fit | mp_block_thickness, mp_inner_diameter, mouthpiece_through_hole, mp_counterbore_diameter |
| `G2Fujara_MouthpieceBottom` | same as MouthpieceTop | same |
| `G2FujaraFlue` | g_body_ID, g_thru_passage_OD, c_glue_gap | flue_block_diameter |
| `G2FujaraFluePlug` | g_thru_passage_OD, c_wax_seal_fit | flue_plug_width |
| `mouthpiece` (blow-tube) | g_mp_tube_OD, g_mp_tube_ID | — |
| `Cork` | g_mp_block_ID, c_cork_press | cork_mid_diameter |
| `toptube`, `bottomtube` | g_mp_tube_OD, g_mp_tube_ID | — |

## 9. Configuration scheme

Each row in `Fujara-SW-Design-Table.xlsx` is one fujara key. Configurations:

| Configuration | Description | Status |
|---|---|---|
| `MASTER_TEMPLATE` | seed for new keys; reflects the current build | populated from May 2026 dump |
| `G2_69in` | low G2, 69.125" body | matches current single-config build |
| `D2_94in` | low D2, ~94" body — traditional bass fujara | TBD; populate from workbook |
| `F2_77in` | F2, ~77" body | TBD |
| `A2_60in` | high A2, ~60" body — compact | TBD |

Body-length scaling for a fujara is dominated by the open-pipe length plus the NAF K2 correction. Tony's parametric workbook (`fujara/design-table/fujara-dimensions-parametric.xlsx`) holds the per-key numbers; populating the design table from it is a one-time copy.

The `MASTER_TEMPLATE` row is the seed: it preserves the current geometry so that if the design table loses a column or breaks, MasterLayout falls back to a known-good baseline. **Never delete `MASTER_TEMPLATE`.** When you add a new key, copy its row and edit.

## 10. The macro CSV → SW round-trip

`assets/solidworks/Extract_Dimensions.swp` walks the assembly and emits one row per dimension entity per configuration. The full output schema is documented in the v4 SolidWorks integration reference; the relevant columns for round-trip validation are `DimFullName`, `Value_in`, `IsLinked`, `IsGlobalVar`, `EquationOrComment`.

Two checkpoints:

1. **After wiring MasterLayout** — run the macro on `Fujara_Assembly.SLDASM`, save the CSV to `CAD/fujara-body/G2Fujara_Assembly.SLDASM_dimensions.csv`. Run `python scripts/ingest_dimension_csv.py --csv <that> --workbook sw-reference/Fujara-SW-Design-Table.xlsx --design-sheet Sheet1`. The script reports any global that's in the design table but not in SW (or vice versa), and any value mismatch.
2. **Before any destructive edit** — capture the macro output. After the edit, capture again and diff. Any unintended dim change shows up immediately.

Tony's existing macro file lives at `CAD/Extract_Fujara_Dimensions.swp` and `CAD/ExtractFujaraDimensions.bas` (the same logic, source-readable form). The skill's reference `Extract_Dimensions.swp` is the v4 generic; either macro produces a CSV with the same column schema.

## 11. Naming conventions

| Side | Convention |
|---|---|
| Excel `Master_Inputs` sheet | snake_case identifiers, blue cells = inputs |
| SW global equations | identical snake_case identifiers, quoted LHS, value with explicit `mm` or `in` suffix |
| SW design-table headers | `$VALUE@<global>@Equations` |
| SW dimension full names | `<dim_name>@<sketch_name>@<part_name>.Part` |
| Macro CSV `DimFullName` | identical to SW dimension full name |

**Iron-clad rule:** the same identifier appears unchanged across all five places. If `g_body_OD` is the global on the SW side, it is `g_body_OD` in `Master_Inputs.csv`, in `Fujara-SW-Design-Table.csv` column header `$VALUE@g_body_OD@Equations`, and in the macro CSV's `EquationOrComment` field.

## 12. Quality gates

Before declaring MasterLayout done:

- [ ] Every global in §5–§7 is defined exactly once in `G2Fujara_MasterLayout`'s Tools > Equations.
- [ ] Every downstream part either (a) inherits via Convert Entities from a master sketch, or (b) defines its consumed globals in its own Equations panel and pulls them from the same SW design table.
- [ ] No raw-number sketch dimension exists. Every feature dim is `=g_<name>`, `=<global arithmetic>`, or a literal that's explicitly a voicing-tuning parameter (the two literals listed in §3).
- [ ] `Sketch_Master_Profile` is the root of the rebuild graph. No sketch bypasses it.
- [ ] `Extract_Dimensions.swp` runs cleanly on `Fujara_Assembly.SLDASM` and produces a CSV with no errors.
- [ ] `ingest_dimension_csv.py` reports zero mismatches between the SW dump and `Fujara-SW-Design-Table.xlsx` for the active configuration.
- [ ] All configurations in the design table rebuild without errors.
- [ ] The two voicing literals (`fipple_height`, `flue_height@slot`) are unchanged from the current build. These are voicing-tuned, not parametric.
- [ ] The `g_glue_glap` / `g_slip_fit` typos from the current dump are repaired.
- [ ] `true_sound_hole_to_splitting_edge_offset` (assembly-level KPI from `fujara_equations.md`) still computes to 0.0093"-ish for the `MASTER_TEMPLATE` configuration. If it drifts more than a few thou, investigate before committing.

## 13. Pack-and-Go forward path (Moseno)

The MasterLayout part is what gets cloned for Moseno. The mechanics:

1. SolidWorks > File > Pack and Go on `Fujara_Assembly.SLDASM`. Choose a destination outside the fujara repo (e.g., `moseno/CAD/` once that's set up).
2. Rename the part files in the Pack-and-Go dialog. The intent is a `G3Moseno_*` namespace:
   - `G2Fujara_MasterLayout` → `G3Moseno_MasterLayout`
   - `G2FujaraTop` → `G3MosenoTop`
   - `FujaraBottomG2` → `G3MosenoBottom`
   - keep mouthpiece/cork/flue parts but rename. (The blow-pipe story is different for Moseno — see the Moseno MasterLayout doc.)
3. After Pack-and-Go, edit the new MasterLayout's globals to Moseno values. The rename map and additional Moseno-specific globals are documented in `moseno/sw-reference/Fujara-to-Moseno-Migration.md`.

The two big design deltas Moseno introduces:

- **External blow-pipe.** Fujara routes air through a parallel block glued onto the body; Moseno has a free-standing blow-pipe tube routed to the labium. New globals: `g_blow_pipe_L`, `g_blow_pipe_OD`, `g_blow_pipe_ID`, `g_blow_pipe_wall`. The mouthpiece-block parts may be omitted entirely (the Moseno mouthpiece is the blow-pipe tube + a fipple block).
- **Six diatonic finger holes + four foot tuning holes** instead of three overtone-aid holes. Globals expand to `g_fipple_to_hole1..6` and `g_foot_to_tuning_hole1..4` plus a per-key `g_hole_dia_main` and `g_hole_dia_tuning`.

Both deltas are additive — fujara globals carry over with one rename (`g_fipple_to_hole1` etc. stay the same; new holes just add new globals). Per-part feature topology changes more (six holes need a new sketch), but the parametric skeleton's tier-1 set extends rather than rebuilding.

---

## Quick-start for wiring up MasterLayout in SolidWorks

1. Create the new part: `File > New > Part`, save as `G2Fujara_MasterLayout.SLDPRT` next to the assembly file.
2. Add globals: `Tools > Equations > Manage Equations`. Paste the tier-1 globals from §5, then the tier-2 from §6, then the tier-3 derived from §7. Use `=value*mm` form — SW accepts it regardless of document units.
3. Insert the design table: `Insert > Tables > Design Table > From Existing File`. Point at `Fujara-SW-Design-Table.xlsx` (saved-as from `Fujara-SW-Design-Table.csv`). SW imports it as the embedded design table.
4. Build the master sketches (§3 hierarchy) on the Front plane. Drive every dimension from a global (`=g_<name>`).
5. Save. Open `Fujara_Assembly.SLDASM`, insert the MasterLayout part as a component (no mate — fix it at the assembly origin).
6. For each existing body part, do **Insert > Part > G2Fujara_MasterLayout** to bring the master sketches in as derived sketches; use Convert Entities to drive the body part's own sketches from them. (This is the in-context pattern; it preserves the body parts' edit-in-isolation usability.)
7. Run `Extract_Dimensions.swp`. Diff the output against the design table via `ingest_dimension_csv.py`.
8. Once clean, commit `Fujara_Assembly.SLDASM`, `G2Fujara_MasterLayout.SLDPRT`, and the dimensions CSV to git.

The sketches and the equations together define the parametric skeleton. Everything else in the assembly is a downstream consumer.

---

## References

- `design-table/fujara_equations.md` — Tony's hand-written per-part equation block. The MasterLayout doc supersedes the source-of-truth claim but doesn't replace the per-part explanatory content.
- `sw-reference/Fujara-Master-Inputs.csv` — flat globals listing.
- `sw-reference/Fujara-SW-Design-Table.csv` — SW-shaped design table (open in Excel, save as .xlsx, then `Insert > Tables > Design Table > From Existing File`).
- `CAD/fujara-body/G2Fujara_Assembly.SLDASM_dimensions.csv` — May 2026 macro dump (current SW state).
- `instrument-maker-v4/references/solidworks-integration.md` — the v4 generic SW reference doc.
- `drone-flutes/sw-reference/Drone-Flutes-SolidWorks-MasterLayout.docx` — sister-instrument MasterLayout reference.
- `moseno/sw-reference/Moseno-SolidWorks-MasterLayout.md` — the Moseno equivalent of this doc.
- `moseno/sw-reference/Fujara-to-Moseno-Migration.md` — Pack-and-Go playbook.
