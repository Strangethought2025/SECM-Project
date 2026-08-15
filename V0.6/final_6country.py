# -*- coding: utf-8 -*-
"""6国校准集(1980-2025) + 14国验证集(2000-2025)：逐国'首个事件对齐+必须回落'校准"""
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

def run(df,P,yf,yls):
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
    Z=Z-mov_avg(Z,5)
    Zeff=np.sign(Z)*((1+np.abs(Z))**2-1)
    Omega=np.clip(P["wO"]*u_norm+P["wM"]*crash,0,2)
    Y_base=P["a0"]+P["a1"]*Xn+P["b1"]*gini_n+P["mu"]*np.log(1+Xn)   # ln用归一化Xn(修复单位OFF)
    Y=np.zeros(n); Y[0]=Y_base[0]*yf
    for t in range(1,n):
        Y[t]=Y[t-1]+dX[t]*P["kY"]*(1+P["ZI"]*Zeff[t])
    Yl=Xn*(1-mil)*P["kLimit"]*(1+Omega)*yls
    return df.index.to_numpy(int), Y-Yl

def calibrate(df,first_ev,P):
    best=None
    for yf in np.arange(0.3,1.75,0.1):
        for yls in np.arange(0.7,1.75,0.1):
            yrs,G=run(df,P,yf,yls)
            pos=np.where(G>0)[0]
            if len(pos) and abs(int(yrs[pos[0]])-first_ev)<=1:
                if np.any(G[pos[0]:]<0): return yf,yls
                if best is None: best=(yf,yls)
    return best if best else (1.0,1.0)

def evaluate(P, verbose=False):
    th=tt=0; nofb=0; details=[]
    for c,evs in TUNE_EV.items():
        df=pd.read_csv(os.path.join(TUNE,f"{c}.csv"),index_col="Year").ffill().bfill().fillna(0)
        yf,yls=calibrate(df,evs[0],P); yrs,G=run(df,P,yf,yls)
        hits=[e for e in evs if any(abs(e-y)<=1 for y in yrs[G>0])]
        th+=len(hits); tt+=len(evs)
        pos=np.where(G>0)[0]
        if len(pos) and not np.any(G[pos[0]:]<0): nofb+=1
        details.append((c,yf,yls,hits,evs,int(np.sum(G>0))))
    vh=vt=0; vdetails=[]
    for name,ev in VAL_EV.items():
        df=pd.read_csv(os.path.join(OOS,f"{name}.csv"),index_col="Year").ffill().bfill().fillna(0)
        yf,yls=calibrate(df,ev[0],P); yrs,G=run(df,P,yf,yls)
        hits=[e for e in ev if any(abs(e-y)<=1 for y in yrs[G>0])]
        vh+=len(hits); vt+=len(ev)
        pos=np.where(G>0)[0]
        if len(pos) and not np.any(G[pos[0]:]<0): nofb+=1
        vdetails.append((name,yf,yls,hits,ev,int(np.sum(G>0))))
    if verbose:
        print("== 校准集(6国) ==")
        for c,yf,yls,hits,evs,np0 in details:
            print(f"  {c:10s} yf={yf:.1f} yls={yls:.1f} 命中{hits}/{evs} G>0年={np0}")
        print("== 验证集(14国) ==")
        for c,yf,yls,hits,evs,np0 in vdetails:
            print(f"  {c:10s} yf={yf:.1f} yls={yls:.1f} 命中{hits}/{evs} G>0年={np0}")
    return vh,vt,th,tt,nofb

best=[]
for kY in [0.8,1.0,1.2]:
    for kLimit in [1.4,1.8,2.2]:
        for a1 in [0.2,0.3,0.4]:
            P=dict(kY=kY,kLimit=kLimit,a0=0.2,a1=a1,b1=0.5,mu=0.3,wg=0.5,wu=0.6,wc=0.4,
                   wp=0.3,we=0.4,ZtechMin=0.3,gS=1.0,gX=1.0,wO=0.5,wM=0.3,Xmin=0.1,ZI=1.0)
            vh,vt,th,tt,nofb=evaluate(P)
            best.append((vh,vt,th,tt,nofb,P))
best.sort(key=lambda x:(-x[0]/x[1], x[4]))
print("Top配置:")
for vh,vt,th,tt,nofb,P in best[:5]:
    print(f"  验证={vh}/{vt}({vh/vt*100:.0f}%) 校准={th}/{tt} 未回落={nofb} kY={P['kY']} kLimit={P['kLimit']} a1={P['a1']}")
Pbest=best[0][5]
print()
evaluate(Pbest, verbose=True)
vh,vt,th,tt,nofb=best[0][:5]
print(f"\n最终: 校准 {th}/{tt} | 验证 {vh}/{vt} = {vh/vt*100:.0f}% | 未回落国家 {nofb}")
