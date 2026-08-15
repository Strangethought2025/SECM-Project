# -*- coding: utf-8 -*-
"""网格搜索：正确结构下搜最优参数组合（设计哲学不变，系数放开）"""
import pandas as pd, numpy as np, os, io, sys, itertools
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
BASE = r"E:\AI-Personal\SECM-Project\Data\DATAsource\1980_2020 Source"
WB = r"E:\AI-Personal\SECM-Project\V0.6"
OOS = r"E:\AI-Personal\SECM-Project\V0.6\oos"
CRISIS = {"USA":[1988,2007],"Japan":[1997],"Argentina":[1980,1982,1989,1995,2001],"Greece":[2008,2012],
          "SouthKorea":[1997],"Mexico":[1982,1994],"Turkey":[2000,2001],"Indonesia":[1997],
          "Thailand":[1997],"Brazil":[1983,1990,1994],"Chile":[1982],"Russia":[1998],
          "India":[1991],"SouthAfrica":[]}
def mov_avg(x,w): return pd.Series(x).rolling(w,center=True,min_periods=1).mean().to_numpy()

def load(name):
    if name in ("USA","Japan","Argentina","Greece"):
        df=pd.read_excel(os.path.join(BASE,f"SECM_V24_{name}.xlsx"),sheet_name=0).ffill()
        wb=pd.read_csv(os.path.join(WB,f"wb_{name}.csv"),index_col="Year")
        df=df.join(wb,on="Year",how="left").ffill().bfill()
        df["GDP"]=df["gdp_percap"]*df["Population"]
        df=df.rename(columns={"PatentCount":"Patent","MilitaryRatio":"Military","ArableLandTotal":"Arable"})
        years=df["Year"].to_numpy(int)
    else:
        df=pd.read_csv(os.path.join(OOS,f"{name}.csv"),index_col="Year").ffill().bfill()
        df=df.rename(columns={"Military":"Mpct"}); df["Military"]=df["Mpct"]/100
        years=df.index.to_numpy(int)
    return df, years

def run(df, P):
    pop=df["Population"].to_numpy(float); patent=df["Patent"].to_numpy(float)
    edu=df["EduRate"].to_numpy(float); gini=df["Gini"].to_numpy(float)
    mil=df["Military"].to_numpy(float); unemp=df["unemployment"].to_numpy(float)
    mcap=df["mcap_gdp"].to_numpy(float); arable=df["Arable"].to_numpy(float)
    X=df["GDP"].to_numpy(float); Xn=X/X[0]; Xn=np.maximum(Xn,P["Xmin"]); dX=np.diff(Xn,prepend=Xn[0])
    pg=np.zeros(len(df))
    for t in range(1,len(df)):
        pr=patent[t-1] if patent[t-1]>0 else 1.0
        pg[t]=np.clip((patent[t]-patent[t-1])/pr,-1,1)
    edu_n=edu/np.nanmax(edu) if np.nanmax(edu)>0 else edu
    Ztech=np.maximum(P["wp"]*mov_avg(pg,3)+P["we"]*edu_n, P["ZtechMin"])
    u_norm=unemp/np.nanmax(unemp); mg=np.zeros(len(df))
    for t in range(1,len(df)):
        pr=mcap[t-1] if mcap[t-1]>0 else 1.0
        mg[t]=np.clip((mcap[t]-mcap[t-1])/pr,-1,1)
    Zneg=P["wu"]*u_norm+P["wg"]*(gini/100)+P["wc"]*np.clip(-mg,0,1)
    Z=np.clip(Zneg-Ztech,-1,1)
    popP=np.zeros(len(df))
    if np.nanmax(arable)>0: popP=np.clip((pop/arable)/np.nanmedian(pop/arable)-1,0,3)
    welfare=P["we"]*edu_n
    Yl=(Xn-mil*Xn)*(P["w0"]+welfare)
    Y=np.zeros(len(df)); Y[0]=P["Y0"]; crisis=0.0
    for t in range(1,len(df)):
        dXc=dX[t]-P["damage"]*crisis
        Y[t]=Y[t-1]+dXc*P["kY"]*(1+P["ZImpactK"]*Z[t])*(1+popP[t])
        crisis=1.0 if Y[t]>Yl[t] else max(0.0,crisis-0.5)
    return Y-Yl

def sig_peaks(years,G,w=5,thresh=0.06):
    base=mov_avg(G,w); out=[]
    for t in range(1,len(G)-1):
        if G[t]>=G[t-1] and G[t]>=G[t+1] and G[t]>0 and (G[t]-base[t])>thresh: out.append(int(years[t]))
    return out

def score(P):
    tot_hit=tot_ev=0
    for name,ev in CRISIS.items():
        df,years=load(name); G=run(df,P); pk=sig_peaks(years,G)
        tot_hit+=sum(1 for e in ev if any(abs(e-p)<=1 for p in pk)); tot_ev+=len(ev)
    return tot_hit,tot_ev

grid = {"kY":[1.5,2.0,3.0],"ZImpactK":[0.5,1.0,2.0],"w0":[0.4,0.6,0.8],"wu":[0.3,0.5,0.7],
        "wc":[0.2,0.4,0.6],"damage":[0.03,0.08,0.15]}
FIX = dict(wg=0.3,wp=0.3,we=0.4,ZtechMin=0.3,Xmin=0.1,Y0=1.0)
best=[]
for vals in itertools.product(*grid.values()):
    P=dict(zip(grid.keys(),vals)); P.update(FIX)
    h,e=score(P); best.append((h,P))
best.sort(key=lambda x:-x[0])
print(f"最优命中: {best[0][0]}/{best[1][0] if len(best)>1 else 0} (总事件23)")
for h,P in best[:8]:
    print(f"  {h}/23  {P}")
