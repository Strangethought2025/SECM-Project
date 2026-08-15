# -*- coding: utf-8 -*-
"""样本外扩展：拉 10 国世界银行数据（GDP作X、专利、入学、Gini、军费、耕地、失业、股市）"""
import requests, pandas as pd, io, sys, os
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")

OUT = r"E:\AI-Personal\SECM-Project\V0.6\oos"
os.makedirs(OUT, exist_ok=True)

COUNTRIES = {
    "SouthKorea":"KR","Mexico":"MX","Turkey":"TR","Indonesia":"ID","Thailand":"TH",
    "Brazil":"BR","Chile":"CL","Russia":"RU","India":"IN","SouthAfrica":"ZA",
}
IND = {
    "Population":"SP.POP.TOTL",
    "GDP":"NY.GDP.MKTP.CD",            # GDP 现价美元(作X代理)
    "Patent":"IP.PAT.RESD",            # 居民专利申请
    "EduRate":"SE.TER.ENRR",           # 高等教育毛入学率
    "Gini":"SI.POV.GINI",
    "Military":"MS.MIL.XPND.GD.ZS",    # 军费 %GDP
    "Arable":"AG.LND.ARBL.HA",         # 耕地公顷
    "unemployment":"SL.UEM.TOTL.ZS",
    "mcap_gdp":"CM.MKT.LCAP.GD.ZS",
}

def fetch(ccode, ind):
    url=f"https://api.worldbank.org/v2/country/{ccode}/indicator/{ind}?format=json&date=1980:2022&per_page=100"
    try:
        d=requests.get(url,timeout=30).json()
        return {int(x["date"]):x["value"] for x in (d[1] or []) if x.get("value") is not None}
    except Exception as e:
        return {}

for name,cc in COUNTRIES.items():
    row={}
    for key,ind in IND.items():
        row[key]=pd.Series(fetch(cc,ind))
    df=pd.DataFrame(row).sort_index(); df.index.name="Year"
    df.to_csv(os.path.join(OUT,f"{name}.csv"))
    nonnull = {k: df[k].notna().sum() for k in IND}
    print(f"{name}: shape={df.shape} 非空年数={nonnull}")
print("\n完成，存于", OUT)
