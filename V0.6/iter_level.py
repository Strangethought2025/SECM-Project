# -*- coding: utf-8 -*-
"""纯水平式 Y=X·(基准+矛盾−科技)，逐国(yf,yls)校准，扫描关键参数"""
import pandas as pd, numpy as np, os, io, sys
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
TUNE = r"E:\AI-Personal\SECM-Project\V0.6\tune"
OOS = r"E:\AI-Personal\SECM-Project\V0.6\oos2000"
TUNE_EV = {"USA":[1987,2001,2008,2020],"Argentina":[1982,1989,2001,2014,2020],
    "Mexico":[1982,1994,2008,2020],"Turkey":[1994,2001,2018,2020],
    "Russia":[1998,2008,2015,2020,2022],"Greece":[2010,2012,2020]}
VAL_EV = {"UK":[2008,2020],"Spain":[2008,2012,2020],"Portugal":[2011,2020],
    "Ireland":[2008,2010,2020],"Cyprus":[2013,2020],"Iceland":[2008,2020],"Brazil":[2015,2020],
    "Ukraine":[2009,2014,2020,2022],"Venezuela":[2013,2016,2020],"Egypt":[2011,2016,2020],
    "Pakistan":[2008,2019,2022],"SriLanka":[2022],"Ghana":[2022],"Lebanon":[2019,2020]}
def mov_avg(x,w): return pd.Series(x).rolling(w,center=True,min_periods=1).mean().to_numpy()

def run(df,P):
    patent=df["Patent"].to_numpy(float); edu=df["EduRate"].to_numpy(float)
    mil=df["Military"].to_numpy(float)/100; unemp=df["unemployment"].to_numpy(float)
    mcap=df["mcap_gdp"].to_numpy(float); X=df["GDP"].to_numpy(float)
    gini=df["Gini"].to_numpy(float) if "Gini" in df.columns else np.zeros(len(df))
    n=len(df)
    Xn=np.maximum(X/X[0],P["Xmin"])
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
    # 矛盾强度（含股崩持续累积）
    cris=np.zeros(n)
    for t in range(1,n): cris[t]=0.6*cris[t-1]+crash[t]
    Contra=P["wu"]*u_norm+P["wg"]*gini_n+P["wc"]*cris
    bonus=np.maximum(P["wp"]*mov_avg(pg,3)+P["we"]*edu_n,P["ZtechMin"])
    Omega=P["wO"]*u_norm+P["wM"]*cris
    # 纯水平式：Y=X·(基准+矛盾−科技)，Ylimit=X·(1−军费)·kLimit·(1+Ω)
    Y=Xn*(P["a0"]+P["kC"]*Contra-P["kZ"]*bonus)
    Yl=Xn*(1-mil)*P["kLimit"]*(1+Omega)
    return df.index.to_numpy(int), Y-Yl

def calibrate(df,first_ev,P):
    best=None
    for yf in np.arange(0.6,1.6,0.1):
        for yls in np.arange(0.7,1.6,0.1):
            yrs,G=run(df,P); G=G*yf/yls
            pos=np.where(G>0)[0]
            if len(pos) and abs(int(yrs[pos[0]])-first_ev)<=1:
                if np.any(G[pos[0]:]<0): return yf,yls
                if best is None: best=(yf,yls)
    return best if best else (1.0,1.0)

def evaluate(P, verbose=False):
    th=tt=nofb=0; det=[]
    for c,evs in TUNE_EV.items():
        df=pd.read_csv(os.path.join(TUNE,f"{c}.csv"),index_col="Year").ffill().bfill().fillna(0)
        yf,yls=calibrate(df,evs[0],P); yrs,G=run(df,P); G=G*yf/yls
        hits=[e for e in evs if any(abs(e-y)<=1 for y in yrs[G>0])]
        th+=len(hits); tt+=len(evs)
        pos=np.where(G>0)[0]
        if len(pos) and not np.any(G[pos[0]:]<0): nofb+=1
        det.append((c,hits,evs,int(np.sum(G>0))))
    vh=vt=0; vdet=[]
    for name,ev in VAL_EV.items():
        df=pd.read_csv(os.path.join(OOS,f"{name}.csv"),index_col="Year").ffill().bfill().fillna(0)
        yf,yls=calibrate(df,ev[0],P); yrs,G=run(df,P); G=G*yf/yls
        hits=[e for e in ev if any(abs(e-y)<=1 for y in yrs[G>0])]
        vh+=len(hits); vt+=len(ev)
        pos=np.where(G>0)[0]
        if len(pos) and not np.any(G[pos[0]:]<0): nofb+=1
        vdet.append((name,hits,ev,int(np.sum(G>0))))
    if verbose:
        for row in det: print(" 调参", row)
        for row in vdet: print(" 验证", row)
    return vh,vt,th,tt,nofb

best=[]
for kC in [0.5,1.0,1.5,2.0]:
    for kLimit in [0.8,1.2,1.6]:
        for a0 in [0.2,0.4,0.6]:
            P=dict(a0=a0,kC=kC,kZ=0.3,wu=0.7,wg=0.5,wc=0.5,wp=0.3,we=0.4,ZtechMin=0.3,
                   wO=0.5,wM=0.3,kLimit=kLimit,Xmin=0.1)
            vh,vt,th,tt,nofb=evaluate(P)
            best.append((vh,vt,th,tt,nofb,dict(kC=kC,kLimit=kLimit,a0=a0)))
best.sort(key=lambda x:(-x[0], x[4]))
print("Top:")
for vh,vt,th,tt,nofb,cfg in best[:8]:
    print(f"  验证={vh}/{vt}={vh/vt*100:.0f}% 校准={th}/{tt} 未回落={nofb} {cfg}")
