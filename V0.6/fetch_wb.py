# -*- coding: utf-8 -*-
"""从世界银行 API 拉取四国补充指标（失业率、股市市值/GDP、GDP），存 CSV 供模型用"""
import requests, pandas as pd, io, sys
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")

COUNTRIES = {"USA":"US","Japan":"JP","Argentina":"AR","Greece":"GR"}
IND = {
    "unemployment": "SL.UEM.TOTL.ZS",       # 失业率 %
    "mcap_gdp": "CM.MKT.LCAP.GD.ZS",         # 股市市值/GDP %
    "gdp_percap": "NY.GDP.PCAP.KD",          # 人均GDP(2015$)
}

def fetch(code, ind, name):
    url = f"https://api.worldbank.org/v2/country/{code}/indicator/{ind}?format=json&date=1980:2020&per_page=100"
    try:
        r = requests.get(url, timeout=30)
        data = r.json()
        rows = data[1] if len(data) > 1 and data[1] else []
        out = {}
        for x in rows:
            if x.get("value") is not None:
                out[int(x["date"])] = x["value"]
        return out
    except Exception as e:
        return {"_error": str(e)}

for name, ccode in COUNTRIES.items():
    row = {}
    for key, ind in IND.items():
        d = fetch(ccode, ind, key)
        if "_error" in d:
            print(f"{name} {key}: ERROR {d['_error']}")
        else:
            row[key] = pd.Series(d)
            print(f"{name} {key}: {len(d)} 个年份")
    df = pd.DataFrame(row).sort_index()
    df.index.name = "Year"
    df.to_csv(rf"E:\AI-Personal\SECM-Project\V0.6\wb_{name}.csv")
    print(f"  已存 wb_{name}.csv, shape={df.shape}, 年份 {df.index.min()}-{df.index.max()}\n")
