# Round 23 B8 — `fujara` issue #5

Lane `B8` V5 build-packet starter.

Scope: focus bore profile confidence and side-branch authority gating before any CAD/CADX/fabrication claims.

Current status: **V5 build-packet candidate for design review**. This is not
build-ready, measured, or runtime-verified.

## Packet Files

- `design.md` — issue scope and authority boundary
- `family-spec.csv` — single family/spec row describing side-branch architecture
- `bore-station-plan.csv` — measurement plan for the main bore and side branch
- `validation-loop.csv` — explicit measurement and authority steps
- `validation.csv` — move-condition gates from L2 to L3/L4
- `visual-output-register.csv` — visual/dependency authority control
- `acoustic-model.md` — bore/flue/side-tube acoustic reasoning and tuning discipline
- Root V5 files (`design.md`, `bom.csv`, `sourcing.csv`, `cut-list.csv`,
  `validation.csv`, `risks.md`, `drawing-brief.md`, `photo-shotlist.md`)
  mirror the issue #5 acceptance surface.

## Non-claims

- This starter does not include build-ready DXF/CAD geometry.
- No validated bore profile, flue/labium response, or side-tube delivery
  measurements are committed yet.
- No supplier, CNC, or sourcing claims are final.
- This packet is intended for planning, design review, and first-party capture planning only.
