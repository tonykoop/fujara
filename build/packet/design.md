# Fujara Issue #5 V5 Starter

Issue context: `fujara` needs a V5 starter with explicit **bore** and **side-branch** authority gates.

## Scope

- Keep the packet at **V5 build-packet candidate for design review** until
  measurements justify a higher label.
- Focus on long-bore geometry, flue/labium response, and side air-tube delivery
  without treating the side tube as a pitched resonator by default.
- Record what is *observed* vs what is *inferred* from design history.

## Known and Inferred

Observed inputs:

- Existing fujara design table (`fujara-design-table.xlsx`, `design-table/fujara-dimensions-parametric.xlsx`) contains derived candidate dimensions and length-to-diameter ratios.
- Repo CAD references are present for the instrument body and labium structures but are not validated as fabrication-ready in this lane.

Inferred/Starter scope:

- Side air-tube relation to the labium remains the key response variable that
  should be measured before any authoritative CAD/DXF updates.
- Main-bore station geometry, end correction, flue width, sound-hole length,
  labium distance, and side-tube leakage are tracked as measurement blockers
  until `validation-loop` rows are populated.

## Authority Rules for this Packet

- `family-spec.csv` is the packet acoustic-law register and declares a
  validator-checkable open-open edge-tone/overtone flute row.
- `bore-station-plan.csv` is a measurement scaffold, not authority on its own.
- `visual-output-register.csv` must keep generated or concept outputs as non-authoritative unless proven by measured rows.
- No branch transitions to L3/L4 until acoustic-law and bore/side-branch measurement gates are passed.

## Gate Plan

Populate measurement rows and update gate status in this order:

1. Confirm acoustic-law row and side air-tube delivery hypothesis in `family-spec.csv`.
2. Measure bore stations and side-branch transition distances in `bore-station-plan.csv`.
3. Complete `validation-loop.csv` for response, bore station capture, and authority gating.
4. Advance `validation.csv` gates only when all evidence is present.

## First Tests to Collect

- Main-bore stations: mouth-end, side-branch injection point, and labium end.
- Side-branch geometry: entry path length, offset to labium, and junction angle.
- Side-branch response behavior: leak/suction checks and basic pressure-to-stability notes.
- One non-structural visual check only (photo/plan review) before any fabrication claim.
