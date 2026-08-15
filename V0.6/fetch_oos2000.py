# -*- coding: utf-8 -*-
"""2000-2025 扩展样本：并发拉取 20 国世界银行数据"""
import requests, pandas as pd, os, io, sys
from concurrent.futures import ThreadPoolExecutor
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
OUT = r"E:\AI-Personal\SECM-Project\V0.6\oos2000"
os.makedirs(OUT, exist_ok=True)
COUNTRIES = {
    "USA":"US","UK":"GB","Spain":"ES","Portugal":"PT","Ireland":"IE","Greece":"GR",
    "Cyprus":"CY","Iceland":"IS","Turkey":"TR","Argentina":"AR","Brazil":"BR","Mexico":"MX",
    "Russia":"RU","Ukraine":"UA","Venezuela":"VE","Egypt":"EG","Pakistan":"PK",
    "SriLanka":"LK","Ghana":"GH","Lebanon":"LB",
}
IND = {
    "Population":"SP.POP.TOTL","GDP":"NY.GDP.MKTP.CD","Patent":"IP.PAT.RESD",
    "EduRate":"SE.TER.ENRR","Military":"MS.MIL.XPND.GD.ZS",
    "unemployment":"SL.UEM.TOTL.ZS","mcap_gdp":"CM.MKT.LCAP.GD.ZS",
}
def fetch_one(cc, ind):
    url=f"https://api.worldbank.org/v2/country/{cc}/indicator/{ind}?format=json&date=2000:2025&per_page=100"
    try:
        d=requests.get(url,timeout=15).json()
        return {int(x["date"]):x["value"] for x in (d[1] or []) if x.get("value") is not None}
    except: return {}

def fetch_country(item):
    name,cc = item
    tasks = [(k,i) for k,i in IND.items()]
    with ThreadPoolExecutor(max_workers=8) as ex:
        results = list(ex.map(lambda t: (t[0], fetch_one(cc, t[1])), tasks))
    row = {k: pd.Series(d) for k,d in results}
    df = pd.DataFrame(row).sort_index(); df.index.name="Year"
    df.to_csv(os.path.join(OUT,f"{name}.csv"))
    return name, df.shape

with ThreadPoolExecutor(max_workers=5) as ex:
    for name, shape in ex.map(fetch_country, COUNTRIES.items()):
        print(f"{name:12s} shape={shape}")
print("\n完成:", OUT)
