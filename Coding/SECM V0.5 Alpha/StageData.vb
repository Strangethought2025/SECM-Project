Public Class StageData

    ' 存储变量组：X/Y/Z/其他全都在这
    Public Vars As New Dictionary(Of String, Double)

    ' 运行步数（单位年 or tick）
    Public Steps As Integer = 1

    ' 可选：阶段自定义名称（用于UI显示）
    Public Label As String = ""

    ' 可选：仿真运行结果缓存（上次执行结果）
    Public Output As New Dictionary(Of String, String)

    ' 可选：构造函数（支持一行创建）
    Public Sub New(Optional inputVars As Dictionary(Of String, Double) = Nothing, Optional stepsVal As Integer = 1)
        If inputVars IsNot Nothing Then
            Me.Vars = New Dictionary(Of String, Double)(inputVars)
        End If
        Me.Steps = stepsVal
    End Sub

End Class