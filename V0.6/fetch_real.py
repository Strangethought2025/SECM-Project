# -*- coding: utf-8 -*-
"""补拉真实指标：一次能源/凶杀率/医疗支出/贫困率 → 合并进现有数据"""
import requests, pandas as pd, os, io, sys
from concurrent.futures import ThreadPoolExecutor
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
TUNE = r"E:\AI-Personal\SECM-Project\V0.6\tune"
OOS = r"E:\AI-Personal\SECM-Project\V0.6\oos2000"
# 国家 → (目录, 代码)
ALL = {"USA":(TUNE,"US"),"Argentina":(TUNE,"AR"),"Mexico":(TUNE,"MX"),"Turkey":(TUNE,"TR"),
    "Russia":(TUNE,"RU"),"Greece":(TUNE,"GR"),
    "UK":(OOS,"GB"),"Spain":(OOS,"ES"),"Portugal":(OOS,"PT"),"Ireland":(OOS,"IE"),
    "Cyprus":(OOS,"CY"),"Iceland":(OOS,"IS"),"Brazil":(OOS,"BR"),"Ukraine":(OOS,"UA"),
    "Venezuela":(OOS,"VE"),"Egypt":(OOS,"EG"),"Pakistan":(OOS,"PK"),"SriLanka":(OOS,"LK"),
    "Ghana":(OOS,"GH"),"Lebanon":(OOS,"LB")}
NEW_IND = {"energy_pc":"EG.USE.PCAP.KG.OE",      # 一次能源 kg油当量/人
           "murder":"VC.IHR.PSRC.P5",            # 凶杀率 /10万
           "health":"SH.XPD.CHEX.GD.ZS"}         # 医疗支出 %GDP
def f1(cc,ind):
    url=f"https://api.worldbank.org/v2/country/{cc}/indicator/{ind}?format=json&date=1980:2025&per_page=100"
    try:
        d=requests.get(url,timeout=15).json()
        return {int(x["date"]):x["value"] for x in (d[1] or []) if x.get("value") is not None}
    except: return {}
def fc(item):
    name,(dir,cc)=item
    path=os.path.join(dir,f"{name}.csv")
    if not os.path.exists(path): return f"{name}: 无csv"
    df=pd.read_csv(path,index_col="Year")
    with ThreadPoolExecutor(max_workers=3) as ex:
        res=list(ex.map(lambda t:(t[0],f1(cc,t[1])), NEW_IND.items()))
    for k,d in res:
        s=pd.Series(d); s.index.name="Year"
        df[k]=s
    df.to_csv(path)
    nn={k:df[k].notna().sum() for k in NEW_IND}
    return f"{name}: 能源={nn['energy_pc']} 凶杀={nn['murder']} 医疗={nn['health']}"
with ThreadPoolExecutor(max_workers=6) as ex:
    for r in ex.map(fc, ALL.items()): print(r)
print("完成")
