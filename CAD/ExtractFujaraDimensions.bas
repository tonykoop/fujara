' ============================================================
' ExtractFujaraDimensions.swp
' ------------------------------------------------------------
' Walks the active SolidWorks assembly, opens every component,
' and dumps EVERY dimension (named + unnamed), every global
' variable, and every equation to a CSV next to the assembly.
'
' Output columns:
'   Component, ConfigName, FeatureName, FeatureType,
'   DimFullName, Value_mm, Value_in, Tolerance_Type,
'   IsDriven, IsLinked, IsGlobalVar, EquationOrComment
'
' Designed for the Pack-and-Go fujara assembly. Will not
' modify any geometry — read-only walk.
'
' Usage:
'   1. Open the Pack-and-Go fujara assembly in SolidWorks.
'   2. Tools > Macro > New (or Edit), paste this code into a
'      blank module, save as ExtractFujaraDimensions.swp.
'   3. Tools > Macro > Run > select main.
'   4. CSV is written to <AssemblyPath>_dimensions.csv.
' ============================================================

Option Explicit

Dim swApp           As SldWorks.SldWorks
Dim swTopModel      As SldWorks.ModelDoc2
Dim swTopAssy       As SldWorks.AssemblyDoc
Dim outFileNum      As Integer
Dim seenPaths       As Object   ' Scripting.Dictionary, dedupe shared parts

Sub main()
    Set swApp = Application.SldWorks
    Set swTopModel = swApp.ActiveDoc

    If swTopModel Is Nothing Then
        MsgBox "Open the fujara assembly first.", vbExclamation
        Exit Sub
    End If

    If swTopModel.GetType <> swDocASSEMBLY Then
        MsgBox "Active doc is not an assembly. Open the .SLDASM and try again.", vbExclamation
        Exit Sub
    End If

    Set swTopAssy = swTopModel
    Set seenPaths = CreateObject("Scripting.Dictionary")

    Dim outPath As String
    outPath = swTopModel.GetPathName & "_dimensions.csv"

    outFileNum = FreeFile
    Open outPath For Output As #outFileNum
    Print #outFileNum, "Component,ConfigName,FeatureName,FeatureType," & _
                       "DimFullName,Value_mm,Value_in,Tolerance_Type," & _
                       "IsDriven,IsLinked,IsGlobalVar,EquationOrComment"

    ' --- Walk top-level components ---
    Dim vComps As Variant
    vComps = swTopAssy.GetComponents(False)   ' False = top-level only; True = flatten subassemblies

    Dim i As Long
    For i = 0 To UBound(vComps)
        Dim swComp As SldWorks.Component2
        Set swComp = vComps(i)

        Dim compModel As SldWorks.ModelDoc2
        Set compModel = swComp.GetModelDoc2

        If Not compModel Is Nothing Then
            Dim compPath As String
            compPath = compModel.GetPathName
            If Not seenPaths.Exists(compPath) Then
                seenPaths.Add compPath, True
                ProcessModel compModel, swComp.Name2
            End If
        End If
    Next i

    ' --- Also process the assembly itself for assembly-level features (mates, layout sketch) ---
    ProcessModel swTopModel, "[ASSEMBLY] " & swTopModel.GetTitle

    Close #outFileNum

    MsgBox "Dimensions exported to:" & vbCrLf & outPath & vbCrLf & vbCrLf & _
           "Components walked: " & seenPaths.Count + 1, vbInformation
End Sub

' ------------------------------------------------------------
Sub ProcessModel(model As SldWorks.ModelDoc2, compLabel As String)
    Dim configName As String
    On Error Resume Next
    configName = model.GetActiveConfiguration.Name
    If Err.Number <> 0 Then configName = "<unknown>"
    On Error GoTo 0

    ' --- Walk all features (including nested in folders / patterns) ---
    Dim swFeat As SldWorks.Feature
    Set swFeat = model.FirstFeature
    WalkFeature swFeat, model, compLabel, configName

    ' --- Dump global variables and equations ---
    Dim swEqMgr As SldWorks.EquationMgr
    Set swEqMgr = model.GetEquationMgr
    If Not swEqMgr Is Nothing Then
        Dim eq As Long
        For eq = 0 To swEqMgr.GetCount - 1
            Dim isGlob As Boolean
            isGlob = swEqMgr.GlobalVariable(eq)
            Dim eqText As String
            eqText = SafeCsv(swEqMgr.Equation(eq))
            Print #outFileNum, _
                SafeCsv(compLabel) & "," & _
                SafeCsv(configName) & "," & _
                "[Equation " & eq & "]," & _
                "Equation," & _
                "," & _
                "," & _
                "," & _
                "," & _
                "," & _
                "," & _
                IIf(isGlob, "TRUE", "FALSE") & "," & _
                eqText
        Next eq
    End If
End Sub

' ------------------------------------------------------------
' Walks top-level features and their immediate sub-features (sketches inside extrudes, etc.)
Sub WalkFeature(startFeat As SldWorks.Feature, model As SldWorks.ModelDoc2, compLabel As String, configName As String)
    Dim swFeat As SldWorks.Feature
    Set swFeat = startFeat

    Do While Not swFeat Is Nothing
        DumpFeatureDimensions swFeat, model, compLabel, configName

        ' Walk sub-features one level deep using GetNextSubFeature (NOT GetNextFeature)
        Dim swSubFeat As SldWorks.Feature
        Set swSubFeat = swFeat.GetFirstSubFeature
        Do While Not swSubFeat Is Nothing
            DumpFeatureDimensions swSubFeat, model, compLabel, configName
            Set swSubFeat = swSubFeat.GetNextSubFeature
        Loop

        Set swFeat = swFeat.GetNextFeature
    Loop
End Sub

' ------------------------------------------------------------
Sub DumpFeatureDimensions(swFeat As SldWorks.Feature, model As SldWorks.ModelDoc2, compLabel As String, configName As String)
    Dim swDispDim As SldWorks.DisplayDimension
    Set swDispDim = swFeat.GetFirstDisplayDimension

    Do While Not swDispDim Is Nothing
        Dim swDim As SldWorks.Dimension
        Set swDim = swDispDim.GetDimension2(0)

        If Not swDim Is Nothing Then
            Dim valSI As Double
            valSI = swDim.GetSystemValue3(swSetValue_InThisConfiguration, configName)(0)

            Dim valMm As Double, valIn As Double
            valMm = valSI * 1000#
            valIn = valSI / 0.0254

            Dim tolType As String
            tolType = "N/A"
            On Error Resume Next
            tolType = TolTypeName(swDispDim.GetTolerance.Type)
            On Error GoTo 0

            Dim isDriven As Boolean, isLinked As Boolean
            isDriven = False
            isLinked = False
            On Error Resume Next
            isDriven = (swDim.DrivenState = swDimensionDrivenState_e.swDimensionDriven)
            isLinked = swDim.LinkedToShape
            On Error GoTo 0

            Print #outFileNum, _
                SafeCsv(compLabel) & "," & _
                SafeCsv(configName) & "," & _
                SafeCsv(swFeat.Name) & "," & _
                SafeCsv(swFeat.GetTypeName2) & "," & _
                SafeCsv(swDim.FullName) & "," & _
                Format(valMm, "0.0000") & "," & _
                Format(valIn, "0.0000") & "," & _
                tolType & "," & _
                IIf(isDriven, "TRUE", "FALSE") & "," & _
                IIf(isLinked, "TRUE", "FALSE") & "," & _
                "FALSE,"
        End If

        Set swDispDim = swFeat.GetNextDisplayDimension(swDispDim)
    Loop
End Sub

' ------------------------------------------------------------
Function TolTypeName(t As Long) As String
    Select Case t
        Case 0: TolTypeName = "None"
        Case 1: TolTypeName = "Basic"
        Case 2: TolTypeName = "Bilateral"
        Case 3: TolTypeName = "Limit"
        Case 4: TolTypeName = "Symmetric"
        Case 5: TolTypeName = "MIN"
        Case 6: TolTypeName = "MAX"
        Case 7: TolTypeName = "Fit"
        Case Else: TolTypeName = "Other(" & t & ")"
    End Select
End Function

' ------------------------------------------------------------
Function SafeCsv(s As String) As String
    Dim r As String
    r = Replace(s, """", """""")     ' escape internal quotes
    r = Replace(r, vbCrLf, " | ")
    r = Replace(r, vbLf, " | ")
    r = Replace(r, vbCr, " | ")
    If InStr(r, ",") > 0 Or InStr(r, """") > 0 Then
        SafeCsv = """" & r & """"
    Else
        SafeCsv = r
    End If
End Function
