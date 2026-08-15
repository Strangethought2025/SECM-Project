# -*- coding: utf-8 -*-
"""最终版：乘法递推+回拉(缩G>0期)，先美阿校准再20国验证"""
import pandas as pd, numpy as np, os, io, sys
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
TUNE = r"E:\AI-Personal\SECM-Project\V0.6\tune"
OOS = r"E:\AI-Personal\SECM-Project\V0.6\oos2000"
EVENTS = {"USA":[2008,2020],"UK":[2008,2020],"Spain":[2008,2012,2020],"Portugal":[2011,2020],
    "Ireland":[2008,2010,2020],"Greece":[2010,2012,2020],"Cyprus":[2013,2020],"Iceland":[2008,2020],
    "Turkey":[2001,2018,2020],"Argentina":[2001,2014,2018,2020],"Brazil":[2015,2020],
    "Mexico":[2008,2020],"Russia":[2008,2015,2020,2022],"Ukraine":[2009,2014,2020,2022],
    "Venezuela":[2013,2016,2020],"Egypt":[2011,2016,2020],"Pakistan":[2008,2019,2022],
    "SriLanka":[2022],"Ghana":[2022],"Lebanon":[2019,2020]}
def mov_avg(x,w): return pd.Series(x).rolling(w,center=True,min_periods=1).mean().to_numpy()

def run(df,P):
    patent=df["Patent"].to_numpy(float); edu=df["EduRate"].to_numpy(float)
    mil=df["Military"].to_numpy(float)/100; unemp=df["unemployment"].to_numpy(float)
    mcap=df["mcap_gdp"].to_numpy(float); X=df["GDP"].to_numpy(float)
    gini=df["Gini"].to_numpy(float) if "Gini" in df.columns else np.zeros(len(df))
    n=len(df)
    Xn=np.maximum(X/X[0],P["Xmin"]); dX=np.diff(Xn,prepend=Xn[0])
    gX=np.diff(X,prepend=X[0])/np.maximum(X,1)
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
    tech=np.maximum(mov_avg(pg,3)*P["wp"]+edu_n*P["we"], P["ZtechMin"])
    neg=P["wu"]*u_norm+P["wc"]*crash+P["wg"]*gini_n
    Z=np.clip(neg-tech,-1.5,1.5)
    Zeff=np.sign(Z)*np.log(1+np.abs(Z))   # log 变换
    burden=np.zeros(n)
    for t in range(1,n): burden[t]=burden[t-1]*0.9+max(0.0,P["gThresh"]-gX[t])
    Yl=Xn*(1-mil)*(P["w0"]+P["we"]*edu_n)-P["kBurden"]*burden
    Y=np.zeros(n); Y[0]=P["a1"]*Xn[0]+P["a2"]*u_norm[0]+P["a3"]*(1-edu_n[0]); crisis=0.0
    for t in range(1,n):
        # 乘法递推（美阿9/9全中的形式）+ 回拉
        Y[t]=Y[t-1]*(1+P["kY"]*(dX[t]/max(Xn[t-1],0.1)+P["kZ"]*Zeff[t])-P["damage"]*crisis)
        Y[t]-=P["revert"]*max(0.0,Y[t]-Yl[t])   # 越线回拉→缩G>0期
        crisis=1.0 if Y[t]>Yl[t] else max(0.0,crisis-0.5)
    return df.index.to_numpy(int), Y-Yl

P=dict(kY=1.0,kZ=1.5,w0=0.7,wu=0.7,wc=0.3,wg=0.2,wp=0.3,we=0.4,ZtechMin=0.3,
       Xmin=0.1,a1=0.4,a2=0.3,a3=0.3,damage=0.03,gThresh=0.02,kBurden=0.3,revert=0.15)

# 校准集：美+阿 1980-2025
TUNE_EV = {"USA":[1987,2001,2008,2020], "Argentina":[1982,1989,2001,2014,2020]}
th=tt=fp=fpt=0
for c,evs in TUNE_EV.items():
    df=pd.read_csv(os.path.join(TUNE,f"{c}.csv"),index_col="Year").ffill().bfill().fillna(0)
    yrs,G=run(df,P); gy=yrs[G>0]
    hits=[e for e in evs if any(abs(e-y)<=1 for y in gy)]
    th+=len(hits); tt+=len(evs)
    for t,y in enumerate(yrs):
        if y not in evs:
            fpt+=1; fp+=1 if G[t]>0 else 0
    print(f"调参集 {c}: 命中{hits}/{evs}  G>0年={np.sum(G>0)}")
print(f"调参集合计: {th}/{tt} 命中, 误报 {fp}/{fpt}\n")

# 验证集：20国 2000-2025
vh=vt=0
for name,ev in EVENTS.items():
    df=pd.read_csv(os.path.join(OOS,f"{name}.csv"),index_col="Year").ffill().bfill().fillna(0)
    yrs,G=run(df,P); gy=yrs[G>0]
    hits=[e for e in ev if any(abs(e-y)<=1 for y in gy)]
    vh+=len(hits); vt+=len(ev)
    print(f"{name:12s} 事件{ev} 命中{hits}  G>0年={np.sum(G>0)}")
print(f"\n验证集: {vh}/{vt} = {vh/vt*100:.0f}%")
