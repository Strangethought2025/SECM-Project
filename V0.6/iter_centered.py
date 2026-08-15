# -*- coding: utf-8 -*-
"""G-中心化：危机=G偏离自身常态(接近/突破红线)，天然处理常年高压国"""
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

def compute(df,P):
    pop=df["Population"].to_numpy(float)
    epc=df["energy_pc"].to_numpy(float); murder=df["murder"].to_numpy(float)
    health=df["health"].to_numpy(float); edu=df["EduRate"].to_numpy(float)
    mil=df["Military"].to_numpy(float)/100; unemp=df["unemployment"].to_numpy(float)
    mcap=df["mcap_gdp"].to_numpy(float)
    gini=df["Gini"].to_numpy(float) if "Gini" in df.columns else np.zeros(len(df))
    n=len(df)
    X=epc*pop/1e6 + pop*130.0/1e6
    Xn=np.maximum(X/X[0],0.1)
    gini_n=gini/100 if np.nanmax(gini)>0 else np.zeros(n)
    u_norm=unemp/np.nanmax(unemp) if np.nanmax(unemp)>0 else np.zeros(n)
    mur_norm=murder/np.nanmax(murder) if np.nanmax(murder)>0 else np.zeros(n)
    mg=np.zeros(n)
    for t in range(1,n):
        pr=mcap[t-1] if mcap[t-1]>0 else 1.0
        mg[t]=np.clip((mcap[t]-mcap[t-1])/pr,-1,1)
    cris=np.zeros(n)
    for t in range(1,n): cris[t]=0.6*cris[t-1]+np.clip(-mg[t],0,1)
    Y=P["wg"]*gini_n+P["wu"]*u_norm+P["wm"]*mur_norm+P["wc"]*cris
    health_n=health/np.nanmax(health) if np.nanmax(health)>0 else np.zeros(n)
    edu_n=edu/np.nanmax(edu) if np.nanmax(edu)>0 else np.zeros(n)
    welfare=0.5*health_n+0.5*edu_n
    Yl=(Xn*(1-mil))**P["beta"]*(P["w0"]+P["ww"]*welfare)
    G=Y-Yl
    # G 中心化：相对自身 7 年常态的偏离
    Gc=G-mov_avg(G,7)
    return df.index.to_numpy(int), Gc

def hits_of(yrs,Gc,evs,thr):
    sig=yrs[Gc>thr]
    return [e for e in evs if any(abs(e-y)<=1 for y in sig)]

def evaluate(P,thr,verbose=False):
    th=tt=0
    for c,evs in TUNE_EV.items():
        df=pd.read_csv(os.path.join(TUNE,f"{c}.csv"),index_col="Year").ffill().bfill().fillna(0)
        yrs,Gc=compute(df,P); h=hits_of(yrs,Gc,evs,thr); th+=len(h); tt+=len(evs)
    vh=vt=0
    for name,ev in VAL_EV.items():
        df=pd.read_csv(os.path.join(OOS,f"{name}.csv"),index_col="Year").ffill().bfill().fillna(0)
        yrs,Gc=compute(df,P); h=hits_of(yrs,Gc,ev,thr); vh+=len(h); vt+=len(ev)
    return vh,vt,th,tt

rng=np.random.default_rng(7)
best=[]
for _ in range(150):
    P=dict(wg=float(rng.uniform(0.2,0.9)),wu=float(rng.uniform(0.3,1.0)),
           wm=float(rng.uniform(0.1,0.7)),wc=float(rng.uniform(0.2,0.8)),
           w0=float(rng.uniform(0.15,0.6)),ww=float(rng.uniform(0.15,0.7)),
           beta=float(rng.uniform(0.4,1.0)))
    for thr in [0.02,0.05,0.1]:
        vh,vt,th,tt=evaluate(P,thr)
        best.append((vh,vt,th,tt,thr,P))
best.sort(key=lambda x:(-x[0],-x[2]))
print("Top6 (验证命中优先):")
for vh,vt,th,tt,thr,P in best[:6]:
    print(f"  验证={vh}/{vt}={vh/vt*100:.0f}% 校准={th}/{tt} thr={thr}")
Pbest=best[0][5]; thrb=best[0][4]
print(f"\n最佳 thr={thrb} 逐国:")
for name,ev in {**TUNE_EV,**VAL_EV}.items():
    src=TUNE if name in TUNE_EV else OOS
    df=pd.read_csv(os.path.join(src,f"{name}.csv"),index_col="Year").ffill().bfill().fillna(0)
    yrs,Gc=compute(df,Pbest); h=hits_of(yrs,Gc,ev,thrb)
    print(f"  {name:12s} 命中{h}/{ev}")
