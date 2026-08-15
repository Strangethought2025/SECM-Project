# -*- coding: utf-8 -*-
"""拉美国+阿根廷 1980-2025 长序列（调参集）"""
import requests, pandas as pd, os, io, sys
from concurrent.futures import ThreadPoolExecutor
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
OUT = r"E:\AI-Personal\SECM-Project\V0.6\tune"
os.makedirs(OUT, exist_ok=True)
COUNTRIES = {"USA":"US","Argentina":"AR"}
IND = {"Population":"SP.POP.TOTL","GDP":"NY.GDP.MKTP.CD","Patent":"IP.PAT.RESD",
    "EduRate":"SE.TER.ENRR","Military":"MS.MIL.XPND.GD.ZS","unemployment":"SL.UEM.TOTL.ZS",
    "mcap_gdp":"CM.MKT.LCAP.GD.ZS","Gini":"SI.POV.GINI"}
def fetch_one(cc,ind):
    url=f"https://api.worldbank.org/v2/country/{cc}/indicator/{ind}?format=json&date=1980:2025&per_page=100"
    try:
        d=requests.get(url,timeout=15).json()
        return {int(x["date"]):x["value"] for x in (d[1] or []) if x.get("value") is not None}
    except: return {}
def fc(item):
    name,cc=item
    with ThreadPoolExecutor(max_workers=8) as ex:
        res=list(ex.map(lambda t:(t[0],fetch_one(cc,t[1])), IND.items()))
    df=pd.DataFrame({k:pd.Series(d) for k,d in res}).sort_index(); df.index.name="Year"
    df.to_csv(os.path.join(OUT,f"{name}.csv"))
    print(f"{name}: shape={df.shape} 失业非空={df['unemployment'].notna().sum()} 股市非空={df['mcap_gdp'].notna().sum()} Gini={df['Gini'].notna().sum()}")
with ThreadPoolExecutor(max_workers=2) as ex:
    list(ex.map(fc, COUNTRIES.items()))
print("完成:", OUT)
