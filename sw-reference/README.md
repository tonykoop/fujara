# Fujara — SolidWorks Reference

Authoritative SolidWorks-side reference for the Fujara assembly. Companion to
`design-table/fujara_equations.md` (per-part explanatory content) and
`drone-flutes/sw-reference/Drone-Flutes-SolidWorks-MasterLayout.docx` (sister-instrument template).

## Files

- `Fujara-SolidWorks-MasterLayout.md` — design intent for the parametric skeleton: master sketch hierarchy, tier-1/2/3 globals, per-part inheritance, configuration scheme, quality gates, Pack-and-Go forward path. **Read first.**
- `Fujara-Master-Inputs.csv` — flat list of every `g_*` and `c_*` global plus tier-3 derived dims and voicing literals. The human-edit surface for the design table.
- `Fujara-SW-Design-Table.csv` — SW-shaped design table. Open in Excel, save as `Fujara-SW-Design-Table.xlsx`, then in SolidWorks: `Insert > Tables > Design Table > From Existing File`.

## Workflow

```
Master_Inputs.csv (edit globals here)
  ↓
Fujara-SW-Design-Table.csv → save as .xlsx
  ↓
Insert > Tables > Design Table > From Existing File
  ↓
G2Fujara_MasterLayout.SLDPRT (skeleton part, Tools > Equations)
  ↓
Sketch dimensions = g_<name>
  ↓
Downstream parts consume master sketches via Convert Entities + share globals via the same design table
  ↓
Extract_Dimensions.swp → CAD/fujara-body/G2Fujara_Assembly.SLDASM_dimensions.csv
  ↓
ingest_dimension_csv.py validates SW vs Excel
```

## Configurations (initial)

| Configuration | Status |
|---|---|
| `MASTER_TEMPLATE` | seed; preserves current build values; **never delete** |
| `G2_69in` | matches current single-config geometry from May 2026 macro dump |
| `D2_94in` | TBD — populate from `design-table/fujara-dimensions-parametric.xlsx` |
| `F2_77in` | TBD — populate from workbook |
| `A2_60in` | TBD — populate from workbook |

The non-MASTER_TEMPLATE rows have placeholder body lengths — replace with the workbook's per-key values before activating those configurations in SW.

## Migration to Moseno

The MasterLayout part is what Pack-and-Go's into the Moseno repo. See
`moseno/sw-reference/Fujara-to-Moseno-Migration.md` for the rename map and
the Moseno-specific deltas (external blow-pipe, six diatonic finger holes,
four foot tuning holes).
