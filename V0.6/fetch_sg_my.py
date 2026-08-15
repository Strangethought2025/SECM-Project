# -*- coding: utf-8 -*-
"""抓取 新加坡/马来西亚 1980-2025 全指标 (世界银行批量, 免费)"""
import requests, zipfile, io, os, pandas as pd, numpy as np
UA = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"}
OOS = r"E:\AI-Personal\SECM-Project\V0.6\oos2000"
IND = {"Population":"SP.POP.TOTL","GDP":"NY.GDP.MKTP.CD","Patent":"IP.PAT.RESD",
       "EduRate":"SE.TER.ENRR","Military":"MS.MIL.XPND.GD.ZS",
       "unemployment":"SL.UEM.TOTL.ZS","mcap_gdp":"CM.MKT.LCAP.GD.ZS",
       "Gini":"SI.POV.GINI","energy_pc":"EG.USE.PCAP.KG.OE",
       "murder":"VC.IHR.PSRC.P5","health":"SH.XPD.CHEX.GD.ZS"}

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
    m = m[(m["Year"]>=1980)&(m["Year"]<=2025)]
    return {c: m[m["Country Name"]==c].set_index("Year")["v"] for c in m["Country Name"].unique()}

have = {col: bulk(code) for col, code in IND.items()}
for name in ["Singapore","Malaysia"]:
    df = pd.DataFrame({"Year": list(range(1980,2026))})
    for col in IND:
        s = have[col].get(name)
        df[col] = df["Year"].map(s) if s is not None else np.nan
    n = {c: int(df[c].notna().sum()) for c in IND}
    df.to_csv(os.path.join(OOS, f"{name}.csv"), index=False)
    print(name, {c: v for c, v in n.items()})
