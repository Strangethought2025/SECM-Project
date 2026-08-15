# -*- coding: utf-8 -*-
"""诊断：欧债国 G 曲线 + 换成'G>0持续期'检测"""
import pandas as pd, numpy as np, os, io, sys
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
OOS = r"E:\AI-Personal\SECM-Project\V0.6\oos2000"
def mov_avg(x,w): return pd.Series(x).rolling(w,center=True,min_periods=1).mean().to_numpy()

def run(df,P):
    patent=df["Patent"].to_numpy(float); edu=df["EduRate"].to_numpy(float)
    mil=df["Military"].to_numpy(float)/100; unemp=df["unemployment"].to_numpy(float)
    mcap=df["mcap_gdp"].to_numpy(float); X=df["GDP"].to_numpy(float)
    Xn=np.maximum(X/X[0],P["Xmin"]); dX=np.diff(Xn,prepend=Xn[0])
    pg=np.zeros(len(df))
    for t in range(1,len(df)):
        pr=patent[t-1] if patent[t-1]>0 else 1.0
        pg[t]=np.clip((patent[t]-patent[t-1])/pr,-1,1)
    edu_n=edu/np.nanmax(edu) if np.nanmax(edu)>0 else edu
    Ztech=np.maximum(P["wp"]*mov_avg(pg,3)+P["we"]*edu_n,P["ZtechMin"])
    u_norm=unemp/np.nanmax(unemp); mg=np.zeros(len(df))
    for t in range(1,len(df)):
        pr=mcap[t-1] if mcap[t-1]>0 else 1.0
        mg[t]=np.clip((mcap[t]-mcap[t-1])/pr,-1,1)
    Z=np.clip(P["wu"]*u_norm+P["wc"]*np.clip(-mg,0,1)-Ztech,-1,1)
    Yl=(Xn-mil*Xn)*(P["w0"]+P["we"]*edu_n)
    Y=np.zeros(len(df)); Y[0]=P["Y0"]; crisis=0.0
    for t in range(1,len(df)):
        Y[t]=Y[t-1]+(dX[t]-P["damage"]*crisis)*P["kY"]*(1+P["ZImpactK"]*Z[t])
        crisis=1.0 if Y[t]>Yl[t] else max(0.0,crisis-0.5)
    return df.index.to_numpy(int), Y, Yl

P=dict(kY=3.0,ZImpactK=1.0,w0=0.4,wu=0.7,wc=0.3,wp=0.3,we=0.4,ZtechMin=0.3,Xmin=0.1,Y0=1.0,damage=0.03)
for c in ["Greece","Portugal","Ireland","Spain","Iceland","Cyprus"]:
    df=pd.read_csv(os.path.join(OOS,f"{c}.csv"),index_col="Year").ffill().bfill()
    yrs,Y,Yl=run(df,P); G=Y-Yl
    above=[int(y) for y,g in zip(yrs,G) if g>0]
    print(f"{c}: G>0年份={above}")
    print("   G: "+" ".join(f"{y}:{g:+.2f}" for y,g in zip(yrs,G) if y%3==0))
