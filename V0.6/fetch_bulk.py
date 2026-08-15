# -*- coding: utf-8 -*-
"""批量下载(每指标一次请求全国家CSV,绕限流) → 合并进各国数据"""
import requests, zipfile, io as iolib, pandas as pd, os, sys
sys.stdout = iolib.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
TUNE = r"E:\AI-Personal\SECM-Project\V0.6\tune"
OOS = r"E:\AI-Personal\SECM-Project\V0.6\oos2000"
ALL = {"USA":TUNE,"Argentina":TUNE,"Mexico":TUNE,"Turkey":TUNE,"Russia":TUNE,"Greece":TUNE,
       "UK":OOS,"Spain":OOS,"Portugal":OOS,"Ireland":OOS,"Cyprus":OOS,"Iceland":OOS,
       "Brazil":OOS,"Ukraine":OOS,"Venezuela":OOS,"Egypt":OOS,"Pakistan":OOS,
       "SriLanka":OOS,"Ghana":OOS,"Lebanon":OOS}
CODE = {"USA":"USA","Argentina":"ARG","Mexico":"MEX","Turkey":"TUR","Russia":"RUS","Greece":"GRC",
    "UK":"GBR","Spain":"ESP","Portugal":"PRT","Ireland":"IRL","Cyprus":"CYP","Iceland":"ISL",
    "Brazil":"BRA","Ukraine":"UKR","Venezuela":"VEN","Egypt":"EGY","Pakistan":"PAK",
    "SriLanka":"LKA","Ghana":"GHA","Lebanon":"LBN"}
INDS = {"energy_pc":"EG.USE.PCAP.KG.OE","murder":"VC.IHR.PSRC.P5","health":"SH.XPD.CHEX.GD.ZS"}

def bulk(ind):
    url=f"https://api.worldbank.org/v2/en/indicator/{ind}?downloadformat=csv"
    try:
        r=requests.get(url,timeout=120)
        if r.content[:2]==b"PK":
            z=zipfile.ZipFile(iolib.BytesIO(r.content))
            name=[n for n in z.namelist() if n.endswith(".csv")][0]
            return z.read(name).decode("utf-8-sig")
        return r.text
    except Exception as e:
        return None

for key,ind in INDS.items():
    txt=bulk(ind)
    if txt is None:
        print(f"{key}: 下载失败"); continue
    lines=txt.splitlines()
    if len(lines)<2: print(f"{key}: 空"); continue
    header=lines[0].split(",")
    yidx=[i for i,h in enumerate(header) if h.isdigit()]
    print(f"{key}: {len(lines)-1} 国家行, 年份列 {len(yidx)}")
    # 保存临时全表
    with open(os.path.join(TUNE,f"_bulk_{key}.csv"),"w",encoding="utf-8") as f:
        f.write(txt)
    # 合并进各国
    dfb=pd.read_csv(os.path.join(TUNE,f"_bulk_{key}.csv"))
    for name,d in ALL.items():
        cc=CODE[name]
        sub=dfb[dfb["Country Code"]==cc]
        if sub.empty: continue
        row=sub.iloc[0]
        series={int(y):row[y] for y in yidx if pd.notna(row[y])}
        path=os.path.join(d,f"{name}.csv")
        df=pd.read_csv(path,index_col="Year")
        df[key]=pd.Series(series)
        df.to_csv(path)
print("合并完成")
