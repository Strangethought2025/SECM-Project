Imports NPOI.SS.Formula.Functions

Public Class SECM_Engine

    ''' <summary>
    ''' 变量安全读取，缺失自动为0（建议保留）
    ''' </summary>
    Public Function SafeGet(dict As Dictionary(Of String, Double), key As String, Optional defaultValue As Double = 0) As Double
        If dict IsNot Nothing AndAlso dict.ContainsKey(key) Then
            Return dict(key)
        Else
            Return defaultValue
        End If
    End Function

    Public Function MapExcelFields(inputDict As Dictionary(Of String, Double)) As Dictionary(Of String, Double)
        Dim result As New Dictionary(Of String, Double)
        Dim fieldMap As New Dictionary(Of String, String)

        ' === 年份与人口 ===
        fieldMap.Add("Year", "Year")
        fieldMap.Add("Population", "Population")
        fieldMap.Add("Population_Last", "PopulationLast")
        fieldMap.Add("PopulationLast", "PopulationLast")
        fieldMap.Add("PopulationLastYear", "PopulationLast")

        ' === 产能类 ===
        fieldMap.Add("primary_energy_kwh", "PrimaryEnergy")
        fieldMap.Add("PrimaryEnergy", "PrimaryEnergy")
        fieldMap.Add("PrimaryEnergy_Last", "PrimaryEnergyLast")
        fieldMap.Add("PrimaryEnergyLast", "PrimaryEnergyLast")
        fieldMap.Add("PrimaryEnergyLastYear", "PrimaryEnergyLast")

        fieldMap.Add("animal_power_kwh", "AnimalPower")
        fieldMap.Add("AnimalPower", "AnimalPower")
        fieldMap.Add("AnimalPower_Last", "AnimalPowerLast")
        fieldMap.Add("AnimalPowerLast", "AnimalPowerLast")
        fieldMap.Add("AnimalPowerLastYear", "AnimalPowerLast")

        ' === 额外的 X 指标 ===
        fieldMap.Add("X_realLast", "X_realLast")
        fieldMap.Add("X_normalLast", "X_normalLast")

        ' === 科技红利类 ===
        fieldMap.Add("Patent", "PatentCount")
        fieldMap.Add("PatentCount", "PatentCount")
        fieldMap.Add("Patent_Last", "PatentLast")
        fieldMap.Add("PatentLast", "PatentLast")
        fieldMap.Add("PatentLastYear", "PatentLast")
        fieldMap.Add("BonusTheta", "BonusTheta")
        fieldMap.Add("BonusP", "BonusP")

        ' === 教育与劳动力 ===
        fieldMap.Add("EduRate", "EduRate")
        fieldMap.Add("STEMShare", "STEMShare")
        fieldMap.Add("TFPGrowth", "TFPGrowth")

        ' === 复杂性与社会经济 ===
        fieldMap.Add("Gini", "Gini")
        fieldMap.Add("Trust", "Trust")
        fieldMap.Add("SavingsRate", "SavingsRate")
        fieldMap.Add("DebtRate", "DebtRate")
        fieldMap.Add("DebtRatio", "DebtRate") ' 兼容旧命名
        fieldMap.Add("UnemploymentRate", "UnemploymentRate")
        fieldMap.Add("PovertyRate", "PovertyRate")
        fieldMap.Add("MurderRate", "MurderRate")
        fieldMap.Add("MCapGDP", "MCapGDP")
        fieldMap.Add("LPI", "LPI")

        ' === 保障覆盖率 ===
        fieldMap.Add("HealthcareCoverage", "MedCover")
        fieldMap.Add("PensionCoverage", "PensionCover")
        fieldMap.Add("FreeEduCoverage", "EduCover")
        fieldMap.Add("UnempInsCoverage", "WelfareCover")
        fieldMap.Add("SocialSecIndex", "SocialCoverage")

        ' === 外部冲击与漂移 ===
        fieldMap.Add("OmegaShock", "OmegaShock")
        fieldMap.Add("ZShock", "ZShock")
        fieldMap.Add("Drift", "Drift")

        ' === 军费与土地 ===
        fieldMap.Add("MilitaryRatio", "MilitaryRatio")
        fieldMap.Add("ArableLandCapita", "ArableLandCapita")
        fieldMap.Add("ArableLandTotal", "ArableLandTotal")

        ' === 参数控制项 ===
        fieldMap.Add("GammaS", "GammaS")
        fieldMap.Add("GammaX", "GammaX")
        fieldMap.Add("ZcWeight", "ZcWeight")
        fieldMap.Add("YBaseA0", "YBaseA0")
        fieldMap.Add("YBaseB1", "YBaseB1")
        fieldMap.Add("YBaseA1", "YBaseA1")
        fieldMap.Add("MuY0", "MuY0")
        fieldMap.Add("LandCapLimitCoef", "LandCapLimitCoef")
        fieldMap.Add("KLimit", "KLimit")
        fieldMap.Add("KY", "KY")
        fieldMap.Add("SDecayRate", "SDecayRate")
        fieldMap.Add("KS", "KS")
        fieldMap.Add("S0", "S0")
        fieldMap.Add("YFirst", "YFirst")
        fieldMap.Add("YLimitDecayBeta", "YLimitDecayBeta")
        fieldMap.Add("ZImpactK", "ZImpactK")

        ' === 应用映射 ===
        For Each kvp In inputDict
            Dim key = kvp.Key.Trim()
            Dim value = kvp.Value
            If fieldMap.ContainsKey(key) Then
                result(fieldMap(key)) = value
            Else
                result(key) = value
            End If
        Next

        Return result
    End Function
    ''' <summary>
    ''' 归一化输入参数（V25）
    ''' - 不再计算 X_real / X_normal，直接使用外部传入
    ''' - 百分比类 Excel 已为小数制
    ''' - 计算 Zc、PopPressure 等
    ''' - 顺带保存上一年数据（如果有）
    ''' </summary>
    Public Function NormalizeInputs(inputDict As Dictionary(Of String, Double),
                             xBase As Double,
                             X_real As Double,
                             X_normal As Double) As Dictionary(Of String, Double)

        Dim normDict As New Dictionary(Of String, Double)

        ' 直接赋值 X
        normDict("X_real") = X_real
        normDict("X_base") = xBase
        normDict("X_normal") = X_normal

        ''' <<< 新增：上一年值（如果 Excel 传了，就保存）
        normDict("X_realLast") = SafeGet(inputDict, "X_realLast", X_real)
        normDict("X_normalLast") = SafeGet(inputDict, "X_normalLast", X_normal)

        ' 百分比 / 比例类输入 clip 到 [0,1]
        normDict("Gini") = Clip01(SafeGet(inputDict, "Gini"))
        normDict("Trust") = Clip01(SafeGet(inputDict, "Trust"))
        normDict("SavingsRate") = Clip01(SafeGet(inputDict, "SavingsRate"))
        normDict("DebtRate") = Clip01(SafeGet(inputDict, "DebtRate"))
        normDict("UnemploymentRate") = Clip01(SafeGet(inputDict, "UnemploymentRate"))
        normDict("PovertyRate") = Clip01(SafeGet(inputDict, "PovertyRate"))
        normDict("MurderRate") = Clip01(SafeGet(inputDict, "MurderRate"))
        normDict("MilitaryRatio") = Clip01(SafeGet(inputDict, "MilitaryRatio"))
        normDict("LPI") = SafeGet(inputDict, "LPI")

        ' 保障覆盖率
        normDict("MedCover") = Clip01(SafeGet(inputDict, "MedCover"))
        normDict("PensionCover") = Clip01(SafeGet(inputDict, "PensionCover"))
        normDict("EduCover") = Clip01(SafeGet(inputDict, "EduCover"))
        normDict("WelfareCover") = Clip01(SafeGet(inputDict, "WelfareCover"))
        normDict("SocialCoverage") = Clip01(SafeGet(inputDict, "SocialCoverage"))

        ' 教育与科技
        normDict("EduRate") = Clip01(SafeGet(inputDict, "EduRate"))
        normDict("STEMShare") = Clip01(SafeGet(inputDict, "STEMShare"))
        normDict("TFPGrowth") = SafeGet(inputDict, "TFPGrowth")
        normDict("BonusTheta") = SafeGet(inputDict, "BonusTheta")
        normDict("BonusP") = SafeGet(inputDict, "BonusP")

        ' 城市化率
        normDict("UrbanRate") = Clip01(SafeGet(inputDict, "UrbanRate"))

        ' S_popdens
        Dim pop As Double = SafeGet(inputDict, "Population")
        Dim arableLand As Double = SafeGet(inputDict, "ArableLandTotal")
        Dim spopdens As Double = Double.NaN
        If arableLand > 0 AndAlso normDict("UrbanRate") > 0 Then
            Dim PD_arable As Double = pop / arableLand
            spopdens = 1 - (1 / (normDict("UrbanRate") * PD_arable))
            If spopdens < 0 Then spopdens = 0
            If spopdens > 2.5 Then spopdens = 2.5
        End If
        normDict("Spopdens") = spopdens

        ' Zc
        Dim w_Zc As Double = Clip(SafeGet(inputDict, "ZcWeight", 1.0), 0, 2.0)
        normDict("Zc") = Calc_Zc_V25(normDict("Gini"),
                     normDict("MurderRate"),
                     normDict("PovertyRate"),
                     SafeGet(inputDict, "MCapGDP"),
                     normDict("Trust"),
                     spopdens,
                     w_Zc)
        normDict("w_Zc") = w_Zc

        ' relax
        Dim relaxList As New List(Of Double)
        If normDict("MedCover") > 0 Then relaxList.Add(normDict("MedCover"))
        If normDict("PensionCover") > 0 Then relaxList.Add(normDict("PensionCover"))
        If normDict("EduCover") > 0 Then relaxList.Add(normDict("EduCover"))
        If normDict("WelfareCover") > 0 Then relaxList.Add(normDict("WelfareCover"))
        Dim relax As Double = If(relaxList.Count > 0, relaxList.Average(), normDict("SocialCoverage"))
        relax = Clip01(relax)
        normDict("relax") = relax

        ' Oc
        Dim ocList As New List(Of Double)
        If normDict("SavingsRate") >= 0 Then ocList.Add(-normDict("SavingsRate"))
        If normDict("UnemploymentRate") >= 0 Then ocList.Add(Math.Sqrt(2) * normDict("UnemploymentRate"))
        If normDict("DebtRate") >= 0 Then ocList.Add(normDict("DebtRate"))
        If normDict("LPI") >= 0 Then ocList.Add(-normDict("LPI") / 10.0)
        Dim Oc As Double = If(ocList.Count > 0, ocList.Average(), 0)

        ' 外部冲击
        Dim Osh As Double = SafeGet(inputDict, "OmegaShock", 0)
        If Double.IsNaN(Osh) Then Osh = 0
        normDict("Oc") = Oc
        normDict("Oshock") = Osh
        normDict("OmegaShock") = Osh
        normDict("Omega") = Oc + Osh

        ' PopPressure
        Dim pe As Double = SafeGet(inputDict, "PrimaryEnergy")
        Dim ap As Double = SafeGet(inputDict, "AnimalPower")
        Dim humanKWPE As Double = (pop * 130.0) / 1_000_000
        Dim peoplePerHa As Double = If(arableLand > 0, pop / arableLand, 0)
        Dim kwpe_pc As Double = If(pop > 0, (pe + ap + humanKWPE) * 1_000_000 / pop, 0)
        Dim landCapLimit As Double = SafeGet(inputDict, "LandCapLimitCoef", 15)

        Dim popPressure As Double = 0
        If landCapLimit > 0 And kwpe_pc > 0 Then
            popPressure = peoplePerHa / (kwpe_pc / landCapLimit)
        End If
        normDict("PopPressure") = popPressure

        Return normDict
    End Function


    Public Function RunOnce_V25(inputDict As Dictionary(Of String, Double),
                     Optional isFirstYear As Boolean = False,
                     Optional debugEnabled As Boolean = False,
                     Optional logwindow As RichTextBox = Nothing) As Dictionary(Of String, Double)

        Dim result As New Dictionary(Of String, Double)

        ' ===== 1. 计算 X =====
        Dim baseX As Double = SafeGet(inputDict, "XBase")
        If baseX < 1 Then baseX = 1
        Dim xDict = Calc_X_V25(inputDict, baseX)
        Dim X_real As Double = xDict("X_real")
        Dim X_normal As Double = xDict("X_normal")
        baseX = xDict("X_base")

        ' ===== 2. Normalize 其它输入（使用已计算的 X）=====
        Dim normVars = NormalizeInputs(inputDict, baseX, X_real, X_normal)
        Dim Zc As Double = normVars("Zc")
        Dim relax As Double = normVars("relax")
        Dim PopPressure As Double = normVars("PopPressure")

        ' ==== 外部冲击保险 ====
        Dim OmegaShock As Double = SafeGet(inputDict, "OmegaShock", SafeGet(normVars, "OmegaShock"))
        Dim ZShock As Double = SafeGet(inputDict, "ZShock", SafeGet(normVars, "ZShock"))

        ' ===== 3. Parameters =====
        Dim kY As Double = SafeGet(inputDict, "kY")
        Dim kLimit As Double = SafeGet(inputDict, "kLimit")
        Dim gammaX As Double = SafeGet(inputDict, "GammaX")
        Dim gammaS As Double = SafeGet(inputDict, "GammaS")
        Dim drift As Double = SafeGet(inputDict, "Drift")
        Dim SDecayRate As Double = SafeGet(inputDict, "SDecayRate")
        Dim Eps As Double = SafeGet(inputDict, "YLimitEps", 0.01)
        Dim YFirst As Double = SafeGet(inputDict, "YFirst")

        ' ===== 4. Previous State =====
        Dim Z_prev As Double = SafeGet(inputDict, "Z_prev")
        Dim S_prev As Double = SafeGet(inputDict, "S_prev")
        Dim Y_prev As Double = If(isFirstYear, 0, SafeGet(inputDict, "Y_prev"))

        ' ✅ 首年用当前值，其余年份优先取 Excel 传的上一年值
        Dim X_normal_prev As Double
        If isFirstYear Then
            X_normal_prev = X_normal
        Else
            ' 优先取 Excel 中的 Last 列（MapExcelFields 已映射）
            X_normal_prev = SafeGet(inputDict, "X_normalLast", X_normal)
        End If

        ' ===== 5. Omega =====
        Dim Omega As Double = Calc_Omega_V25(normVars)

        ' ===== 6. X_bonus =====
        Dim bonusDict = Calc_X_Bonus_V26(normVars)
        Dim X_bonus_t As Double = bonusDict("X_bonus_t")
        Dim X_bonus_norm As Double = bonusDict("X_bonus_norm")

        ' ===== 7. Z轴推进 =====
        Dim Z_t As Double = 0, Z_scaled As Double = 0, Z_eff As Double = 0
        If Not isFirstYear Then
            Dim zDict = Calc_Z_V25(drift, ZShock, relax, gammaS, Zc, gammaX, X_bonus_norm)
            Z_t = zDict("Z_t")
            Z_scaled = zDict("Z_scaled")
            Z_eff = zDict("Z_eff")
        End If

        ' ===== 8. Y_base =====
        Dim Y_base As Double = Calc_Y_base_V25(inputDict, X_normal, X_real, isFirstYear)

        ' ===== 9. Y_t =====
        Dim yearNum As Integer = CInt(SafeGet(inputDict, "Year"))
        Dim startYear As Integer = CInt(SafeGet(inputDict, "StartYear"))
        Dim isSecondYear As Boolean = (yearNum = startYear + 1)
        Dim ZImpactK As Double = SafeGet(inputDict, "ZImpactK", 1.0)

        Dim Y_t As Double = Calc_Y_t_V25(
    isFirstYear,
    isSecondYear,
    YFirst,
    Y_base,
    Y_prev,
    X_normal,
    Z_eff,
    PopPressure,
    kY,
    ZImpactK,            ' ✅ 新增参数
    X_normal_prev
    )

        ' ===== 10. Y_limit =====
        Dim deltaX As Double = X_normal - X_normal_prev
        Dim YLimitDecayBeta As Double = SafeGet(inputDict, "YLimitDecayBeta")
        Dim military As Double = SafeGet(normVars, "MilitaryRatio")
        Dim Y_limit As Double = Calc_Y_limit_V25(X_normal, kLimit, Omega, military, Eps, deltaX, YLimitDecayBeta)


        ' ===== 11. S_pool推进 =====
        Dim S_t As Double = Calc_S(Y_t, Y_limit, S_prev, SDecayRate)

        ' ===== 12. 崩溃判定 =====
        Dim I_reset As Integer = Calc_I_reset(S_t, Y_limit)

        ' ===== 13. 输出结果 =====
        result("Year") = SafeGet(inputDict, "Year") ' <<< 新增年份列
        result("X_real") = X_real
        result("X_normal") = X_normal
        result("Zc") = Zc
        result("Omega") = Omega
        result("X_bonus_t") = X_bonus_t
        result("X_bonus_norm") = X_bonus_norm
        result("Z_t") = Z_t
        result("Z_scaled") = Z_scaled
        result("Z_eff") = Z_eff
        result("Y_base") = Y_base
        result("Y_t") = Y_t
        result("Y_limit") = Y_limit
        result("S_t") = S_t
        result("I_reset") = I_reset

        ' ===== 14. 日志 =====
        If debugEnabled AndAlso logwindow IsNot Nothing Then
            deltaX = If(Double.IsNaN(X_normal_prev), Double.NaN, X_normal - X_normal_prev)
            logwindow.AppendText($"==== 年份 {SafeGet(inputDict, "Year")} ===={vbCrLf}")
            logwindow.AppendText($"X_base={baseX}, X_real={X_real}, X_normal={X_normal}, X_normal_prev={X_normal_prev}, ΔX={deltaX}{vbCrLf}")
            logwindow.AppendText($"Omega={Omega}, Zc={Zc}, OmegaShock={OmegaShock}{vbCrLf}")
            logwindow.AppendText($"Z_prev={Z_prev}, Z_t={Z_t}, Z_eff={Z_eff}{vbCrLf}")
            logwindow.AppendText($"PopPressure={PopPressure}, Y_prev={Y_prev}{vbCrLf}")
            logwindow.AppendText($"Y_base={Y_base}, Y_t={Y_t}{vbCrLf}")
            logwindow.AppendText($"Y_limit={Y_limit}, S_t={S_t}, I_reset={I_reset}{vbCrLf}")
            logwindow.AppendText($"X_bonus_t={X_bonus_t}, X_bonus_norm={X_bonus_norm}{vbCrLf}{vbCrLf}")
        End If

        Return result
    End Function


    ' ===== 新增：X计算模块 =====
    Public Function Calc_X_V25(inputDict As Dictionary(Of String, Double),
                       Optional xBase As Double = Double.NaN) As Dictionary(Of String, Double)

        Dim result As New Dictionary(Of String, Double)

        ' 安全读取输入值（缺失默认0）
        Dim pe As Double = SafeGet(inputDict, "PrimaryEnergy", 0)   ' 百万 kWh
        Dim ap As Double = SafeGet(inputDict, "AnimalPower", 0)     ' 百万 kWh
        Dim pop As Double = SafeGet(inputDict, "Population", 0)     ' 人口

        ' 百万人力产能 (百万 kWh)
        Dim humanKWPE As Double = (pop * 130.0) / 1_000_000
        Dim X_real As Double = Math.Max(0, pe + ap + humanKWPE)

        ' 首次运行锁定基准值
        If Double.IsNaN(xBase) OrElse xBase <= 0 Then
            xBase = If(X_real > 0, X_real, 1)
        End If

        ' 归一化
        Dim X_normal As Double = If(xBase > 0, X_real / xBase, 0)
        If Double.IsNaN(X_normal) OrElse X_normal < 0 Then X_normal = 0

        ' ΔX（与 Excel 模板中的上一年值比较）
        Dim X_normal_last As Double = SafeGet(inputDict, "X_normalLast", X_normal)
        Dim deltaX As Double = X_normal - X_normal_last

        ' 输出
        result("X_real") = X_real
        result("X_base") = xBase
        result("X_normal") = X_normal
        result("deltaX") = deltaX   ' 新增输出项

        Return result
    End Function

    ''' <summary>
    ''' V26+ 年度科技红利主轴：
    ''' X_bonus_t = θ · STEM · EduRate · (1 + TFP)
    '''              · [1 + (PatDen - PatDen_last) / PatDen_last]
    '''              · [1 + (Xt - Xt_last) / Xt_last] ^ P
    ''' - θ = BonusTheta
    ''' - P = BonusP
    ''' - Xt = X_real / X_real_首年
    ''' - clip 归一红利到 [0, 5.0]
    ''' </summary>
    Public Function Calc_X_Bonus_V26(normDict As Dictionary(Of String, Double),
                                 Optional X_real_0 As Double = 0,
                                 Optional X_real_last As Double = 0,
                                 Optional PatDen_last As Double = 0) As Dictionary(Of String, Double)

        Dim result As New Dictionary(Of String, Double)

        ' === 输入变量 ===
        Dim theta As Double = SafeGet(normDict, "BonusTheta")
        Dim pExp As Double = SafeGet(normDict, "BonusP")
        Dim STEM As Double = SafeGet(normDict, "STEMShare")
        Dim EduRate As Double = SafeGet(normDict, "EduRate")
        Dim TFP As Double = SafeGet(normDict, "TFPGrowth")
        Dim PatentCount As Double = SafeGet(normDict, "PatentCount")
        Dim Population As Double = SafeGet(normDict, "Population")
        Dim X_real As Double = SafeGet(normDict, "X_real")
        Dim X_base As Double = SafeGet(normDict, "X_base")

        ' === 相对产能 Xt ===
        Dim Xt As Double = 0
        If X_real_0 > 0 Then
            Xt = X_real / X_real_0
        End If

        Dim Xt_last As Double = 0
        If X_real_0 > 0 AndAlso X_real_last > 0 Then
            Xt_last = X_real_last / X_real_0
        End If

        ' === 专利密度（件/百万人） ===
        Dim PatDen As Double = 0
        If Population > 0 Then
            PatDen = PatentCount / (Population / 1_000_000.0)
        End If

        ' === 修订公式（同比增速 + 1） ===
        Dim patFactor As Double = 1.0
        If PatDen_last > 0 Then
            patFactor = 1 + ((PatDen - PatDen_last) / PatDen_last)
        End If

        Dim xtFactor As Double = 1.0
        If Xt_last > 0 Then
            xtFactor = 1 + ((Xt - Xt_last) / Xt_last)
            xtFactor = xtFactor ^ pExp
        End If

        Dim tfpFactor As Double = 1 + TFP
        If tfpFactor < 0 Then tfpFactor = 0 ' 可选保护，避免负数

        Dim X_bonus_t As Double = theta * STEM * EduRate * tfpFactor * patFactor * xtFactor

        ' clip 到非负
        If X_bonus_t < 0 Then X_bonus_t = 0
        result("X_bonus_t") = X_bonus_t

        ' === 归一红利（最大 5.0） ===
        Dim X_bonus_norm As Double = X_bonus_t
        If X_bonus_norm < 0 Then X_bonus_norm = 0
        If X_bonus_norm > 5 Then X_bonus_norm = 5

        result("X_bonus_norm") = X_bonus_norm

        ' 额外返回中间变量（调试用）
        result("PatDen") = PatDen
        result("PatDen_last") = PatDen_last
        result("Xt") = Xt
        result("Xt_last") = Xt_last

        Return result
    End Function
    ''' <summary>
    ''' V25 Z轴结构：
    ''' Z_raw = 平均( ZShock, -relax, γS·Zc, -γX·X_bonus_norm, [可选 Drift] )
    ''' - Zc 已包含 Spopdens（人口密度摩擦项）和 w_Zc 权重
    ''' - Drift = 0 时不计入张力平均项
    ''' - clip 主值到 ±7，再缩放到 ±1.4
    ''' - 非线性平方映射（正保持正，负保持负）
    ''' </summary>
    Public Function Calc_Z_V25(drift As Double,
                           ZShock As Double,
                           relax As Double,
                           gammaS As Double,
                           Zc As Double,
                           gammaX As Double,
                           X_bonus_norm As Double,
                           Optional Z_MAX_THEORY As Double = 7.0,
                           Optional Z_SCALE_MAX As Double = 1.4) As Dictionary(Of String, Double)

        Dim result As New Dictionary(Of String, Double)

        ' ===== 累加结构张力项 =====
        Dim zTerms As New List(Of Double)
        zTerms.Add(ZShock)                           ' 外部冲击（加压或缓解）
        zTerms.Add(-relax)                           ' 社会保障减压
        zTerms.Add(gammaS * Zc)                      ' 复杂度加压（已含 Spopdens）
        zTerms.Add(-gammaX * X_bonus_norm)           ' 科技红利减压
        If drift <> 0 Then zTerms.Add(drift)         ' 红皇后（可选）

        ' ===== 求平均（动态分母） =====
        Dim Z_t As Double = zTerms.Average()

        ' ===== 1. clip 主值（理论 ±7） =====
        Z_t = Math.Max(Math.Min(Z_t, Z_MAX_THEORY), -Z_MAX_THEORY)
        result("Z_t") = Z_t

        ' ===== 2. 缩放后 clip =====
        Dim Z_scaled As Double = Z_t / Z_MAX_THEORY * Z_SCALE_MAX
        Z_scaled = Math.Max(Math.Min(Z_scaled, Z_SCALE_MAX), -Z_SCALE_MAX)
        result("Z_scaled") = Z_scaled

        ' === 改进版非线性放大（保持原符号） ===
        Dim Z_eff As Double
        Dim absVal As Double = Math.Abs(Z_scaled)

        ' 幅度放大
        Dim amp As Double = (1 + absVal) ^ 2 - 1

        ' 恢复原符号
        Z_eff = Math.Sign(Z_scaled) * amp

        result("Z_eff") = Z_eff


        ' 调试输出（可选）
        Debug.Print($"[Z_V25] Drift={drift}, ZShock={ZShock}, relax={relax}, γS·Zc={gammaS * Zc}, -γX·红利={-gammaX * X_bonus_norm}, Count={zTerms.Count}, Z_t={Z_t}, Z_eff={Z_eff}")

        Return result
    End Function
    ''' <summary>
    ''' 计算 Ω（社会抵抗力综合指标）—— V25版
    ''' Oc（结构削弱因子）+ OmegaShock（外部冲击）
    ''' </summary>
    Public Function Calc_Omega_V25(inputDict As Dictionary(Of String, Double)) As Double
        ' === 1. 基础数据获取 ===
        Dim savingsRate As Double = SafeGet(inputDict, "SavingsRate")         ' 储蓄率（小数）
        Dim unemploymentRate As Double = SafeGet(inputDict, "UnemploymentRate") ' 失业率（小数）
        Dim debtRate As Double = SafeGet(inputDict, "DebtRate")               ' 债务率（小数）
        Dim lpi As Double = SafeGet(inputDict, "LPI")                         ' 物流绩效指数（0~5）
        Dim omegaShock As Double = SafeGet(inputDict, "OmegaShock")           ' 外部冲击

        ' === 2. 百分比类 Clip 到 [0,1] ===
        savingsRate = Clip01(savingsRate)
        unemploymentRate = Clip01(unemploymentRate)
        debtRate = Clip01(debtRate)

        ' === 3. Oc（结构削弱因子）计算 ===
        ' 负向权重：储蓄率越高，Oc 越低（缓解张力）
        ' 正向权重：失业率、债务率越高，Oc 越高（加剧张力）
        ' LPI 除以10反映基建改善（减压）
        Dim ocList As New List(Of Double)
        If savingsRate >= 0 Then ocList.Add(-savingsRate)
        If unemploymentRate >= 0 Then ocList.Add(Math.Sqrt(2) * unemploymentRate)
        If debtRate >= 0 Then ocList.Add(debtRate)
        If lpi >= 0 Then ocList.Add(-(lpi / 10.0))

        Dim Oc As Double = If(ocList.Count > 0, ocList.Average(), 0)

        ' === 4. Ω 计算 ===
        Dim Omega As Double = Oc + omegaShock

        ' === 5. Clip 限制，防止极端值干扰计算 ===
        If Omega > 5 Then Omega = 5
        If Omega < -5 Then Omega = -5

        Return Omega
    End Function


    ''' <summary>
    ''' 计算结构张力基线 Y_base（V25）
    ''' 首年优先使用外部输入（Excel → 控件），否则按公式计算
    ''' </summary>
    Public Function Calc_Y_base_V25(inputDict As Dictionary(Of String, Double),
                                 X_normal As Double,
                                 X_real As Double,
                                 Optional isFirstYear As Boolean = False) As Double
        ' === 1. 首年外部输入优先 ===
        If isFirstYear Then
            Dim Y_base_input As Double = SafeGet(inputDict, "Y_base")
            If Y_base_input > 0 Then
                Return Y_base_input
            End If
        End If

        ' === 2. 参数获取 ===
        Dim a0 As Double = SafeGet(inputDict, "YBaseA0")   ' 截距项
        Dim a1 As Double = SafeGet(inputDict, "YBaseA1")   ' X_normal 系数
        Dim b1 As Double = SafeGet(inputDict, "YBaseB1")   ' Gini 系数
        Dim gini As Double = Clip01(SafeGet(inputDict, "Gini"))
        Dim mu As Double = SafeGet(inputDict, "MuY0")      ' 平滑项

        ' === 3. 公式计算（V25口径） ===
        ' Y_base = a0 + a1 * X_normal + b1 * Gini + μ * log(1 + X_real)
        Dim Y_base As Double = a0 + a1 * X_normal + b1 * gini + mu * Math.Log(1 + Math.Max(0, X_real))

        ' === 4. Clip 限制 ===
        If Y_base < 0 Then Y_base = 0

        Return Y_base
    End Function
    ''' <summary>
    ''' V25社会张力推进公式（三段式，加入 kY 系数和 ZImpactK 可调项）
    ''' 1. 首年：用外给 YFirst（若有）或计算的 Y_base
    ''' 2. 第二年：用 Y_base + ΔX * kY * (1 + ZImpactK * Z_eff) * (1 + PopPressure)
    ''' 3. 第三年及以后：用 Y_prev + ΔX * kY * (1 + ZImpactK * Z_eff) * (1 + PopPressure)
    ''' </summary>
    Public Function Calc_Y_t_V25(isFirstYear As Boolean,
                              isSecondYear As Boolean,
                              YFirst As Double,
                              Y_base As Double,
                              Y_prev As Double,
                              X_normal As Double,
                              Z_eff As Double,
                              PopPressure As Double,
                              kY As Double,
                              ZImpactK As Double,
                              Optional X_normal_prev As Double = Double.NaN) As Double

        Dim deltaX As Double = X_normal - X_normal_prev
        Dim Y_t As Double

        If isFirstYear Then
            If YFirst > 0 Then
                Y_t = YFirst
            Else
                Y_t = Y_base
            End If
        ElseIf isSecondYear Then
            Y_t = Y_base + (deltaX * kY * (1 + ZImpactK * Z_eff)) * (1 + PopPressure)
        Else
            Y_t = Y_prev + (deltaX * kY * (1 + ZImpactK * Z_eff)) * (1 + PopPressure)
        End If

        If Y_t < 0 Then Y_t = 0
        Return Y_t
    End Function

    Public Function Calc_Y_limit_V25(X_normal As Double,
                                 kLimit As Double,
                                 Omega As Double,
                                 MilitaryRatio As Double,
                                 Optional Eps As Double = 0.01,
                                 Optional deltaX As Double = 0,
                                 Optional YLimitDecayBeta As Double = 0) As Double

        Dim baseX As Double = X_normal * (1 - Math.Max(0, Math.Min(1, MilitaryRatio)))
        Dim Y_limit As Double

        If Omega <= 1 Then
            Y_limit = baseX * kLimit * (1 + Math.Abs(Omega))
            ' 当 ΔX<0 时额外衰减
            If deltaX < 0 AndAlso YLimitDecayBeta > 0 Then
                Y_limit /= ((1 + YLimitDecayBeta) * (1 + Math.Abs(deltaX)))
            End If
        Else
            Y_limit = baseX * kLimit / (1 + Omega)
            ' 当 ΔX<0 时额外衰减
            If deltaX < 0 AndAlso YLimitDecayBeta > 0 Then
                Y_limit /= ((1 + YLimitDecayBeta) * (1 + Math.Abs(deltaX)))
            End If
        End If

        Y_limit += Eps
        If Y_limit < 0 Then Y_limit = 0
        Return Y_limit
    End Function





    ''' <summary>
    ''' 计算 Z 轴用的人口密度矛盾项 S_popdens,t
    ''' - 反映高人口密度 + 高城市化带来的摩擦效应
    ''' - UrbanRate ∈ [0,1]，缺失则返回 NaN（不参与 avg_plus）
    ''' - PD_arable = 人口 / 耕地总面积 (人/ha)
    ''' - 返回值 clip 至 [0, 2.5] 可选（文档建议）
    ''' </summary>
    Public Function Calc_Spopdens(population As Double,
                              arableLandTotal As Double,
                              urbanRate As Double) As Double
        ' 检查缺失
        If arableLandTotal <= 0 OrElse urbanRate <= 0 Then
            Return Double.NaN ' 缺失标记
        End If

        Dim PD_arable As Double = population / arableLandTotal ' 人/ha
        Dim spopdens As Double = 1 - (1 / (urbanRate * PD_arable))

        ' 保护：小于 0 取 0
        If spopdens < 0 Then spopdens = 0

        ' 可选 clip 上限
        If spopdens > 3 Then spopdens = 3

        Return spopdens
    End Function
    ''' <summary>
    ''' 计算 Y 轴用的人口压力系数 PopPressure_t
    ''' - 反映土地—人口承载矛盾对张力增长速度的倍增作用
    ''' - PeoplePerHa = 人口 / 耕地总面积 (人/ha)
    ''' - KWPE_pc = 人均一次能源 + 畜力 + 人力 (kWh/人·年)
    ''' - LandCapLimitCoef = 土地承载限制系数 (默认 15 kWh/人·年)
    ''' </summary>
    Public Function Calc_PopPressure(population As Double,
                                 arableLandTotal As Double,
                                 primaryEnergy As Double,
                                 animalPower As Double,
                                 Optional landCapLimitCoef As Double = 15) As Double

        Dim humanKWPE As Double = (population * 130.0) / 1_000_000 ' 百万人力产能 (百万 kWh)
        Dim totalKWPE As Double = primaryEnergy + animalPower + humanKWPE

        Dim peoplePerHa As Double = If(arableLandTotal > 0, population / arableLandTotal, 0)
        Dim kwpe_pc As Double = If(population > 0, totalKWPE * 1_000_000 / population, 0) ' kWh/人·年

        Dim popPressure As Double = 0
        If landCapLimitCoef > 0 AndAlso kwpe_pc > 0 Then
            popPressure = peoplePerHa / (kwpe_pc / landCapLimitCoef)
        End If

        Return popPressure
    End Function

    ''' <summary>
    ''' 危机池递推
    ''' 当 Y_t 超过 Y_limit 时，危机池 S_t 累积压力
    ''' 否则 S_t 按衰减率缓慢释放
    ''' 递推后 S_t clip 保证非负
    ''' </summary>
    Public Function Calc_S(Y_t As Double, Y_limit As Double, S_prev As Double, SDecayRate As Double) As Double
        Dim S_t As Double
        If Y_t > Y_limit Then
            S_t = S_prev + (Y_t - Y_limit) ' 超限压力累积
        Else
            S_t = S_prev * (1 - SDecayRate) ' 宽松期缓慢释放
        End If
        If S_t < 0 Then S_t = 0 ' clip保护
        Return S_t
    End Function
    ''' <summary>
    ''' 计算 V25 Zc（社会矛盾复杂度）
    ''' - 包含 Spopdens（人口密度摩擦项）
    ''' - 忽略 NaN，动态分母平均
    ''' - 最后乘权重 w_Zc 并 clip ≤ 2.5
    ''' </summary>
    Public Function Calc_Zc_V25(Gini As Double,
                             MurderRate As Double,
                             PovertyRate As Double,
                             MCapGDP As Double,
                             Trust As Double,
                             Spopdens As Double,
                             Optional w_Zc As Double = 1.0) As Double

        Dim zcList As New List(Of Double)

        ' 基尼
        If Gini > 0 Then zcList.Add(Gini)

        ' 谋杀率 √2
        Dim mterm As Double = MurderRate * Math.Sqrt(2)
        If mterm > 0 Then zcList.Add(mterm)

        ' 贫困率 √2
        Dim pterm As Double = PovertyRate * Math.Sqrt(2)
        If pterm > 0 Then zcList.Add(pterm)

        ' 股市市值/GDP（clip ≤ 3）
        If MCapGDP > 0 Then zcList.Add(Math.Min(MCapGDP, 3))

        ' 信任缺失度
        If Trust > 0 Then zcList.Add(1 - Trust)

        ' 人口密度摩擦项
        If Not Double.IsNaN(Spopdens) AndAlso Spopdens > 0 Then zcList.Add(Spopdens)

        ' 平均 + 权重 + clip
        Dim baseZc As Double = If(zcList.Count > 0, zcList.Average(), 0)
        Dim Zc As Double = Clip(w_Zc * baseZc, 0, 5)

        Return Zc
    End Function

    ''' <summary>
    ''' 崩溃判定
    ''' 当危机池 S_t 超过阈值时，输出崩溃标志 1，否则 0
    ''' 阈值一般设为 n × Y_limit，n 为可调参数（如1或2）
    ''' </summary>
    Public Function Calc_I_reset(S_t As Double, threshold As Double) As Integer
        Dim flag As Integer = If(S_t >= threshold, 1, 0)
        Return flag
    End Function

    ''' <summary>
    ''' 将数值 clip 到 [0,1]
    ''' </summary>
    Private Function Clip01(val As Double) As Double
        If val < 0 Then Return 0
        If val > 1 Then Return 1
        Return val
    End Function

    ''' <summary>
    ''' 将数值 clip 到任意 [min, max] 区间
    ''' </summary>
    Private Function Clip(val As Double, minVal As Double, maxVal As Double) As Double
        If val < minVal Then Return minVal
        If val > maxVal Then Return maxVal
        Return val
    End Function



End Class
