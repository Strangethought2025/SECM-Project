# -*- coding: utf-8 -*-
"""补抓资本流动三指标: FDI净流入/GDP + 组合证券净流入 + 外汇储备 (世界银行批量, 免费)"""
import requests, zipfile, io, os, pandas as pd, numpy as np
UA = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"}
DIRS = [r"E:\AI-Personal\SECM-Project\V0.6\tune",
        r"E:\AI-Personal\SECM-Project\V0.6\oos2000"]
IND = {"fdi_gdp":   "BX.KLT.DINV.WD.GD.ZS",   # FDI净流入 %GDP
       "portfolio": "BX.PEF.TOTL.CD.WD",      # 组合证券净流入 现价美元
       "reserves":  "FI.RES.TOTL.CD"}         # 外汇储备(不含黄金) 现价美元
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
            if s is None: row.append((col, 0)); continue
            mapped = df["Year"].map(s)
            if col in df.columns: df[col] = df[col].combine_first(mapped)
            else: df[col] = mapped
            row.append((col, df[col].notna().sum()))
        df.to_csv(os.path.join(folder, f), index=False)
        report[f"{folder}\\{f}"] = row
for k, v in report.items():
    print(k, " ".join(f"{c}:{n}" for c, n in v))
