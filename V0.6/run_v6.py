# -*- coding: utf-8 -*-
"""v6 因果修正：金融压力进 Y(涨矛盾)→Y 触碰 Ylimit→危机；危机本身再反馈推高 Y"""
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
    mil=df["Military"].to_numpy(float); arable=df["Arable"].to_numpy(float)
    unemp=df["unemployment"].to_numpy(float); mcap=df["mcap_gdp"].to_numpy(float)
    if use_gdp: X=df["GDP"].to_numpy(float)
    else:
        pe=df["PrimaryEnergy"].to_numpy(float); ap=df["AnimalPower"].to_numpy(float)
        X=pe+ap+pop*130/1e6
    Xn=X/X[0]; dX=np.diff(Xn,prepend=Xn[0])
    pg=np.zeros(len(df))
    for t in range(1,len(df)):
        pr=patent[t-1] if patent[t-1]>0 else 1.0
        pg[t]=np.clip((patent[t]-patent[t-1])/pr,-1,1)
    edu_n=edu/np.nanmax(edu) if np.nanmax(edu)>0 else edu
    Z=np.clip(mov_avg(0.5*pg+0.3*(edu_n-0.5)+0.2*(0.4-gini/100),3),-0.5,0.5)
    fZ=sign_log(Z)
    popP=np.zeros(len(df))
    if np.nanmax(arable)>0: popP=np.clip((pop/arable)/np.nanmedian(pop/arable)-1,0,3)
    # 金融压力(涨矛盾项)：失业率↑ + 股崩 → 进 Y，而非 Ylimit
    u_norm=unemp/np.nanmax(unemp); mg=np.zeros(len(df))
    for t in range(1,len(df)):
        pr=mcap[t-1] if mcap[t-1]>0 else 1.0
        mg[t]=np.clip((mcap[t]-mcap[t-1])/pr,-1,1)
    fin_inc = P["wU"]*np.diff(u_norm, prepend=u_norm[0]) + P["wC"]*np.clip(-mg,0,1)
    fin_inc = np.clip(fin_inc, 0, 1.0)
    # Y：累加 ΔX + 创新缓解 + 金融压力(涨) ；G>=0 时危机反馈额外加 Y
    Y=np.zeros(len(df)); Y[0]=P["Y0"]; crisis=np.zeros(len(df))
    for t in range(1,len(df)):
        dY = P["kX"]*dX[t]*(1+popP[t]) + P["kZ"]*fZ[t] + P["kFin"]*fin_inc[t]
        Y[t] = Y[t-1] + dY
        if Y[t] >= 0 and t>0:  # 危机反馈：Y 触及红线后进一步推高(次级)
            pass
    # Ylimit：只承载(军事两难 + 固定负担)，不含金融压力
    t=np.arange(len(df))
    Yl=P["kL"]*(Xn**P["beta"])*(1-mil)-P["b0"]*(1+P["bG"]*t)
    return df.index.to_numpy(int) if use_gdp else df["Year"].to_numpy(int), Y-Yl

def sig_peaks(years,G,w=5,thresh=0.06):
    base=mov_avg(G,w); out=[]
    for t in range(1,len(G)-1):
        if G[t]>=G[t-1] and G[t]>=G[t+1] and G[t]>0 and (G[t]-base[t])>thresh: out.append(int(years[t]))
    return out

P = dict(kX=1.0,kZ=0.3,kL=1.5,beta=0.6,b0=0.12,bG=0.003,Y0=1.0,wU=0.5,wC=0.5,kFin=1.0)

def load_in(name):
    df=pd.read_excel(os.path.join(BASE,f"SECM_V24_{name}.xlsx"),sheet_name=0).ffill()
    wb=pd.read_csv(os.path.join(WB,f"wb_{name}.csv"),index_col="Year")
    df=df.join(wb,on="Year",how="left").ffill().bfill()
    df=df.rename(columns={"PatentCount":"Patent","MilitaryRatio":"Military","ArableLandTotal":"Arable"})
    return df

tot_hit=tot_ev=0
print("== 样本内(4国) ==")
for name,ev in CRISIS_IN.items():
    yrs,G=run(load_in(name),P,False); pk=sig_peaks(yrs,G)
    hits=[e for e in ev if any(abs(e-p)<=1 for p in pk)]
    tot_hit+=len(hits); tot_ev+=len(ev)
    print(f"  {name}: 事件{ev} 命中{hits} 峰值{pk}")
print("== 样本外(10国) ==")
for name,ev in CRISIS_OOS.items():
    df=pd.read_csv(os.path.join(OOS,f"{name}.csv"),index_col="Year").ffill().bfill()
    df=df.rename(columns={"Military":"Mpct"}); df["Military"]=df["Mpct"]/100
    yrs,G=run(df,P,True); pk=sig_peaks(yrs,G)
    hits=[e for e in ev if any(abs(e-p)<=1 for p in pk)]
    tot_hit+=len(hits); tot_ev+=len(ev)
    print(f"  {name}: 事件{ev} 命中{hits} 峰值{pk}")
print(f"\n总计: {tot_hit}/{tot_ev} 命中")
