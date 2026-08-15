# -*- coding: utf-8 -*-
"""样本外验证：10国，GDP作X，四国调的参数直接跑，不重调"""
import pandas as pd, numpy as np, os, io, sys
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
OOS = r"E:\AI-Personal\SECM-Project\V0.6\oos"

# 独立危机事件（Laeven-Valencia 银行危机 + Reinhart-Rogoff 违约）
CRISIS = {
    "SouthKorea":[1997], "Mexico":[1982,1994], "Turkey":[2000,2001],
    "Indonesia":[1997], "Thailand":[1997], "Brazil":[1983,1990,1994],
    "Chile":[1982], "Russia":[1998], "India":[1991], "SouthAfrica":[],
}
def sign_log(z): return np.sign(z)*np.log(1+np.abs(z))
def mov_avg(x,w): return pd.Series(x).rolling(w,center=True,min_periods=1).mean().to_numpy()

def run(f, P):
    df = pd.read_csv(os.path.join(OOS,f), index_col="Year").ffill().bfill()
    pop=df["Population"].to_numpy(float); gdp=df["GDP"].to_numpy(float)
    patent=df["Patent"].to_numpy(float); edu=df["EduRate"].to_numpy(float)
    gini=df["Gini"].to_numpy(float); mil=df["Military"].to_numpy(float)
    arable=df["Arable"].to_numpy(float); unemp=df["unemployment"].to_numpy(float)
    mcap=df["mcap_gdp"].to_numpy(float)
    X=gdp; Xn=X/X[0]; dX=np.diff(Xn,prepend=Xn[0])
    # Z：专利增速 + 教育 + 流动性(无TFP)
    pg=np.zeros(len(df))
    for t in range(1,len(df)):
        pr=patent[t-1] if patent[t-1]>0 else 1.0
        pg[t]=np.clip((patent[t]-patent[t-1])/pr,-1,1)
    edu_n=edu/np.nanmax(edu) if np.nanmax(edu)>0 else edu
    Z=np.clip(mov_avg(0.5*pg+0.3*(edu_n-0.5)+0.2*(0.4-gini/100),3),-0.5,0.5)
    fZ=sign_log(Z)
    # 土地压力（缺耕地则=0）
    popP=np.zeros(len(df))
    if np.nanmax(arable)>0:
        popP=np.clip((pop/arable)/np.nanmedian(pop/arable)-1,0,3)
    # Y
    Y=np.zeros(len(df)); Y[0]=P["Y0"]
    for t in range(1,len(df)): Y[t]=Y[t-1]+P["kX"]*dX[t]*(1+popP[t])+P["kZ"]*fZ[t]
    # 金融压力
    u_norm=unemp/np.nanmax(unemp); mg=np.zeros(len(df))
    for t in range(1,len(df)):
        pr=mcap[t-1] if mcap[t-1]>0 else 1.0
        mg[t]=np.clip((mcap[t]-mcap[t-1])/pr,-1,1)
    fstress=np.clip(P["wU"]*u_norm+P["wC"]*np.clip(-mg,0,1),0,0.8)
    t=np.arange(len(df))
    Yl=P["kL"]*(Xn**P["beta"])*(1-mil/100)*(1-fstress)-P["b0"]*(1+P["bG"]*t)
    return df.index.to_numpy(int), Y-Yl

def sig_peaks(years,G,w=5,thresh=0.06):
    base=mov_avg(G,w); out=[]
    for t in range(1,len(G)-1):
        if G[t]>=G[t-1] and G[t]>=G[t+1] and G[t]>0 and (G[t]-base[t])>thresh:
            out.append(int(years[t]))
    return out

P = dict(kX=1.0, kZ=0.3, kL=1.5, beta=0.6, b0=0.12, bG=0.003, Y0=1.0, wU=0.5, wC=0.5)

tot_hit=tot_ev=0
for name in CRISIS:
    yrs,G = run(name+".csv", P)
    peaks=sig_peaks(yrs,G)
    hits=[ev for ev in CRISIS[name] if any(abs(ev-p)<=1 for p in peaks)]
    tot_hit+=len(hits); tot_ev+=len(CRISIS[name]) if CRISIS[name] else 0
    print(f"{name:12s} 事件={CRISIS[name]} 命中={hits} 峰值={peaks}")
print(f"\n样本外总计: {tot_hit}/{tot_ev} 命中（四国参数，未重调）")
