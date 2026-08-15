# -*- coding: utf-8 -*-
"""2000-2025 扩展验证：20国，加宽事件清单(违约/IMF/银行/新冠/经济调整)"""
import pandas as pd, numpy as np, os, io, sys
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
OOS = r"E:\AI-Personal\SECM-Project\V0.6\oos2000"

# 加宽事件：主权违约/IMF/银行危机/新冠/经济大调整（2000-2025）
EVENTS = {
    "USA":[2008,2020],"UK":[2008,2020],"Spain":[2008,2012,2020],"Portugal":[2011,2020],
    "Ireland":[2008,2010,2020],"Greece":[2010,2012,2020],"Cyprus":[2013,2020],"Iceland":[2008,2020],
    "Turkey":[2001,2018,2020],"Argentina":[2001,2014,2018,2020],"Brazil":[2015,2020],
    "Mexico":[2008,2020],"Russia":[2008,2015,2020,2022],"Ukraine":[2009,2014,2020,2022],
    "Venezuela":[2013,2016,2020],"Egypt":[2011,2016,2020],"Pakistan":[2008,2019,2022],
    "SriLanka":[2022],"Ghana":[2022],"Lebanon":[2019,2020],
}
def mov_avg(x,w): return pd.Series(x).rolling(w,center=True,min_periods=1).mean().to_numpy()

def run(df, P):
    patent=df["Patent"].to_numpy(float); edu=df["EduRate"].to_numpy(float)
    mil=df["Military"].to_numpy(float)/100; unemp=df["unemployment"].to_numpy(float)
    mcap=df["mcap_gdp"].to_numpy(float); X=df["GDP"].to_numpy(float)
    Xn=X/X[0]; Xn=np.maximum(Xn,P["Xmin"]); dX=np.diff(Xn,prepend=Xn[0])
    pg=np.zeros(len(df))
    for t in range(1,len(df)):
        pr=patent[t-1] if patent[t-1]>0 else 1.0
        pg[t]=np.clip((patent[t]-patent[t-1])/pr,-1,1)
    edu_n=edu/np.nanmax(edu) if np.nanmax(edu)>0 else np.zeros(len(df))
    Ztech=np.maximum(P["wp"]*mov_avg(pg,3)+P["we"]*edu_n, P["ZtechMin"])
    u_norm=unemp/np.nanmax(unemp) if np.nanmax(unemp)>0 else np.zeros(len(df))
    mg=np.zeros(len(df))
    for t in range(1,len(df)):
        pr=mcap[t-1] if mcap[t-1]>0 else 1.0
        mg[t]=np.clip((mcap[t]-mcap[t-1])/pr,-1,1)
    Zneg=P["wu"]*u_norm+P["wc"]*np.clip(-mg,0,1)
    Z=np.clip(Zneg-Ztech,-1,1)
    Yl=(Xn-mil*Xn)*(P["w0"]+P["we"]*edu_n)
    Y=np.zeros(len(df)); Y[0]=P["Y0"]; crisis=0.0
    for t in range(1,len(df)):
        dXc=dX[t]-P["damage"]*crisis
        Y[t]=Y[t-1]+dXc*P["kY"]*(1+P["ZImpactK"]*Z[t])
        crisis=1.0 if Y[t]>Yl[t] else max(0.0,crisis-0.5)
    return df.index.to_numpy(int), Y-Yl

def sig_peaks(years,G,w=4,thresh=0.06):
    base=mov_avg(G,w); out=[]
    for t in range(1,len(G)-1):
        if G[t]>=G[t-1] and G[t]>=G[t+1] and G[t]>0 and (G[t]-base[t])>thresh: out.append(int(years[t]))
    return out

P = dict(kY=3.0,ZImpactK=2.0,w0=0.6,wu=0.7,wc=0.4,wp=0.3,we=0.4,ZtechMin=0.3,Xmin=0.1,Y0=1.0,damage=0.03)

tot_hit=tot_ev=0; detail=[]
for name,ev in EVENTS.items():
    df=pd.read_csv(os.path.join(OOS,f"{name}.csv"),index_col="Year").ffill().bfill().fillna(0)
    yrs,G=run(df,P); pk=sig_peaks(yrs,G)
    hits=[e for e in ev if any(abs(e-p)<=1 for p in pk)]
    tot_hit+=len(hits); tot_ev+=len(ev)
    detail.append((name,ev,hits,pk))
    print(f"{name:12s} 事件{ev} 命中{hits}")
print(f"\n总计: {tot_hit}/{tot_ev} = {tot_hit/tot_ev*100:.0f}%")
# 去掉新冠2020再看一次
tot2=0; ev2=0
for name,ev,hits,pk in detail:
    e2=[x for x in ev if x!=2020]; h2=[x for x in hits if x!=2020]
    ev2+=len(e2); tot2+=len(h2)
print(f"去掉新冠2020后: {tot2}/{ev2} = {tot2/ev2*100:.0f}%")
