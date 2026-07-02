# MCP Session Log

V5 provenance — aligned with `tonykoop/instrument-maker` V5 build-packet standard.

This repository has historical SolidWorks and design-table artifacts plus
Round 30 hand-authored review artifacts and a bob/r1 monolithic-variant scaffold.
No Claude Desktop MCP session was run in any lane.

| session_id | tool | input_authority | outputs | role | authority_result | review_status | notes |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 2026-05-18-scad-v1 | openscad | design-table/fujara-dimensions-parametric.xlsx; sw-reference/Fujara-SW-Design-Table.csv | CAD/fujara.scad | cad_authoring | pending_measurement | unreviewed | OpenSCAD starter from design-table/SolidWorks references; review scaffold; NOT fabrication authority. |
| 2026-05-18-svg-dxf-v1 | illustrator_manual | design-table/fujara-dimensions-parametric.xlsx | drawings/fujara.svg; drawings/fujara.dxf | drawing_cleanup | derived_preview | unreviewed | Vector review plates; candidate dimension references; not CAM toolpaths. |
| 2026-05-18-print-v1 | manual | design.md; bom.csv; validation.csv | print-packet/assembly-plate.pdf | print_plate | derived_preview | unreviewed | Generated from packet text for review; no Photoshop/Illustrator MCP session available. |
| 2026-05-29-bob-r1-monolithic | openscad | CAD/fujara.scad; family-spec.csv; design-table/fujara-dimensions-parametric.xlsx | CAD/fujara-body-monolithic/fujara-monolithic.scad | cad_authoring | pending_measurement | unreviewed | Monolithic body variant (issue #2): integrates Flue_Top geometry into Body_Top + Body_Bottom modules. All flue/labium dimensions are measurement-required starters. Not fabrication authority. |
| fable-v5-refresh-2026-07-01 | claude-code (Fable 5) | design-table/fujara-dimensions-parametric.xlsx | fujara-design-table.xlsx, design-table/fujara-dimensions-parametric.xlsx | packet_refresh | fabrication | self_checked | V5 refresh pass; historical design-table workbooks reviewed against parametric authority. No dimension changes. Provenance row registers fujara-design-table.xlsx into the log to satisfy V5 fabrication-artifact logging. |
| fable-v5-refresh-2026-07-01 | solidworks (native source, pre-existing) | design-table/fujara-dimensions-parametric.xlsx | CAD/fujara-body/Fujara_Assembly.SLDASM, CAD/fujara-body/G2Fujara_Assembly.SLDASM_dimensions.csv | source_registration | fabrication | self_checked | Registers pre-existing native SolidWorks assembly + its extracted G2 dimension CSV into the provenance log (no MCP session run). Candidate dimension review only; select/review per key before build. |
| fable-v5-refresh-2026-07-01 | claude-code (Fable 5) + OpenSCAD CLI | design-table/fujara-dimensions-parametric.xlsx | CAD/fujara.scad | cad_authoring | pending_measurement | self_checked | Existing OpenSCAD starter (kept, not rewritten). openscad render check: pass (openscad -o STL, exit 0). |
| fable-v5-refresh-2026-07-01 | claude-code (Fable 5) | design-table/fujara-dimensions-parametric.xlsx | build/wolfram/side-branch-relation/fujara_sidebranch_starter.wl | analysis_source | derived_preview | unreviewed | Existing Wolfram side-branch starter; source-only (not executed). L2 evidence. |
