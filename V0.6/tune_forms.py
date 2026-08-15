# -*- coding: utf-8 -*-
"""多形式调参：美+阿1980-2025，试验多种数学形式，危机命中−误报惩罚 打分"""
import pandas as pd, numpy as np, os, io, sys, itertools
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
TUNE = r"E:\AI-Personal\SECM-Project\V0.6\tune"
CRISIS = {"USA":[1987,2001,2008,2020], "Argentina":[1982,1989,2001,2014,2020]}
def mov_avg(x,w): return pd.Series(x).rolling(w,center=True,min_periods=1).mean().to_numpy()

def run(df, F, P):
    patent=df["Patent"].to_numpy(float); edu=df["EduRate"].to_numpy(float)
    mil=df["Military"].to_numpy(float)/100; unemp=df["unemployment"].to_numpy(float)
    mcap=df["mcap_gdp"].to_numpy(float); X=df["GDP"].to_numpy(float); gini=df["Gini"].to_numpy(float)
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
    # 科技项
    tech=mov_avg(pg,3)*P["wp"]+edu_n*P["we"]
    tech=np.maximum(tech, P["ZtechMin"])
    # 负面项
    neg=P["wu"]*u_norm+P["wc"]*crash+P["wg"]*gini_n
    # Z 计算方式
    if F["zcalc"]=="diff":
        Z=neg-tech
    elif F["zcalc"]=="ratio":
        Z=(neg+0.1)/(tech+0.1)-1.0
    elif F["zcalc"]=="ratio_gini":
        Z=(P["wu"]*u_norm+P["wc"]*crash)/(tech+0.1) - 0.5 - gini_n*0.5
    if F["center"]:
        Z=Z-mov_avg(Z,5)
    Z=np.clip(Z,-1.5,1.5)
    # Z 变换形式
    if F["ztrans"]=="linear": Zeff=Z
    elif F["ztrans"]=="log": Zeff=np.sign(Z)*np.log(1+np.abs(Z))
    elif F["ztrans"]=="pow2": Zeff=np.sign(Z)*((1+np.abs(Z))**2-1)
    elif F["ztrans"]=="powinv": Zeff=np.sign(Z)*(1-1/(1+np.abs(Z)))
    elif F["ztrans"]=="tanh": Zeff=np.tanh(2*Z)
    # 停滞负担
    burden=np.zeros(n)
    for t in range(1,n): burden[t]=burden[t-1]*0.9+max(0.0,P["gThresh"]-gX[t])
    # Ylimit 形式
    if F["ylim"]=="linear":
        Yl=Xn*(1-mil)*(P["w0"]+P["we"]*edu_n)-P["kBurden"]*burden
    else:
        Yl=(Xn**P["beta"])*(1-mil)*(P["w0"]+P["we"]*edu_n)-P["kBurden"]*burden
    # Y 递推形式
    Y=np.zeros(n); Y[0]=P["a1"]*Xn[0]+P["a2"]*u_norm[0]+P["a3"]*(1-edu_n[0]); crisis=0.0
    for t in range(1,n):
        if F["yrec"]=="add_mult":
            Y[t]=Y[t-1]+(dX[t]-P["damage"]*crisis)*P["kY"]*(1+P["ZI"]*Zeff[t])
        elif F["yrec"]=="add_add":
            Y[t]=Y[t-1]+P["kY"]*dX[t]+P["kZ"]*Zeff[t]-(P["damage"]*crisis)
        else:  # mult
            Y[t]=Y[t-1]*(1+P["kY"]*(dX[t]/max(Xn[t-1],0.1)+P["kZ"]*Zeff[t])-P["damage"]*crisis)
        crisis=1.0 if Y[t]>Yl[t] else max(0.0,crisis-0.5)
    return df.index.to_numpy(int), Y-Yl

def score(F,P):
    hits=0; tot=0; fp=0; fp_tot=0
    for c,evs in CRISIS.items():
        df=pd.read_csv(os.path.join(TUNE,f"{c}.csv"),index_col="Year").ffill().bfill().fillna(0)
        yrs,G=run(df,F,P); gy=yrs[G>0]
        for e in evs:
            tot+=1
            if any(abs(e-y)<=1 for y in gy): hits+=1
        for t,y in enumerate(yrs):
            if y not in evs and abs(G[t])>0:  # 非危机年
                fp_tot+=1
                if G[t]>0: fp+=1
    return hits,tot,fp,fp_tot

P=dict(kY=3.0,ZI=1.0,kZ=0.4,w0=0.7,wu=0.7,wc=0.3,wg=0.2,wp=0.3,we=0.4,ZtechMin=0.3,
       Xmin=0.1,a1=0.4,a2=0.3,a3=0.3,damage=0.03,gThresh=0.02,kBurden=0.3,beta=0.6)

forms=[{"zcalc":zc,"ztrans":zt,"yrec":yr,"ylim":yl,"center":ce}
       for zc in ["diff","ratio"] for zt in ["linear","log","pow2","powinv","tanh"]
       for yr in ["add_mult","add_add","mult"] for yl in ["linear","power"] for ce in [True,False]]
print(f"组合数={len(forms)}")
best=[]
for F in forms:
    h,t,fp,fpt=score(F,P)
    # 分数 = 命中率 − 0.7×误报率
    s=(h/t)-0.7*(fp/fpt if fpt>0 else 0)
    best.append((s,h,t,fp,F))
best.sort(key=lambda x:-x[0])
for s,h,t,fp,F in best[:12]:
    print(f"分={s:.3f} 命中={h}/{t} 误报={fp}  {F}")
