# Fujara Drawing Brief

Current status: V5 build-packet candidate, not build-ready.

## Drawing Set

- `drawings/fujara.svg`: human-readable vector review plate.
- `drawings/fujara.dxf`: dimensioned review plate for CAD/CAM handoff checks.
- `CAD/fujara.scad`: OpenSCAD starter showing named parameters and layout.
- `print-packet/assembly-plate.pdf`: annotated review/assembly plate.

## Authority Chain

Fabrication dimensions are controlled by the design tables, SolidWorks source
CAD, SolidWorks dimension CSVs, and reviewed CAD/DXF exports. The SVG, DXF,
OpenSCAD starter, and print plate in this lane are candidate review artifacts
that must be checked against the selected key/configuration before machining.

Generated images and renders are concept-only and do not control bore length,
hole position, flue geometry, side-tube placement, or toolpaths.

## Required Callouts

- Target note and frequency.
- Open-open governing model and temperature assumption.
- Long chamber length and bore ID source.
- Hole positions at 68%, 73%, and 83% of long chamber length.
- Flue width, sound-hole length, labium edge distance, and side-tube junction
  as measurement-required until captured.
- Explicit "not CAM-ready" note on any DXF that has not been shop-reviewed.
