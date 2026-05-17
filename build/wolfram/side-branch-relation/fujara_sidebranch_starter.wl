(*
  Fujara issue #5 / PR #6
  Sidecar Wolfram starter: bore-side-branch relation sensitivity
  Lane: B7 (Round 24)
*)

ClearAll["Global`*"];

metadata = <|
  "Instrument" -> "Fujara",
  "Issue" -> 5,
  "Lane" -> "B7",
  "DraftPR" -> "#6",
  "Version" -> "instrument-maker v4.4.5",
  "GeneratedAt" -> DateString["ISODateTime"],
  "Scope" -> "starter only; outputs are runtime evidence only, not build validation"
|>;

areaFromDiameterIn[diamIn_] := Pi*(diamIn*0.0254/2)^2;

cAir = 343.0; (* m/s *)
rhoAir = 1.205; (* kg/m^3 *)
inchToMeter = 0.0254;

k[freqHz_] := (2.0*Pi*freqHz)/cAir;

openTubeInputImpedance[diamIn_, lengthIn_, freqHz_] := Module[
  {area, effLengthM},
  area = areaFromDiameterIn[diamIn];
  effLengthM = (lengthIn*inchToMeter) + 0.6*((diamIn*inchToMeter)/2.0);
  If[area <= 0 || effLengthM <= 0 || freqHz <= 0,
    Indeterminate,
    I*(rhoAir*cAir/area)*Cot[k[freqHz]*effLengthM]
  ]
];

junctionCoupling[case_, freqHz_] := Module[
  {
    mainD, sideD, sideL, mainAdj, phaseOffset, zMain, zSide,
    yMain, ySide, shuntFraction, phaseTerm, perturbation
  },
  {
    mainD, sideD, sideL, mainAdj, phaseOffset
  } = Lookup[
    case,
    {
      "mainBoreDiameterIn",
      "sideBranchDiameterIn",
      "sideBranchLengthIn",
      "mainAdjacentLengthIn",
      "labiumPhaseOffsetIn"
    }
  ];

  zMain = openTubeInputImpedance[mainD, mainAdj, freqHz];
  zSide = openTubeInputImpedance[sideD, sideL, freqHz];

  yMain = If[zMain === Indeterminate, Indeterminate, 1/zMain];
  ySide = If[zSide === Indeterminate, Indeterminate, 1/zSide];

  shuntFraction = If[
    And[yMain =!= Indeterminate, ySide =!= Indeterminate, Abs[yMain + ySide] > 0],
    Chop[Abs[ySide/(yMain + ySide)]],
    Indeterminate
  ];

  phaseTerm = If[phaseOffset > 0,
    Chop[Cos[k[freqHz]*(phaseOffset*inchToMeter)]^2],
    1.0
  ];

  perturbation = If[
    NumberQ[shuntFraction] && NumberQ[phaseTerm],
    phaseTerm*shuntFraction*(1.0 + 0.5*sideL/mainAdj),
    Indeterminate
  ];

  <|
    "Case" -> case["Case"],
    "FrequencyHz" -> freqHz,
    "MainBoreDiameterIn" -> mainD,
    "SideBranchDiameterIn" -> sideD,
    "SideBranchLengthIn" -> sideL,
    "MainAdjacentLengthIn" -> mainAdj,
    "LabiumPhaseOffsetIn" -> phaseOffset,
    "ShuntFraction" -> shuntFraction,
    "PhaseTerm" -> phaseTerm,
    "Perturbation" -> perturbation,
    "MainImpedanceReal" -> If[NumberQ[zMain], Re[zMain], Indeterminate],
    "MainImpedanceImag" -> If[NumberQ[zMain], Im[zMain], Indeterminate],
    "SideImpedanceReal" -> If[NumberQ[zSide], Re[zSide], Indeterminate],
    "SideImpedanceImag" -> If[NumberQ[zSide], Im[zSide], Indeterminate]
  |>
];

cases = {
  <|
    "Case" -> "A2-1.25in-bore",
    "mainBoreDiameterIn" -> 1.25,
    "sideBranchDiameterIn" -> 0.190,
    "sideBranchLengthIn" -> 4.0,
    "mainAdjacentLengthIn" -> 54.0,
    "labiumPhaseOffsetIn" -> 0.5,
    "Description" -> "Tight, conservative side branch"
  |>,
  <|
    "Case" -> "A2-1.19in-bore",
    "mainBoreDiameterIn" -> 1.19,
    "sideBranchDiameterIn" -> 0.200,
    "sideBranchLengthIn" -> 4.5,
    "mainAdjacentLengthIn" -> 54.0,
    "labiumPhaseOffsetIn" -> 1.0,
    "Description" -> "Narrower bore, longer air path"
  |>,
  <|
    "Case" -> "A2-1.31in-bore",
    "mainBoreDiameterIn" -> 1.31,
    "sideBranchDiameterIn" -> 0.180,
    "sideBranchLengthIn" -> 3.5,
    "mainAdjacentLengthIn" -> 54.0,
    "labiumPhaseOffsetIn" -> 0.25,
    "Description" -> "Wider bore with short side branch"
  |>
};

frequencies = {73., 98., 122., 147., 196., 220., 294., 349., 440.};

rows = Flatten@Table[
  junctionCoupling[c, f],
  {c, cases},
  {f, frequencies}
];

csvHeader = {
  "Case", "FrequencyHz", "MainBoreDiameterIn", "SideBranchDiameterIn",
  "SideBranchLengthIn", "MainAdjacentLengthIn", "LabiumPhaseOffsetIn",
  "ShuntFraction", "PhaseTerm", "Perturbation",
  "MainImpedanceReal", "MainImpedanceImag",
  "SideImpedanceReal", "SideImpedanceImag"
};

rowToCsv[record_Association] := {
  record["Case"], record["FrequencyHz"], record["MainBoreDiameterIn"],
  record["SideBranchDiameterIn"], record["SideBranchLengthIn"],
  record["MainAdjacentLengthIn"], record["LabiumPhaseOffsetIn"],
  record["ShuntFraction"], record["PhaseTerm"], record["Perturbation"],
  record["MainImpedanceReal"], record["MainImpedanceImag"],
  record["SideImpedanceReal"], record["SideImpedanceImag"]
};

outputDir = DirectoryName[$InputFileName];
csvPath = FileNameJoin[{outputDir, "fujara_sidebranch_study.csv"}];
summaryPath = FileNameJoin[{outputDir, "fujara_sidebranch_summary.json"}];

caseGroups = GroupBy[rows, #Case&];
caseSummaries = KeyValueMap[
  Function[{caseName, group},
    Module[{numeric, peak, min, max},
      numeric = Select[group, NumberQ[#"Perturbation"]&];
      peak = If[Length[numeric] > 0, MaximalBy[numeric, #"Perturbation"][[1]], Missing["NoNumeric"]];
      min = If[Length[numeric] > 0, MinimalBy[numeric, #"Perturbation"][[1]], Missing["NoNumeric"]];
      max = If[Length[numeric] > 0, MaximalBy[numeric, #"Perturbation"][[1]], Missing["NoNumeric"]];
      <|
        "Case" -> caseName,
        "CaseDescription" -> SelectFirst[cases, #Case == caseName &]["Description"],
        "FrequencyCount" -> Length[group],
        "NumericRecordCount" -> Length[numeric],
        "PeakFrequencyHz" -> If[peak === Missing["NoNumeric"], Missing["NoNumeric"], peak["FrequencyHz"]],
        "PeakPerturbation" -> If[peak === Missing["NoNumeric"], Missing["NoNumeric"], peak["Perturbation"]],
        "MinPerturbation" -> If[min === Missing["NoNumeric"], Missing["NoNumeric"], min["Perturbation"]],
        "MaxPerturbation" -> If[max === Missing["NoNumeric"], Missing["NoNumeric"], max["Perturbation"]]
      |>
    ]
  ],
  caseGroups
];

Export[csvPath, Prepend[rowToCsv /@ rows, csvHeader], "CSV"];

Export[
  summaryPath,
  <|
    "metadata" -> metadata,
    "assumptions" -> {
      "model" -> "lossless 1D open-tube side-branch shunt heuristic",
      "runtimeOnly" -> True,
      "unit" -> "Inches and Hz inputs with SI conversion in code",
      "noPhysicalValidation" -> True
    },
    "parameters" -> <|
      "frequenciesHz" -> frequencies,
      "cases" -> cases
    |>,
    "caseSummaries" -> Values[caseSummaries],
    "artifactPaths" -> <|
      "studyCsv" -> csvPath,
      "summaryJson" -> summaryPath
    |
  |>,
  "JSON"
];

Print["B7-fujara-side-branch runtime executed"]; 
Print["outputCsv=" <> csvPath];
Print["outputSummary=" <> summaryPath];
