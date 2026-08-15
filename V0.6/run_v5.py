# -*- coding: utf-8 -*-
"""v5：Ylimit 加入金融压力(失业率↑ + 股市暴跌)→ 金融危机年承载下探"""
import pandas as pd, numpy as np, os, io, sys
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
BASE = r"E:\AI-Personal\SECM-Project\Data\DATAsource\1980_2020 Source"
WB = r"E:\AI-Personal\SECM-Project\V0.6"
CRISIS = {"USA":[1987,2001,2008,2020],"Japan":[1991,1995,2008],
          "Argentina":[1982,1989,1990,2001],"Greece":[2009,2010]}
def sign_log(z): return np.sign(z)*np.log(1+np.abs(z))
def mov_avg(x,w): return pd.Series(x).rolling(w,center=True,min_periods=1).mean().to_numpy()

def run(country, P):
    df = pd.read_excel(os.path.join(BASE,f"SECM_V24_{country}.xlsx"),sheet_name=0).ffill()
    wb = pd.read_csv(os.path.join(WB,f"wb_{country}.csv"), index_col="Year")
    df = df.join(wb, on="Year", how="left").ffill().bfill()
    pop=df["Population"].to_numpy(float); pe=df["PrimaryEnergy"].to_numpy(float)
    ap=df["AnimalPower"].to_numpy(float); edu=df["EduRate"].to_numpy(float)
    gini=df["Gini"].to_numpy(float); mil=df["MilitaryRatio"].to_numpy(float)
    arable=df["ArableLandTotal"].to_numpy(float); patent=df["PatentCount"].to_numpy(float)
    tfp=df["TFPGrowth"].to_numpy(float)
    unemp=df["unemployment"].to_numpy(float)          # WB 失业率
    mcap=df["mcap_gdp"].to_numpy(float)               # WB 股市市值/GDP

    X_full = pe+ap+pop*130/1e6; Xn = X_full/X_full[0]
    dX = np.diff(Xn, prepend=Xn[0])
    # Z 四因 + 平滑
    pg=np.zeros(len(df))
    for t in range(1,len(df)):
        pr=patent[t-1] if patent[t-1]>0 else 1.0
        pg[t]=np.clip((patent[t]-patent[t-1])/pr,-1,1)
    edu_n=edu/np.nanmax(edu)
    Z=np.clip(mov_avg(0.25*pg+0.8*tfp+0.15*(0.4-gini/100)+0.05*(edu_n-0.5),3),-0.5,0.5)
    fZ=sign_log(Z)
    kwpe=X_full*1e6/pop; popP=np.clip((pop/arable)/(kwpe/15),0,3)
    # Y
    Y=np.zeros(len(df)); Y[0]=P["Y0"]
    for t in range(1,len(df)): Y[t]=Y[t-1]+P["kX"]*dX[t]*(1+popP[t])+P["kZ"]*fZ[t]
    # 金融压力：失业率(归一) + 股市暴跌
    u_norm = unemp/np.nanmax(unemp) if np.nanmax(unemp)>0 else np.zeros(len(df))
    mg=np.zeros(len(df))
    for t in range(1,len(df)):
        pr=mcap[t-1] if mcap[t-1]>0 else 1.0
        mg[t]=np.clip((mcap[t]-mcap[t-1])/pr,-1,1)
    mcrash=np.clip(-mg,0,1)   # 暴跌→压力
    fstress = P["wU"]*u_norm + P["wC"]*mcrash
    fstress = np.clip(fstress, 0, 0.8)
    # Ylimit：趋势(β<1) × 军事 × (1−金融压力) − 负担
    t=np.arange(len(df))
    Yl = P["kL"]*(Xn**P["beta"])*(1-mil)*(1-fstress) - P["b0"]*(1+P["bG"]*t)
    return df["Year"].to_numpy(int), Y-Yl

P = dict(kX=1.0, kZ=0.3, kL=1.5, beta=0.6, b0=0.12, bG=0.003, Y0=1.0, wU=0.5, wC=0.5)
for c in CRISIS:
    yrs,G = run(c,P)
    crossings=[int(yrs[t]) for t in range(1,len(G)) if G[t-1]<0 and G[t]>=0]
    peaks=[int(yrs[t]) for t in range(1,len(G)-1) if G[t]>=G[t-1] and G[t]>=G[t+1] and G[t]>0]
    hits=[cy for cy in CRISIS[c] if any(abs(cy-y)<=2 for y in crossings+peaks)]
    print(f"\n{c}: 危机={CRISIS[c]} 命中={hits} ({len(hits)}/{len(CRISIS[c])})")
    print(f"  越线:{crossings}  峰值:{peaks}")
    print("  G: " + " ".join(f"{y}:{g:+.2f}" for y,g in zip(yrs,G) if y%4==0))
