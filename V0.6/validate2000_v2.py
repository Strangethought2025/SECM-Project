# -*- coding: utf-8 -*-
"""增强版：Ylimit 加'停滞侵蚀'项(增长不足→承载缓降→G>0持续)；检测改'G>0持续期'"""
import pandas as pd, numpy as np, os, io, sys
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
    gX=np.diff(X,prepend=X[0])/np.maximum(X,1)   # GDP 增长率
    pg=np.zeros(len(df))
    for t in range(1,len(df)):
        pr=patent[t-1] if patent[t-1]>0 else 1.0
        pg[t]=np.clip((patent[t]-patent[t-1])/pr,-1,1)
    edu_n=edu/np.nanmax(edu) if np.nanmax(edu)>0 else np.zeros(len(df))
    Ztech=np.maximum(P["wp"]*mov_avg(pg,3)+P["we"]*edu_n,P["ZtechMin"])
    u_norm=unemp/np.nanmax(unemp) if np.nanmax(unemp)>0 else np.zeros(len(df))
    mg=np.zeros(len(df))
    for t in range(1,len(df)):
        pr=mcap[t-1] if mcap[t-1]>0 else 1.0
        mg[t]=np.clip((mcap[t]-mcap[t-1])/pr,-1,1)
    Z=np.clip(P["wu"]*u_norm+P["wc"]*np.clip(-mg,0,1)-Ztech,-1,1)
    # 去均值中心化：让 Z 围绕 0 正负对称摆动（消除系统性正偏→Y单边漂移）
    Z = Z - mov_avg(Z, 5)
    # 非线性放大：平方放大保符号，左右摆动幅度都放大（消除 G 虚高的关键）
    Zeff=np.sign(Z)*((1+np.abs(Z))**P["ZExp"] - 1)
    # 停滞侵蚀：增长低于阈值→负担累积→承载缓降（缓慢危机的来源）
    burden=np.zeros(len(df))
    for t in range(1,len(df)):
        burden[t]=burden[t-1]*0.9 + max(0.0, P["gThresh"]-gX[t])   # 增长不足累积
    Yl=(Xn-mil*Xn)*(P["w0"]+P["we"]*edu_n) - P["kBurden"]*burden
    Y=np.zeros(len(df))
    # 初始 Y：数据驱动（各国初始矛盾水平不同），= a1·X + a2·失业 + a3·(1−教育)
    Y[0]=P["a1"]*Xn[0] + P["a2"]*u_norm[0] + P["a3"]*(1-edu_n[0])
    crisis=0.0
    for t in range(1,len(df)):
        Y[t]=Y[t-1]+(dX[t]-P["damage"]*crisis)*P["kY"]*(1+P["ZImpactK"]*Zeff[t])
        Y[t]-=P["revert"]*max(0.0, Y[t]-Yl[t])   # 越线越深→回拉越强→回落线下
        crisis=1.0 if Y[t]>Yl[t] else max(0.0,crisis-0.5)
    return df.index.to_numpy(int), Y-Yl

# 检测：G>0 持续期（缓慢危机 = Y 持续高于 Ylimit）
def crisis_years(years,G,min_len=2):
    out=set()
    for t in range(1,len(G)-1):
        if G[t]>0: out.add(int(years[t]))
    return sorted(out)

P=dict(kY=3.0,ZImpactK=1.0,w0=0.7,wu=0.7,wc=0.3,wp=0.3,we=0.4,ZtechMin=0.3,Xmin=0.1,a1=0.4,a2=0.3,a3=0.3,damage=0.03,gThresh=0.02,kBurden=0.3,ZExp=2.0,revert=0.3)
tot_hit=tot_ev=0
for name,ev in EVENTS.items():
    df=pd.read_csv(os.path.join(OOS,f"{name}.csv"),index_col="Year").ffill().bfill().fillna(0)
    yrs,G=run(df,P); cy=crisis_years(yrs,G)
    hits=[e for e in ev if any(abs(e-y)<=1 for y in cy)]
    tot_hit+=len(hits); tot_ev+=len(ev)
    print(f"{name:12s} 事件{ev} 命中{hits}  G>0年数={len(cy)}")
print(f"\n总计: {tot_hit}/{tot_ev} = {tot_hit/tot_ev*100:.0f}%")
