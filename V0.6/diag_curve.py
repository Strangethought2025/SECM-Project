# -*- coding: utf-8 -*-
"""看曲线形态: USA/UK/Portugal 的 Y/Yl/G 每5年"""
import pandas as pd, numpy as np, os, io, sys, json
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
HERE = os.path.dirname(os.path.abspath(__file__))
P = json.load(open(os.path.join(HERE,"best_params.json"),encoding="utf-8"))
def mov_avg(x,w): return pd.Series(x).rolling(w,center=True,min_periods=1).mean().to_numpy()
def norm(x):
    x=np.asarray(x,float)
    if not np.any(~np.isnan(x)): return np.zeros_like(x)
    m=np.nanmax(x)
    return (x/m if m and m>0 else np.zeros_like(x))
def compute(df,P):
    pop=df["Population"].to_numpy(float); epc=df["energy_pc"].to_numpy(float)
    murder=df["murder"].to_numpy(float); health=df["health"].to_numpy(float)
    edu=df["EduRate"].to_numpy(float)
    mil=np.nan_to_num(df["Military"].to_numpy(float)/100, nan=0.0)
    unemp=df["unemployment"].to_numpy(float); mcap=df["mcap_gdp"].to_numpy(float)
    gini=df["Gini"].to_numpy(float) if "Gini" in df.columns else np.full(len(df),np.nan)
    patent=df["Patent"].to_numpy(float)
    debt=df["debt_gdp"].to_numpy(float) if "debt_gdp" in df.columns else np.full(len(df),np.nan)
    credit=df["credit_gdp"].to_numpy(float) if "credit_gdp" in df.columns else np.full(len(df),np.nan)
    npl=df["npl"].to_numpy(float) if "npl" in df.columns else np.full(len(df),np.nan)
    gov_exp=df["gov_exp"].to_numpy(float) if "gov_exp" in df.columns else np.full(len(df),np.nan)
    n=len(df)
    X=epc*pop/1e6 + pop*130.0/1e6
    Xn=np.maximum(X/X[0],0.1); dX=np.diff(Xn,prepend=Xn[0])
    gini_n=gini/100; u_norm=norm(unemp); mur_norm=norm(murder)
    mg=np.zeros(n)
    for t in range(1,n):
        pr=mcap[t-1] if mcap[t-1]>0 else np.nan
        mg[t]=np.clip((mcap[t]-mcap[t-1])/pr,-1,1) if not np.isnan(pr) else 0
    cris=np.zeros(n)
    for t in range(1,n): cris[t]=0.6*cris[t-1]+np.clip(-mg[t],0,1)
    cg=np.zeros(n)
    for t in range(1,n):
        pr=credit[t-1] if credit[t-1]>0 else np.nan
        cg[t]=np.clip((credit[t]-credit[t-1])/pr,-1,1) if not np.isnan(pr) else 0
    ccris=np.zeros(n)
    for t in range(1,n): ccris[t]=0.6*ccris[t-1]+np.clip(-cg[t],0,1)
    pg=np.zeros(n)
    for t in range(1,n):
        pr=patent[t-1] if patent[t-1]>0 else np.nan
        pg[t]=np.clip((patent[t]-patent[t-1])/pr,-1,1) if not np.isnan(pr) else 0
    edu_n=norm(edu); npl_n=norm(npl); ge_n=norm(gov_exp)
    Zc=np.nanmean(np.vstack([P["wg"]*gini_n,P["wu"]*u_norm,P["wm"]*mur_norm,
                             P["wc"]*cris,P["wcr"]*ccris,P["wnp"]*npl_n,P["wge"]*ge_n]),axis=0)
    bonus=np.maximum(np.nanmean(np.vstack([P["wp"]*mov_avg(pg,3),P["we"]*edu_n]),axis=0),P["ZtechMin"])
    Z=Zc-P["gX"]*bonus; Z=Z-mov_avg(Z,5)
    Zeff=np.sign(Z)*((1+np.abs(Z))**2-1)
    health_n=norm(health)
    welfare=np.nanmean(np.vstack([0.5*health_n,0.5*edu_n]),axis=0)
    debt_n=norm(debt)
    Yl=(Xn*(1-mil))**P["beta"]*(P["w0"]+P["ww"]*welfare)/(1+P["wd"]*debt_n)
    Y_base=P["a0"]+P["a1"]*Xn+P["mu"]*np.log(1+Xn)
    Y=np.zeros(n); Y[0]=Y_base[0]
    for t in range(1,n):
        Y[t]=Y[t-1]+dX[t]*P["kY"]*(1+P["ZI"]*Zeff[t])+P["kZ"]*Zeff[t]
    return df.index.to_numpy(int),Y,Yl
for folder,name in [(os.path.join(HERE,"tune"),"USA"),(os.path.join(HERE,"oos2000"),"UK"),
                   (os.path.join(HERE,"oos2000"),"Portugal")]:
    df=pd.read_csv(os.path.join(folder,f"{name}.csv"),index_col="Year").ffill().bfill()
    yrs,Y,Yl=compute(df,P)
    G=Y-Yl
    print(f"\n== {name} ==")
    for i,y in enumerate(yrs):
        if y%5==0 or G[i]>0.3:
            bar="#"*min(int(max(G[i],0)*30),60)
            print(f"  {y}: Y={Y[i]:.2f} Yl={Yl[i]:.2f} G={G[i]:+.2f} {bar}")
