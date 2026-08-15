# -*- coding: utf-8 -*-
"""补拉墨西哥/土耳其/俄罗斯/希腊 1980-2025（6国校准集）"""
import requests, pandas as pd, os, io, sys
from concurrent.futures import ThreadPoolExecutor
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
OUT = r"E:\AI-Personal\SECM-Project\V0.6\tune"
COUNTRIES = {"Mexico":"MX","Turkey":"TR","Russia":"RU","Greece":"GR"}
IND = {"Population":"SP.POP.TOTL","GDP":"NY.GDP.MKTP.CD","Patent":"IP.PAT.RESD",
    "EduRate":"SE.TER.ENRR","Military":"MS.MIL.XPND.GD.ZS","unemployment":"SL.UEM.TOTL.ZS",
    "mcap_gdp":"CM.MKT.LCAP.GD.ZS","Gini":"SI.POV.GINI"}
def f1(cc,ind):
    url=f"https://api.worldbank.org/v2/country/{cc}/indicator/{ind}?format=json&date=1980:2025&per_page=100"
    try:
        d=requests.get(url,timeout=15).json()
        return {int(x["date"]):x["value"] for x in (d[1] or []) if x.get("value") is not None}
    except: return {}
def fc(item):
    name,cc=item
    with ThreadPoolExecutor(max_workers=8) as ex:
        res=list(ex.map(lambda t:(t[0],f1(cc,t[1])), IND.items()))
    df=pd.DataFrame({k:pd.Series(d) for k,d in res}).sort_index(); df.index.name="Year"
    df.to_csv(os.path.join(OUT,f"{name}.csv"))
    print(f"{name}: 年数={len(df)} 失业={df['unemployment'].notna().sum()} 股市={df['mcap_gdp'].notna().sum()} Gini={df['Gini'].notna().sum()}")
with ThreadPoolExecutor(max_workers=4) as ex:
    list(ex.map(fc, COUNTRIES.items()))
print("完成")
