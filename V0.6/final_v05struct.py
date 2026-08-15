# -*- coding: utf-8 -*-
"""V0.5 结构还原：Y_base水平项(随X同速)+累加器(短期)+Ylimit含Ω韧性 —— 美阿校准→20国验证"""
import pandas as pd, numpy as np, os, io, sys, itertools
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
TUNE = r"E:\AI-Personal\SECM-Project\V0.6\tune"
OOS = r"E:\AI-Personal\SECM-Project\V0.6\oos2000"
EVENTS = {"USA":[2008,2020],"UK":[2008,2020],"Spain":[2008,2012,2020],"Portugal":[2011,2020],
    "Ireland":[2008,2010,2020],"Greece":[2010,2012,2020],"Cyprus":[2013,2020],"Iceland":[2008,2020],
    "Turkey":[2001,2018,2020],"Argentina":[2001,2014,2018,2020],"Brazil":[2015,2020],
    "Mexico":[2008,2020],"Russia":[2008,2015,2020,2022],"Ukraine":[2009,2014,2020,2022],
    "Venezuela":[2013,2016,2020],"Egypt":[2011,2016,2020],"Pakistan":[2008,2019,2022],
    "SriLanka":[2022],"Ghana":[2022],"Lebanon":[2019,2020]}
TUNE_EV = {"USA":[1987,2001,2008,2020], "Argentina":[1982,1989,2001,2014,2020]}
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
    # Zc（V0.5 复杂度矛盾指数）：Gini+失业+股崩（凶杀/贫困/信任数据暂缺，可用时补）
    Zc=np.clip(P["wg"]*gini_n+P["wu"]*u_norm+P["wc"]*crash, 0, 1.5)
    # 科技红利（V0.5 X_bonus 的简化）
    bonus=np.maximum(P["wp"]*mov_avg(pg,3)+P["we"]*edu_n, P["ZtechMin"])
    # Z = γS·Zc − γX·bonus
    Z=np.clip(P["gS"]*Zc-P["gX"]*bonus,-1.5,1.5)
    Zeff=np.sign(Z)*((1+np.abs(Z))**2-1)   # V0.5 平方放大保符号
    # Ω 韧性（V0.5）：用失业+股崩代理（储蓄/债务/LPI 可补）
    Omega=np.clip(P["wO"]*u_norm+P["wM"]*crash, 0, 2)
    # PopPressure（土地，缺耕地数据则=0）
    popP=0.0
    # Y_base（V0.5 水平项：随 X 同速）
    Y_base=P["a0"]+P["a1"]*Xn+P["b1"]*gini_n+P["mu"]*np.log(1+X)
    # Y 递推（V0.5）：Y[0]=Y_base[0]，之后累加 ΔX·kY·(1+ZI·Zeff)·(1+popP)
    Y=np.zeros(n); Y[0]=Y_base[0]
    for t in range(1,n):
        Y[t]=Y[t-1]+dX[t]*P["kY"]*(1+P["ZI"]*Zeff[t])*(1+popP)
    # Ylimit（V0.5）：Xn·(1−mil)·kLimit·(1+|Ω|) − 负担
    Yl=Xn*(1-mil)*P["kLimit"]*(1+Omega)
    return df.index.to_numpy(int), Y-Yl

def score(df,evs,P):
    yrs,G=run(df,P); gy=yrs[G>0]
    hits=sum(1 for e in evs if any(abs(e-y)<=1 for y in gy))
    fp=sum(1 for t,y in enumerate(yrs) if y not in evs and G[t]>0)
    fpt=sum(1 for y in yrs if y not in evs)
    return hits,len(evs),fp,fpt

# 快速扫描关键参数（美阿调参集）
best=[]
for kY in [1.0,1.5,2.0]:
  for kLimit in [1.0,1.4,1.8]:
    for a1 in [0.3,0.5,0.7]:
      P=dict(kY=kY,kLimit=kLimit,a0=0.2,a1=a1,b1=0.5,mu=0.3,wg=0.5,wu=0.6,wc=0.4,
             wp=0.3,we=0.4,ZtechMin=0.3,gS=1.0,gX=1.0,wO=0.5,wM=0.3,Xmin=0.1,ZI=1.0)
      th=tt=fp=fpt=0
      for c,evs in TUNE_EV.items():
        df=pd.read_csv(os.path.join(TUNE,f"{c}.csv"),index_col="Year").ffill().bfill().fillna(0)
        h,t,f,ft=score(df,evs,P); th+=h; tt+=t; fp+=f; fpt+=ft
      s=(th/tt)-0.6*(fp/fpt if fpt else 0)
      best.append((s,th,tt,fp,P))
best.sort(key=lambda x:-x[0])
print("美阿调参集 Top5:")
for s,h,t,fp,P in best[:5]:
    print(f"  分={s:.3f} 命中={h}/{t} 误报={fp}  kY={P['kY']} kLimit={P['kLimit']} a1={P['a1']}")
Pbest=best[0][4]
print("\n== 20国验证（最佳参数） ==")
vh=vt=0
for name,ev in EVENTS.items():
    df=pd.read_csv(os.path.join(OOS,f"{name}.csv"),index_col="Year").ffill().bfill().fillna(0)
    h,t,_,_=score(df,ev,Pbest); vh+=h; vt+=t
    print(f"  {name:12s} 命中{h}/{t}")
print(f"\n验证集: {vh}/{vt} = {vh/vt*100:.0f}%")
