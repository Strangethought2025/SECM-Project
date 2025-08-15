<Global.Microsoft.VisualBasic.CompilerServices.DesignerGenerated()> _
Partial Class FormHelp
    Inherits System.Windows.Forms.Form

    'Form 重写 Dispose，以清理组件列表。
    <System.Diagnostics.DebuggerNonUserCode()> _
    Protected Overrides Sub Dispose(ByVal disposing As Boolean)
        Try
            If disposing AndAlso components IsNot Nothing Then
                components.Dispose()
            End If
        Finally
            MyBase.Dispose(disposing)
        End Try
    End Sub

    'Windows 窗体设计器所必需的
    Private components As System.ComponentModel.IContainer

    '注意: 以下过程是 Windows 窗体设计器所必需的
    '可以使用 Windows 窗体设计器修改它。  
    '不要使用代码编辑器修改它。
    <System.Diagnostics.DebuggerStepThrough()> _
    Private Sub InitializeComponent()
        Dim resources As System.ComponentModel.ComponentResourceManager = New System.ComponentModel.ComponentResourceManager(GetType(FormHelp))
        rtbHelp = New RichTextBox()
        SuspendLayout()
        ' 
        ' rtbHelp
        ' 
        rtbHelp.Dock = DockStyle.Fill
        rtbHelp.Location = New Point(0, 0)
        rtbHelp.Name = "rtbHelp"
        rtbHelp.ReadOnly = True
        rtbHelp.Size = New Size(804, 663)
        rtbHelp.TabIndex = 0
        rtbHelp.Text = resources.GetString("rtbHelp.Text")
        ' 
        ' FormHelp
        ' 
        AutoScaleDimensions = New SizeF(7F, 17F)
        AutoScaleMode = AutoScaleMode.Font
        ClientSize = New Size(804, 663)
        Controls.Add(rtbHelp)
        Name = "FormHelp"
        Text = "User Manual"
        ResumeLayout(False)
    End Sub

    Friend WithEvents rtbHelp As RichTextBox
End Class
