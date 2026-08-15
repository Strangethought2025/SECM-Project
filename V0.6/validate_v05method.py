# -*- coding: utf-8 -*-
"""V0.5 方法论：全局参数冻结，逐国只校准 YFirst(初始Y) 对齐第一个事件，其余为预测"""
import pandas as pd, numpy as np, os, io, sys
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
OOS = r"E:\AI-Personal\SECM-Project\V0.6\oos2000"
EVENTS = {"USA":[2008,2020],"UK":[2008,2020],"Spain":[2008,2012,2020],"Portugal":[2011,2020],
    "Ireland":[2008,2010,2020],"Greece":[2010,2012,2020],"Cyprus":[2013,2020],"Iceland":[2008,2020],
    "Turkey":[2001,2018,2020],"Argentina":[2001,2014,2018,2020],"Brazil":[2015,2020],
    "Mexico":[2008,2020],"Russia":[2008,2015,2020,2022],"Ukraine":[2009,2014,2020,2022],
    "Venezuela":[2013,2016,2020],"Egypt":[2011,2016,2020],"Pakistan":[2008,2019,2022],
    "SriLanka":[2022],"Ghana":[2022],"Lebanon":[2019,2020]}
def mov_avg(x,w): return pd.Series(x).rolling(w,center=True,min_periods=1).mean().to_numpy()

def compute(df, P, Yfirst):
    patent=df["Patent"].to_numpy(float); edu=df["EduRate"].to_numpy(float)
    mil=df["Military"].to_numpy(float)/100; unemp=df["unemployment"].to_numpy(float)
    mcap=df["mcap_gdp"].to_numpy(float); X=df["GDP"].to_numpy(float)
    Xn=np.maximum(X/X[0],P["Xmin"]); dX=np.diff(Xn,prepend=Xn[0])
    gX=np.diff(X,prepend=X[0])/np.maximum(X,1)
    pg=np.zeros(len(df))
    for t in range(1,len(df)):
        pr=patent[t-1] if patent[t-1]>0 else 1.0
        pg[t]=np.clip((patent[t]-patent[t-1])/pr,-1,1)
    edu_n=edu/np.nanmax(edu) if np.nanmax(edu)>0 else np.zeros(len(df))
    Ztech=np.maximum(P["wp"]*mov_avg(pg,3)+P["we"]*edu_n,P["ZtechMin"])
    u_norm=unemp/np.nanmax(unemp) if np.nanmax(unemp)>0 else np.zeros(len(df))
    mg=np.zeros(len(df))
    for t in range(1,len(df)):
        pr=mcap[t-1] if mcap[t-1]>0 else 1.0
        mg[t]=np.clip((mcap[t]-mcap[t-1])/pr,-1,1)
    Z=np.clip(P["wu"]*u_norm+P["wc"]*np.clip(-mg,0,1)-Ztech,-1,1)
    Z=Z-mov_avg(Z,5)
    Zeff=np.sign(Z)*((1+np.abs(Z))**P["ZExp"]-1)
    burden=np.zeros(len(df))
    for t in range(1,len(df)): burden[t]=burden[t-1]*0.9+max(0.0,P["gThresh"]-gX[t])
    Yl=(Xn-mil*Xn)*(P["w0"]+P["we"]*edu_n)-P["kBurden"]*burden
    Y=np.zeros(len(df)); Y[0]=Yfirst; crisis=0.0
    for t in range(1,len(df)):
        Y[t]=Y[t-1]+(dX[t]-P["damage"]*crisis)*P["kY"]*(1+P["ZImpactK"]*Zeff[t])
        crisis=1.0 if Y[t]>Yl[t] else max(0.0,crisis-0.5)
    return df.index.to_numpy(int), Y-Yl

# 冻结的全局参数（按0.5方法论：美国调好即锁）
P=dict(kY=3.0,ZImpactK=1.0,w0=0.7,wu=0.7,wc=0.3,wp=0.3,we=0.4,ZtechMin=0.3,Xmin=0.1,
       damage=0.03,gThresh=0.02,kBurden=0.3,ZExp=2.0)

tot_hit=tot_ev=0
for name,ev in EVENTS.items():
    df=pd.read_csv(os.path.join(OOS,f"{name}.csv"),index_col="Year").ffill().bfill().fillna(0)
    yrs=df.index.to_numpy(int)
    first=ev[0]
    # 逐国校准 YFirst：扫描使"第一个事件年 G 首次转正"
    best_yf=None; best_G=None
    for yf in np.arange(0.2, 2.5, 0.05):
        _,G=compute(df,P,yf)
        # 找 G 首次>0 的年份
        pos=np.where(G>0)[0]
        first_pos = int(yrs[pos[0]]) if len(pos) else None
        if first_pos is not None and abs(first_pos-first)<=1:
            best_yf=yf; best_G=G; break
    if best_yf is None:
        # 退而求其次：取使第一个事件年 G>0 的 yf
        for yf in np.arange(0.2, 2.5, 0.05):
            _,G=compute(df,P,yf)
            i=np.where(yrs==first)[0]
            if len(i) and G[i[0]]>0: best_yf=yf; best_G=G; break
    if best_yf is None:
        best_yf=0.5; _,best_G=compute(df,P,best_yf)
    G=best_G
    hits=[e for e in ev if any(abs(e-y)<=1 for y in yrs[G>0])]
    tot_hit+=len(hits); tot_ev+=len(ev)
    print(f"{name:12s} YFirst={best_yf:.2f} 事件{ev} 命中{hits}  G>0年={np.sum(G>0)}")
print(f"\n总计: {tot_hit}/{tot_ev} = {tot_hit/tot_ev*100:.0f}%")
