# Fujara V5 Candidate Design Notes

Current status: V5 build-packet candidate, not build-ready.

The fujara is treated here as an open-open edge-tone/overtone flute. The long
main bore controls the fundamental and overblown harmonic series; the side air
tube and flue deliver the jet to the labium and can strongly affect response,
but they are not modeled as a second pitched resonator in this packet.

## Governing Acoustic Model

- `acoustic_law`: `open_open`
- `end_condition`: `both_ends_open`
- First-pass pipe relation: `L_eff = c / (2 f)`
- Room-temperature validator check: 20 C speed of sound.
- Warm-playing discipline: final tuning must compare room measurements with a
  breath-warmed condition before any trim/cut geometry is released.

For the A2 study baseline at 110 Hz, the simple open-open relation gives a
room-temperature effective length near 1559 mm before end-correction choices.
The committed family-spec row records a validator-compatible first-pass
geometry length of 1550.96 mm after the validator's default open-open end
correction. Existing SolidWorks and workbook dimensions remain the design
evidence to review, not proof of a tuned physical build.

## Bore, Flue, And Side-Tube Discipline

The V5 packet separates three questions that were previously easy to blend:

- Main bore: length, inner diameter, wall thickness, and open-end correction.
- Flue/labium: jet width, sound-hole length, nest depth, edge distance, and
  voicing adjustability.
- Side air tube: delivery path length, leakage, pressure drop, junction angle,
  and alignment to the labium.

The side tube should be measured as an air-delivery branch. Do not use it to
move the fundamental unless a measured prototype shows a repeatable coupled
resonance effect.

## Fabrication Authority

Candidate fabrication authority is limited to the design tables, native
SolidWorks files, SolidWorks dimension CSVs, the OpenSCAD starter, and the
dimensioned vector plate. Generated or rendered images are concept-only. The
DXF is a dimensioned review plate, not CAM-ready toolpath output.

## Promotion Blockers

- Measure bore stations at the foot, mid-body, branch/labium zone, and top.
- Measure flue width, sound-hole length, labium edge distance, and nest depth.
- Confirm side-tube leakage and junction angle before treating response claims
  as stable.
- Record tuner measurements for fundamental and overblown partials at a known
  temperature/humidity.
- Export/review CAD/DXF from the authoritative CAD workflow before machining.
