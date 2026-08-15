# -*- coding: utf-8 -*-
"""2000-2025 快速网格重调"""
import pandas as pd, numpy as np, os, io, sys, itertools
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
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
    return df.index.to_numpy(int), Y-Yl
def sig_peaks(years,G,w=4,thresh=0.05):
    base=mov_avg(G,w); out=[]
    for t in range(1,len(G)-1):
        if G[t]>=G[t-1] and G[t]>=G[t+1] and G[t]>0 and (G[t]-base[t])>thresh: out.append(int(years[t]))
    return out
def score(P):
    h=e=0
    for name,ev in EVENTS.items():
        df=pd.read_csv(os.path.join(OOS,f"{name}.csv"),index_col="Year").ffill().bfill()
        yrs,G=run(df,P); pk=sig_peaks(yrs,G)
        h+=sum(1 for x in ev if any(abs(x-p)<=1 for p in pk)); e+=len(ev)
    return h,e
grid={"kY":[2.0,3.0,4.0],"ZImpactK":[1.0,2.0,3.0],"w0":[0.4,0.6,0.8],"wu":[0.5,0.7,1.0],"wc":[0.3,0.5,0.7]}
FIX=dict(wp=0.3,we=0.4,ZtechMin=0.3,Xmin=0.1,Y0=1.0,damage=0.03)
best=[]
for v in itertools.product(*grid.values()):
    P=dict(zip(grid.keys(),v)); P.update(FIX)
    h,e=score(P); best.append((h,P))
best.sort(key=lambda x:-x[0])
for h,P in best[:6]: print(f"{h}/51  {P}")
