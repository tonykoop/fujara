# Capstone Reproducibility

Run:

```
python3 capstone/scripts/run_capstone.py
```

That regenerates every artefact in `capstone/design-table/`,
`capstone/modal/`, `capstone/acoustic/`, and `capstone/figures/`.
Inputs are pure code + material constants in
`capstone/scripts/fujara_design_math.py`. No external data files.

## Environment

- Python: `3.12.x` (system).
- Required packages: `numpy >= 2.0`, `scipy >= 1.17`, `matplotlib >= 3.10`.
- No FEniCS / dolfinx, no `mph` (Comsol), no Wolframscript required.
  See `capstone/capstone-deck.md` Slide 9 for the FEM substitution
  disclosure.

## SHA256 of capstone artefacts (post-run)

Recompute with:

```
find capstone -type f \( -name '*.csv' -o -name '*.png' \) | sort | xargs sha256sum
```

| Path | SHA256 |
| --- | --- |
| `capstone/design-table/aspect-ratio-matrix.csv` | `2bb3e3512a65a9227c6a567b4d86860c03fde15d2e0f6a631192c71222c4680d` |
| `capstone/modal/L45D34/modes.csv` | `c6da6270c7e5a5c85850f8f49f5b6f4ee88a33e712023ec7f74b42e5b8d43d93` |
| `capstone/modal/L50D31/modes.csv` | `2141d7d3e72e45094e1e54d2cf5f9b0b34cbdc0ea3db01474084b48da3a8b78f` |
| `capstone/modal/L55D28/modes.csv` | `6fa0f9da4c38cb13320683a1acabcdb7da4da1e71e33fa861c36f05b6db0e92b` |
| `capstone/modal/L60D26/modes.csv` | `ab92961e7f2ac2ae1dfdc2b3d4f0b0ccf5c5ec32c236ee70057ff23e696e557e` |
| `capstone/acoustic/L45D34/cavity_modes.csv` | `df0fbf2bf4454acd196d3e4a1326f5f759daa14cc3d5a83125118029f3b27b2e` |
| `capstone/acoustic/L50D31/cavity_modes.csv` | `4c806bf7d9c5c0bc15c29b376315ac2e7cad19bf24e515e5b782b8082a4f58e7` |
| `capstone/acoustic/L55D28/cavity_modes.csv` | `819fbcdb56b33c99a1ef356ff8ee6bef942e5ab5cb1700dc62eabd4bbcc5ec6c` |
| `capstone/acoustic/L60D26/cavity_modes.csv` | `b84f92ce7087e08c70a73016ed62c9e6487551c0d9344170c1b878acf7603136` |
| `capstone/acoustic/coupled-vs-uncoupled.csv` | `b572ae4ecaa4af0156a3696be469d952c62f76c0a9ca52841de89bdc1382d606` |
| `capstone/figures/aspect-ratio-geometry.png` | `b49661b10615e660680f95ee428c5bfa720159f578f3cc120d4518a1adb53a26` |
| `capstone/figures/structural-modes.png` | `ba64b94c0be5e83daa45415ddf2deb31bb7478884737797e8d0b1e1d13b74992` |
| `capstone/figures/cavity-modes.png` | `0bf069d107f388a838b60d711ac442229100c2864baafa548d25975935e3a0e8` |
| `capstone/figures/coupled-vs-modal.png` | `86778e7cecedf80cef69482a3df3e49d733c406053775031335a0e0083878a82` |

PNG files include matplotlib metadata that can vary across versions; CSV
files are deterministic.

## Source-script SHA256

| Path | SHA256 |
| --- | --- |
| `capstone/scripts/fujara_design_math.py` | `b0c2646d77e31c4b5d1c39234ce00a66e16efba2bb67d17f0c2a9368f281b0e3` |
| `capstone/scripts/generate_design_table.py` | `74cd738f5ff765199d60bd0d4fde54e7251c2eba1cbe45dda67c32d63bee977d` |
| `capstone/scripts/modal_fem.py` | `11eb2b15c11921df09c6e774a2fcc4370422fdc0ef41eaf18dffcccca3591f3c` |
| `capstone/scripts/acoustic_cavity_fem.py` | `a5c4e7991bb8dc9d35f5c4b721bca4b460e6b93883204f2b08b0617143d94c94` |
| `capstone/scripts/make_figures.py` | `caacf3cac93b82e4f0a3d94155f37c2748594d38abaec19967fbab088680df27` |
| `capstone/scripts/run_capstone.py` | `525e357b4bb55331e62d3a82da72866660938e0893e9a32763f0f19770250ff3` |
