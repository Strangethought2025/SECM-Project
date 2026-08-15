# -*- coding: utf-8 -*-
"""诊断：越线期结构——是否'危机前越线→危机→回落→再越线'（而非一直越线）"""
import pandas as pd, numpy as np, os, io, sys
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
TUNE = r"E:\AI-Personal\SECM-Project\V0.6\tune"
OOS = r"E:\AI-Personal\SECM-Project\V0.6\oos2000"
def mov_avg(x,w): return pd.Series(x).rolling(w,center=True,min_periods=1).mean().to_numpy()

def run(df,P):
    patent=df["Patent"].to_numpy(float); edu=df["EduRate"].to_numpy(float)
    mil=df["Military"].to_numpy(float)/100; unemp=df["unemployment"].to_numpy(float)
    mcap=df["mcap_gdp"].to_numpy(float); X=df["GDP"].to_numpy(float)
    gini=df["Gini"].to_numpy(float) if "Gini" in df.columns else np.zeros(len(df))
    n=len(df)
    Xn=np.maximum(X/X[0],P["Xmin"]); dX=np.diff(Xn,prepend=Xn[0])
    pg=np.zeros(n)
    for t in range(1,n):
        pr=patent[t-1] if patent[t-1]>0 else 1.0
        pg[t]=np.clip((patent[t]-patent[t-1])/pr,-1,1)
    edu_n=edu/np.nanmax(edu) if np.nanmax(edu)>0 else np.zeros(n)
    gini_n=gini/100 if np.nanmax(gini)>0 else np.zeros(n)
    u_norm=unemp/np.nanmax(unemp) if np.nanmax(unemp)>0 else np.zeros(n)
    mg=np.zeros(n)
    for t in range(1,n):
        pr=mcap[t-1] if mcap[t-1]>0 else 1.0
        mg[t]=np.clip((mcap[t]-mcap[t-1])/pr,-1,1)
    crash=np.clip(-mg,0,1)
    Zc=np.clip(P["wg"]*gini_n+P["wu"]*u_norm+P["wc"]*crash,0,1.5)
    bonus=np.maximum(P["wp"]*mov_avg(pg,3)+P["we"]*edu_n,P["ZtechMin"])
    Z=np.clip(P["gS"]*Zc-P["gX"]*bonus,-1.5,1.5)
    Zeff=np.sign(Z)*((1+np.abs(Z))**2-1)
    Omega=np.clip(P["wO"]*u_norm+P["wM"]*crash,0,2)
    Y_base=P["a0"]+P["a1"]*Xn+P["b1"]*gini_n+P["mu"]*np.log(1+X)
    Y=np.zeros(n); Y[0]=Y_base[0]
    for t in range(1,n):
        Y[t]=Y[t-1]+dX[t]*P["kY"]*(1+P["ZI"]*Zeff[t])
    Yl=Xn*(1-mil)*P["kLimit"]*(1+Omega)
    return df.index.to_numpy(int), Y-Yl

P=dict(kY=1.0,kLimit=1.8,a0=0.2,a1=0.3,b1=0.5,mu=0.3,wg=0.5,wu=0.6,wc=0.4,
       wp=0.3,we=0.4,ZtechMin=0.3,gS=1.0,gX=1.0,wO=0.5,wM=0.3,Xmin=0.1,ZI=1.0)

def periods(yrs,G):
    out=[]; start=None
    for i,g in enumerate(G):
        if g>0 and start is None: start=int(yrs[i])
        elif g<=0 and start is not None:
            out.append((start,int(yrs[i-1]))); start=None
    if start is not None: out.append((start,int(yrs[-1])))
    return out

checks=[("USA","tune"),("Argentina","tune"),("Russia","oos"),("Turkey","oos"),("Greece","oos"),("Mexico","oos"),("Spain","oos"),("Brazil","oos")]
for name,src in checks:
    path=os.path.join(TUNE,f"{name}.csv") if src=="tune" else os.path.join(OOS,f"{name}.csv")
    df=pd.read_csv(path,index_col="Year").ffill().bfill().fillna(0)
    yrs,G=run(df,P)
    ps=periods(yrs,G)
    # 检查是否"一直越线不下来"：最后一个越线期是否到数据末尾且长度>10
    tail_long = ps and ps[-1][1]==int(yrs[-1]) and (ps[-1][1]-ps[-1][0])>10
    print(f"{name:10s} 越线期{ps}  {'⚠️末尾长期越线' if tail_long else '✅ 危机后回落'}")
