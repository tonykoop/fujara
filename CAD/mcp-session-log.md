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
