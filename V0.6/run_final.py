# -*- coding: utf-8 -*-
"""SECM V0.6 最终模型（按完整哲学）：
Y 递推 + Z=负面−科技(带下限) + 土地乘子 + Ylimit=(X−军费)×福利 + 只看 G 相对位置
"""
import pandas as pd, numpy as np, os, io, sys
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
BASE = r"E:\AI-Personal\SECM-Project\Data\DATAsource\1980_2020 Source"
WB = r"E:\AI-Personal\SECM-Project\V0.6"
OOS = r"E:\AI-Personal\SECM-Project\V0.6\oos"
CRISIS_IN = {"USA":[1988,2007],"Japan":[1997],"Argentina":[1980,1982,1989,1995,2001],"Greece":[2008,2012]}
CRISIS_OOS = {"SouthKorea":[1997],"Mexico":[1982,1994],"Turkey":[2000,2001],"Indonesia":[1997],
          "Thailand":[1997],"Brazil":[1983,1990,1994],"Chile":[1982],"Russia":[1998],
          "India":[1991],"SouthAfrica":[]}
def mov_avg(x,w): return pd.Series(x).rolling(w,center=True,min_periods=1).mean().to_numpy()

def run(df, P, use_gdp):
    pop=df["Population"].to_numpy(float); patent=df["Patent"].to_numpy(float)
    edu=df["EduRate"].to_numpy(float); gini=df["Gini"].to_numpy(float)
    mil=df["Military"].to_numpy(float); unemp=df["unemployment"].to_numpy(float)
    mcap=df["mcap_gdp"].to_numpy(float); arable=df["Arable"].to_numpy(float)
    X=df["GDP"].to_numpy(float)   # 统一用 GDP 作 X（保留商业周期波动）
    Xn=X/X[0]; Xn=np.maximum(Xn, P["Xmin"])   # 非零下限
    dX=np.diff(Xn,prepend=Xn[0])
    # 科技项(专利增速+教育) 带非零下限
    pg=np.zeros(len(df))
    for t in range(1,len(df)):
        pr=patent[t-1] if patent[t-1]>0 else 1.0
        pg[t]=np.clip((patent[t]-patent[t-1])/pr,-1,1)
    edu_n=edu/np.nanmax(edu) if np.nanmax(edu)>0 else edu
    Ztech = np.maximum(P["wp"]*mov_avg(pg,3) + P["we"]*edu_n, P["ZtechMin"])  # 科技永不归零
    # 负面项(失业+贫富+股崩)
    u_norm=unemp/np.nanmax(unemp); mg=np.zeros(len(df))
    for t in range(1,len(df)):
        pr=mcap[t-1] if mcap[t-1]>0 else 1.0
        mg[t]=np.clip((mcap[t]-mcap[t-1])/pr,-1,1)
    crash=np.clip(-mg,0,1)
    Zneg = P["wu"]*u_norm + P["wg"]*(gini/100) + P["wc"]*crash
    Z = np.clip(Zneg - Ztech, -1.0, 1.0)   # Z=负面−科技, 可负可正
    # 土地矛盾乘子
    popP=np.zeros(len(df))
    if np.nanmax(arable)>0:
        popP=np.clip((pop/arable)/np.nanmedian(pop/arable)-1, 0, 3)
    # Ylimit = (X−军费)×(基准+福利)
    welfare = P["we"]*edu_n
    Yl = (Xn - mil*Xn) * (P["w0"] + welfare)
    # Y 递推 + 危机反馈(危机损伤X→X负→Y掉得比Ylimit快)
    Y=np.zeros(len(df)); Y[0]=P["Y0"]; crisis=0.0
    for t in range(1,len(df)):
        dXc = dX[t] - P["damage"]*crisis   # 危机中生产力被破坏
        Y[t]=Y[t-1] + dXc*P["kY"]*(1+P["ZImpactK"]*Z[t])*(1+popP[t])
        crisis = 1.0 if Y[t] > Yl[t] else max(0.0, crisis-0.5)
    return df.index.to_numpy(int) if use_gdp else df["Year"].to_numpy(int), Y-Yl

def sig_peaks(years,G,w=5,thresh=0.08):
    base=mov_avg(G,w); out=[]
    for t in range(1,len(G)-1):
        if G[t]>=G[t-1] and G[t]>=G[t+1] and G[t]>0 and (G[t]-base[t])>thresh: out.append(int(years[t]))
    return out

P = dict(kY=2.0, ZImpactK=1.0, wu=0.5, wg=0.3, wc=0.4, wp=0.3, we=0.4,
         ZtechMin=0.3, w0=0.8, Xmin=0.1, Y0=1.0, damage=0.08)
def load_in(name):
    df=pd.read_excel(os.path.join(BASE,f"SECM_V24_{name}.xlsx"),sheet_name=0).ffill()
    wb=pd.read_csv(os.path.join(WB,f"wb_{name}.csv"),index_col="Year")
    df=df.join(wb,on="Year",how="left").ffill().bfill()
    df["GDP"]=df["gdp_percap"]*df["Population"]
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
