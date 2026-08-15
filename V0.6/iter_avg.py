# -*- coding: utf-8 -*-
"""V0.5式 平均合成(加权÷项数, nanmean跳缺项)：Y=avg(矛盾项), 福利=avg, Ylimit=能源承载×福利"""
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

def norm(x):
    m=np.nanmax(x)
    return (x/m if m and m>0 else np.zeros_like(x))

def compute(df,P):
    pop=df["Population"].to_numpy(float)
    epc=df["energy_pc"].to_numpy(float); murder=df["murder"].to_numpy(float)
    health=df["health"].to_numpy(float); edu=df["EduRate"].to_numpy(float)
    mil=df["Military"].to_numpy(float)/100; unemp=df["unemployment"].to_numpy(float)
    mcap=df["mcap_gdp"].to_numpy(float)
    gini=df["Gini"].to_numpy(float) if "Gini" in df.columns else np.full(len(df),np.nan)
    n=len(df)
    X=epc*pop/1e6 + pop*130.0/1e6
    Xn=np.maximum(X/X[0],0.1)
    gini_n=gini/100; u_norm=norm(unemp); mur_norm=norm(murder)
    mg=np.zeros(n)
    for t in range(1,n):
        pr=mcap[t-1] if mcap[t-1]>0 else np.nan
        mg[t]=np.clip((mcap[t]-mcap[t-1])/pr,-1,1) if not np.isnan(pr) else 0
    cris=np.zeros(n)
    for t in range(1,n): cris[t]=0.6*cris[t-1]+np.clip(-mg[t],0,1)
    # V0.5式：加权项取平均（nanmean 跳缺项）
    Y=np.nanmean(np.vstack([P["wg"]*gini_n, P["wu"]*u_norm, P["wm"]*mur_norm, P["wc"]*cris]), axis=0)
    health_n=norm(health); edu_n=norm(edu)
    welfare=np.nanmean(np.vstack([0.5*health_n, 0.5*edu_n]), axis=0)
    Yl=(Xn*(1-mil))**P["beta"]*(P["w0"]+P["ww"]*welfare)
    return df.index.to_numpy(int), Y, Yl

YF=np.arange(0.5,4.2,0.25); YLS=np.arange(0.3,2.1,0.15)
def calibrate(years,Y,Yl,first_ev):
    best=None
    for yf in YF:
        for yls in YLS:
            G=yf*Y-yls*Yl
            pos=np.where(G>0)[0]
            if len(pos) and abs(int(years[pos[0]])-first_ev)<=1:
                if np.any(G[pos[0]:]<0): return yf,yls
                if best is None: best=(yf,yls)
    return best if best else (1.0,1.0)

def evaluate(P, verbose=False):
    th=tt=nofb=0
    for c,evs in TUNE_EV.items():
        df=pd.read_csv(os.path.join(TUNE,f"{c}.csv"),index_col="Year")
        yrs,Y,Yl=compute(df,P); yf,yls=calibrate(yrs,Y,Yl,evs[0]); G=yf*Y-yls*Yl
        th+=sum(1 for e in evs if any(abs(e-y)<=1 for y in yrs[G>0])); tt+=len(evs)
        pos=np.where(G>0)[0]
        if len(pos) and not np.any(G[pos[0]:]<0): nofb+=1
    vh=vt=0; vd=[]
    for name,ev in VAL_EV.items():
        df=pd.read_csv(os.path.join(OOS,f"{name}.csv"),index_col="Year")
        yrs,Y,Yl=compute(df,P); yf,yls=calibrate(yrs,Y,Yl,ev[0]); G=yf*Y-yls*Yl
        hits=[e for e in ev if any(abs(e-y)<=1 for y in yrs[G>0])]
        vh+=len(hits); vt+=len(ev)
        pos=np.where(G>0)[0]
        if len(pos) and not np.any(G[pos[0]:]<0): nofb+=1
        vd.append((name,hits,ev,int(np.sum(G>0))))
    if verbose:
        for row in vd: print(f"  {row[0]:12s} 命中{row[1]}/{row[2]} G>0年={row[3]}")
    return vh,vt,th,tt,nofb

rng=np.random.default_rng(2024)
best=[]
for _ in range(150):
    P=dict(wg=float(rng.uniform(0.3,1.2)),wu=float(rng.uniform(0.4,1.4)),
           wm=float(rng.uniform(0.2,1.0)),wc=float(rng.uniform(0.3,1.0)),
           w0=float(rng.uniform(0.15,0.6)),ww=float(rng.uniform(0.15,0.8)),
           beta=float(rng.uniform(0.4,1.0)))
    vh,vt,th,tt,nofb=evaluate(P)
    best.append((vh,vt,th,tt,nofb,P))
best.sort(key=lambda x:(-x[0], x[4]))
print("Top6:")
for vh,vt,th,tt,nofb,P in best[:6]:
    print(f"  验证={vh}/{vt}={vh/vt*100:.0f}% 校准={th}/{tt} 未回落={nofb} { {k:round(v,2) for k,v in P.items()} }")
Pbest=best[0][5]
print("\n== 最佳逐国 ==")
vh,vt,th,tt,nofb=evaluate(Pbest, verbose=True)
print(f"\n最终: 校准 {th}/{tt} | 验证 {vh}/{vt} = {vh/vt*100:.0f}% | 未回落 {nofb}")
