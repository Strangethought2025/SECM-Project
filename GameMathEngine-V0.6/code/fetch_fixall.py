# -*- coding: utf-8 -*-
"""全量补洞: 8个核心指标批量下载, 回填所有CSV的缺失列/年份 (同一套指标)"""
import requests, zipfile, io, os, pandas as pd, numpy as np
UA = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"}
DIRS = [r"E:\AI-Personal\SECM-Project\V0.6\tune",
        r"E:\AI-Personal\SECM-Project\V0.6\oos2000"]
IND = {"Population":"SP.POP.TOTL","GDP":"NY.GDP.MKTP.CD","Patent":"IP.PAT.RESD",
       "EduRate":"SE.TER.ENRR","Military":"MS.MIL.XPND.GD.ZS",
       "unemployment":"SL.UEM.TOTL.ZS","mcap_gdp":"CM.MKT.LCAP.GD.ZS",
       "Gini":"SI.POV.GINI","energy_pc":"EG.USE.PCAP.KG.OE",
       "murder":"VC.IHR.PSRC.P5","health":"SH.XPD.CHEX.GD.ZS"}
MAP = {"usa":"United States","uk":"United Kingdom","srilanka":"Sri Lanka",
       "venezuela":"Venezuela, RB","russia":"Russian Federation",
       "egypt":"Egypt, Arab Rep.","lebanon":"Lebanon","korea":"Korea, Rep.",
       "turkey":"Turkiye","iran":"Iran, Islamic Rep."}

def bulk(code):
    url = f"https://api.worldbank.org/v2/en/indicator/{code}?downloadformat=csv"
    r = requests.get(url, headers=UA, timeout=120)
    z = zipfile.ZipFile(io.BytesIO(r.content))
    csvname = [n for n in z.namelist() if n.startswith("API_") and n.endswith(".csv")][0]
    raw = pd.read_csv(z.open(csvname), skiprows=4)
    raw = raw[raw["Country Name"].notna()]
    m = raw.melt(id_vars=["Country Name"], var_name="Year", value_name="v")
    m["Year"] = pd.to_numeric(m["Year"], errors="coerce")
    m = m.dropna(subset=["Year","v"])
    m = m[m["Year"] >= 1980]
    return {c: m[m["Country Name"]==c].set_index("Year")["v"] for c in m["Country Name"].unique()}

have = {col: bulk(code) for col, code in IND.items()}
report = {}
for folder in DIRS:
    for f in os.listdir(folder):
        if not f.endswith(".csv") or f.startswith("_"): continue
        base = f[:-4]; low = base.lower()
        wb = MAP.get(low, low.capitalize())
        if base == "SriLanka": wb = "Sri Lanka"
        df = pd.read_csv(os.path.join(folder, f))
        row = []
        for col in IND:
            s = have[col].get(wb)
            if s is None:
                row.append((col, "无WB数据")); continue
            before = df[col].notna().sum() if col in df.columns else 0
            mapped = df["Year"].map(s)
            if col in df.columns:
                df[col] = df[col].combine_first(mapped)
            else:
                df[col] = mapped
            after = df[col].notna().sum()
            if after > before:
                row.append((col, f"{before}->{after}"))
        if row:
            df.to_csv(os.path.join(folder, f), index=False)
            report[f"{folder}\\{f}"] = row
for k, v in report.items():
    print(k, "; ".join(f"{c}:{n}" for c, n in v))
print("\n补完后再查全空列:")
for folder in DIRS:
    for f in sorted(os.listdir(folder)):
        if not f.endswith(".csv") or f.startswith("_"): continue
        df = pd.read_csv(os.path.join(folder, f))
        bad = [c for c in df.columns if df[c].notna().sum() == 0]
        if bad: print(f"  {folder}\\{f}: 仍全空 {bad}")
