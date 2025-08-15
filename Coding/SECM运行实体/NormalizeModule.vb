' ===== 模块：NormalizeModule.vb =====
' 功能：统一处理所有归一化相关操作，防止重复调用、单位错乱

Module NormalizeModule

    ''' <summary>
    ''' 将结构性生产力 X_real 归一化，用于参与后续 Y_limit 计算等。
    ''' </summary>
    Public Function Normalize_X_real(X_real As Double, baseX As Double) As Double
        If baseX <= 0 Then Return 0
        Return X_real / baseX
    End Function

    ''' <summary>
    ''' 归一化 X_bonus 值，防止对 Z 的影响过强。
    ''' 可视需要添加 tanh 或 log 缓冲。
    ''' </summary>
    Public Function Normalize_X_bonus(X_bonus As Double, scale As Double) As Double
        If scale <= 0 Then Return 0
        Return X_bonus / scale
    End Function

    ''' <summary>
    ''' 限制 Z 值在某个合理范围内，例如 [-10, +10]。
    ''' 防止 Z 爆炸或失效。
    ''' </summary>
    Public Function Clip_Z(Z As Double, Optional minVal As Double = -10, Optional maxVal As Double = 10) As Double
        Return Math.Max(minVal, Math.Min(maxVal, Z))
    End Function

    ''' <summary>
    ''' 归一化专利数据，可用最大值或历史均值缩放。
    ''' </summary>
    Public Function Normalize_Patents(rawPatent As Double, maxPatent As Double) As Double
        If maxPatent <= 0 Then Return 0
        Return rawPatent / maxPatent
    End Function

    ''' <summary>
    ''' 通用归一函数：Value ÷ 标准值，防止重复写相似函数。
    ''' </summary>
    Public Function Normalize_Value(value As Double, standard As Double) As Double
        If standard <= 0 Then Return 0
        Return value / standard
    End Function

End Module
