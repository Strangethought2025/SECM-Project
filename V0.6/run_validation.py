# -*- coding: utf-8 -*-
"""SECM V0.6 历史验证器 —— 四国运行 + 危机事件对齐"""
import pandas as pd, numpy as np, os, io, sys
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
sys.path.insert(0, os.path.dirname(__file__))
from model import compute

BASE = r"E:\AI-Personal\SECM-Project\Data\DATAsource\1980_2020 Source"
CRISIS = {"USA":[1987,2001,2008,2020],"Japan":[1991,1995,2008],
          "Argentina":[1982,1989,1990,2001],"Greece":[2009,2010]}

P = dict(kX=1.0, kZ=0.3, kL=1.4, beta=0.6, win=5, b0=0.15, bG=0.003, Y0=1.0)

for c in CRISIS:
    df = pd.read_excel(os.path.join(BASE, f"SECM_V24_{c}.xlsx"), sheet_name=0).ffill()
    Y, Yl, G, Z, cycle, Xn = compute(df, P)
    yrs = df["Year"].to_numpy(int)
    # 真实越线事件：G 从负转正
    crossings = [int(yrs[t]) for t in range(1, len(G)) if G[t-1] < 0 and G[t] >= 0]
    # 越线后的局部峰值
    peaks = [int(yrs[t]) for t in range(1, len(G)-1) if G[t] >= G[t-1] and G[t] >= G[t+1] and G[t] > 0]
    hits = [cy for cy in CRISIS[c] if any(abs(cy-y) <= 2 for y in crossings + peaks)]
    print(f"\n{c}: 危机={CRISIS[c]} 命中={hits} ({len(hits)}/{len(CRISIS[c])})")
    print(f"  越线年份: {crossings}")
    print(f"  越线后峰值: {peaks}")
    print("  G: " + " ".join(f"{y}:{g:+.2f}" for y, g in zip(yrs, G) if y % 4 == 0))
    # 能源周期在危机年的值（验证衰退下探）
    print("  能源周期(危机年): " + " ".join(f"{cy}:{cycle[np.where(yrs==cy)[0][0]]:.3f}" for cy in CRISIS[c] if cy in yrs))
