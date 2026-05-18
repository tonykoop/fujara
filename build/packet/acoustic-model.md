# Fujara Bore, Flue, And Side-Tube Acoustic Model

Current status: V5 build-packet candidate, not build-ready.

## Model Choice

The fujara packet uses `acoustic_law=open_open` and
`end_condition=both_ends_open`.

That is deliberate: the fujara is an edge-tone overtone flute. Its long main
bore controls the fundamental and harmonic-series behavior. The side air tube
delivers breath to the labium; it should be measured for leakage, pressure
drop, centerline length, and junction angle, but it is not treated as a pitched
side branch unless measured evidence proves a repeatable coupling effect.

## First-Pass Length Check

At 20 C, the validator's open-open relation uses:

```text
L_geom = 343000 / (2 * target_hz) - 8.13 mm
```

For the A2 study baseline:

```text
target_hz = 110.00
L_geom = 1550.96 mm
```

This row exists so `validate_acoustic_law.py` checks the model and stops silent
physics drift. It does not replace the existing design table, SolidWorks
configurations, or measured tuning work.

## Flue And Labium Variables

Before any public build packet or shop cut:

- Measure flue width and height.
- Measure sound-hole length and labium edge distance.
- Confirm nest depth and side-tube outlet alignment.
- Record response notes at low, medium, and overblown pressure.
- Log temperature and humidity for every tuning measurement.

## Tuning Discipline

The next physical validation pass should record:

- Fundamental pitch at room temperature.
- Fundamental pitch after breath-warmed stabilization.
- Overblown partials through the practical melody range.
- Three-hole response against the 68%, 73%, and 83% layout rule.
- Cents error against the target scale, with any trim decision logged before
  geometry is revised.
