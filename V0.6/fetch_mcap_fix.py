# -*- coding: utf-8 -*-
"""补抓缺股市数据的国家: CM.MKT.LCAP.GD.ZS (市值/GDP)"""
import requests, zipfile, io, os, pandas as pd, numpy as np
IND = "CM.MKT.LCAP.GD.ZS"
OOS = r"E:\AI-Personal\SECM-Project\V0.6\oos2000"
TUNE = r"E:\AI-Personal\SECM-Project\V0.6\tune"
UA = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"}
url = f"https://api.worldbank.org/v2/en/indicator/{IND}?downloadformat=csv"
print("下载:", IND)
r = requests.get(url, headers=UA, timeout=120)
z = zipfile.ZipFile(io.BytesIO(r.content))
csvname = [n for n in z.namelist() if n.startswith("API_") and n.endswith(".csv")][0]
raw = pd.read_csv(z.open(csvname), skiprows=4)
raw = raw[raw["Country Name"].notna()]
melt = raw.melt(id_vars=["Country Name"], var_name="Year", value_name="mcap")
melt["Year"] = pd.to_numeric(melt["Year"], errors="coerce")
melt = melt.dropna(subset=["Year","mcap"])
melt = melt[melt["Year"] >= 1980]
have = {c: melt[melt["Country Name"] == c].set_index("Year")["mcap"]
        for c in melt["Country Name"].unique()}

NEED = {"Cyprus":"Cyprus","Iceland":"Iceland","Greece":"Greece","Japan":"Japan",
        "Ukraine":"Ukraine","Venezuela":"Venezuela, RB"}
fixed = []
for folder in (OOS, TUNE):
    for f in os.listdir(folder):
        if not f.endswith(".csv") or f.startswith("_"): continue
        base = f[:-4]
        key = NEED.get(base, None)
        if key is None or key not in have: continue
        df = pd.read_csv(os.path.join(folder, f))
        have_n = df["mcap_gdp"].notna().sum() if "mcap_gdp" in df.columns else 0
        if have_n >= 10: continue
        s = have[key]
        df["mcap_gdp"] = df["Year"].map(s)
        df.to_csv(os.path.join(folder, f), index=False)
        fixed.append(f"{folder}\\{f}: 补 {df['mcap_gdp'].notna().sum()} 年")
print("\n".join(fixed) if fixed else "无国家需要补")
