# Design Intent — fujara rev A

- Master CAD: `CAD/fujara.scad` (sha256: 190f380fcafa50e0e100f06de4f9074fb25d0c7fa3dfdc7ff3e39e73c57e09af) with native SolidWorks assembly `CAD/fujara-body/Fujara_Assembly.SLDASM`, driven by `design-table/fujara-dimensions-parametric.xlsx` (sha256: 8067350d3233be8ecccbec798d0cbfb39151a577be4614266ba0883d7fdd3033)
- Function: Slovak overtone shepherd's flute (fujara) — a deep, harmonics-driven stave-built flute (traditionally 5–8 ft tall) that plays melodies from the natural overtone series rather than from finger holes. Long open-open main bore with a side air-delivery tube (jet delivery, not a pitched resonator) and three-hole voicing. First pass uses an open-open validator model.
- Environment: long stave glue-up (bore distortion risk); breath-contact finishes must be cured/food-safe; overtone response depends on bore + flue/labium + side tube measured together. Cultural attribution to Slovak fujara tradition stays visible (engineering derivation, not ownership).
- Target qty: 1 (per selected key). Deadline: TBD. Budget/unit ceiling: TBD.

## Critical dimensions (carry tolerances)

| Feature | Nominal | Tolerance | Why critical | Source |
| --- | --- | --- | --- | --- |
| A2 predicted geometric length | 1550.96 mm | measure fundamental + overtone alignment | fundamental pitch (A2 = 110.00 Hz) | family-spec.csv FUJ-A2-STUDY (physics_derived) |
| Main bore ID | 31.75 mm | measure after stave glue-up | bore governs pitch/overtones | family-spec.csv FUJ-A2-STUDY |
| Bore aspect ratio | 49.0 | recompute from measured bore | slender-bore overtone behavior | family-spec.csv FUJ-A2-STUDY |
| Three tone-hole positions | 68/73/83% of long chamber length | tune to overtone scale physically | melodic overtone scale | family-spec.csv hole_rule |
| Flue width | TBD | response-critical; adjust by hand | voicing / speaking | family-spec.csv (measurement_required) |
| Side air tube role | air-delivery branch (measurement_required) | measure leakage/pressure/junction | jet delivery + response | family-spec.csv side_tube_role |

## Incidental (free for DFM)

- Exterior body styling/taper, decorative carving/banding, stave count cosmetics, finish color, mouthpiece exterior — subject to breath-safety.

## Must-nots (DFM may never violate)

- Flue/labium/voicing geometry is response-critical and tuning-sensitive: refine by hand, never freeze from the scaffold or a lossy export (risks.md Acoustic).
- Do not treat SolidWorks files as authority for a given key until a configuration-specific export is reviewed (risks.md Fabrication).
- DXF/SVG plates are review plates, not CNC toolpaths — do not cut from them (register / risks.md).
- Do not treat the side air tube as a pitched resonator without measurements (family-spec).
- Breath-contact finishes/adhesives must be fully cured and food-safe (risks.md Safety).

## Material intent

- Preferred: stave-built wood body per bom.csv; long stock with adequate lathe/workholding capacity.
- Acceptable subs: per sourcing.csv (spec-first; live prices unverified; breath-safe finishes only).
- Forbidden: uncured/non-food-safe interior finishes on breath-contact surfaces.

## Stage status

Stage 0 intake complete 2026-07-01. Gate A (Alpha shop compile) NOT yet run — no concessions logged, nothing presented as shippable. L2 candidate; authority remains measurement-gated.
