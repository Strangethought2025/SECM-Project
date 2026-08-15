# -*- coding: utf-8 -*-
"""诊断: 打印四国 Y/Yl/Zc各分量 逐年曲线"""
import pandas as pd, numpy as np, os, io, sys
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
OOS = r"E:\AI-Personal\SECM-Project\V0.6\oos2000"
Pbest={'wg':0.5749090723515404,'wu':1.0449549190323226,'wm':0.4031953098284189,
 'wc':0.35952381931006405,'wcr':0.6084047457502312,'wnp':0.4238883579823924,
 'wge':0.2983727477872843,'wp':0.4074812196482345,'we':0.6590698025204353,
 'gX':0.7584774339327947,'ZtechMin':0.3192456947408183,'kY':0.8919836496049793,
 'ZI':1.2804585678233185,'w0':0.7986063389428535,'ww':0.30482283475175265,
 'wd':1.1996873091039064,'beta':0.7109681983174195,'a0':0.2710588099151265,
 'a1':0.3278092941934585,'mu':0.3680670393102681}

def mov_avg(x,w): return pd.Series(x).rolling(w,center=True,min_periods=1).mean().to_numpy()
def norm(x):
    m=np.nanmax(x)
    return (x/m if m and m>0 else np.zeros_like(x))

def compute(df,P):
    pop=df["Population"].to_numpy(float); epc=df["energy_pc"].to_numpy(float)
    murder=df["murder"].to_numpy(float); health=df["health"].to_numpy(float)
    edu=df["EduRate"].to_numpy(float); mil=df["Military"].to_numpy(float)/100
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
        Y[t]=Y[t-1]+dX[t]*P["kY"]*(1+P["ZI"]*Zeff[t])
    return dict(years=df.index.to_numpy(int),Y=Y,Yl=Yl,Xn=Xn,u=u_norm,gini=gini_n,
                mur=mur_norm,cris=cris,ccris=ccris,npl=npl_n,ge=ge_n,debt=debt_n,
                wel=welfare,Z=Z,Zeff=Zeff)

for name in ["Iceland","Ireland","Cyprus","Portugal"]:
    df=pd.read_csv(os.path.join(OOS,f"{name}.csv"),index_col="Year").ffill().bfill()
    d=compute(df,Pbest)
    G=d["Y"]-d["Yl"]
    print(f"\n=== {name}: Y/Yl 比值范围 {np.min(d['Y']/d['Yl']):.2f}~{np.max(d['Y']/d['Yl']):.2f}  最大G={np.max(G):.3f}({d['years'][np.argmax(G)]})")
    print(f"  Y[0]={d['Y'][0]:.3f} Yl[0]={d['Yl'][0]:.3f}  wel[0]={d['wel'][0]:.3f} debt_n[0]={d['debt'][0]:.3f}")
    for i,y in enumerate(d["years"]):
        if y in [2000,2004,2007,2008,2009,2010,2011,2012,2013,2014,2015,2019,2020,2022,2025]:
            print(f"  {y}: Y={d['Y'][i]:.3f} Yl={d['Yl'][i]:.3f} G={G[i]:+.3f} | u={d['u'][i]:.2f} cris={d['cris'][i]:.2f} ccris={d['ccris'][i]:.2f} npl={d['npl'][i]:.2f} ge={d['ge'][i]:.2f} debt={d['debt'][i]:.2f} Xn={d['Xn'][i]:.2f} wel={d['wel'][i]:.2f}")
