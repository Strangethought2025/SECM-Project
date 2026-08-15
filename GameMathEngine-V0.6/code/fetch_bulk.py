# -*- coding: utf-8 -*-
"""批量下载(浏览器UA+下载端点,返回ZIP) → 解包 → 合并进各国数据"""
import requests, zipfile, io as iolib, pandas as pd, os, sys
sys.stdout = iolib.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
TUNE = r"E:\AI-Personal\SECM-Project\V0.6\tune"
OOS = r"E:\AI-Personal\SECM-Project\V0.6\oos2000"
ALL = {"USA":(TUNE,"USA"),"Argentina":(TUNE,"ARG"),"Mexico":(TUNE,"MEX"),"Turkey":(TUNE,"TUR"),
       "Russia":(TUNE,"RUS"),"Greece":(TUNE,"GRC"),
       "UK":(OOS,"GBR"),"Spain":(OOS,"ESP"),"Portugal":(OOS,"PRT"),"Ireland":(OOS,"IRL"),
       "Cyprus":(OOS,"CYP"),"Iceland":(OOS,"ISL"),"Brazil":(OOS,"BRA"),"Ukraine":(OOS,"UKR"),
       "Venezuela":(OOS,"VEN"),"Egypt":(OOS,"EGY"),"Pakistan":(OOS,"PAK"),
       "SriLanka":(OOS,"LKA"),"Ghana":(OOS,"GHA"),"Lebanon":(OOS,"LBN")}
INDS = {"energy_pc":"EG.USE.PCAP.KG.OE","murder":"VC.IHR.PSRC.P5","health":"SH.XPD.CHEX.GD.ZS"}
UA = {"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36"}

def bulk(ind):
    url=f"https://api.worldbank.org/v2/en/indicator/{ind}?downloadformat=csv"
    r=requests.get(url,headers=UA,timeout=120)
    if r.content[:2]!=b"PK":
        return None, f"非zip(前80字符: {r.content[:80]!r})"
    z=zipfile.ZipFile(iolib.BytesIO(r.content))
    csv_name=[n for n in z.namelist() if n.endswith(".csv") and n.startswith("API_")][0]
    return z.read(csv_name).decode("utf-8-sig"), csv_name

for key,ind in INDS.items():
    txt,info=bulk(ind)
    if txt is None:
        print(f"{key}: 失败 {info}"); continue
    dfb=pd.read_csv(iolib.StringIO(txt), skiprows=4)   # 跳过4行元数据
    # 年份列 = 纯数字列名
    ycols=[c for c in dfb.columns if str(c).isdigit()]
    print(f"{key}: 全表 {len(dfb)} 行, 年份列 {len(ycols)}")
    dfb.to_csv(os.path.join(TUNE,f"_bulk_{key}.csv"),index=False)
    # 合并进各国
    for name,(d,cc) in ALL.items():
        sub=dfb[dfb["Country Code"]==cc]
        if sub.empty:
            print(f"  {name}: 表中无 {cc}"); continue
        row=sub.iloc[0]
        series={int(y):row[y] for y in ycols if pd.notna(row[y])}
        path=os.path.join(d,f"{name}.csv")
        df=pd.read_csv(path,index_col="Year")
        df[key]=pd.Series(series)
        df.to_csv(path)
    print(f"{key}: 合并完成")
print("全部完成")
