# -*- coding: utf-8 -*-
"""从 IMF WEO 提取政府债务(GGXWDG_NGDP) → 补进所有国家"""
import requests, pandas as pd, io, sys, os
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
TUNE = r"E:\AI-Personal\SECM-Project\V0.6\tune"
OOS = r"E:\AI-Personal\SECM-Project\V0.6\oos2000"
ALL = {"USA":(TUNE,"USA"),"Argentina":(TUNE,"ARG"),"Mexico":(TUNE,"MEX"),"Turkey":(TUNE,"TUR"),
       "Russia":(TUNE,"RUS"),"Greece":(TUNE,"GRC"),
       "UK":(OOS,"GBR"),"Spain":(OOS,"ESP"),"Portugal":(OOS,"PRT"),"Ireland":(OOS,"IRL"),
       "Cyprus":(OOS,"CYP"),"Iceland":(OOS,"ISL"),"Brazil":(OOS,"BRA"),"Ukraine":(OOS,"UKR"),
       "Venezuela":(OOS,"VEN"),"Egypt":(OOS,"EGY"),"Pakistan":(OOS,"PAK"),
       "SriLanka":(OOS,"LKA"),"Ghana":(OOS,"GHA"),"Lebanon":(OOS,"LBN"),
        "Singapore":(OOS,"SGP"),"Malaysia":(OOS,"MYS")}
url = "https://www.imf.org/-/media/Files/Publications/WEO/WEO-Database/2024/October/WEOOct2024all.xls"
r = requests.get(url, timeout=120, headers={"User-Agent":"Mozilla/5.0"})
txt = r.content.decode("utf-16")
df = pd.read_csv(io.StringIO(txt), sep="\t", low_memory=False)
ycols = [c for c in df.columns if str(c).isdigit()]
# 债务指标
debt = df[df["WEO Subject Code"]=="GGXWDG_NGDP"]
print(f"债务行数: {len(debt)}")
for name,(d,iso) in ALL.items():
    sub = debt[debt["ISO"]==iso]
    if sub.empty: print(f"{name}: 无"); continue
    row = sub.iloc[0]
    series = {}
    for y in ycols:
        v = row[y]
        if pd.notna(v) and str(v) not in ("n/a","--"):
            try: series[int(y)] = float(v)
            except: pass
    path = os.path.join(d,f"{name}.csv")
    ddf = pd.read_csv(path,index_col="Year")
    s = pd.Series(series); s.index.name="Year"
    ddf["debt_gdp"] = s
    ddf.to_csv(path)
    print(f"{name}: 债务 {ddf['debt_gdp'].notna().sum()} 年")
print("完成")
