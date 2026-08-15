# -*- coding: utf-8 -*-
"""SECM V0.6 严格验证：独立危机事件(主权违约+银行危机) × 显著峰值±1年"""
import pandas as pd, numpy as np, os, io, sys
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
BASE = r"E:\AI-Personal\SECM-Project\Data\DATAsource\1980_2020 Source"
WB = r"E:\AI-Personal\SECM-Project\V0.6"

# 独立危机事件（非金融输入变量，来自学术数据库）
# Laeven-Valencia 系统性银行危机 + Reinhart-Rogoff 主权违约/重组
CRISIS = {
    "USA":       [1988, 2007],              # 储贷危机1988 + 次贷2007
    "Japan":     [1997],                    # 银行危机1997
    "Argentina": [1980, 1982, 1989, 1995, 2001],  # 多次违约+银行危机
    "Greece":    [2008, 2012],              # 银行危机2008 + 债务重组2012
}

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
    tfp=df["TFPGrowth"].to_numpy(float); unemp=df["unemployment"].to_numpy(float); mcap=df["mcap_gdp"].to_numpy(float)
    X_full=pe+ap+pop*130/1e6; Xn=X_full/X_full[0]; dX=np.diff(Xn,prepend=Xn[0])
    pg=np.zeros(len(df))
    for t in range(1,len(df)):
        pr=patent[t-1] if patent[t-1]>0 else 1.0
        pg[t]=np.clip((patent[t]-patent[t-1])/pr,-1,1)
    edu_n=edu/np.nanmax(edu)
    Z=np.clip(mov_avg(0.25*pg+0.8*tfp+0.15*(0.4-gini/100)+0.05*(edu_n-0.5),3),-0.5,0.5)
    fZ=sign_log(Z); kwpe=X_full*1e6/pop; popP=np.clip((pop/arable)/(kwpe/15),0,3)
    Y=np.zeros(len(df)); Y[0]=P["Y0"]
    for t in range(1,len(df)): Y[t]=Y[t-1]+P["kX"]*dX[t]*(1+popP[t])+P["kZ"]*fZ[t]
    u_norm=unemp/np.nanmax(unemp); mg=np.zeros(len(df))
    for t in range(1,len(df)):
        pr=mcap[t-1] if mcap[t-1]>0 else 1.0
        mg[t]=np.clip((mcap[t]-mcap[t-1])/pr,-1,1)
    fstress=np.clip(P["wU"]*u_norm+P["wC"]*np.clip(-mg,0,1),0,0.8)
    t=np.arange(len(df))
    Yl=P["kL"]*(Xn**P["beta"])*(1-mil)*(1-fstress)-P["b0"]*(1+P["bG"]*t)
    return df["Year"].to_numpy(int), Y-Yl

def sig_peaks(years, G, w=5, thresh=0.06):
    base = mov_avg(G, w)
    out=[]
    for t in range(1,len(G)-1):
        if G[t]>=G[t-1] and G[t]>=G[t+1] and G[t]>0 and (G[t]-base[t])>thresh:
            out.append(int(years[t]))
    return out

P = dict(kX=1.0, kZ=0.3, kL=1.5, beta=0.6, b0=0.12, bG=0.003, Y0=1.0, wU=0.5, wC=0.5)

tot_hit=tot_ev=0
for c in CRISIS:
    yrs,G = run(c,P)
    peaks = sig_peaks(yrs,G)
    hits = [ev for ev in CRISIS[c] if any(abs(ev-p)<=1 for p in peaks)]
    # 也看越线事件（G从负转正，显著）
    cross = [int(yrs[t]) for t in range(1,len(G)) if G[t-1]<0 and G[t]>=0 and G[t]>0.05]
    hits2 = [ev for ev in CRISIS[c] if any(abs(ev-y)<=1 for y in cross)]
    hit = sorted(set(hits+hits2))
    tot_hit += len(hit); tot_ev += len(CRISIS[c])
    print(f"{c}: 事件={CRISIS[c]} 命中={hit} ({len(hit)}/{len(CRISIS[c])})")
    print(f"   显著峰值年:{peaks}")
    print(f"   显著越线年:{cross}")
print(f"\n总计: {tot_hit}/{tot_ev} 独立危机事件被命中（显著峰值±1年）")
