# -*- coding: utf-8 -*-
"""IMF WEO(UTF-16 TSV) 提取失业率LUR → 补进缺失业数据的国家"""
import requests, pandas as pd, io, sys, os
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
TUNE = r"E:\AI-Personal\SECM-Project\V0.6\tune"
OOS = r"E:\AI-Personal\SECM-Project\V0.6\oos2000"
url = "https://www.imf.org/-/media/Files/Publications/WEO/WEO-Database/2024/October/WEOOct2024all.xls"
r = requests.get(url, timeout=120, headers={"User-Agent":"Mozilla/5.0"})
txt = r.content.decode("utf-16")
df = pd.read_csv(io.StringIO(txt), sep="\t", low_memory=False)
print(f"WEO 全表: {df.shape}")
# 失业率 LUR
lur = df[df["WEO Subject Code"]=="LUR"].copy()
print(f"LUR 行数: {len(lur)}, 国家数: {lur['ISO'].nunique()}")
# 需要补的国家（失业率缺失或极少）
NEED = {"Ireland":("IRL",OOS),"Cyprus":("CYP",OOS),"Iceland":("ISL",OOS),
        "Portugal":("PRT",OOS),"Russia":("RUS",TUNE)}
for name,(iso,d) in NEED.items():
    sub = lur[lur["ISO"]==iso]
    if sub.empty:
        print(f"{name}: WEO无数据"); continue
    row = sub.iloc[0]
    ycols = [c for c in df.columns if str(c).isdigit()]
    series = {}
    for y in ycols:
        v = row[y]
        if pd.notna(v) and str(v) not in ("n/a","--"):
            try: series[int(y)] = float(v)
            except: pass
    path = os.path.join(d,f"{name}.csv")
    ddf = pd.read_csv(path,index_col="Year")
    # 只填空缺
    s = pd.Series(series); s.index.name="Year"
    ddf["unemployment"] = ddf["unemployment"].combine_first(s)
    ddf.to_csv(path)
    print(f"{name}: 补 {len(series)} 年 (总非空 {ddf['unemployment'].notna().sum()})")
print("完成")
