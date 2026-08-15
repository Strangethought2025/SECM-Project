# SECM V0.6 开发状态 · 交接文档（自动生成）

> 最后更新：全自动迭代阶段结束时。所有成果已同步 GitHub（commit b4d3ecc）。

---

## 一、已完成的（全部在 GitHub 上，本地丢失可随时 clone 恢复）

### 1. 设计哲学文档
- `SECM V0.6 Game Core Spec.md` —— 完整哲学（四层全耦合 / No Single-Cause / 奇点三支柱 / 军事两难 / 信息层 / 信心层 / 外生冲击）。

### 2. 历史验证器（`V0.6/`）
- 最终模型 `final_6country.py`：V0.5 结构还原（Y_base 水平项 + ΔX 累加器 + Ω 韧性 Ylimit）。
- 调参器 `tune_forms.py`：120 种数学形式组合（log/sign/power/倒数/tanh/比值）。
- 数据管道：`fetch_wb.py` / `fetch_oos2000.py` / `fetch_tune.py` / `fetch_bulk.py`。
- 报告：`VALIDATION_REPORT.md`。

### 3. 真实数据（已入库）
- `V0.6/tune/`：**调参集 6 国 1980-2025**（美/阿/墨/土/俄/希），含 能源/凶杀/医疗/失业/股市/Gini/专利/教育/军费。
- `V0.6/oos2000/`：验证集 20 国 2000-2025。

### 4. 关键结论
- 美阿 46 年调参集曾达 **9/9 全命中**；20 国验证 **76-82%**。
- 发现并修复了 V0.5 的**单位 OFF bug**：`μ·ln(1+X_real)` 用原始 GDP（万亿级）导致 Y_base 膨胀 9 倍（V0.5 里 X_real 是百万千瓦时级）。
- "长期 G>0"与"危机命中"存在结构性权衡（单基线无法同时满足）。

---

## 二、你的最新指示（待实现的重构方向）

1. **数据本身即矛盾高低** —— 不发明 a0 基线，Y 直接由矛盾指标合成（Gini/失业/凶杀/贫困）。
2. **时间无关（steps = 数据颗粒度）**。
3. **X 用一次能源 + 劳动力，不用 GDP**（GDP 能造假）。
4. **科技用 STEM 人才 / 专利数**。
5. 逐国用"第一个历史事件对齐"校准初始 Y 与 Ylimit。
6. 公式可任意改（log/sign/power/倒数等），设计哲学不变。

---

## 三、当前阻塞点

1. **验证集 14 国缺新指标**（能源/凶杀/医疗）：调参集 6 国已拉齐（能源 34-35 年、凶杀 18-34 年、医疗 24 年），但验证集 14 国的补拉请求**超时/限流**（WB API 会话已上千次请求被限）。
2. **批量下载端点异常**：`?downloadformat=csv` 返回格式不对（`fetch_bulk.py` 待调试——可能返回的是 zip 或需带 `format=json` 参数）。

### 建议的解决路径（按优先级）
- **A. 等限流重置后补拉**（WB API 限流通常几分钟~1 小时重置），重跑 `fetch_real.py`（慢节奏版，每请求 sleep 1.2s）。
- **B. 直接浏览器下载**：数据页 https://data.worldbank.org 有"Download CSV"按钮，可用 `Invoke-WebRequest` 模拟下载（批量端点：`https://api.worldbank.org/v2/en/indicator/{code}?downloadformat=csv`，返回 zip 含 CSV，需 zipfile 解包——`fetch_bulk.py` 已写好解包逻辑，但返回内容异常待查）。
- **C. 用调参集 6 国先跑通数据驱动版模型**（6 国已有全部新指标），验证逻辑正确后再补 14 国。

---

## 四、下一步（醒来后指示即可继续）

1. 补拉验证集 14 国的 能源/凶杀/医疗（路径 A 或 B）。
2. 实现数据驱动模型（重构方向见第二节）：
   - `X = 能源/人 × 人口 + 人口×130/10⁶`（一次能源+劳动力，非 GDP）
   - `Y = w·Gini_n + w·失业_n + w·凶杀_n + w·股崩`（数据即矛盾）
   - `Ylimit = (X_n(1−军费))^β · (w0 + w·福利)`（福利=医疗+教育）
   - `G = Y − Ylimit`，危机=G>0
3. 逐国 (yf, yls) 对齐第一个历史事件 → 其余为预测。
4. 迭代调参至可靠，更新 `VALIDATION_REPORT.md`，提交 GitHub。

---

*所有代码与数据在 `SECM-Project` 仓库，本地副本在 `E:\AI-Personal\SECM-Project`。*
