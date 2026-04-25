# Fujara — Engineering Documentation for the Slovak Overtone Shepherd's Flute

> *Parametric design documentation for stave-built fujaras — the deep, harmonics-driven Slovak shepherd's flute, traditionally 5–8 feet tall and tuned to play melodies from the natural overtone series rather than from finger holes.*

![Hero photo](images/00-hero-fujara.jpg)
*(placeholder)*

## What this is

Engineering documentation for the **fujara** — a tall, three-hole, side-blown overtone flute originating with the shepherds of central Slovakia. The fujara is recognized by UNESCO as a Masterpiece of the Oral and Intangible Heritage of Humanity (proclaimed 2005, inscribed on the Representative List in 2008).

This repository combines:

1. **A parametric design table** ([`design-table/fujara-dimensions-parametric.xlsx`](design-table/fujara-dimensions-parametric.xlsx)) covering fundamentals from **D2 (~73 Hz, 94" blank) up through F#3 (~185 Hz, 40" blank)**, with formulas that derive every build dimension — bore ID at four candidate aspect ratios (45:1 / 50:1 / 55:1 / 60:1), wall thickness, the three traditional finger-hole positions, blank dimensions — from a single input: the target fundamental note.
2. **CAD geometry** for the body, the side-blown mouthpiece chamber, the labium/voicing geometry at the top of the main bore, and the cutting jigs.
3. **Acoustic analysis** comparing the fujara's harmonic-series voicing to my [Native American flute](https://github.com/tonykoop/flutes) calculations — the design table includes a "NAF CALC K2" cross-reference column.

Sister project to [`flutes`](https://github.com/tonykoop/flutes), [`djembe`](https://github.com/tonykoop/djembe), [`dundun`](https://github.com/tonykoop/dundun), [`didgeridoo`](https://github.com/tonykoop/didgeridoo), and [`ashiko-drum-workshop`](https://github.com/tonykoop/ashiko-drum-workshop).

## Cultural attribution

The fujara originates with the shepherds of the **Podpoľanie region of central Slovakia** and is considered an emblem of Slovak rural and pastoral culture. UNESCO recognized "Fujara and its music" on the Representative List of the Intangible Cultural Heritage of Humanity in 2008 (initially proclaimed a Masterpiece in 2005). The instrument carries deep cultural significance in Slovak folk music — particularly in *trávnice* (grass songs) and shepherd melodies — and contemporary makers in Slovakia continue traditional methods, often using elderberry or other native woods.

The instruments documented in this repository are built in respect for that tradition by a non-Slovak maker, using stave construction with locally-available North American hardwoods. The engineering documented here is my own derivation; the cultural and musical practice belongs to the Slovak communities from whom the instrument originates.

## Background — what makes a fujara different from every other flute in this portfolio

The fujara is acoustically and architecturally distinctive in three ways:

**1. Melody comes from the harmonic series, not from finger holes.** A fujara has only **three finger holes** (compared to six on a Native American flute, six on a recorder). Those three holes shift the air column's effective length only slightly — they're tuning aids, not melody keys. The melody itself is produced by the player **overblowing** the air column to excite progressively higher harmonics: the 2nd partial (octave above fundamental), 3rd (perfect 5th above that), 4th (octave above the 2nd), 5th (major 3rd), 6th, 7th, 8th, and so on. Combined with the three hole positions, this yields the lydian-flavored modal scale characteristic of fujara melody.

**2. Side-blown air path with a parallel chamber.** Unlike an end-blown flute (didgeridoo, recorder), the fujara has a thin secondary tube running parallel to the main bore for the player's air. The mouthpiece is at the top of this side tube; air travels down it, gets routed across a precisely-cut **labium** (sound-hole edge) at the top of the main bore, and excites the main air column. This split allows the player to address the labium at exactly the right angle and pressure without their face being directly above the bore — important when the instrument is 6+ feet tall.

**3. The instrument is *long*.** A fujara tuned to D2 (~73 Hz) wants a build length of roughly 94 inches — close to 8 feet. Even a shorter F#3 fujara is over 3 feet. The proportions are dictated by acoustics: a low fundamental at audible loudness needs a long air column. The challenge of building one is that you cannot just CNC-mill an 8-foot pipe out of one block of hardwood — staves are practically required.

## The parametric design table

The single engineering-heavy artifact in this repository is the parametric design table. Variables are listed in column A, calculated/tabulated values flow from them:

**User-set variables (per key):**

| Var | Meaning | Range across D2 → F#3 |
|---|---|---|
| A | Blank length | 94" (D2) → 40" (F#3) |
| B | Blank width | 2.25" → 1.5" |
| C | Blank thickness | 1.125" → 0.75" |
| D | Mouthpiece length | 20" → 14" |
| F | Spacing | 0.75" (constant) |
| H | Extra length (chuck jaws) | 2.5" |
| K | Bore inner diameter | 1.25" → 0.875" |
| L | Wall thickness | 0.3125" → 0.1875" |
| M | Nest distance from mouthpiece | 17.75" → 9.75" |
| N–P | Sunken nest depth, width, length | 0.34" / 0.875" / 4.0" |
| Q | Sound hole + flue width | 0.625" → 0.375" |
| R | Sound hole length | 0.25" |

**Calculated/derived (per key, formula-driven):**

- Long Chamber length (the playing tube) and acoustic length (with K1 foot-end and K2 sound-hole end corrections)
- The three hole positions: **Hole 3 at 68%, Hole 2 at 73%, and Hole 1 at 83%** of the way from the foot end of the long chamber. These percentages are the traditional fujara hole positions.
- Hole frequencies for each note in the resulting scale, derived from the chromatic equal-temperament reference `f = 440 × 2^((n-49)/12)`.
- Inner diameters at four candidate **length-to-diameter aspect ratios — 45:1, 50:1, 55:1, 60:1** — to evaluate trade-offs between bright/forward and dark/recessive voicing.

The table extends from **D2 (piano key 18) up to F#3 (piano key 34)** — about an octave and a half of fundamentals, encompassing both the deepest traditional fujaras and the more compact "fujarka" variants.

## Engineering challenges this repository documents

**1. Acoustic length and end correction.** A fujara's effective acoustic length differs from its physical length because of two end corrections: K1 at the open foot end (~0.4 × bore radius) and K2 at the sound-hole end (much larger, varying with sound-hole geometry). The design table calculates K2 directly from the sound-hole + nest geometry rather than using a constant — and cross-references against my Native American flute K2 calculations as a sanity check.

**2. Stave construction at unusual proportions.** Building an 8-foot stave-glued cylinder is not the same engineering problem as building an 18-inch ashiko or a 30-inch djembe body. The aspect ratio makes glue-up clamping and lathe turning their own categories of challenge — you can't fit a 94-inch blank between standard lathe centers.

**3. Voicing the labium.** Unlike a NAF (where a removable bird/fetish block does the voicing), the fujara's labium is cut directly into the main bore at the top of the long chamber, with the side-tube air path positioned to address it. Small differences in labium geometry produce large differences in playability. The design table establishes the geometry; the build is where the voicing is dialed in.

## CAD and jig design

> *(Forthcoming.)*

Repository structure is laid out for:

- `/CAD/fujara-body/` — the long chamber geometry and side-tube assembly, parametric in target fundamental.
- `/CAD/labium-and-nest/` — the cut at the top of the main bore that the air strikes, and the sunken nest where the side tube meets the main body.
- `/CAD/jigs/` — cutting fixtures. The hole-positioning jig is the most interesting — it has to mark Hole 3, Hole 2, Hole 1 at the calculated percentages of the long chamber length, which itself varies by key.

## Comparison across the instrument portfolio

The fujara closes a useful gap across my instrument repos:

| Instrument | Body | Acoustic principle | Tuning |
|---|---|---|---|
| ashiko | truncated cone | open membrane (head) | drum |
| djembe | goblet | open membrane (head) | drum |
| dundun | cylinder, dual-headed | dual coupled membranes | drum |
| didgeridoo | long cylinder/cone | overblown bore, lip drone | overtone series |
| flutes (NAF) | short cylinder | fipple + finger holes | pentatonic minor |
| **fujara** | **long cylinder** | **fipple + overblown overtone series** | **harmonic series** |

The fujara is the only flute in the portfolio that derives its melody from overblowing rather than finger holes — and the only one tall enough that *single-piece construction is impractical*, making stave-build the natural method.

## What this work is for

- **The acoustic question** — does a parametric design table that works for short NAFs scale up to 8-foot fujaras? The shared "NAF CALC K2" reference column in the design table is the bridge: same end-correction model, very different proportions.
- **The fabrication question** — what stave count, glue-up sequence, and lathe arrangement make an 8-foot tall hollow wooden cylinder achievable for one person to build?
- **The portfolio frame** — the fujara extends the engineering documentation to a sixth instrument family and a seventh continent (Slovakia / Eastern Europe). Together with the others, the repos document a coherent practice across drum and flute traditions on multiple continents.

## License

Released under [CC-BY 4.0](LICENSE) — use freely with attribution. The fujara originates with Slovak culture and is recognized by UNESCO as Intangible Cultural Heritage; the engineering documentation, parametric design table, and CAD work in this repository are my own work, free to reuse and adapt with credit.

## Repository structure

```
fujara/
├── README.md                  ← you are here
├── LICENSE                    ← CC-BY 4.0
├── .gitignore
├── design-table/
│   └── fujara-dimensions-parametric.xlsx   ← the engineering core
├── research/                  ← Slovak fujara references, UNESCO documentation
├── analysis/                  ← acoustic length math, harmonic series mapping
├── CAD/
│   ├── fujara-body/           ← long chamber + side tube parametric in key
│   ├── labium-and-nest/       ← labium cut + side-tube interface
│   └── jigs/                  ← hole-positioning jig (variable by key)
├── drawings/                  ← PDF exports
├── images/                    ← finished-build photos + figures
└── reference/                 ← fujara playing references, scale documentation
```

## Status

| Section | Status |
|---|---|
| Repo description, license, gitignore | ✓ done |
| Parametric design table | ✓ committed (the engineering core) |
| Cultural attribution | ✓ done |
| Hero photo | forthcoming |
| CAD — body geometry | not started (requires SolidWorks access) |
| CAD — labium and nest | not started |
| CAD — jigs | not started |
| Acoustic length cross-check vs. NAF | partially in design table; full writeup forthcoming |
| Physical builds | searching personal archives |

A repository in motion, not a finished portfolio piece.
