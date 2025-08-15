Public Class FormHelp
    Public Sub New()
        ' 这是初始化窗体控件的必需调用
        InitializeComponent()
    End Sub
    Private Sub FormHelp_Load(sender As Object, e As EventArgs) Handles MyBase.Load
        Dim helpText As String = ""

        helpText &= "SECM V0.5 Alpha – Quick Help" & vbCrLf & vbCrLf

        helpText &= "1. What is SECM?" & vbCrLf
        helpText &= "The Societal Evolution Computational Model (SECM) simulates how productivity (X), social tension (Y), carrying capacity (Y_limit), systemic vulnerability (Ω), and innovation (X_bonus) interact over time." & vbCrLf
        helpText &= "It can be used for historical backtesting or scenario-based experiments." & vbCrLf & vbCrLf

        helpText &= "2. How to Use" & vbCrLf
        helpText &= "Two operation modes:" & vbCrLf
        helpText &= "  1) Snapshot Mode – Enter yearly data manually in the UI:" & vbCrLf
        helpText &= "     - Fill Snapshot Pt.1 with demographic, energy, and economy data." & vbCrLf
        helpText &= "     - Fill Snapshot Pt.2 with social structure, coverage rates, and shocks." & vbCrLf
        helpText &= "  2) Excel Batch Mode – Import the provided Excel template:" & vbCrLf
        helpText &= "     - Prepare data in SECM_V0.5_AllInputs_Template.xlsx." & vbCrLf
        helpText &= "     - Empty cells will use current UI parameter values." & vbCrLf
        helpText &= "Click Run Simulation to execute. Results appear in the log area and can be exported." & vbCrLf & vbCrLf

        helpText &= "3. Useful Tips" & vbCrLf
        helpText &= "- YFirst only shifts the Y curve vertically — it does not change the trend." & vbCrLf
        helpText &= "- Watch Z_eff for turning points — a sign that tension direction is changing." & vbCrLf
        helpText &= "- In Excel mode, parameters can change mid-run by editing rows." & vbCrLf
        helpText &= "- Use View Chart to export clean CSVs for plotting." & vbCrLf & vbCrLf

        helpText &= "4. Notes & Disclaimer" & vbCrLf
        helpText &= "- SECM is an analytical tool, not a prediction oracle." & vbCrLf
        helpText &= "- Output quality depends on input data accuracy." & vbCrLf
        helpText &= "- Large positive Ω means lower carrying capacity; large negative Ω means stronger resilience." & vbCrLf
        helpText &= "- For full details, see the included User Manual." & vbCrLf

        rtbHelp.Text = helpText
    End Sub



End Class