<Global.Microsoft.VisualBasic.CompilerServices.DesignerGenerated()>
Partial Class Form1
    Inherits System.Windows.Forms.Form

    'Form overrides dispose to clean up the component list.
    <System.Diagnostics.DebuggerNonUserCode()>
    Protected Overrides Sub Dispose(disposing As Boolean)
        Try
            If disposing AndAlso components IsNot Nothing Then
                components.Dispose()
            End If
        Finally
            MyBase.Dispose(disposing)
        End Try
    End Sub

    'Required by the Windows Form Designer
    Private components As System.ComponentModel.IContainer

    'NOTE: The following procedure is required by the Windows Form Designer
    'It can be modified using the Windows Form Designer.  
    'Do not modify it using the code editor.
    <System.Diagnostics.DebuggerStepThrough()>
    Private Sub InitializeComponent()
        Dim resources As System.ComponentModel.ComponentResourceManager = New System.ComponentModel.ComponentResourceManager(GetType(Form1))
        btnClear = New Button()
        Label4 = New Label()
        txtStartYear = New TextBox()
        btnRun = New Button()
        btnReset = New Button()
        btnExportCSV = New Button()
        btnPlotChart = New Button()
        btnClearLog = New Button()
        btnExit = New Button()
        btnLoadNation = New Button()
        btnSaveNation = New Button()
        logwindow = New RichTextBox()
        saveProfileDialog = New SaveFileDialog()
        openProfileDialog = New OpenFileDialog()
        Label6 = New Label()
        btnImportExcel = New Button()
        lblExcelStatus = New Label()
        OpenFileDialog1 = New OpenFileDialog()
        OpenFileDialog2 = New OpenFileDialog()
        chkUseExcel = New CheckBox()
        simResultGrid = New DataGridView()
        TabPage4 = New TabPage()
        txtDrift = New TextBox()
        Label3 = New Label()
        Label7 = New Label()
        txtZcWeight = New TextBox()
        Label40 = New Label()
        Label2 = New Label()
        Label44 = New Label()
        txtGammaX = New TextBox()
        txtGammaS = New TextBox()
        Label31 = New Label()
        Label33 = New Label()
        Label66 = New Label()
        Label67 = New Label()
        Label51 = New Label()
        Label50 = New Label()
        Label49 = New Label()
        Label68 = New Label()
        txtMuY0 = New TextBox()
        Label58 = New Label()
        txtYBaseB1 = New TextBox()
        Label55 = New Label()
        txtYBaseA1 = New TextBox()
        Label52 = New Label()
        txtYBaseA0 = New TextBox()
        Label48 = New Label()
        Label47 = New Label()
        TabPage2 = New TabPage()
        UrbanRate = New TextBox()
        Label82 = New Label()
        txtPovertyRate = New TextBox()
        Label74 = New Label()
        Label75 = New Label()
        txtMurderRate = New TextBox()
        Label72 = New Label()
        Label73 = New Label()
        Label63 = New Label()
        Label64 = New Label()
        Label65 = New Label()
        Label62 = New Label()
        Label61 = New Label()
        txtOmegaShock = New TextBox()
        txtZShock = New TextBox()
        Label60 = New Label()
        txtSocialSecIndex = New TextBox()
        Label71 = New Label()
        txtUnempInsCoverage = New TextBox()
        Label70 = New Label()
        txtFreeEduCoverage = New TextBox()
        Label69 = New Label()
        txtPensionCoverage = New TextBox()
        Label59 = New Label()
        txtHealthCoverage = New TextBox()
        Label57 = New Label()
        Label56 = New Label()
        Label54 = New Label()
        Label53 = New Label()
        Label42 = New Label()
        Label38 = New Label()
        TabPage1 = New TabPage()
        Label80 = New Label()
        txtYFirst = New TextBox()
        Label79 = New Label()
        Label78 = New Label()
        txtPatentLast = New TextBox()
        txtAnimalPowerLast = New TextBox()
        txtPrimaryEnergyLast = New TextBox()
        txtPopulationLast = New TextBox()
        txtGini = New TextBox()
        txtLPI = New TextBox()
        ArableLandTotal = New TextBox()
        txtMCapGDP = New TextBox()
        txtMilitaryGDP = New TextBox()
        txtUnemploymentRate = New TextBox()
        txtDebtRate = New TextBox()
        txtSavingsRate = New TextBox()
        txtTrust = New TextBox()
        txtTFP = New TextBox()
        txtSTEMRate = New TextBox()
        txtEduRate = New TextBox()
        txtPatentCount = New TextBox()
        txtAnimalPower = New TextBox()
        txtPrimaryEnergy = New TextBox()
        txtPopulation = New TextBox()
        txtYear = New TextBox()
        Label1 = New Label()
        Label28 = New Label()
        Label27 = New Label()
        Label26 = New Label()
        Label25 = New Label()
        Label24 = New Label()
        Label23 = New Label()
        Label22 = New Label()
        Label21 = New Label()
        Label20 = New Label()
        Label19 = New Label()
        Label18 = New Label()
        Label17 = New Label()
        Label16 = New Label()
        Label15 = New Label()
        Label5 = New Label()
        Label32 = New Label()
        TabControl1 = New TabControl()
        TabPage5 = New TabPage()
        Label8 = New Label()
        Label12 = New Label()
        txtZImpactK = New TextBox()
        Label81 = New Label()
        Label83 = New Label()
        txtYLimitDecayBeta = New TextBox()
        txtLandCapLimitCoef = New TextBox()
        Label76 = New Label()
        Label77 = New Label()
        Label13 = New Label()
        Label11 = New Label()
        txtBonusTheta = New TextBox()
        txtSInit = New TextBox()
        txtSDecayRate = New TextBox()
        Label10 = New Label()
        Label30 = New Label()
        Label45 = New Label()
        Label37 = New Label()
        Label36 = New Label()
        txtKY = New TextBox()
        Label43 = New Label()
        txtLimitCoef = New TextBox()
        txtSAccumCoef = New TextBox()
        Label35 = New Label()
        Label34 = New Label()
        Label41 = New Label()
        Label9 = New Label()
        txtBonusP = New TextBox()
        Label46 = New Label()
        btnHelp = New Button()
        btnExportExcel = New Button()
        DebugMode = New CheckBox()
        CType(simResultGrid, ComponentModel.ISupportInitialize).BeginInit()
        TabPage4.SuspendLayout()
        TabPage2.SuspendLayout()
        TabPage1.SuspendLayout()
        TabControl1.SuspendLayout()
        TabPage5.SuspendLayout()
        SuspendLayout()
        ' 
        ' btnClear
        ' 
        btnClear.Location = New Point(347, 597)
        btnClear.Name = "btnClear"
        btnClear.Size = New Size(161, 30)
        btnClear.TabIndex = 1
        btnClear.Text = "🔄 Clear Inputs"
        btnClear.UseVisualStyleBackColor = True
        ' 
        ' Label4
        ' 
        Label4.AutoSize = True
        Label4.Location = New Point(909, 9)
        Label4.Name = "Label4"
        Label4.Size = New Size(65, 17)
        Label4.TabIndex = 6
        Label4.Text = "Start Year"
        ' 
        ' txtStartYear
        ' 
        txtStartYear.Location = New Point(980, 6)
        txtStartYear.Name = "txtStartYear"
        txtStartYear.Size = New Size(146, 23)
        txtStartYear.TabIndex = 7
        ' 
        ' btnRun
        ' 
        btnRun.Location = New Point(514, 598)
        btnRun.Name = "btnRun"
        btnRun.Size = New Size(119, 65)
        btnRun.TabIndex = 8
        btnRun.Text = "▶ Run Simulation"
        btnRun.UseVisualStyleBackColor = True
        ' 
        ' btnReset
        ' 
        btnReset.Location = New Point(347, 562)
        btnReset.Name = "btnReset"
        btnReset.Size = New Size(161, 30)
        btnReset.TabIndex = 9
        btnReset.Text = "♻ Reset Defaults"
        btnReset.UseVisualStyleBackColor = True
        ' 
        ' btnExportCSV
        ' 
        btnExportCSV.Location = New Point(347, 633)
        btnExportCSV.Name = "btnExportCSV"
        btnExportCSV.Size = New Size(161, 30)
        btnExportCSV.TabIndex = 13
        btnExportCSV.Text = "📋 Export CSV"
        btnExportCSV.UseVisualStyleBackColor = True
        ' 
        ' btnPlotChart
        ' 
        btnPlotChart.Location = New Point(13, 633)
        btnPlotChart.Name = "btnPlotChart"
        btnPlotChart.Size = New Size(161, 30)
        btnPlotChart.TabIndex = 14
        btnPlotChart.Text = "📊 View Chart"
        btnPlotChart.UseVisualStyleBackColor = True
        ' 
        ' btnClearLog
        ' 
        btnClearLog.Location = New Point(13, 598)
        btnClearLog.Name = "btnClearLog"
        btnClearLog.Size = New Size(161, 30)
        btnClearLog.TabIndex = 15
        btnClearLog.Text = "🗑 Clear Log"
        btnClearLog.UseVisualStyleBackColor = True
        ' 
        ' btnExit
        ' 
        btnExit.Location = New Point(180, 633)
        btnExit.Name = "btnExit"
        btnExit.Size = New Size(161, 30)
        btnExit.TabIndex = 16
        btnExit.Text = "⏹ Exit"
        btnExit.UseVisualStyleBackColor = True
        ' 
        ' btnLoadNation
        ' 
        btnLoadNation.Location = New Point(180, 562)
        btnLoadNation.Name = "btnLoadNation"
        btnLoadNation.Size = New Size(161, 30)
        btnLoadNation.TabIndex = 17
        btnLoadNation.Text = vbTab & "🇺🇳 Load Country Preset"
        btnLoadNation.UseVisualStyleBackColor = True
        ' 
        ' btnSaveNation
        ' 
        btnSaveNation.Location = New Point(180, 597)
        btnSaveNation.Name = "btnSaveNation"
        btnSaveNation.Size = New Size(161, 30)
        btnSaveNation.TabIndex = 18
        btnSaveNation.Text = "🇨🇳 Save as Preset"
        btnSaveNation.UseVisualStyleBackColor = True
        ' 
        ' logwindow
        ' 
        logwindow.Location = New Point(643, 562)
        logwindow.Name = "logwindow"
        logwindow.Size = New Size(785, 102)
        logwindow.TabIndex = 24
        logwindow.Text = ""
        ' 
        ' openProfileDialog
        ' 
        openProfileDialog.FileName = "OpenFileDialog1"
        ' 
        ' Label6
        ' 
        Label6.AutoSize = True
        Label6.Location = New Point(643, 9)
        Label6.Name = "Label6"
        Label6.Size = New Size(69, 17)
        Label6.TabIndex = 25
        Label6.Text = "Result Log"
        ' 
        ' btnImportExcel
        ' 
        btnImportExcel.Location = New Point(13, 562)
        btnImportExcel.Name = "btnImportExcel"
        btnImportExcel.Size = New Size(161, 30)
        btnImportExcel.TabIndex = 27
        btnImportExcel.Text = "Import Excel"
        btnImportExcel.UseVisualStyleBackColor = True
        ' 
        ' lblExcelStatus
        ' 
        lblExcelStatus.AutoSize = True
        lblExcelStatus.Location = New Point(1132, 9)
        lblExcelStatus.Name = "lblExcelStatus"
        lblExcelStatus.Size = New Size(92, 17)
        lblExcelStatus.TabIndex = 28
        lblExcelStatus.Text = "No file loaded"
        ' 
        ' OpenFileDialog1
        ' 
        OpenFileDialog1.FileName = "OpenFileDialog1"
        ' 
        ' OpenFileDialog2
        ' 
        OpenFileDialog2.FileName = "OpenFileDialog2"
        ' 
        ' chkUseExcel
        ' 
        chkUseExcel.Location = New Point(514, 562)
        chkUseExcel.Name = "chkUseExcel"
        chkUseExcel.Size = New Size(123, 41)
        chkUseExcel.TabIndex = 29
        chkUseExcel.Text = "Use Excel Data (override form)"
        chkUseExcel.UseVisualStyleBackColor = True
        ' 
        ' simResultGrid
        ' 
        simResultGrid.ColumnHeadersHeightSizeMode = DataGridViewColumnHeadersHeightSizeMode.AutoSize
        simResultGrid.Location = New Point(643, 38)
        simResultGrid.Name = "simResultGrid"
        simResultGrid.Size = New Size(1028, 485)
        simResultGrid.TabIndex = 30
        ' 
        ' TabPage4
        ' 
        TabPage4.Controls.Add(txtDrift)
        TabPage4.Controls.Add(Label3)
        TabPage4.Controls.Add(Label7)
        TabPage4.Controls.Add(txtZcWeight)
        TabPage4.Controls.Add(Label40)
        TabPage4.Controls.Add(Label2)
        TabPage4.Controls.Add(Label44)
        TabPage4.Controls.Add(txtGammaX)
        TabPage4.Controls.Add(txtGammaS)
        TabPage4.Controls.Add(Label31)
        TabPage4.Controls.Add(Label33)
        TabPage4.Controls.Add(Label66)
        TabPage4.Controls.Add(Label67)
        TabPage4.Controls.Add(Label51)
        TabPage4.Controls.Add(Label50)
        TabPage4.Controls.Add(Label49)
        TabPage4.Controls.Add(Label68)
        TabPage4.Controls.Add(txtMuY0)
        TabPage4.Controls.Add(Label58)
        TabPage4.Controls.Add(txtYBaseB1)
        TabPage4.Controls.Add(Label55)
        TabPage4.Controls.Add(txtYBaseA1)
        TabPage4.Controls.Add(Label52)
        TabPage4.Controls.Add(txtYBaseA0)
        TabPage4.Controls.Add(Label48)
        TabPage4.Controls.Add(Label47)
        TabPage4.Location = New Point(4, 26)
        TabPage4.Name = "TabPage4"
        TabPage4.Padding = New Padding(3)
        TabPage4.Size = New Size(617, 514)
        TabPage4.TabIndex = 3
        TabPage4.Text = "System Calibration Tab"
        TabPage4.UseVisualStyleBackColor = True
        ' 
        ' txtDrift
        ' 
        txtDrift.Location = New Point(332, 99)
        txtDrift.Name = "txtDrift"
        txtDrift.Size = New Size(100, 23)
        txtDrift.TabIndex = 108
        ' 
        ' Label3
        ' 
        Label3.Location = New Point(331, 40)
        Label3.Name = "Label3"
        Label3.Size = New Size(278, 56)
        Label3.TabIndex = 107
        Label3.Text = "Even without big shocks, society slowly gets more tense — this sets the speed. (0 =turn off, normally turn off)"
        ' 
        ' Label7
        ' 
        Label7.Location = New Point(332, 4)
        Label7.Name = "Label7"
        Label7.Size = New Size(277, 36)
        Label7.TabIndex = 106
        Label7.Text = "Drift (how fast society gets more stressful on its own)  "
        ' 
        ' txtZcWeight
        ' 
        txtZcWeight.Location = New Point(331, 192)
        txtZcWeight.Name = "txtZcWeight"
        txtZcWeight.Size = New Size(100, 23)
        txtZcWeight.TabIndex = 105
        ' 
        ' Label40
        ' 
        Label40.Location = New Point(332, 150)
        Label40.Name = "Label40"
        Label40.Size = New Size(277, 39)
        Label40.TabIndex = 104
        Label40.Text = "Weight multiplier for Zc (social complexity index). Range: 0–2, default 1.0."
        ' 
        ' Label2
        ' 
        Label2.AutoSize = True
        Label2.Location = New Point(332, 133)
        Label2.Name = "Label2"
        Label2.Size = New Size(253, 17)
        Label2.TabIndex = 103
        Label2.Text = "Zc Weight (w_Zc, social complexity weight)"
        ' 
        ' Label44
        ' 
        Label44.AutoSize = True
        Label44.FlatStyle = FlatStyle.Flat
        Label44.ForeColor = Color.IndianRed
        Label44.Location = New Point(152, 4)
        Label44.Name = "Label44"
        Label44.Size = New Size(173, 17)
        Label44.TabIndex = 99
        Label44.Text = "Z Axis Feedback Coefficients"
        ' 
        ' txtGammaX
        ' 
        txtGammaX.Location = New Point(7, 190)
        txtGammaX.Name = "txtGammaX"
        txtGammaX.Size = New Size(100, 23)
        txtGammaX.TabIndex = 98
        ' 
        ' txtGammaS
        ' 
        txtGammaS.Location = New Point(10, 99)
        txtGammaS.Name = "txtGammaS"
        txtGammaS.Size = New Size(100, 23)
        txtGammaS.TabIndex = 93
        ' 
        ' Label31
        ' 
        Label31.AutoSize = True
        Label31.Location = New Point(10, 23)
        Label31.Name = "Label31"
        Label31.Size = New Size(181, 17)
        Label31.TabIndex = 94
        Label31.Text = "Gamma S (γ_S, complexity Zc)"
        ' 
        ' Label33
        ' 
        Label33.Location = New Point(10, 150)
        Label33.Name = "Label33"
        Label33.Size = New Size(209, 37)
        Label33.TabIndex = 97
        Label33.Text = "How much technology/innovation reduces Z (social tension)."
        ' 
        ' Label66
        ' 
        Label66.Location = New Point(10, 40)
        Label66.Name = "Label66"
        Label66.Size = New Size(297, 56)
        Label66.TabIndex = 95
        Label66.Text = "How sensitive Z (social tension) is to the aggregated social complexity Zc." & vbLf & "(No longer related to S, the accumulated crisis pool.)"
        ' 
        ' Label67
        ' 
        Label67.AutoSize = True
        Label67.Location = New Point(10, 125)
        Label67.Name = "Label67"
        Label67.Size = New Size(197, 17)
        Label67.TabIndex = 96
        Label67.Text = "Gamma X (γ_X, innovation relief)"
        ' 
        ' Label51
        ' 
        Label51.Location = New Point(318, 424)
        Label51.Name = "Label51"
        Label51.Size = New Size(291, 34)
        Label51.TabIndex = 92
        Label51.Text = "Gini amplification coefficient (suggested: 0.05–0.7, default: 0.1)"
        ' 
        ' Label50
        ' 
        Label50.Location = New Point(318, 324)
        Label50.Name = "Label50"
        Label50.Size = New Size(291, 54)
        Label50.TabIndex = 91
        Label50.Text = "Population pressure sensitivity: effect of per capita productivity (use 0.05-0.5 if X_real/pop in MWh/person)"
        ' 
        ' Label49
        ' 
        Label49.Location = New Point(7, 398)
        Label49.Name = "Label49"
        Label49.Size = New Size(291, 34)
        Label49.TabIndex = 90
        Label49.Text = "Inverse productivity parameter (suggested: 0.01-0.5, default: 0.1)"
        ' 
        ' Label68
        ' 
        Label68.ForeColor = Color.IndianRed
        Label68.Location = New Point(3, 226)
        Label68.Name = "Label68"
        Label68.Size = New Size(582, 75)
        Label68.TabIndex = 89
        Label68.Text = resources.GetString("Label68.Text")
        ' 
        ' txtMuY0
        ' 
        txtMuY0.Location = New Point(318, 461)
        txtMuY0.Name = "txtMuY0"
        txtMuY0.Size = New Size(100, 23)
        txtMuY0.TabIndex = 88
        ' 
        ' Label58
        ' 
        Label58.AutoSize = True
        Label58.Location = New Point(318, 407)
        Label58.Name = "Label58"
        Label58.Size = New Size(41, 17)
        Label58.TabIndex = 87
        Label58.Text = "MuY0"
        ' 
        ' txtYBaseB1
        ' 
        txtYBaseB1.Location = New Point(318, 381)
        txtYBaseB1.Name = "txtYBaseB1"
        txtYBaseB1.Size = New Size(100, 23)
        txtYBaseB1.TabIndex = 86
        ' 
        ' Label55
        ' 
        Label55.AutoSize = True
        Label55.Location = New Point(318, 301)
        Label55.Name = "Label55"
        Label55.Size = New Size(58, 17)
        Label55.TabIndex = 85
        Label55.Text = "YBaseB1"
        ' 
        ' txtYBaseA1
        ' 
        txtYBaseA1.Location = New Point(7, 435)
        txtYBaseA1.Name = "txtYBaseA1"
        txtYBaseA1.Size = New Size(100, 23)
        txtYBaseA1.TabIndex = 84
        ' 
        ' Label52
        ' 
        Label52.AutoSize = True
        Label52.Location = New Point(7, 381)
        Label52.Name = "Label52"
        Label52.Size = New Size(58, 17)
        Label52.TabIndex = 83
        Label52.Text = "YBaseA1"
        ' 
        ' txtYBaseA0
        ' 
        txtYBaseA0.Location = New Point(7, 355)
        txtYBaseA0.Name = "txtYBaseA0"
        txtYBaseA0.Size = New Size(100, 23)
        txtYBaseA0.TabIndex = 82
        ' 
        ' Label48
        ' 
        Label48.Location = New Point(7, 318)
        Label48.Name = "Label48"
        Label48.Size = New Size(291, 34)
        Label48.TabIndex = 81
        Label48.Text = "Baseline constant for structural tension (suggested: 0.01-0.5, default: 0.08)"
        ' 
        ' Label47
        ' 
        Label47.AutoSize = True
        Label47.Location = New Point(7, 301)
        Label47.Name = "Label47"
        Label47.Size = New Size(58, 17)
        Label47.TabIndex = 80
        Label47.Text = "YBaseA0"
        ' 
        ' TabPage2
        ' 
        TabPage2.Controls.Add(UrbanRate)
        TabPage2.Controls.Add(Label82)
        TabPage2.Controls.Add(txtPovertyRate)
        TabPage2.Controls.Add(Label74)
        TabPage2.Controls.Add(Label75)
        TabPage2.Controls.Add(txtMurderRate)
        TabPage2.Controls.Add(Label72)
        TabPage2.Controls.Add(Label73)
        TabPage2.Controls.Add(Label63)
        TabPage2.Controls.Add(Label64)
        TabPage2.Controls.Add(Label65)
        TabPage2.Controls.Add(Label62)
        TabPage2.Controls.Add(Label61)
        TabPage2.Controls.Add(txtOmegaShock)
        TabPage2.Controls.Add(txtZShock)
        TabPage2.Controls.Add(Label60)
        TabPage2.Controls.Add(txtSocialSecIndex)
        TabPage2.Controls.Add(Label71)
        TabPage2.Controls.Add(txtUnempInsCoverage)
        TabPage2.Controls.Add(Label70)
        TabPage2.Controls.Add(txtFreeEduCoverage)
        TabPage2.Controls.Add(Label69)
        TabPage2.Controls.Add(txtPensionCoverage)
        TabPage2.Controls.Add(Label59)
        TabPage2.Controls.Add(txtHealthCoverage)
        TabPage2.Controls.Add(Label57)
        TabPage2.Controls.Add(Label56)
        TabPage2.Controls.Add(Label54)
        TabPage2.Controls.Add(Label53)
        TabPage2.Controls.Add(Label42)
        TabPage2.Controls.Add(Label38)
        TabPage2.Location = New Point(4, 26)
        TabPage2.Name = "TabPage2"
        TabPage2.Padding = New Padding(3)
        TabPage2.Size = New Size(617, 514)
        TabPage2.TabIndex = 1
        TabPage2.Text = "Snapshot Mode Pt 2"
        TabPage2.UseVisualStyleBackColor = True
        ' 
        ' UrbanRate
        ' 
        UrbanRate.Location = New Point(499, 435)
        UrbanRate.Name = "UrbanRate"
        UrbanRate.Size = New Size(100, 23)
        UrbanRate.TabIndex = 127
        ' 
        ' Label82
        ' 
        Label82.Location = New Point(282, 438)
        Label82.Name = "Label82"
        Label82.Size = New Size(270, 20)
        Label82.TabIndex = 125
        Label82.Text = "Urban Rate"
        ' 
        ' txtPovertyRate
        ' 
        txtPovertyRate.Location = New Point(173, 488)
        txtPovertyRate.Name = "txtPovertyRate"
        txtPovertyRate.Size = New Size(100, 23)
        txtPovertyRate.TabIndex = 124
        ' 
        ' Label74
        ' 
        Label74.Location = New Point(6, 458)
        Label74.Name = "Label74"
        Label74.Size = New Size(270, 39)
        Label74.TabIndex = 123
        Label74.Text = "Poverty rate in decimal, converted to fraction in Zc formula."
        ' 
        ' Label75
        ' 
        Label75.Location = New Point(6, 438)
        Label75.Name = "Label75"
        Label75.Size = New Size(270, 20)
        Label75.TabIndex = 122
        Label75.Text = "Poverty Rate"
        ' 
        ' txtMurderRate
        ' 
        txtMurderRate.Location = New Point(498, 386)
        txtMurderRate.Name = "txtMurderRate"
        txtMurderRate.Size = New Size(100, 23)
        txtMurderRate.TabIndex = 121
        ' 
        ' Label72
        ' 
        Label72.Location = New Point(279, 364)
        Label72.Name = "Label72"
        Label72.Size = New Size(270, 39)
        Label72.TabIndex = 120
        Label72.Text = "Homicide rate in decimal, converted to fraction in Zc formula."
        ' 
        ' Label73
        ' 
        Label73.Location = New Point(279, 344)
        Label73.Name = "Label73"
        Label73.Size = New Size(270, 20)
        Label73.TabIndex = 119
        Label73.Text = "Murder Rate"
        ' 
        ' Label63
        ' 
        Label63.Location = New Point(279, 277)
        Label63.Name = "Label63"
        Label63.Size = New Size(320, 38)
        Label63.TabIndex = 118
        Label63.Text = "Positive values = reduce resilience" & vbCrLf & "Negative values = boost resilience"
        ' 
        ' Label64
        ' 
        Label64.Location = New Point(279, 192)
        Label64.Name = "Label64"
        Label64.Size = New Size(320, 70)
        Label64.TabIndex = 117
        Label64.Text = resources.GetString("Label64.Text")
        ' 
        ' Label65
        ' 
        Label65.AutoSize = True
        Label65.Location = New Point(279, 175)
        Label65.Name = "Label65"
        Label65.Size = New Size(86, 17)
        Label65.TabIndex = 116
        Label65.Text = "OmegaShock"
        ' 
        ' Label62
        ' 
        Label62.Location = New Point(279, 87)
        Label62.Name = "Label62"
        Label62.Size = New Size(320, 59)
        Label62.TabIndex = 115
        Label62.Text = "Positive values = increase tension/stress Negative values = relief, e.g., peace treaties, reconciliation, major reforms" & vbCrLf
        ' 
        ' Label61
        ' 
        Label61.Location = New Point(279, 23)
        Label61.Name = "Label61"
        Label61.Size = New Size(320, 61)
        Label61.TabIndex = 114
        Label61.Text = "Represents sudden increases in systemic tension or social pressure for a given year—such as major political events, mass protests, civil unrest, war, etc."
        ' 
        ' txtOmegaShock
        ' 
        txtOmegaShock.Location = New Point(498, 318)
        txtOmegaShock.Name = "txtOmegaShock"
        txtOmegaShock.Size = New Size(100, 23)
        txtOmegaShock.TabIndex = 113
        ' 
        ' txtZShock
        ' 
        txtZShock.Location = New Point(498, 149)
        txtZShock.Name = "txtZShock"
        txtZShock.Size = New Size(100, 23)
        txtZShock.TabIndex = 112
        ' 
        ' Label60
        ' 
        Label60.AutoSize = True
        Label60.Location = New Point(279, 6)
        Label60.Name = "Label60"
        Label60.Size = New Size(50, 17)
        Label60.TabIndex = 111
        Label60.Text = "ZShock"
        ' 
        ' txtSocialSecIndex
        ' 
        txtSocialSecIndex.Location = New Point(6, 412)
        txtSocialSecIndex.Name = "txtSocialSecIndex"
        txtSocialSecIndex.Size = New Size(100, 23)
        txtSocialSecIndex.TabIndex = 14
        ' 
        ' Label71
        ' 
        Label71.Location = New Point(3, 370)
        Label71.Name = "Label71"
        Label71.Size = New Size(270, 39)
        Label71.TabIndex = 13
        Label71.Text = vbTab & "0–1, automatically calculated average of the above fields; fallback for manual entry if others are missing"
        ' 
        ' txtUnempInsCoverage
        ' 
        txtUnempInsCoverage.Location = New Point(6, 324)
        txtUnempInsCoverage.Name = "txtUnempInsCoverage"
        txtUnempInsCoverage.Size = New Size(100, 23)
        txtUnempInsCoverage.TabIndex = 12
        ' 
        ' Label70
        ' 
        Label70.Location = New Point(3, 282)
        Label70.Name = "Label70"
        Label70.Size = New Size(270, 39)
        Label70.TabIndex = 11
        Label70.Text = "0–1, proportion of total population covered by unemployment insurance (optional)"
        ' 
        ' txtFreeEduCoverage
        ' 
        txtFreeEduCoverage.Location = New Point(6, 236)
        txtFreeEduCoverage.Name = "txtFreeEduCoverage"
        txtFreeEduCoverage.Size = New Size(100, 23)
        txtFreeEduCoverage.TabIndex = 10
        ' 
        ' Label69
        ' 
        Label69.Location = New Point(3, 195)
        Label69.Name = "Label69"
        Label69.Size = New Size(270, 38)
        Label69.TabIndex = 9
        Label69.Text = vbTab & "0–1, proportion of total population with access to free basic education"
        ' 
        ' txtPensionCoverage
        ' 
        txtPensionCoverage.Location = New Point(6, 149)
        txtPensionCoverage.Name = "txtPensionCoverage"
        txtPensionCoverage.Size = New Size(100, 23)
        txtPensionCoverage.TabIndex = 8
        ' 
        ' Label59
        ' 
        Label59.Location = New Point(3, 107)
        Label59.Name = "Label59"
        Label59.Size = New Size(270, 39)
        Label59.TabIndex = 7
        Label59.Text = vbTab & "0–1, proportion of total population covered by pension plans"
        ' 
        ' txtHealthCoverage
        ' 
        txtHealthCoverage.Location = New Point(6, 61)
        txtHealthCoverage.Name = "txtHealthCoverage"
        txtHealthCoverage.Size = New Size(100, 23)
        txtHealthCoverage.TabIndex = 6
        ' 
        ' Label57
        ' 
        Label57.Location = New Point(3, 23)
        Label57.Name = "Label57"
        Label57.Size = New Size(270, 35)
        Label57.TabIndex = 5
        Label57.Text = "0–1, proportion of total population covered by health insurance"
        ' 
        ' Label56
        ' 
        Label56.Location = New Point(3, 350)
        Label56.Name = "Label56"
        Label56.Size = New Size(270, 20)
        Label56.TabIndex = 4
        Label56.Text = "Social Security Coverage Index"
        ' 
        ' Label54
        ' 
        Label54.Location = New Point(3, 262)
        Label54.Name = "Label54"
        Label54.Size = New Size(270, 20)
        Label54.TabIndex = 3
        Label54.Text = "Unemployment Insurance Coverage"
        ' 
        ' Label53
        ' 
        Label53.Location = New Point(3, 175)
        Label53.Name = "Label53"
        Label53.Size = New Size(270, 20)
        Label53.TabIndex = 2
        Label53.Text = "Free Education Coverage"
        ' 
        ' Label42
        ' 
        Label42.Location = New Point(3, 87)
        Label42.Name = "Label42"
        Label42.Size = New Size(270, 20)
        Label42.TabIndex = 1
        Label42.Text = "Pension Coverage"
        ' 
        ' Label38
        ' 
        Label38.Location = New Point(3, 3)
        Label38.Name = "Label38"
        Label38.Size = New Size(270, 20)
        Label38.TabIndex = 0
        Label38.Text = "Health Insurance Coverage"
        ' 
        ' TabPage1
        ' 
        TabPage1.Controls.Add(Label80)
        TabPage1.Controls.Add(txtYFirst)
        TabPage1.Controls.Add(Label79)
        TabPage1.Controls.Add(Label78)
        TabPage1.Controls.Add(txtPatentLast)
        TabPage1.Controls.Add(txtAnimalPowerLast)
        TabPage1.Controls.Add(txtPrimaryEnergyLast)
        TabPage1.Controls.Add(txtPopulationLast)
        TabPage1.Controls.Add(txtGini)
        TabPage1.Controls.Add(txtLPI)
        TabPage1.Controls.Add(ArableLandTotal)
        TabPage1.Controls.Add(txtMCapGDP)
        TabPage1.Controls.Add(txtMilitaryGDP)
        TabPage1.Controls.Add(txtUnemploymentRate)
        TabPage1.Controls.Add(txtDebtRate)
        TabPage1.Controls.Add(txtSavingsRate)
        TabPage1.Controls.Add(txtTrust)
        TabPage1.Controls.Add(txtTFP)
        TabPage1.Controls.Add(txtSTEMRate)
        TabPage1.Controls.Add(txtEduRate)
        TabPage1.Controls.Add(txtPatentCount)
        TabPage1.Controls.Add(txtAnimalPower)
        TabPage1.Controls.Add(txtPrimaryEnergy)
        TabPage1.Controls.Add(txtPopulation)
        TabPage1.Controls.Add(txtYear)
        TabPage1.Controls.Add(Label1)
        TabPage1.Controls.Add(Label28)
        TabPage1.Controls.Add(Label27)
        TabPage1.Controls.Add(Label26)
        TabPage1.Controls.Add(Label25)
        TabPage1.Controls.Add(Label24)
        TabPage1.Controls.Add(Label23)
        TabPage1.Controls.Add(Label22)
        TabPage1.Controls.Add(Label21)
        TabPage1.Controls.Add(Label20)
        TabPage1.Controls.Add(Label19)
        TabPage1.Controls.Add(Label18)
        TabPage1.Controls.Add(Label17)
        TabPage1.Controls.Add(Label16)
        TabPage1.Controls.Add(Label15)
        TabPage1.Controls.Add(Label5)
        TabPage1.Controls.Add(Label32)
        TabPage1.Location = New Point(4, 26)
        TabPage1.Name = "TabPage1"
        TabPage1.Padding = New Padding(3)
        TabPage1.Size = New Size(617, 514)
        TabPage1.TabIndex = 0
        TabPage1.Text = "Snapshot Mode Pt 1"
        TabPage1.UseVisualStyleBackColor = True
        ' 
        ' Label80
        ' 
        Label80.Location = New Point(424, 237)
        Label80.Name = "Label80"
        Label80.Size = New Size(174, 61)
        Label80.TabIndex = 111
        Label80.Text = "Initial Y_t value for the first simulation year (overrides calculated Y_base)."
        ' 
        ' txtYFirst
        ' 
        txtYFirst.Location = New Point(424, 301)
        txtYFirst.Name = "txtYFirst"
        txtYFirst.Size = New Size(136, 23)
        txtYFirst.TabIndex = 110
        ' 
        ' Label79
        ' 
        Label79.AutoSize = True
        Label79.Location = New Point(424, 220)
        Label79.Name = "Label79"
        Label79.Size = New Size(116, 17)
        Label79.TabIndex = 109
        Label79.Text = "Initial Y (First Year)"
        ' 
        ' Label78
        ' 
        Label78.AutoSize = True
        Label78.Location = New Point(457, 20)
        Label78.Name = "Label78"
        Label78.Size = New Size(61, 17)
        Label78.TabIndex = 108
        Label78.Text = "Last Year"
        ' 
        ' txtPatentLast
        ' 
        txtPatentLast.Location = New Point(424, 133)
        txtPatentLast.Name = "txtPatentLast"
        txtPatentLast.Size = New Size(136, 23)
        txtPatentLast.TabIndex = 107
        ' 
        ' txtAnimalPowerLast
        ' 
        txtAnimalPowerLast.Location = New Point(424, 104)
        txtAnimalPowerLast.Name = "txtAnimalPowerLast"
        txtAnimalPowerLast.Size = New Size(136, 23)
        txtAnimalPowerLast.TabIndex = 106
        ' 
        ' txtPrimaryEnergyLast
        ' 
        txtPrimaryEnergyLast.Location = New Point(424, 75)
        txtPrimaryEnergyLast.Name = "txtPrimaryEnergyLast"
        txtPrimaryEnergyLast.Size = New Size(136, 23)
        txtPrimaryEnergyLast.TabIndex = 105
        ' 
        ' txtPopulationLast
        ' 
        txtPopulationLast.Location = New Point(424, 46)
        txtPopulationLast.Name = "txtPopulationLast"
        txtPopulationLast.Size = New Size(136, 23)
        txtPopulationLast.TabIndex = 104
        ' 
        ' txtGini
        ' 
        txtGini.Location = New Point(272, 249)
        txtGini.Name = "txtGini"
        txtGini.Size = New Size(136, 23)
        txtGini.TabIndex = 101
        ' 
        ' txtLPI
        ' 
        txtLPI.Location = New Point(272, 481)
        txtLPI.Name = "txtLPI"
        txtLPI.Size = New Size(136, 23)
        txtLPI.TabIndex = 84
        ' 
        ' ArableLandTotal
        ' 
        ArableLandTotal.Location = New Point(272, 452)
        ArableLandTotal.Name = "ArableLandTotal"
        ArableLandTotal.Size = New Size(136, 23)
        ArableLandTotal.TabIndex = 83
        ' 
        ' txtMCapGDP
        ' 
        txtMCapGDP.Location = New Point(272, 423)
        txtMCapGDP.Name = "txtMCapGDP"
        txtMCapGDP.Size = New Size(136, 23)
        txtMCapGDP.TabIndex = 82
        ' 
        ' txtMilitaryGDP
        ' 
        txtMilitaryGDP.Location = New Point(272, 394)
        txtMilitaryGDP.Name = "txtMilitaryGDP"
        txtMilitaryGDP.Size = New Size(136, 23)
        txtMilitaryGDP.TabIndex = 81
        ' 
        ' txtUnemploymentRate
        ' 
        txtUnemploymentRate.Location = New Point(272, 365)
        txtUnemploymentRate.Name = "txtUnemploymentRate"
        txtUnemploymentRate.Size = New Size(136, 23)
        txtUnemploymentRate.TabIndex = 80
        ' 
        ' txtDebtRate
        ' 
        txtDebtRate.Location = New Point(272, 336)
        txtDebtRate.Name = "txtDebtRate"
        txtDebtRate.Size = New Size(136, 23)
        txtDebtRate.TabIndex = 79
        ' 
        ' txtSavingsRate
        ' 
        txtSavingsRate.Location = New Point(272, 307)
        txtSavingsRate.Name = "txtSavingsRate"
        txtSavingsRate.Size = New Size(136, 23)
        txtSavingsRate.TabIndex = 78
        ' 
        ' txtTrust
        ' 
        txtTrust.Location = New Point(272, 278)
        txtTrust.Name = "txtTrust"
        txtTrust.Size = New Size(136, 23)
        txtTrust.TabIndex = 77
        ' 
        ' txtTFP
        ' 
        txtTFP.Location = New Point(272, 220)
        txtTFP.Name = "txtTFP"
        txtTFP.Size = New Size(136, 23)
        txtTFP.TabIndex = 76
        ' 
        ' txtSTEMRate
        ' 
        txtSTEMRate.Location = New Point(272, 191)
        txtSTEMRate.Name = "txtSTEMRate"
        txtSTEMRate.Size = New Size(136, 23)
        txtSTEMRate.TabIndex = 75
        ' 
        ' txtEduRate
        ' 
        txtEduRate.Location = New Point(272, 162)
        txtEduRate.Name = "txtEduRate"
        txtEduRate.Size = New Size(136, 23)
        txtEduRate.TabIndex = 74
        ' 
        ' txtPatentCount
        ' 
        txtPatentCount.Location = New Point(272, 133)
        txtPatentCount.Name = "txtPatentCount"
        txtPatentCount.Size = New Size(136, 23)
        txtPatentCount.TabIndex = 73
        ' 
        ' txtAnimalPower
        ' 
        txtAnimalPower.Location = New Point(272, 104)
        txtAnimalPower.Name = "txtAnimalPower"
        txtAnimalPower.Size = New Size(136, 23)
        txtAnimalPower.TabIndex = 72
        ' 
        ' txtPrimaryEnergy
        ' 
        txtPrimaryEnergy.Location = New Point(272, 75)
        txtPrimaryEnergy.Name = "txtPrimaryEnergy"
        txtPrimaryEnergy.Size = New Size(136, 23)
        txtPrimaryEnergy.TabIndex = 71
        ' 
        ' txtPopulation
        ' 
        txtPopulation.Location = New Point(272, 46)
        txtPopulation.Name = "txtPopulation"
        txtPopulation.Size = New Size(136, 23)
        txtPopulation.TabIndex = 70
        ' 
        ' txtYear
        ' 
        txtYear.Location = New Point(272, 17)
        txtYear.Name = "txtYear"
        txtYear.Size = New Size(136, 23)
        txtYear.TabIndex = 49
        ' 
        ' Label1
        ' 
        Label1.AutoSize = True
        Label1.Location = New Point(8, 252)
        Label1.Name = "Label1"
        Label1.Size = New Size(191, 17)
        Label1.TabIndex = 102
        Label1.Text = "Wealth Gini Coefficient (0.0–1.0)"
        ' 
        ' Label28
        ' 
        Label28.AutoSize = True
        Label28.Location = New Point(8, 484)
        Label28.Name = "Label28"
        Label28.Size = New Size(224, 17)
        Label28.TabIndex = 100
        Label28.Text = "Logistics Performance Index (0.0–5.0)"
        ' 
        ' Label27
        ' 
        Label27.AutoSize = True
        Label27.Location = New Point(8, 455)
        Label27.Name = "Label27"
        Label27.Size = New Size(131, 17)
        Label27.TabIndex = 99
        Label27.Text = "Arable Land Total Ha"
        ' 
        ' Label26
        ' 
        Label26.AutoSize = True
        Label26.Location = New Point(8, 426)
        Label26.Name = "Label26"
        Label26.Size = New Size(203, 17)
        Label26.TabIndex = 98
        Label26.Text = "Financial Sector Share (% of GDP)"
        ' 
        ' Label25
        ' 
        Label25.AutoSize = True
        Label25.Location = New Point(8, 397)
        Label25.Name = "Label25"
        Label25.Size = New Size(192, 17)
        Label25.TabIndex = 97
        Label25.Text = "Military Expenditure (% of GDP)"
        ' 
        ' Label24
        ' 
        Label24.AutoSize = True
        Label24.Location = New Point(8, 368)
        Label24.Name = "Label24"
        Label24.Size = New Size(149, 17)
        Label24.TabIndex = 96
        Label24.Text = "Unemployment Rate (%)"
        ' 
        ' Label23
        ' 
        Label23.AutoSize = True
        Label23.Location = New Point(8, 339)
        Label23.Name = "Label23"
        Label23.Size = New Size(156, 17)
        Label23.TabIndex = 95
        Label23.Text = "Household Debt Rate (%)"
        ' 
        ' Label22
        ' 
        Label22.AutoSize = True
        Label22.Location = New Point(8, 310)
        Label22.Name = "Label22"
        Label22.Size = New Size(172, 17)
        Label22.TabIndex = 94
        Label22.Text = "Household Savings Rate (%)"
        ' 
        ' Label21
        ' 
        Label21.AutoSize = True
        Label21.Location = New Point(8, 281)
        Label21.Name = "Label21"
        Label21.Size = New Size(98, 17)
        Label21.TabIndex = 93
        Label21.Text = "Social Trust (%)"
        ' 
        ' Label20
        ' 
        Label20.AutoSize = True
        Label20.Location = New Point(8, 223)
        Label20.Name = "Label20"
        Label20.Size = New Size(180, 17)
        Label20.TabIndex = 92
        Label20.Text = "TFP Growth Rate (% per year)"
        ' 
        ' Label19
        ' 
        Label19.AutoSize = True
        Label19.Location = New Point(8, 194)
        Label19.Name = "Label19"
        Label19.Size = New Size(167, 17)
        Label19.TabIndex = 91
        Label19.Text = "STEM Workforce Share (%)"
        ' 
        ' Label18
        ' 
        Label18.AutoSize = True
        Label18.Location = New Point(8, 165)
        Label18.Name = "Label18"
        Label18.Size = New Size(161, 17)
        Label18.TabIndex = 90
        Label18.Text = "Higher Education Rate (%)"
        ' 
        ' Label17
        ' 
        Label17.AutoSize = True
        Label17.Location = New Point(8, 49)
        Label17.Name = "Label17"
        Label17.Size = New Size(156, 17)
        Label17.TabIndex = 89
        Label17.Text = "Total Population (people)"
        ' 
        ' Label16
        ' 
        Label16.AutoSize = True
        Label16.Location = New Point(8, 78)
        Label16.Name = "Label16"
        Label16.Size = New Size(258, 17)
        Label16.TabIndex = 88
        Label16.Text = "Primary Energy Consumption (Million kWh)"
        ' 
        ' Label15
        ' 
        Label15.AutoSize = True
        Label15.Location = New Point(8, 107)
        Label15.Name = "Label15"
        Label15.Size = New Size(229, 17)
        Label15.TabIndex = 87
        Label15.Text = "Estimated Animal Power (Million kWh)"
        ' 
        ' Label5
        ' 
        Label5.AutoSize = True
        Label5.Location = New Point(8, 136)
        Label5.Name = "Label5"
        Label5.Size = New Size(166, 17)
        Label5.TabIndex = 86
        Label5.Text = "Utility Patent Grants (count)"
        ' 
        ' Label32
        ' 
        Label32.AutoSize = True
        Label32.Location = New Point(8, 20)
        Label32.Name = "Label32"
        Label32.Size = New Size(34, 17)
        Label32.TabIndex = 36
        Label32.Text = "Year"
        ' 
        ' TabControl1
        ' 
        TabControl1.Controls.Add(TabPage1)
        TabControl1.Controls.Add(TabPage2)
        TabControl1.Controls.Add(TabPage4)
        TabControl1.Controls.Add(TabPage5)
        TabControl1.Location = New Point(12, 12)
        TabControl1.Name = "TabControl1"
        TabControl1.SelectedIndex = 0
        TabControl1.Size = New Size(625, 544)
        TabControl1.TabIndex = 0
        ' 
        ' TabPage5
        ' 
        TabPage5.Controls.Add(Label8)
        TabPage5.Controls.Add(Label12)
        TabPage5.Controls.Add(txtZImpactK)
        TabPage5.Controls.Add(Label81)
        TabPage5.Controls.Add(Label83)
        TabPage5.Controls.Add(txtYLimitDecayBeta)
        TabPage5.Controls.Add(txtLandCapLimitCoef)
        TabPage5.Controls.Add(Label76)
        TabPage5.Controls.Add(Label77)
        TabPage5.Controls.Add(Label13)
        TabPage5.Controls.Add(Label11)
        TabPage5.Controls.Add(txtBonusTheta)
        TabPage5.Controls.Add(txtSInit)
        TabPage5.Controls.Add(txtSDecayRate)
        TabPage5.Controls.Add(Label10)
        TabPage5.Controls.Add(Label30)
        TabPage5.Controls.Add(Label45)
        TabPage5.Controls.Add(Label37)
        TabPage5.Controls.Add(Label36)
        TabPage5.Controls.Add(txtKY)
        TabPage5.Controls.Add(Label43)
        TabPage5.Controls.Add(txtLimitCoef)
        TabPage5.Controls.Add(txtSAccumCoef)
        TabPage5.Controls.Add(Label35)
        TabPage5.Controls.Add(Label34)
        TabPage5.Controls.Add(Label41)
        TabPage5.Controls.Add(Label9)
        TabPage5.Controls.Add(txtBonusP)
        TabPage5.Location = New Point(4, 26)
        TabPage5.Name = "TabPage5"
        TabPage5.Padding = New Padding(3)
        TabPage5.Size = New Size(617, 514)
        TabPage5.TabIndex = 5
        TabPage5.Text = "Core System Parameters"
        TabPage5.UseVisualStyleBackColor = True
        ' 
        ' Label8
        ' 
        Label8.Location = New Point(332, 299)
        Label8.Name = "Label8"
        Label8.Size = New Size(213, 17)
        Label8.TabIndex = 109
        Label8.Text = "ZImpactK"
        ' 
        ' Label12
        ' 
        Label12.Location = New Point(332, 316)
        Label12.Name = "Label12"
        Label12.Size = New Size(278, 74)
        Label12.TabIndex = 110
        Label12.Text = "Coefficient controlling the influence strength of Z_t on Y calculation. Default is 1.0, adjustable to amplify or reduce the effect of Z."
        ' 
        ' txtZImpactK
        ' 
        txtZImpactK.Location = New Point(332, 387)
        txtZImpactK.Name = "txtZImpactK"
        txtZImpactK.Size = New Size(100, 23)
        txtZImpactK.TabIndex = 111
        ' 
        ' Label81
        ' 
        Label81.Location = New Point(332, 195)
        Label81.Name = "Label81"
        Label81.Size = New Size(264, 20)
        Label81.TabIndex = 106
        Label81.Text = "Y_limit Decay Factor on X Decline (β)"
        ' 
        ' Label83
        ' 
        Label83.Location = New Point(330, 215)
        Label83.Name = "Label83"
        Label83.Size = New Size(278, 55)
        Label83.TabIndex = 107
        Label83.Text = "Multiplier (>1) applied to Y_limit when ΔX < 0, making Y_limit decrease faster than Y during productivity decline. Default 1.2–1.5."
        ' 
        ' txtYLimitDecayBeta
        ' 
        txtYLimitDecayBeta.Location = New Point(330, 273)
        txtYLimitDecayBeta.Name = "txtYLimitDecayBeta"
        txtYLimitDecayBeta.Size = New Size(100, 23)
        txtYLimitDecayBeta.TabIndex = 108
        ' 
        ' txtLandCapLimitCoef
        ' 
        txtLandCapLimitCoef.Location = New Point(6, 148)
        txtLandCapLimitCoef.Name = "txtLandCapLimitCoef"
        txtLandCapLimitCoef.Size = New Size(100, 23)
        txtLandCapLimitCoef.TabIndex = 103
        ' 
        ' Label76
        ' 
        Label76.AutoSize = True
        Label76.Location = New Point(6, 37)
        Label76.Name = "Label76"
        Label76.Size = New Size(297, 17)
        Label76.TabIndex = 104
        Label76.Text = "Land Capacity Limit Coefficient (kWh/person·year)"
        ' 
        ' Label77
        ' 
        Label77.Location = New Point(6, 54)
        Label77.Name = "Label77"
        Label77.Size = New Size(297, 95)
        Label77.TabIndex = 105
        Label77.Text = resources.GetString("Label77.Text")
        ' 
        ' Label13
        ' 
        Label13.FlatStyle = FlatStyle.Flat
        Label13.ForeColor = Color.IndianRed
        Label13.Location = New Point(6, 175)
        Label13.Name = "Label13"
        Label13.Size = New Size(254, 17)
        Label13.TabIndex = 101
        Label13.Text = "Innovation & Technology Bonus Parameters"
        ' 
        ' Label11
        ' 
        Label11.FlatStyle = FlatStyle.Flat
        Label11.ForeColor = Color.IndianRed
        Label11.Location = New Point(0, 320)
        Label11.Name = "Label11"
        Label11.Size = New Size(253, 52)
        Label11.TabIndex = 100
        Label11.Text = "S (Crisis Pool)" & vbLf & "Visual only — shows accumulated overload, no effect on calculations."
        ' 
        ' txtBonusTheta
        ' 
        txtBonusTheta.Location = New Point(6, 217)
        txtBonusTheta.Name = "txtBonusTheta"
        txtBonusTheta.Size = New Size(100, 23)
        txtBonusTheta.TabIndex = 99
        ' 
        ' txtSInit
        ' 
        txtSInit.Location = New Point(0, 485)
        txtSInit.Name = "txtSInit"
        txtSInit.Size = New Size(100, 23)
        txtSInit.TabIndex = 93
        ' 
        ' txtSDecayRate
        ' 
        txtSDecayRate.Location = New Point(0, 393)
        txtSDecayRate.Name = "txtSDecayRate"
        txtSDecayRate.Size = New Size(100, 23)
        txtSDecayRate.TabIndex = 96
        ' 
        ' Label10
        ' 
        Label10.Location = New Point(0, 373)
        Label10.Name = "Label10"
        Label10.Size = New Size(219, 17)
        Label10.TabIndex = 94
        Label10.Text = "S Decay Rate (crisis dissipation rate)"
        ' 
        ' Label30
        ' 
        Label30.Location = New Point(0, 465)
        Label30.Name = "Label30"
        Label30.Size = New Size(177, 17)
        Label30.TabIndex = 91
        Label30.Text = "Initial S₀ (starting crisis level) "
        ' 
        ' Label45
        ' 
        Label45.AutoSize = True
        Label45.FlatStyle = FlatStyle.Flat
        Label45.ForeColor = Color.IndianRed
        Label45.Location = New Point(73, 3)
        Label45.Name = "Label45"
        Label45.Size = New Size(151, 17)
        Label45.TabIndex = 90
        Label45.Text = "Core System Parameters"
        ' 
        ' Label37
        ' 
        Label37.Location = New Point(331, 114)
        Label37.Name = "Label37"
        Label37.Size = New Size(213, 17)
        Label37.TabIndex = 84
        Label37.Text = "Y Coefficient (kY, tension multiplier)"
        ' 
        ' Label36
        ' 
        Label36.Location = New Point(331, 131)
        Label36.Name = "Label36"
        Label36.Size = New Size(278, 35)
        Label36.TabIndex = 85
        Label36.Text = "How much tension is generated per unit productivity."
        ' 
        ' txtKY
        ' 
        txtKY.Location = New Point(332, 169)
        txtKY.Name = "txtKY"
        txtKY.Size = New Size(100, 23)
        txtKY.TabIndex = 86
        ' 
        ' Label43
        ' 
        Label43.Location = New Point(6, 197)
        Label43.Name = "Label43"
        Label43.Size = New Size(229, 17)
        Label43.TabIndex = 97
        Label43.Text = "Bonus Theta (initial innovation pool θ)"
        ' 
        ' txtLimitCoef
        ' 
        txtLimitCoef.Location = New Point(331, 88)
        txtLimitCoef.Name = "txtLimitCoef"
        txtLimitCoef.Size = New Size(100, 23)
        txtLimitCoef.TabIndex = 89
        ' 
        ' txtSAccumCoef
        ' 
        txtSAccumCoef.Location = New Point(0, 439)
        txtSAccumCoef.Name = "txtSAccumCoef"
        txtSAccumCoef.Size = New Size(100, 23)
        txtSAccumCoef.TabIndex = 83
        ' 
        ' Label35
        ' 
        Label35.Location = New Point(331, 3)
        Label35.Name = "Label35"
        Label35.Size = New Size(265, 34)
        Label35.TabIndex = 87
        Label35.Text = "Scaling factor for the societal tolerance limit (Y_limit)."
        ' 
        ' Label34
        ' 
        Label34.Location = New Point(331, 37)
        Label34.Name = "Label34"
        Label34.Size = New Size(280, 59)
        Label34.TabIndex = 88
        Label34.Text = "Higher values mean greater capacity to handle structural tension." & vbLf & "Used in Y_limit calculation"
        ' 
        ' Label41
        ' 
        Label41.Location = New Point(0, 419)
        Label41.Name = "Label41"
        Label41.Size = New Size(253, 17)
        Label41.TabIndex = 81
        Label41.Text = "Crisis Pool Accumulation Coefficient (k_S)"
        ' 
        ' Label9
        ' 
        Label9.Location = New Point(6, 243)
        Label9.Name = "Label9"
        Label9.Size = New Size(277, 23)
        Label9.TabIndex = 78
        Label9.Text = "Tech Bonus Exponent P"
        ' 
        ' txtBonusP
        ' 
        txtBonusP.Location = New Point(6, 269)
        txtBonusP.Name = "txtBonusP"
        txtBonusP.Size = New Size(100, 23)
        txtBonusP.TabIndex = 80
        ' 
        ' Label46
        ' 
        Label46.Location = New Point(1434, 572)
        Label46.Name = "Label46"
        Label46.Size = New Size(237, 92)
        Label46.TabIndex = 31
        Label46.Text = "Author: Xiaofei Feng" & vbCrLf & "Copyright © Xiaofei Feng 2025" & vbCrLf & "Unauthorized commercial use, distribution, or model plagiarism is strictly prohibited. All rights reserved." & vbCrLf & "Email: strangethought2025@gmail.com"
        ' 
        ' btnHelp
        ' 
        btnHelp.BackColor = Color.RosyBrown
        btnHelp.Location = New Point(739, 529)
        btnHelp.Name = "btnHelp"
        btnHelp.Size = New Size(164, 29)
        btnHelp.TabIndex = 32
        btnHelp.Text = "Help (User Manual)"
        btnHelp.UseVisualStyleBackColor = False
        ' 
        ' btnExportExcel
        ' 
        btnExportExcel.Location = New Point(718, 6)
        btnExportExcel.Name = "btnExportExcel"
        btnExportExcel.Size = New Size(160, 23)
        btnExportExcel.TabIndex = 33
        btnExportExcel.Text = "Export result to Excel"
        btnExportExcel.UseVisualStyleBackColor = True
        ' 
        ' DebugMode
        ' 
        DebugMode.Location = New Point(643, 529)
        DebugMode.Name = "DebugMode"
        DebugMode.Size = New Size(99, 27)
        DebugMode.TabIndex = 34
        DebugMode.Text = "Debug Log"
        DebugMode.UseVisualStyleBackColor = True
        ' 
        ' Form1
        ' 
        AutoScaleDimensions = New SizeF(7F, 17F)
        AutoScaleMode = AutoScaleMode.Font
        ClientSize = New Size(1683, 673)
        Controls.Add(DebugMode)
        Controls.Add(btnExportExcel)
        Controls.Add(btnHelp)
        Controls.Add(Label46)
        Controls.Add(simResultGrid)
        Controls.Add(chkUseExcel)
        Controls.Add(lblExcelStatus)
        Controls.Add(btnImportExcel)
        Controls.Add(Label6)
        Controls.Add(logwindow)
        Controls.Add(btnSaveNation)
        Controls.Add(btnLoadNation)
        Controls.Add(btnExit)
        Controls.Add(btnClearLog)
        Controls.Add(btnPlotChart)
        Controls.Add(btnExportCSV)
        Controls.Add(btnReset)
        Controls.Add(btnRun)
        Controls.Add(txtStartYear)
        Controls.Add(Label4)
        Controls.Add(btnClear)
        Controls.Add(TabControl1)
        Name = "Form1"
        Text = "SECM Simulator (Societal Evolution Computational Model) V0.5 Alpha"
        CType(simResultGrid, ComponentModel.ISupportInitialize).EndInit()
        TabPage4.ResumeLayout(False)
        TabPage4.PerformLayout()
        TabPage2.ResumeLayout(False)
        TabPage2.PerformLayout()
        TabPage1.ResumeLayout(False)
        TabPage1.PerformLayout()
        TabControl1.ResumeLayout(False)
        TabPage5.ResumeLayout(False)
        TabPage5.PerformLayout()
        ResumeLayout(False)
        PerformLayout()
    End Sub
    Friend WithEvents txtSector1 As Label
    Friend WithEvents txtPopulation1 As Label
    Friend WithEvents txtGDP As Label
    Friend WithEvents Xaxis As Label
    Friend WithEvents Yaxis As Label
    Friend WithEvents txtFinance As Label
    Friend WithEvents txtSector3 As Label
    Friend WithEvents txtSector2 As Label
    Friend WithEvents txtInputFinancialShare As TextBox
    Friend WithEvents txtInputTertiaryShare As TextBox
    Friend WithEvents txtInputSecondaryShare As TextBox
    Friend WithEvents txtInputPrimaryShare As TextBox
    Friend WithEvents txtInputPopulation As TextBox
    Friend WithEvents txtInputGDP As TextBox
    Friend WithEvents txtInputEducation As TextBox
    Friend WithEvents txtInputGini As TextBox
    Friend WithEvents txtInputUnemployment As TextBox
    Friend WithEvents txtInputOverseas As TextBox
    Friend WithEvents txtInputMilitary As TextBox
    Friend WithEvents txtInputHealthcare As TextBox
    Friend WithEvents txtInputTradeBalance As TextBox
    Friend WithEvents txtInputNatureIndex As TextBox
    Friend WithEvents btnClear As Button
    Friend WithEvents Label4 As Label
    Friend WithEvents txtStartYear As TextBox
    Friend WithEvents btnRun As Button
    Friend WithEvents btnReset As Button
    Friend WithEvents btnExportCSV As Button
    Friend WithEvents btnPlotChart As Button
    Friend WithEvents btnClearLog As Button
    Friend WithEvents btnExit As Button
    Friend WithEvents btnLoadNation As Button
    Friend WithEvents btnSaveNation As Button
    Friend WithEvents logwindow As RichTextBox
    Friend WithEvents saveProfileDialog As SaveFileDialog
    Friend WithEvents openProfileDialog As OpenFileDialog
    Friend WithEvents txtInputArableLand As TextBox
    Friend WithEvents txtInputAreaPerCapita As TextBox
    Friend WithEvents Label6 As Label
    Friend WithEvents btnImportExcel As Button
    Friend WithEvents lblExcelStatus As Label
    Friend WithEvents OpenFileDialog1 As OpenFileDialog
    Friend WithEvents OpenFileDialog2 As OpenFileDialog
    Friend WithEvents chkUseExcel As CheckBox
    Friend WithEvents simResultGrid As DataGridView
    Friend WithEvents TabPage4 As TabPage
    Friend WithEvents TabPage2 As TabPage
    Friend WithEvents TabPage1 As TabPage
    Friend WithEvents txtGini As TextBox
    Friend WithEvents txtLPI As TextBox
    Friend WithEvents ArableLandTotal As TextBox
    Friend WithEvents txtMCapGDP As TextBox
    Friend WithEvents txtMilitaryGDP As TextBox
    Friend WithEvents txtUnemploymentRate As TextBox
    Friend WithEvents txtDebtRate As TextBox
    Friend WithEvents txtSavingsRate As TextBox
    Friend WithEvents txtTrust As TextBox
    Friend WithEvents txtTFP As TextBox
    Friend WithEvents txtSTEMRate As TextBox
    Friend WithEvents txtEduRate As TextBox
    Friend WithEvents txtPatentCount As TextBox
    Friend WithEvents txtAnimalPower As TextBox
    Friend WithEvents txtPrimaryEnergy As TextBox
    Friend WithEvents txtPopulation As TextBox
    Friend WithEvents txtYear As TextBox
    Friend WithEvents Label1 As Label
    Friend WithEvents Label28 As Label
    Friend WithEvents Label27 As Label
    Friend WithEvents Label26 As Label
    Friend WithEvents Label25 As Label
    Friend WithEvents Label24 As Label
    Friend WithEvents Label23 As Label
    Friend WithEvents Label22 As Label
    Friend WithEvents Label21 As Label
    Friend WithEvents Label20 As Label
    Friend WithEvents Label19 As Label
    Friend WithEvents Label18 As Label
    Friend WithEvents Label17 As Label
    Friend WithEvents Label16 As Label
    Friend WithEvents Label15 As Label
    Friend WithEvents Label5 As Label
    Friend WithEvents Label32 As Label
    Friend WithEvents TabControl1 As TabControl
    Friend WithEvents Label46 As Label
    Friend WithEvents btnHelp As Button
    Friend WithEvents btnExportExcel As Button
    Friend WithEvents TabPage5 As TabPage
    Friend WithEvents Label45 As Label
    Friend WithEvents Label37 As Label
    Friend WithEvents Label36 As Label
    Friend WithEvents txtKY As TextBox
    Friend WithEvents txtLimitCoef As TextBox
    Friend WithEvents txtSAccumCoef As TextBox
    Friend WithEvents txtBonusP As TextBox
    Friend WithEvents Label35 As Label
    Friend WithEvents Label34 As Label
    Friend WithEvents Label41 As Label
    Friend WithEvents Label9 As Label
    Friend WithEvents Label13 As Label
    Friend WithEvents Label11 As Label
    Friend WithEvents txtSInit As TextBox
    Friend WithEvents txtBonusTheta As TextBox
    Friend WithEvents txtSDecayRate As TextBox
    Friend WithEvents Label10 As Label
    Friend WithEvents Label30 As Label
    Friend WithEvents Label43 As Label
    Friend WithEvents Label44 As Label
    Friend WithEvents txtGammaX As TextBox
    Friend WithEvents txtGammaS As TextBox
    Friend WithEvents Label31 As Label
    Friend WithEvents Label33 As Label
    Friend WithEvents Label66 As Label
    Friend WithEvents Label67 As Label
    Friend WithEvents Label51 As Label
    Friend WithEvents Label50 As Label
    Friend WithEvents Label49 As Label
    Friend WithEvents Label68 As Label
    Friend WithEvents txtMuY0 As TextBox
    Friend WithEvents Label58 As Label
    Friend WithEvents txtYBaseB1 As TextBox
    Friend WithEvents Label55 As Label
    Friend WithEvents txtYBaseA1 As TextBox
    Friend WithEvents Label52 As Label
    Friend WithEvents txtYBaseA0 As TextBox
    Friend WithEvents Label48 As Label
    Friend WithEvents Label47 As Label
    Friend WithEvents Label38 As Label
    Friend WithEvents txtSocialSecIndex As TextBox
    Friend WithEvents Label71 As Label
    Friend WithEvents txtUnempInsCoverage As TextBox
    Friend WithEvents Label70 As Label
    Friend WithEvents txtFreeEduCoverage As TextBox
    Friend WithEvents Label69 As Label
    Friend WithEvents txtPensionCoverage As TextBox
    Friend WithEvents Label59 As Label
    Friend WithEvents txtHealthCoverage As TextBox
    Friend WithEvents Label57 As Label
    Friend WithEvents Label56 As Label
    Friend WithEvents Label54 As Label
    Friend WithEvents Label53 As Label
    Friend WithEvents Label42 As Label
    Friend WithEvents Label63 As Label
    Friend WithEvents Label64 As Label
    Friend WithEvents Label65 As Label
    Friend WithEvents Label62 As Label
    Friend WithEvents Label61 As Label
    Friend WithEvents txtOmegaShock As TextBox
    Friend WithEvents txtZShock As TextBox
    Friend WithEvents Label60 As Label
    Friend WithEvents DebugMode As CheckBox
    Friend WithEvents txtPovertyRate As TextBox
    Friend WithEvents Label74 As Label
    Friend WithEvents Label75 As Label
    Friend WithEvents txtMurderRate As TextBox
    Friend WithEvents Label72 As Label
    Friend WithEvents Label73 As Label
    Friend WithEvents txtZcWeight As TextBox
    Friend WithEvents Label40 As Label
    Friend WithEvents Label2 As Label
    Friend WithEvents txtLandCapLimitCoef As TextBox
    Friend WithEvents Label76 As Label
    Friend WithEvents Label77 As Label
    Friend WithEvents txtDrift As TextBox
    Friend WithEvents Label3 As Label
    Friend WithEvents Label7 As Label
    Friend WithEvents txtPatentLast As TextBox
    Friend WithEvents txtAnimalPowerLast As TextBox
    Friend WithEvents txtPrimaryEnergyLast As TextBox
    Friend WithEvents txtPopulationLast As TextBox
    Friend WithEvents Label78 As Label
    Friend WithEvents Label80 As Label
    Friend WithEvents txtYFirst As TextBox
    Friend WithEvents Label79 As Label
    Friend WithEvents UrbanRate As TextBox
    Friend WithEvents Label82 As Label
    Friend WithEvents Label81 As Label
    Friend WithEvents Label83 As Label
    Friend WithEvents txtYLimitDecayBeta As TextBox
    Friend WithEvents Label8 As Label
    Friend WithEvents Label12 As Label
    Friend WithEvents txtZImpactK As TextBox

End Class
