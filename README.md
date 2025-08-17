# SECM: Societal Evolution Computational Model (V0.5 Alpha)

[![White Paper DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.16884870.svg)](https://doi.org/10.5281/zenodo.16884870)
[![Validation DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.16881151.svg)](https://doi.org/10.5281/zenodo.16881151)
![License](https://img.shields.io/badge/license-CC%20BY--NC%204.0-blue)  
![Version](https://img.shields.io/badge/version-v0.5--Alpha-orange)

> *“Humanity always advances through contradictions and conflicts.”*

The **SECM (Societal Evolution Computational Model)** is a quantitative framework designed to **analyze and visualize the contradictions within human societies and the structural limits of their capacity to bear these contradictions**.  

Rather than focusing on short-term economic forecasting, SECM emphasizes long-term systemic feedback: how productive capacity interacts with inequality, stress, and external shocks to generate cycles of stability, crisis, and transformation.  

The **V0.5 Alpha release** marks the first full-featured build with a standalone simulator (executable) and a complete illustrated user manual, enabling direct replication of results without programming.

---

📘 **Overview**

SECM captures societal dynamics through three primary axes:

- **X-axis (Productive Capacity):** energy base, infrastructure, KWPE (Kilowatt Productivity Equivalent).  
- **Y-axis (Social Cost / Tension):** class opportunity cost, inequality, population–land stress, systemic frictions.  
- **Z-axis (External Perturbations):** wars, pandemics, exogenous stabilizers or destabilizers.  

Together, these axes describe how societies accumulate stress, when they surpass their contradiction-bearing limit, and how crises or restructurings unfold.

### 🌟 What’s New in V0.5 Alpha

- **Standalone Simulator**  
  A packaged `.exe` (requires .NET 8) with both UI and Excel-driven modes, allowing direct use without coding.  

- **Illustrated User Manual**  
  Full step-by-step instructions with screenshots, enabling non-technical users to run and interpret simulations.  

- **Unified-parameter multi-nation validation**  
  One reference calibration was locked and successfully applied across four countries (USA, Japan, Argentina, Greece), demonstrating cross-national robustness.  

- **Contradiction limit analysis**  
  Tracks when social tension (Y) surpasses the structural tolerance line (Ylimit), reproducing real-world crises (e.g., dot-com slowdown, global financial crisis, sovereign debt collapse).  

- **Extreme stress testing**  
  Robust under horizon truncation and radical Y-axis perturbations, producing Pearson correlations ≈ 1.0 across timeframes.  

- **Comprehensive documentation**  
  Includes the technical white paper, validation report, and LaTeX sources for reproducible research.


---

## 📂 Repository Structure

```text
SECM-Project
│  README.md
│  LICENSE CC BY-NC 4.0
│  citation.bib
│  CITATION.cff
│
├─Coding/SECM V0.5 Alpha      → Source code (VB / .NET 8)
├─Data                        → Input datasets & results
│   ├─DATAsource              → LOCF-patched 1980–2020 data (USA, Japan, Greece, Argentina)
│   └─ResultData              → Simulation outputs & stress tests
├─Diagrams                    → Logical & validation diagrams
├─Document                    → White paper, manuals, validation reports
├─Program                     → Executable builds & input templates
└─Tex                         → LaTeX sources for reproducible docs
```

## 📊 Validation

- **USA (1980–2020):** dot-com slowdown (2001), global financial crisis (2008).  
- **Japan (1980–2020):** stagnation trends, COVID-19 2020 social stress release.  
- **Argentina (1980–2020):** Austral Plan (1985), 2001 collapse, repeated cycles.  
- **Greece (1980–2020):** sovereign debt crisis (2009), two extreme-case stress tests.  

Extreme stress tests produced **Pearson correlation = 1.0** between baseline and shortened horizons, confirming stability and robustness.
---

## 🚀 How to Run

1. **Executable (recommended):**  
   - Download from `Program/Zip/SECM_V0.5_Alpha.zip`.  
   - Requires [.NET 8 runtime](https://dotnet.microsoft.com/en-us/download).  
   - Extract and run `SECM运行实体.exe`.  
   - Full instructions: see *SECM V0.5 Alpha User Manual.pdf*.  

2. **Excel-driven mode:**  
   - Open `SECM_V0.5_AllInputs_Template.xlsx`.  
   - Stage-based simulation supported with dynamic parameter updates.  

3. **Source code:**  
   - Compile `SECM_Engine.vb` under VB / .NET 8.  
   - Dependencies: MathNet.Numerics, NPOI, Newtonsoft.Json, ImageSharp, etc.  

---

## 🔒 License

Licensed under [Creative Commons Attribution-NonCommercial 4.0 International](https://creativecommons.org/licenses/by-nc/4.0/).  
**Commercial or derivative use requires prior permission.**

---

## 📚 Citation

```bibtex
@misc{strangethought2025_secm_v05alpha,
  author       = {Strangethought2025},
  title        = {{SECM: Societal Evolution Computational Model (V0.5 ALPHA)}},
  year         = {2025},
  version      = {V0.5 ALPHA},
  howpublished = {\url{https://github.com/Strangethought2025/SECM-Project}},
  doi          = {10.5281/zenodo.16884870},
  note         = {CC BY-NC 4.0 License}
}
