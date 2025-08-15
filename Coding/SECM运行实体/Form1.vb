Imports System.IO
Imports System.Text
Imports NPOI.SS.UserModel
Imports NPOI.XSSF.UserModel
Imports Newtonsoft.Json
Imports System.Globalization

Public Class Form1
    Private lastResult As Dictionary(Of String, Double)
    Public Sub New()
        ' 这是初始化窗体控件的必需调用
        InitializeComponent()
    End Sub
    Private loadedData As List(Of Dictionary(Of String, Double)) = New List(Of Dictionary(Of String, Double))()
    Private stageList As List(Of StageData) = New List(Of StageData)()
    Private simulationResults As New List(Of Dictionary(Of String, Double))()

    Public Function LoadOneRowFromExcel(dt As DataTable, rowIndex As Integer) As Dictionary(Of String, String)
        Dim rowDict As New Dictionary(Of String, String)

        If rowIndex >= 0 AndAlso rowIndex < dt.Rows.Count Then
            For Each col As DataColumn In dt.Columns
                Dim key As String = col.ColumnName.Trim()
                Dim value As String = dt.Rows(rowIndex)(col).ToString().Trim()
                rowDict(key) = value
            Next
        End If

        Return rowDict
    End Function
    Private Function ParseExcelFile(filePath As String) As List(Of Dictionary(Of String, Double))
        Dim result As New List(Of Dictionary(Of String, Double))()
        Dim fs As FileStream = Nothing
        Try
            fs = New FileStream(filePath, FileMode.Open, FileAccess.Read)
            Dim workbook = New XSSFWorkbook(fs)
            Dim sheet = workbook.GetSheetAt(0)

            ' 第一行是字段名
            Dim headerRow = sheet.GetRow(0)
            Dim headers As New List(Of String)
            For i = 0 To headerRow.LastCellNum - 1
                Dim cell = headerRow.GetCell(i)
                headers.Add(If(cell IsNot Nothing, cell.ToString(), ""))
            Next

            ' 从第二行开始逐行读数据
            For i = 1 To sheet.LastRowNum
                Dim row = sheet.GetRow(i)
                If row Is Nothing Then Continue For

                Dim rowDict As New Dictionary(Of String, Double)
                For j = 0 To headers.Count - 1
                    Dim key = headers(j)
                    If String.IsNullOrWhiteSpace(key) Then Continue For

                    Dim val As Double = 0
                    Dim cell = row.GetCell(j)
                    If cell IsNot Nothing AndAlso Double.TryParse(cell.ToString(), val) Then
                        rowDict(key) = val
                    End If
                Next

                If rowDict.Count > 0 Then
                    result.Add(rowDict)
                End If
            Next

        Catch ex As IOException
            MessageBox.Show(
            "Excel 文件正在被其它程序占用（例如未关闭），请关闭所有 Excel 后重试！" & vbCrLf & vbCrLf &
            "详细错误：" & ex.Message,
            "文件被占用", MessageBoxButtons.OK, MessageBoxIcon.Warning)
        Catch ex As Exception
            MessageBox.Show("导入 Excel 文件发生未知错误：" & ex.Message,
                        "导入失败", MessageBoxButtons.OK, MessageBoxIcon.Error)
        Finally
            If fs IsNot Nothing Then fs.Close()
        End Try

        Return result
    End Function

    Private Function SafeGet(dict As Dictionary(Of String, Double), key As String, Optional defaultValue As Double = 0) As Double
        If dict.ContainsKey(key) Then
            Return dict(key)
        Else
            Return defaultValue
        End If
    End Function

    Private Sub FillParameterFallbacks(dict As Dictionary(Of String, Double))
        Dim defaults As New Dictionary(Of String, Double)

        ' ==== Y轴结构张力主轴 ====
        defaults.Add("kY", CDbl(SafeVal(txtKY.Text)))
        defaults.Add("kLimit", CDbl(SafeVal(txtLimitCoef.Text)))
        defaults.Add("YLimitEps", 0.01)
        defaults.Add("YFirst", CDbl(SafeVal(txtYFirst.Text)))

        ' ==== 科技红利主轴 ====
        defaults.Add("BonusTheta", CDbl(SafeVal(txtBonusTheta.Text)))
        defaults.Add("BonusP", CDbl(SafeVal(txtBonusP.Text)))

        ' ==== Z主轴机制 ====
        defaults.Add("ZcWeight", CDbl(SafeVal(txtZcWeight.Text)))
        defaults.Add("GammaS", CDbl(SafeVal(txtGammaS.Text)))
        defaults.Add("GammaX", CDbl(SafeVal(txtGammaX.Text)))
        defaults.Add("Drift", CDbl(SafeVal(txtDrift.Text)))
        defaults.Add("ZImpactK", CDbl(SafeVal(txtZImpactK.Text))) ' ✅ 新增：Z 对 Y 的影响系数

        ' ==== 外部冲击 ====
        defaults.Add("OmegaShock", CDbl(SafeVal(txtOmegaShock.Text)))
        defaults.Add("ZShock", CDbl(SafeVal(txtZShock.Text)))

        ' ==== 危机池机制 ====
        defaults.Add("SDecayRate", CDbl(SafeVal(txtSDecayRate.Text)))
        defaults.Add("S_prev", CDbl(SafeVal(txtSInit.Text)))

        ' ==== 结构张力首年计算用参数 ====
        defaults.Add("YBaseA0", CDbl(SafeVal(txtYBaseA0.Text)))
        defaults.Add("YBaseA1", CDbl(SafeVal(txtYBaseA1.Text)))
        defaults.Add("YBaseB1", CDbl(SafeVal(txtYBaseB1.Text)))
        defaults.Add("MuY0", CDbl(SafeVal(txtMuY0.Text)))

        ' ==== 新增：X 倒退时 Y_limit 衰减系数 β ====
        defaults.Add("YLimitDecayBeta", CDbl(SafeVal(txtYLimitDecayBeta.Text)))

        ' === 若缺失或为0则用 fallback 替代 ===
        For Each kvp In defaults
            If Not dict.ContainsKey(kvp.Key) _
        OrElse Math.Abs(dict(kvp.Key)) < 0.000000001 Then
                dict(kvp.Key) = kvp.Value
            End If
        Next
    End Sub




    Private Sub LoadPresetFromJson(filePath As String)
        Try
            Dim jsonText As String = File.ReadAllText(filePath)
            Dim paramDict As Dictionary(Of String, Object) = JsonConvert.DeserializeObject(Of Dictionary(Of String, Object))(jsonText)

            For Each kvp In paramDict
                Dim key = kvp.Key.Trim()
                Dim valueStr = kvp.Value.ToString()

                ' 动态寻找并赋值对应控件
                Dim ctrl = Me.Controls.Find("txt" & key, True).FirstOrDefault()
                If ctrl IsNot Nothing AndAlso TypeOf ctrl Is TextBox Then
                    CType(ctrl, TextBox).Text = valueStr
                End If
            Next

            ' --- DEBUG 输出预设参数 ---
            logwindow.AppendText("【DEBUG-预设加载】" & vbCrLf)
            For Each kvp In paramDict
                logwindow.AppendText("    " & kvp.Key & " → " & kvp.Value.ToString() & vbCrLf)
            Next

            MessageBox.Show("✅ 已加载预设：" & Path.GetFileName(filePath), "成功", MessageBoxButtons.OK, MessageBoxIcon.Information)

        Catch ex As Exception
            MessageBox.Show("❌ 加载预设失败：" & ex.Message, "错误", MessageBoxButtons.OK, MessageBoxIcon.Error)
        End Try

    End Sub
    Private Sub ClearAllSimulationState()
        simulationResults.Clear()
        lastResult = Nothing
        logwindow.Clear()
        simResultGrid.DataSource = Nothing
        simResultGrid.Rows.Clear()
        simResultGrid.Refresh()
    End Sub

    Private Function GetDebugMode() As CheckBox
        Return DebugMode
    End Function
    ''' <summary>
    ''' 每轮推进前，只保留下一轮需要的关键状态变量，其余清空
    ''' </summary>
    Private Sub ClearForNextYear(dict As Dictionary(Of String, Double))
        Dim keysToKeep As New HashSet(Of String) From {
        "Y_prev",        ' 上一年的 Y_t
        "XBase",         ' 基准产能
        "X_normalLast",  ' 上一年的归一化产能
        "X_realLast",    ' 上一年的真实产能
        "Z_prev",        ' 上一年的 Z_t
        "S_prev",        ' 上一年的 S_t
        "S_t",           ' 危机池当前值
        "PatentLast"     ' 上一年的专利数
    }

        Dim keys = dict.Keys.ToList()
        For Each key In keys
            If Not keysToKeep.Contains(key) Then
                dict(key) = 0
            End If
        Next
    End Sub


    Private Sub RunSimulationFromExcel(dataList As List(Of Dictionary(Of String, Double)), debugMode As CheckBox)
        ' ===== 全局初始化 =====
        ClearAllSimulationState()
        lastResult = Nothing

        Dim engine As New SECM_Engine()
        Dim globalXBase As Double = 0
        logwindow.Clear()
        simulationResults.Clear()

        ' 按年份排序
        Dim sortedData = dataList.OrderBy(Function(d) If(d.ContainsKey("Year"), d("Year"), 0)).ToList()

        For Each row In sortedData
            ' === 1. 读取当年 Excel 数据 ===
            Dim inputDict As New Dictionary(Of String, Double)
            For Each kvp In row
                inputDict(kvp.Key) = kvp.Value
            Next

            ' === 2. 如果不是首年，补回跨年必须的状态变量 ===
            If lastResult IsNot Nothing Then
                inputDict("Y_prev") = SafeGet(lastResult, "Y_t")
                inputDict("S_prev") = SafeGet(lastResult, "S_t")
                inputDict("Z_prev") = SafeGet(lastResult, "Z_t")
                inputDict("X_prev") = SafeGet(lastResult, "X_normal")
                inputDict("XBase") = SafeGet(lastResult, "XBase")
                inputDict("PatentLast") = SafeGet(lastResult, "PatentCount")

                ' === 从 Excel Last 列计算 X_normalLast ===
                Dim peLast As Double = SafeGet(inputDict, "PrimaryEnergyLast")
                Dim apLast As Double = SafeGet(inputDict, "AnimalPowerLast")
                Dim popLast As Double = SafeGet(inputDict, "PopulationLast")
                If peLast > 0 OrElse apLast > 0 OrElse popLast > 0 Then
                    Dim humanKWPE_Last As Double = (popLast * 130.0) / 1_000_000
                    Dim X_real_last As Double = peLast + apLast + humanKWPE_Last
                    Dim X_normal_last As Double = If(globalXBase > 0, X_real_last / globalXBase, 0)
                    inputDict("X_normalLast") = X_normal_last
                End If
            End If

            ' === 3. 映射字段 & 参数补齐 ===
            inputDict = engine.MapExcelFields(inputDict)
            FillParameterFallbacks(inputDict)

            ' === 4. 首年 XBase 计算 ===
            If globalXBase = 0 Then
                Dim pe As Double = SafeGet(inputDict, "PrimaryEnergy")
                Dim ap As Double = SafeGet(inputDict, "AnimalPower")
                Dim pop As Double = SafeGet(inputDict, "Population")
                Dim humanKWPE As Double = (pop * 130.0) / 1_000_000
                Dim X_real As Double = pe + ap + humanKWPE
                If X_real < 1 Then X_real = 1
                globalXBase = X_real
            End If
            inputDict("XBase") = globalXBase

            ' 首年才初始化这些
            If lastResult Is Nothing Then
                inputDict("X_prev") = 0
                inputDict("Y_prev") = 0
                inputDict("Z_prev") = 0
                inputDict("S_prev") = SafeVal(txtSInit.Text)

                inputDict("YBaseA0") = SafeVal(txtYBaseA0.Text)
                inputDict("YBaseA1") = SafeVal(txtYBaseA1.Text)
                inputDict("YBaseB1") = SafeVal(txtYBaseB1.Text)
                inputDict("MuY0") = SafeVal(txtMuY0.Text)

                If Not inputDict.ContainsKey("PatentLast") Then
                    inputDict("PatentLast") = SafeGet(inputDict, "PatentCount")
                End If
            End If

            ' === 5. 主引擎运行 ===
            Try
                Dim isFirstYear As Boolean = (lastResult Is Nothing)
                Dim result As Dictionary(Of String, Double) =
                engine.RunOnce_V25(inputDict, isFirstYear, debugMode.Checked, logwindow)

                simulationResults.Add(result)
                lastResult = result
                lastResult("PatentLast") = SafeGet(inputDict, "PatentCount")

                ' 输出日志
                If simulationResults.Count = 1 Then
                    logwindow.AppendText("Year,X_real,X_bonus_t,X_bonus_norm,Z_t,Y_t,Y_limit,S_t,I_reset" & vbCrLf)
                End If

                Dim outLine As String = SafeGet(inputDict, "Year").ToString() & "," &
                Math.Round(SafeGet(result, "X_real"), 4) & "," &
                Math.Round(SafeGet(result, "X_bonus_t"), 4) & "," &
                Math.Round(SafeGet(result, "X_bonus_norm"), 4) & "," &
                Math.Round(SafeGet(result, "Z_t"), 4) & "," &
                Math.Round(SafeGet(result, "Y_t"), 4) & "," &
                Math.Round(SafeGet(result, "Y_limit"), 4) & "," &
                Math.Round(SafeGet(result, "S_t"), 4) & "," &
                Math.Round(SafeGet(result, "I_reset"), 0)

                logwindow.AppendText(outLine & vbCrLf)

            Catch ex As Exception
                logwindow.AppendText($"❌ Year {SafeGet(inputDict, "Year")} 运行出错：{ex.Message}" & vbCrLf)
            End Try
        Next

        logwindow.AppendText("✅ Excel 仿真全部完成。" & vbCrLf)

        ' === 6. 输出 DataTable 到 DataGridView ===
        Dim dt As New DataTable()
        simResultGrid.AutoResizeColumns()
        simResultGrid.AutoSizeColumnsMode = DataGridViewAutoSizeColumnsMode.AllCells
        simResultGrid.AllowUserToAddRows = False

        If simulationResults.Count > 0 Then
            For Each key In simulationResults(0).Keys
                dt.Columns.Add(key)
            Next
            For Each result In simulationResults
                Dim row As DataRow = dt.NewRow()
                For Each key In result.Keys
                    row(key) = result(key)
                Next
                dt.Rows.Add(row)
            Next
            simResultGrid.DataSource = dt
        End If
    End Sub



    Private Function SafeVal(txt As String) As Double
        Dim v As Double

        ' ① 先按 InvariantCulture（小数点“.”）试
        If Double.TryParse(txt, NumberStyles.Any,
                       CultureInfo.InvariantCulture, v) Then
            Return v
        End If

        ' ② 再按本机文化（小数点可能是“,”）试
        If Double.TryParse(txt, NumberStyles.Any,
                       CultureInfo.CurrentCulture, v) Then
            Return v
        End If

        ' ③ 还不行就 0
        Return 0
    End Function

    ''' <summary>
    ''' 安全写入日志窗口（需启用 DebugMode）
    ''' </summary>
    Public Shared Sub DebugLog(msg As String)
        Try
            ' 找到当前 Form1 实例（适用于单窗体应用）
            If Application.OpenForms().OfType(Of Form1).Any() Then
                Dim f1 As Form1 = Application.OpenForms().OfType(Of Form1).First()
                If f1.DebugMode IsNot Nothing AndAlso f1.DebugMode.Checked AndAlso f1.logwindow IsNot Nothing Then
                    f1.logwindow.AppendText(DateTime.Now.ToString("HH:mm:ss") & " | " & msg & vbCrLf)
                    f1.logwindow.SelectionStart = f1.logwindow.Text.Length
                    f1.logwindow.ScrollToCaret()
                End If
            End If
        Catch ex As Exception
            Debug.Print("日志写入失败：" & ex.Message)
        End Try
    End Sub





    Private Sub btnRun_Click(sender As Object, e As EventArgs) Handles btnRun.Click
        logwindow.Clear()

        If chkUseExcel.Checked Then
            ' === Excel 数据模式 ===
            If loadedData Is Nothing OrElse loadedData.Count = 0 Then
                MessageBox.Show("请先导入 Excel 数据。", "错误", MessageBoxButtons.OK, MessageBoxIcon.Warning)
                Return
            End If

            RunSimulationFromExcel(loadedData, GetDebugMode())

        Else
            ' === Snapshot 模式 ===
            If stageList.Count = 0 Then
                MessageBox.Show("尚未添加任何阶段数据。", "提示", MessageBoxButtons.OK, MessageBoxIcon.Information)
                Return
            End If

            RunSimulationFromStageList()
        End If
    End Sub


    Private Sub btnImportExcel_Click(sender As Object, e As EventArgs) Handles btnImportExcel.Click
        Dim openFileDialog As New OpenFileDialog()
        openFileDialog.Filter = "Excel 文件 (*.xlsx)|*.xlsx"
        openFileDialog.Title = "请选择要导入的 Excel 文件"

        If openFileDialog.ShowDialog() = DialogResult.OK Then
            Dim filePath As String = openFileDialog.FileName
            loadedData = ParseExcelFile(filePath)

            If loadedData.Count > 0 Then
                MessageBox.Show("✅ Excel 数据导入成功，共 " & loadedData.Count & " 条记录。", "导入成功", MessageBoxButtons.OK, MessageBoxIcon.Information)
                lblExcelStatus.Text = "Loaded: " & Path.GetFileName(filePath)  ' ✅ 显示文件名
            Else
                MessageBox.Show("⚠️ 没有读取到有效数据。", "导入失败", MessageBoxButtons.OK, MessageBoxIcon.Warning)
                lblExcelStatus.Text = "No file loaded"
            End If
        Else
            lblExcelStatus.Text = "No file loaded" ' ✅ 用户取消导入
        End If
    End Sub

    Private Sub RunSimulationFromStageList()
        Dim engine As New SECM_Engine()
        logwindow.Clear()
        simulationResults.Clear()

        Dim yearCounter As Integer = 0
        If Not Integer.TryParse(txtStartYear.Text, yearCounter) Then
            yearCounter = 0
        End If

        For i As Integer = 0 To stageList.Count - 1
            Dim stage = stageList(i)
            Dim inputDict = stage.Vars
            Dim steps = stage.Steps

            ' 字段映射 & 参数补全
            inputDict = engine.MapExcelFields(inputDict)
            FillParameterFallbacks(inputDict)

            For stepIndex As Integer = 1 To steps
                If yearCounter > 0 Then
                    inputDict("Year") = yearCounter
                End If

                ' 外部冲击 fallback
                If Not inputDict.ContainsKey("ZShock") Then inputDict("ZShock") = SafeVal(txtZShock.Text)
                If Not inputDict.ContainsKey("OmegaShock") Then inputDict("OmegaShock") = SafeVal(txtOmegaShock.Text)

                ' ===== 首年初始化 =====
                If lastResult Is Nothing Then
                    inputDict("X_prev") = 0
                    inputDict("Y_prev") = 0
                    inputDict("Z_prev") = SafeVal(txtSAccumCoef.Text)
                    inputDict("S_prev") = SafeVal(txtSInit.Text)

                    ' 首年 X_base 自动赋值（单位：百万千瓦时）
                    Dim pe As Double = SafeGet(inputDict, "PrimaryEnergy")
                    Dim ap As Double = SafeGet(inputDict, "AnimalPower")
                    Dim pop As Double = SafeGet(inputDict, "Population")
                    Dim humanKWPE As Double = (pop * 130) / 1_000_000
                    Dim X_real As Double = pe + ap + humanKWPE
                    If X_real < 1 Then X_real = 1
                    inputDict("XBase") = X_real

                    ' 结构张力参数
                    inputDict("YBaseA0") = SafeVal(txtYBaseA0.Text)
                    inputDict("YBaseA1") = SafeVal(txtYBaseA1.Text)
                    inputDict("YBaseB1") = SafeVal(txtYBaseB1.Text)
                    inputDict("MuY0") = SafeVal(txtMuY0.Text)

                    ' 如果 Excel 或 Stage 数据中已有首年 Y_base 输入，则直接使用
                    If inputDict.ContainsKey("YFirst") Then
                        ' 直接传给引擎的 YFirst 参数
                    End If

                    ' 专利递推初始化
                    If Not inputDict.ContainsKey("PatentLast") Then
                        inputDict("PatentLast") = SafeGet(inputDict, "PatentCount")
                    End If
                Else
                    ' 非首年状态递推
                    inputDict("X_prev") = SafeGet(lastResult, "X_normal")
                    inputDict("Y_prev") = SafeGet(lastResult, "Y_t")
                    inputDict("Z_prev") = SafeGet(lastResult, "Z_t")
                    inputDict("S_prev") = SafeGet(lastResult, "S_t")
                    If lastResult.ContainsKey("PatentCount") Then
                        inputDict("PatentLast") = lastResult("PatentCount")
                    End If
                End If

                ' ===== 主引擎运行（V25） =====
                Try
                    Dim isFirstYear As Boolean = (lastResult Is Nothing)
                    Dim result As Dictionary(Of String, Double) = engine.RunOnce_V25(inputDict, isFirstYear, DebugMode.Checked, logwindow)
                    simulationResults.Add(result)
                    lastResult = result

                    ' 首年输出表头
                    If simulationResults.Count = 1 Then
                        logwindow.AppendText("Year,X_real,X_bonus_t,X_bonus_norm,Z_t,Y_t,Y_base,Y_limit,S_t,I_reset" & vbCrLf)
                    End If

                    ' 每年输出结果行
                    Dim outLine As String = SafeGet(inputDict, "Year").ToString() & "," &
                    Math.Round(result("X_real"), 4) & "," &
                    Math.Round(result("X_bonus_t"), 4) & "," &
                    Math.Round(result("X_bonus_norm"), 4) & "," &
                    Math.Round(result("Z_t"), 4) & "," &
                    Math.Round(result("Y_t"), 4) & "," &
                    Math.Round(result("Y_base"), 4) & "," &
                    Math.Round(result("Y_limit"), 4) & "," &
                    Math.Round(result("S_t"), 4) & "," &
                    Math.Round(result("I_reset"), 0)
                    logwindow.AppendText(outLine & vbCrLf)

                Catch ex As Exception
                    logwindow.AppendText($"❌ 错误（Year {SafeGet(inputDict, "Year")}）：{ex.Message}" & vbCrLf)
                End Try

                yearCounter += 1
            Next
        Next

        logwindow.AppendText("✅ Snapshot 模式仿真全部完成。" & vbCrLf)

        ' 输出到 DataGridView
        Dim dt As New DataTable()
        simResultGrid.AutoResizeColumns()
        simResultGrid.AutoSizeColumnsMode = DataGridViewAutoSizeColumnsMode.AllCells
        simResultGrid.AllowUserToAddRows = False

        If simulationResults.Count > 0 Then
            For Each key In simulationResults(0).Keys
                dt.Columns.Add(key)
            Next
            For Each result In simulationResults
                Dim row As DataRow = dt.NewRow()
                For Each key In result.Keys
                    row(key) = result(key)
                Next
                dt.Rows.Add(row)
            Next
            simResultGrid.DataSource = dt
        End If
    End Sub





    Private Function GetAllTextBoxes(ctrl As Control) As IEnumerable(Of TextBox)
        Dim list As New List(Of TextBox)
        For Each child As Control In ctrl.Controls
            If TypeOf child Is TextBox Then
                list.Add(CType(child, TextBox))
            ElseIf child.HasChildren Then
                list.AddRange(GetAllTextBoxes(child))
            End If
        Next
        Return list
    End Function

    Private Sub btnLoadPreset_Click(sender As Object, e As EventArgs) Handles btnLoadNation.Click
        Dim dialog As New OpenFileDialog()
        dialog.Title = "请选择国家预设 JSON 文件"
        dialog.Filter = "JSON 文件 (*.json)|*.json"
        dialog.InitialDirectory = Application.StartupPath & "\Presets"

        If dialog.ShowDialog() = DialogResult.OK Then
            LoadPresetFromJson(dialog.FileName)
        End If
    End Sub
    Private Sub btnSavePreset_Click(sender As Object, e As EventArgs) Handles btnSaveNation.Click
        Dim paramDict As New Dictionary(Of String, Object)()

        ' 递归遍历所有 TextBox 控件，保证TabPage/Panel/GroupBox里的参数都能保存
        For Each tb As TextBox In GetAllTextBoxes(Me)
            If tb.Name.StartsWith("txt") Then
                Dim fieldName As String = tb.Name.Substring(3)
                paramDict(fieldName) = tb.Text
            End If
        Next

        ' 弹出保存对话框
        Dim dialog As New SaveFileDialog()
        dialog.Title = "保存当前参数为预设"
        dialog.Filter = "JSON 文件 (*.json)|*.json"
        dialog.FileName = "CustomPreset_" & DateTime.Now.ToString("yyyyMMdd_HHmmss") & ".json"
        dialog.InitialDirectory = Application.StartupPath & "\Presets"

        If dialog.ShowDialog() = DialogResult.OK Then
            Try
                Dim jsonText As String = JsonConvert.SerializeObject(paramDict, Formatting.Indented)
                File.WriteAllText(dialog.FileName, jsonText, Encoding.UTF8)
                MessageBox.Show("✅ 当前参数已保存为预设文件。", "保存成功", MessageBoxButtons.OK, MessageBoxIcon.Information)
            Catch ex As Exception
                MessageBox.Show("❌ 保存失败：" & ex.Message, "错误", MessageBoxButtons.OK, MessageBoxIcon.Error)
            End Try
        End If
    End Sub


    Private Sub ClearAllTextBoxes(parent As Control)
        For Each ctrl As Control In parent.Controls
            If TypeOf ctrl Is TextBox AndAlso ctrl.Name.StartsWith("txt") Then
                CType(ctrl, TextBox).Clear()
            ElseIf ctrl.HasChildren Then
                ClearAllTextBoxes(ctrl)
            End If
        Next
    End Sub

    Private Sub btnClear_Click(sender As Object, e As EventArgs) Handles btnClear.Click
        ClearAllTextBoxes(Me)
        MessageBox.Show("🧹 所有输入框内容已清空。", "已清除", MessageBoxButtons.OK, MessageBoxIcon.Information)
    End Sub

    Private Sub btnReset_Click(sender As Object, e As EventArgs) Handles btnReset.Click
        ' Excel 模式下：使用 Excel 第一行恢复参数
        If chkUseExcel.Checked AndAlso loadedData IsNot Nothing AndAlso loadedData.Count > 0 Then
            Dim firstRow = loadedData(0)
            For Each kvp In firstRow
                Dim key = kvp.Key.Trim()
                Dim ctrl = Me.Controls.Find("txt" & key, True).FirstOrDefault()
                If ctrl IsNot Nothing AndAlso TypeOf ctrl Is TextBox Then
                    CType(ctrl, TextBox).Text = kvp.Value.ToString()
                End If
            Next
            MessageBox.Show("📊 已恢复 Excel 第一行参数。", "已恢复", MessageBoxButtons.OK, MessageBoxIcon.Information)

        Else
            ' 否则回退到默认 preset
            Dim presetPath = Application.StartupPath & "\Presets\USA_1980.json"
            If File.Exists(presetPath) Then
                LoadPresetFromJson(presetPath)
            Else
                MessageBox.Show("❌ 无法加载默认预设文件（USA_1980.json）。", "恢复失败", MessageBoxButtons.OK, MessageBoxIcon.Warning)
            End If
        End If
    End Sub

    Private Sub btnExportCSV_Click(sender As Object, e As EventArgs) Handles btnExportCSV.Click
        If simulationResults Is Nothing OrElse simulationResults.Count = 0 Then
            MessageBox.Show("⚠️ 没有可导出的仿真结果，请先运行仿真。", "无数据", MessageBoxButtons.OK, MessageBoxIcon.Warning)
            Return
        End If

        ' 选择保存路径
        Dim saveDialog As New SaveFileDialog()
        saveDialog.Title = "导出仿真结果为 CSV 文件"
        saveDialog.Filter = "CSV 文件 (*.csv)|*.csv"
        saveDialog.FileName = "SECM_Results_" & DateTime.Now.ToString("yyyyMMdd_HHmmss") & ".csv"
        If saveDialog.ShowDialog() <> DialogResult.OK Then Exit Sub

        Try
            Using writer As New StreamWriter(saveDialog.FileName, False, Encoding.UTF8)
                ' 写入表头（统一字段顺序）
                Dim headers = simulationResults(0).Keys.ToList()
                writer.WriteLine(String.Join(",", headers))

                ' 写入每一行数据（允许部分字段缺失）
                For Each rowDict In simulationResults
                    Dim line = String.Join(",", headers.Select(Function(h) If(rowDict.ContainsKey(h), rowDict(h).ToString("0.####"), "")))
                    writer.WriteLine(line)
                Next
            End Using

            MessageBox.Show("✅ 仿真结果已成功导出！", "导出完成", MessageBoxButtons.OK, MessageBoxIcon.Information)

        Catch ex As Exception
            MessageBox.Show("❌ 导出失败：" & ex.Message, "错误", MessageBoxButtons.OK, MessageBoxIcon.Error)
        End Try
    End Sub

    Private Sub btnClearLog_Click(sender As Object, e As EventArgs) Handles btnClearLog.Click
        logwindow.Clear()
        MessageBox.Show("🗑 日志窗口已清空。", "完成", MessageBoxButtons.OK, MessageBoxIcon.Information)
    End Sub

    Private Sub btnViewChart_Click(sender As Object, e As EventArgs) Handles btnPlotChart.Click
        If simulationResults Is Nothing OrElse simulationResults.Count = 0 Then
            MessageBox.Show("⚠️ 没有可视化的数据，请先运行仿真。", "无数据", MessageBoxButtons.OK, MessageBoxIcon.Warning)
            Return
        End If

        ' 定义需要导出的字段
        Dim chartFields As New List(Of String) From {"Year", "X_real", "Y_t", "Y_limit", "Z_t"}

        ' 保存文件路径
        Dim saveDialog As New SaveFileDialog()
        saveDialog.Title = "导出可视化数据（用于绘图）"
        saveDialog.Filter = "CSV 文件 (*.csv)|*.csv"
        saveDialog.FileName = "SECM_ChartData_" & DateTime.Now.ToString("yyyyMMdd_HHmmss") & ".csv"
        If saveDialog.ShowDialog() <> DialogResult.OK Then Exit Sub

        Try
            Using writer As New StreamWriter(saveDialog.FileName, False, Encoding.UTF8)
                ' 写入表头
                writer.WriteLine(String.Join(",", chartFields))

                ' 写入数据
                For Each rowDict In simulationResults
                    Dim line = String.Join(",", chartFields.Select(Function(f) If(rowDict.ContainsKey(f), rowDict(f).ToString("0.####"), "")))
                    writer.WriteLine(line)
                Next
            End Using

            MessageBox.Show("📊 可视化数据导出成功！你可以用 Excel 或 Python 绘图。", "导出完成", MessageBoxButtons.OK, MessageBoxIcon.Information)

        Catch ex As Exception
            MessageBox.Show("❌ 导出失败：" & ex.Message, "错误", MessageBoxButtons.OK, MessageBoxIcon.Error)
        End Try
    End Sub

    Private Sub btnExit_Click(sender As Object, e As EventArgs) Handles btnExit.Click
        Dim result = MessageBox.Show("确定要退出程序吗？", "确认退出", MessageBoxButtons.YesNo, MessageBoxIcon.Question)
        If result = DialogResult.Yes Then
            Application.Exit()
        End If
    End Sub

    Private Sub btnHelp_Click(sender As Object, e As EventArgs) Handles btnHelp.Click
        Dim helpForm As New FormHelp()
        helpForm.ShowDialog()
    End Sub

    Private Sub btnExportExcel_Click(sender As Object, e As EventArgs) Handles btnExportExcel.Click
        If simulationResults Is Nothing OrElse simulationResults.Count = 0 Then
            MessageBox.Show("⚠️ 没有可导出的仿真结果，请先运行仿真。", "无数据", MessageBoxButtons.OK, MessageBoxIcon.Warning)
            Return
        End If

        Dim saveDialog As New SaveFileDialog()
        saveDialog.Title = "导出仿真结果为 Excel 文件"
        saveDialog.Filter = "Excel 文件 (*.xlsx)|*.xlsx"
        saveDialog.FileName = "SECM_Results_" & DateTime.Now.ToString("yyyyMMdd_HHmmss") & ".xlsx"
        If saveDialog.ShowDialog() <> DialogResult.OK Then Exit Sub

        Try
            ' 依赖 NPOI（已经用于Excel导入），可直接写xlsx文件
            Dim workbook As New NPOI.XSSF.UserModel.XSSFWorkbook()
            Dim sheet = workbook.CreateSheet("SECM Results")

            ' 写入表头
            Dim headers = simulationResults(0).Keys.ToList()
            Dim headerRow = sheet.CreateRow(0)
            For j = 0 To headers.Count - 1
                headerRow.CreateCell(j).SetCellValue(headers(j))
            Next

            ' 写入数据
            For i = 0 To simulationResults.Count - 1
                Dim rowDict = simulationResults(i)
                Dim row = sheet.CreateRow(i + 1)
                For j = 0 To headers.Count - 1
                    Dim val = If(rowDict.ContainsKey(headers(j)), rowDict(headers(j)), "")
                    row.CreateCell(j).SetCellValue(val.ToString())
                Next
            Next

            ' 保存文件
            Using fs As New IO.FileStream(saveDialog.FileName, IO.FileMode.Create, IO.FileAccess.Write)
                workbook.Write(fs)
            End Using

            MessageBox.Show("✅ 仿真结果已成功导出为 Excel！", "导出完成", MessageBoxButtons.OK, MessageBoxIcon.Information)

        Catch ex As Exception
            MessageBox.Show("❌ 导出失败：" & ex.Message, "错误", MessageBoxButtons.OK, MessageBoxIcon.Error)
        End Try
    End Sub


End Class
