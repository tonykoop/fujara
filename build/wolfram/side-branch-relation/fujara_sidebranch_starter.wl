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

areaFromDiameterIn[diamIn_?NumericQ] := Pi*(diamIn*0.0254/2)^2;
cAir = 343.0;
rhoAir = 1.205;
inchToMeter = 0.0254;

k[freqHz_?NumericQ] := (2.0*Pi*freqHz)/cAir;

openTubeInputImpedance[diamIn_?NumericQ, lengthIn_?NumericQ, freqHz_?NumericQ] := Module[
  {area, effLengthM},
  area = areaFromDiameterIn[diamIn];
  effLengthM = (lengthIn*inchToMeter) + 0.6*((diamIn*inchToMeter)/2.0);
  I*(rhoAir*cAir/area)*Cot[k[freqHz]*effLengthM]
];

junctionCoupling[case_Association, freqHz_?NumericQ] := Module[
  {mainD, sideD, sideL, mainAdj, phaseOffset, zMain, zSide, yMain, ySide, shuntFraction, phaseTerm, perturbation},
  mainD = case["mainBoreDiameterIn"];
  sideD = case["sideBranchDiameterIn"];
  sideL = case["sideBranchLengthIn"];
  mainAdj = case["mainAdjacentLengthIn"];
  phaseOffset = case["labiumPhaseOffsetIn"];

  zMain = openTubeInputImpedance[mainD, mainAdj, freqHz];
  zSide = openTubeInputImpedance[sideD, sideL, freqHz];
  yMain = 1/zMain;
  ySide = 1/zSide;

  shuntFraction = If[Abs[yMain + ySide] > 0, Chop[Abs[ySide/(yMain + ySide)]], Indeterminate];
  phaseTerm = If[phaseOffset > 0, Chop[Cos[k[freqHz]*(phaseOffset*inchToMeter)]^2], 1.0];
  perturbation = If[NumberQ[shuntFraction] && NumberQ[phaseTerm], phaseTerm*shuntFraction*(1.0 + 0.5*sideL/mainAdj), Indeterminate];

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
    "MainImpedanceReal" -> Re[zMain],
    "MainImpedanceImag" -> Im[zMain],
    "SideImpedanceReal" -> Re[zSide],
    "SideImpedanceImag" -> Im[zSide]
  |>
];

cases = {
  <|"Case" -> "A2-1.25in-bore", "mainBoreDiameterIn" -> 1.25, "sideBranchDiameterIn" -> 0.190, "sideBranchLengthIn" -> 4.0, "mainAdjacentLengthIn" -> 54.0, "labiumPhaseOffsetIn" -> 0.5, "Description" -> "Tight, conservative side branch"|>,
  <|"Case" -> "A2-1.19in-bore", "mainBoreDiameterIn" -> 1.19, "sideBranchDiameterIn" -> 0.200, "sideBranchLengthIn" -> 4.5, "mainAdjacentLengthIn" -> 54.0, "labiumPhaseOffsetIn" -> 1.0, "Description" -> "Narrower bore, longer air path"|>,
  <|"Case" -> "A2-1.31in-bore", "mainBoreDiameterIn" -> 1.31, "sideBranchDiameterIn" -> 0.180, "sideBranchLengthIn" -> 3.5, "mainAdjacentLengthIn" -> 54.0, "labiumPhaseOffsetIn" -> 0.25, "Description" -> "Wider bore with short side branch"|>
};

frequencies = {73., 98., 122., 147., 196., 220., 294., 349., 440.};
rows = Flatten@Table[junctionCoupling[case, freq], {case, cases}, {freq, frequencies}];

rowToCsv[record_Association] := {
  record["Case"], record["FrequencyHz"], record["MainBoreDiameterIn"], record["SideBranchDiameterIn"], record["SideBranchLengthIn"], record["MainAdjacentLengthIn"], record["LabiumPhaseOffsetIn"], record["ShuntFraction"], record["PhaseTerm"], record["Perturbation"], record["MainImpedanceReal"], record["MainImpedanceImag"], record["SideImpedanceReal"], record["SideImpedanceImag"]
};

outputDir = DirectoryName[$InputFileName];
csvPath = FileNameJoin[{outputDir, "fujara_sidebranch_study.csv"}];

Export[csvPath, Prepend[rowToCsv /@ rows, {"Case", "FrequencyHz", "MainBoreDiameterIn", "SideBranchDiameterIn", "SideBranchLengthIn", "MainAdjacentLengthIn", "LabiumPhaseOffsetIn", "ShuntFraction", "PhaseTerm", "Perturbation", "MainImpedanceReal", "MainImpedanceImag", "SideImpedanceReal", "SideImpedanceImag"}], "CSV"];

Print["B7-fujara-side-branch runtime executed"];
Print["outputCsv=" <> csvPath];
