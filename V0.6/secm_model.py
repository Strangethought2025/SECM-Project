# -*- coding: utf-8 -*-
"""SECM V0.6 共享模型核心: mov_avg/norm/compute/calibrate —— final_hybrid/final_metrics/events_engine 共用, 防止复制漂移"""
import pandas as pd, numpy as np

def mov_avg(x,w): return pd.Series(x).rolling(w,center=True,min_periods=1).mean().to_numpy()

def norm(x):
    x=np.asarray(x,float)
    if not np.any(~np.isnan(x)): return np.zeros_like(x)
    m=np.nanmax(x)
    return (x/m if m and m>0 else np.zeros_like(x))

def compute(df,P):
    pop=df["Population"].to_numpy(float)
    epc=df["energy_pc"].to_numpy(float); murder=df["murder"].to_numpy(float)
    health=df["health"].to_numpy(float); edu=df["EduRate"].to_numpy(float)
    mil=np.nan_to_num(df["Military"].to_numpy(float)/100, nan=0.0)  # 无军队国家=0军费负担
    unemp=df["unemployment"].to_numpy(float)
    mcap=df["mcap_gdp"].to_numpy(float)
    gini=df["Gini"].to_numpy(float) if "Gini" in df.columns else np.full(len(df),np.nan)
    patent=df["Patent"].to_numpy(float)
    debt=df["debt_gdp"].to_numpy(float) if "debt_gdp" in df.columns else np.full(len(df),np.nan)
    credit=df["credit_gdp"].to_numpy(float) if "credit_gdp" in df.columns else np.full(len(df),np.nan)
    npl=df["npl"].to_numpy(float) if "npl" in df.columns else np.full(len(df),np.nan)
    gov_exp=df["gov_exp"].to_numpy(float) if "gov_exp" in df.columns else np.full(len(df),np.nan)
    n=len(df)
    X=epc*pop/1e6 + pop*130.0/1e6
    Xn=np.maximum(X/X[0],0.1)
    lnX=np.log(Xn); dlnX=np.diff(lnX,prepend=lnX[0])   # 对数增长: 积分有界(ΣdlnX=lnXn), 防高速增长国Y失控
    gini_n=gini/100; u_norm=norm(unemp); mur_norm=norm(murder)
    mg=np.zeros(n)
    for t in range(1,n):
        pr=mcap[t-1] if mcap[t-1]>0 else np.nan
        mg[t]=np.clip((mcap[t]-mcap[t-1])/pr,-1,1) if not np.isnan(pr) else 0
    cris=np.zeros(n)
    for t in range(1,n): cris[t]=0.6*cris[t-1]+np.clip(-mg[t],0,1)
    # 私人信贷崩盘 = 欠债违约潮 (个人/企业欠债)
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
    edu_n=norm(edu)
    npl_n=norm(npl); ge_n=norm(gov_exp)
    # Zc = 平均合成（防数值乱飞）—— 所有国家同一套指标
    Zc=np.nanmean(np.vstack([P["wg"]*gini_n, P["wu"]*u_norm, P["wm"]*mur_norm,
                             P["wc"]*cris, P["wcr"]*ccris, P["wnp"]*npl_n,
                             P["wge"]*ge_n]),axis=0)
    # 科技红利 = 平均(专利增速, 教育)
    bonus=np.maximum(np.nanmean(np.vstack([P["wp"]*mov_avg(pg,3), P["we"]*edu_n]),axis=0), P["ZtechMin"])
    Z=Zc-P["gX"]*bonus
    Z=Z-mov_avg(Z,5)
    Zeff=np.sign(Z)*((1+np.abs(Z))**P["p"]-1)  # 幂次放大保符号(p=2为原平方, >2尖锐端更锐)
    # 福利 = 平均(医疗, 教育)
    health_n=norm(health)
    welfare=np.nanmean(np.vstack([0.5*health_n, 0.5*edu_n]),axis=0)
    # 政府债务 = 承载力负项: 债越重 Ylimit 越低
    debt_n=norm(debt)
    Yl=(Xn*(1-mil))**P["beta"]*(P["w0"]+P["ww"]*welfare)/(1+P["wd"]*debt_n)
    # Y = 累加器（V0.5结构，逐国可对齐）
    # kZ*Zeff: 直接矛盾推力——危机尖峰直接抬Y; lam: 回拉项——Y不无限爬高
    # Y_base 随 Xn^beta 增长(与Ylimit同幂): 防高速增长国(新加坡/马来西亚)Y无限甩开Ylimit
    Y_base=P["a0"]+P["a1"]*(Xn**P["beta"])+P["mu"]*np.log(1+Xn)
    Y=np.zeros(n); Y[0]=Y_base[0]
    for t in range(1,n):
        Y[t]=Y[t-1]+dlnX[t]*P["kY"]*(1+P["ZI"]*Zeff[t])+P["kZ"]*Zeff[t]-P["lam"]*(Y[t-1]-Y_base[t])
    return df.index.to_numpy(int), Y, Yl

YF=np.arange(0.5,2.6,0.15); YLS=np.arange(0.5,1.8,0.1)
def calibrate(years,Y,Yl,first_ev):
    """逐国校准: (yf,yls)缩放, 首次越线=首事件±1年, 其余全预测."""
    best=None
    for yf in YF:
        for yls in YLS:
            G=yf*Y-yls*Yl
            pos=np.where(G>0)[0]
            if len(pos) and abs(int(years[pos[0]])-first_ev)<=1:
                if np.any(G[pos[0]:]<0): return yf,yls
                if best is None: best=(yf,yls)
    return best if best else (1.0,1.0)
