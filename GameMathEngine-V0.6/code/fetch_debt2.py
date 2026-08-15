# -*- coding: utf-8 -*-
"""补债务三件套: 私人信贷/GDP + 银行坏账率NPL + 政府支出/GDP (救济金) — 全免费世界银行批量下载"""
import requests, zipfile, io, os, pandas as pd, numpy as np
UA = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"}
DIRS = [r"E:\AI-Personal\SECM-Project\V0.6\tune",
        r"E:\AI-Personal\SECM-Project\V0.6\oos2000"]
IND = {"credit_gdp": "FS.AST.PRVT.GD.ZS",
       "npl":        "FB.AST.NPER.ZS",
       "gov_exp":    "GC.XPN.TOTL.GD.ZS"}
# 文件名 -> WB国名
MAP = {"usa":"United States","uk":"United Kingdom","srilanka":"Sri Lanka",
       "venezuela":"Venezuela, RB","russia":"Russian Federation",
       "egypt":"Egypt, Arab Rep.","lebanon":"Lebanon","korea":"Korea, Rep.",
       "turkey":"Turkiye","cyprus":"Cyprus","iran":"Iran, Islamic Rep."}

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
    return {c: m[m["Country Name"]==c].set_index("Year")["v"] for c in m["Country Name"].unique()}

have = {col: bulk(code) for col, code in IND.items()}
stats = {}
for folder in DIRS:
    for f in os.listdir(folder):
        if not f.endswith(".csv") or f.startswith("_"): continue
        base = f[:-4]
        low = base.lower()
        wb = MAP.get(low, low.capitalize())
        if base == "SriLanka": wb = "Sri Lanka"
        df = pd.read_csv(os.path.join(folder, f))
        row = []
        for col, code in IND.items():
            s = have[col].get(wb)
            if s is None:
                row.append((col, 0)); continue
            df[col] = df["Year"].map(s)
            row.append((col, df[col].notna().sum()))
        df.to_csv(os.path.join(folder, f), index=False)
        stats[f"{folder}\\{f}"] = row
for k, v in stats.items():
    print(k, " ".join(f"{c}:{n}" for c, n in v))
