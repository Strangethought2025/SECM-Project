# -*- coding: utf-8 -*-
"""v8：持续危机强度(指数衰减累积) + 危机正反馈；水平式Y，因果方向正确"""
import pandas as pd, numpy as np, os, io, sys
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
BASE = r"E:\AI-Personal\SECM-Project\Data\DATAsource\1980_2020 Source"
WB = r"E:\AI-Personal\SECM-Project\V0.6"
OOS = r"E:\AI-Personal\SECM-Project\V0.6\oos"
CRISIS_IN = {"USA":[1988,2007],"Japan":[1997],"Argentina":[1980,1982,1989,1995,2001],"Greece":[2008,2012]}
CRISIS_OOS = {"SouthKorea":[1997],"Mexico":[1982,1994],"Turkey":[2000,2001],"Indonesia":[1997],
          "Thailand":[1997],"Brazil":[1983,1990,1994],"Chile":[1982],"Russia":[1998],
          "India":[1991],"SouthAfrica":[]}
def sign_log(z): return np.sign(z)*np.log(1+np.abs(z))
def mov_avg(x,w): return pd.Series(x).rolling(w,center=True,min_periods=1).mean().to_numpy()

def run(df, P, use_gdp):
    pop=df["Population"].to_numpy(float); patent=df["Patent"].to_numpy(float)
    edu=df["EduRate"].to_numpy(float); gini=df["Gini"].to_numpy(float)
    mil=df["Military"].to_numpy(float); unemp=df["unemployment"].to_numpy(float)
    mcap=df["mcap_gdp"].to_numpy(float)
    if use_gdp: X=df["GDP"].to_numpy(float)
    else:
        pe=df["PrimaryEnergy"].to_numpy(float); ap=df["AnimalPower"].to_numpy(float)
        X=pe+ap+pop*130/1e6
    Xn=X/X[0]
    pg=np.zeros(len(df))
    for t in range(1,len(df)):
        pr=patent[t-1] if patent[t-1]>0 else 1.0
        pg[t]=np.clip((patent[t]-patent[t-1])/pr,-1,1)
    edu_n=edu/np.nanmax(edu) if np.nanmax(edu)>0 else edu
    Z=np.clip(mov_avg(0.5*pg+0.3*(edu_n-0.5)+0.2*(0.4-gini/100),3),-0.5,0.5)
    fZ=sign_log(Z)
    # 失业水平(归一) + 持续危机强度(股崩指数衰减累积)
    u_norm=unemp/np.nanmax(unemp)
    mg=np.zeros(len(df))
    for t in range(1,len(df)):
        pr=mcap[t-1] if mcap[t-1]>0 else 1.0
        mg[t]=np.clip((mcap[t]-mcap[t-1])/pr,-1,1)
    crash=np.clip(-mg,0,1)
    crisis=np.zeros(len(df))
    for t in range(1,len(df)):
        crisis[t]=P["decay"]*crisis[t-1]+crash[t]   # 持续~3年
    # 水平式 Y + 危机正反馈
    Y=np.zeros(len(df))
    Yl=np.array([P["kL"]*(Xn[t]**P["beta"])*(1-mil[t])-P["b0"]*(1+P["bG"]*t) for t in range(len(df))])
    Y[0]=P["Y0"]
    for t in range(1,len(df)):
        Y[t]=P["a1"]*Xn[t]+P["a2"]*u_norm[t]+P["a3"]*crisis[t]+P["b1"]*(gini[t]/100)+P["kZ"]*fZ[t]
        # 危机正反馈：上期越线(Y>Yl)则本期Y额外升高
        if Y[t-1]>Yl[t-1]:
            Y[t]+=P["fb"]*(Y[t-1]-Yl[t-1])
    return df.index.to_numpy(int) if use_gdp else df["Year"].to_numpy(int), Y-Yl

def sig_peaks(years,G,w=5,thresh=0.08):
    base=mov_avg(G,w); out=[]
    for t in range(1,len(G)-1):
        if G[t]>=G[t-1] and G[t]>=G[t+1] and G[t]>0 and (G[t]-base[t])>thresh: out.append(int(years[t]))
    return out

P = dict(a1=1.0,a2=0.8,a3=0.6,b1=0.5,kZ=0.3,kL=1.6,beta=0.6,b0=0.1,bG=0.003,Y0=1.0,decay=0.5,fb=0.2)
def load_in(name):
    df=pd.read_excel(os.path.join(BASE,f"SECM_V24_{name}.xlsx"),sheet_name=0).ffill()
    wb=pd.read_csv(os.path.join(WB,f"wb_{name}.csv"),index_col="Year")
    df=df.join(wb,on="Year",how="left").ffill().bfill()
    return df.rename(columns={"PatentCount":"Patent","MilitaryRatio":"Military","ArableLandTotal":"Arable"})

tot_hit=tot_ev=0
print("== 样本内 ==")
for name,ev in CRISIS_IN.items():
    yrs,G=run(load_in(name),P,False); pk=sig_peaks(yrs,G)
    hits=[e for e in ev if any(abs(e-p)<=1 for p in pk)]
    tot_hit+=len(hits); tot_ev+=len(ev)
    print(f"  {name}: 事件{ev} 命中{hits} 峰值{pk}")
print("== 样本外 ==")
for name,ev in CRISIS_OOS.items():
    df=pd.read_csv(os.path.join(OOS,f"{name}.csv"),index_col="Year").ffill().bfill()
    df=df.rename(columns={"Military":"Mpct"}); df["Military"]=df["Mpct"]/100
    yrs,G=run(df,P,True); pk=sig_peaks(yrs,G)
    hits=[e for e in ev if any(abs(e-p)<=1 for p in pk)]
    tot_hit+=len(hits); tot_ev+=len(ev)
    print(f"  {name}: 事件{ev} 命中{hits} 峰值{pk}")
print(f"\n总计: {tot_hit}/{tot_ev}")
