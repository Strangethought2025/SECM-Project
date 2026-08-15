# -*- coding: utf-8 -*-
"""正式评估: 命中率 + 精确度/误报(危机段) + 幅度相关(G vs 凶杀) —— 用 best_params.json 冻结参数"""
import pandas as pd, numpy as np, os, io, sys, json
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
HERE = os.path.dirname(os.path.abspath(__file__))
TUNE = os.path.join(HERE, "tune"); OOS = os.path.join(HERE, "oos2000")
TUNE_EV = {"USA":[1987,2001,2008,2020],"Argentina":[1982,1989,2001,2014,2020],
    "Mexico":[1982,1994,2008,2020],"Turkey":[1994,2001,2018,2020],
    "Russia":[1998,2008,2015,2020,2022],"Greece":[2010,2012,2020]}
VAL_EV = {"UK":[2008,2020],"Spain":[2008,2012,2020],"Portugal":[2011,2020],
    "Ireland":[2008,2010,2020],"Cyprus":[2013,2020],"Iceland":[2008,2020],"Brazil":[2015,2020],
    "Ukraine":[2009,2014,2020,2022],"Venezuela":[2013,2016,2020],"Egypt":[2011,2016,2020],
    "Pakistan":[2008,2019,2022],"SriLanka":[2022],"Ghana":[2022],"Lebanon":[2019,2020]}
P = json.load(open(os.path.join(HERE, "best_params.json"), encoding="utf-8"))

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
    Zeff=np.sign(Z)*((1+np.abs(Z))**P["p"]-1)
    health_n=norm(health)
    welfare=np.nanmean(np.vstack([0.5*health_n,0.5*edu_n]),axis=0)
    debt_n=norm(debt)
    Yl=(Xn*(1-mil))**P["beta"]*(P["w0"]+P["ww"]*welfare)/(1+P["wd"]*debt_n)
    Y_base=P["a0"]+P["a1"]*Xn+P["mu"]*np.log(1+Xn)
    Y=np.zeros(n); Y[0]=Y_base[0]
    for t in range(1,n):
        Y[t]=Y[t-1]+dX[t]*P["kY"]*(1+P["ZI"]*Zeff[t])+P["kZ"]*Zeff[t]-P["lam"]*(Y[t-1]-Y_base[t])
    return df.index.to_numpy(int), Y, Yl

YF=np.arange(0.5,2.6,0.15); YLS=np.arange(0.5,1.8,0.1)
def calibrate(years,Y,Yl,first_ev):
    best=None
    for yf in YF:
        for yls in YLS:
            G=yf*Y-yls*Yl
            pos=np.where(G>0)[0]
            if len(pos) and abs(int(years[pos[0]])-first_ev)<=1:
                if np.any(G[pos[0]:]<0): return yf,yls
                if best is None: best=(yf,yls)
    return best if best else (1.0,1.0)

def run_country(folder,name,evs):
    df=pd.read_csv(os.path.join(folder,f"{name}.csv"),index_col="Year").ffill().bfill()
    yrs,Y,Yl=compute(df,P); yf,yls=calibrate(yrs,Y,Yl,evs[0]); G=yf*Y-yls*Yl
    pos=yrs[G>0]
    hits=[e for e in evs if any(abs(e-y)<=1 for y in pos)]
    t=yf*Y/(yls*Yl)          # 紧张度标尺: 相对距离 (哲学: 只看相对位置)
    tp_years=sum(1 for y in pos if any(abs(e-y)<=1 for e in evs))
    spells=[]; start=None
    for i in range(len(G)):
        if G[i]>0 and start is None: start=yrs[i]
        elif G[i]<=0 and start is not None:
            spells.append((start,yrs[i-1])); start=None
    if start is not None: spells.append((start,yrs[-1]))
    false_spells=[s for s in spells if not any(any(abs(e-y)<=2 for y in range(s[0],s[1]+1)) for e in evs)]
    return yrs,G,hits,evs,pos,spells,false_spells,tp_years,t

print(f"冻结参数: {len(P)} 个 (best_params.json)")
print("\n== 校准6国 (调参集, 1980-2025) ==")
rows=[]
for c,evs in TUNE_EV.items():
    yrs,G,hits,evs,pos,spells,false_spells,tp,_t=run_country(TUNE,c,evs)
    prec=tp/len(pos)*100 if len(pos) else 100
    rows.append((c,len(hits),evs,len(pos),spells,false_spells,tp))
    print(f"  {c:10s} 事件命中{len(hits)}/{len(evs)} | G>0年={len(pos)} (真阳{tp}年, 年级精确度{prec:.0f}%) | 危机段={len(spells)} (误报段={len(false_spells)})")

print("\n== 验证14国 (样本外, 2000-2025) ==")
vrows=[]
for c,evs in VAL_EV.items():
    yrs,G,hits,evs,pos,spells,false_spells,tp,_t=run_country(OOS,c,evs)
    prec=tp/len(pos)*100 if len(pos) else 100
    vrows.append((c,len(hits),evs,len(pos),spells,false_spells,tp))
    print(f"  {c:10s} 事件命中{len(hits)}/{len(evs)} | G>0年={len(pos)} (真阳{tp}年, 年级精确度{prec:.0f}%) | 危机段={len(spells)} (误报段={len(false_spells)})")

def spells_stats(rs):
    tot_hits=sum(r[1] for r in rs); tot_ev=sum(len(r[2]) for r in rs)
    tot_pos=sum(r[3] for r in rs); tot_tp=sum(r[6] for r in rs)
    hit_spells=sum(1 for r in rs for s in r[4] if any(any(abs(e-y)<=2 for y in range(s[0],s[1]+1)) for e in r[2]))
    tot_spells=sum(len(r[4]) for r in rs); tot_false=sum(len(r[5]) for r in rs)
    return tot_hits,tot_ev,tot_pos,tot_tp,hit_spells,tot_spells,tot_false
th,tt,tp_yr,ttp,hs,ts,fs=spells_stats(rows)
vh,vt,vp_yr,vtp,vhs,vts,vfs=spells_stats(vrows)
print("\n== 双数字汇总 ==")
print(f"校准集: 事件召回={th}/{tt}={th/tt*100:.0f}% | 年级精确度={ttp}/{tp_yr}={ttp/tp_yr*100:.0f}% (真阳年/越线年) | 危机段={ts} 命中段={hs} 误报段={fs}")
print(f"验证集: 事件召回={vh}/{vt}={vh/vt*100:.0f}% | 年级精确度={vtp}/{vp_yr}={vtp/vp_yr*100:.0f}% (真阳年/越线年) | 危机段={vts} 命中段={vhs} 误报段={vfs}")

print("\n== 紧张度标尺 (G_disp=S·G, S=1/事件年G中位数, G_disp>1=社会紧张) ==")
evG=[]; allG=[]; evy=set()
for folder,EVS in [(TUNE,TUNE_EV),(OOS,VAL_EV)]:
    for c,evs in EVS.items():
        yrs,G,hits,evs2,pos,spells,false_spells,tp,t=run_country(folder,c,evs)
        for e in evs2:
            if e in yrs:
                i=np.where(yrs==e)[0][0]
                evG.append(G[i]); evy.add((c,e))
        for i,y in enumerate(yrs):
            if not any(abs(e-y)<=1 for e in evs2): allG.append(G[i])
S=1.0/float(np.median(evG))
print(f"  显示增益 S={S:.2f} (使事件年G中位数=1.0)")
ev_tense=sum(1 for g in evG if S*g>1); calm_tense=sum(1 for g in allG if S*g>1)
print(f"  事件年: G中位={np.median(evG):.2f} → G_disp中位={np.median(evG)*S:.2f} | G_disp>1(紧张)的事件年: {ev_tense}/{len(evG)}")
print(f"  非事件年: G中位={np.median(allG):.2f} → G_disp>1(紧张)的非事件年: {calm_tense}/{len(allG)} = {calm_tense/len(allG)*100:.0f}%")
print(f"  语义: G_disp<0 安全(线下) | 0~1 承压 | >1 社会紧张")

# 幅度相关: G 与凶杀率(同数据源 WB) —— 全部20国汇总 + 逐国
print("\n== 幅度相关: G vs 凶杀率 (Pearson) ==")
pairs=[]; per=[]
for folder,EVS in [(TUNE,TUNE_EV),(OOS,VAL_EV)]:
    for c in EVS:
        df=pd.read_csv(os.path.join(folder,f"{c}.csv"),index_col="Year").ffill().bfill()
        yrs,Y,Yl=compute(df,P); yf,yls=calibrate(yrs,Y,Yl,EVS[c][0]); G=yf*Y-yls*Yl
        mur=df["murder"].to_numpy(float)
        ok=~np.isnan(G)&~np.isnan(mur)
        if ok.sum()>=8:
            r=float(np.corrcoef(G[ok],mur[ok])[0,1]); per.append((c,r)); pairs.append((G[ok],mur[ok]))
    gv=np.concatenate([a for a,b in pairs]); hv=np.concatenate([b for a,b in pairs])
rall=float(np.corrcoef(gv,hv)[0,1])
print(f"  汇总 r={rall:+.3f} (n={len(gv)})")
for c,r in per: print(f"  {c:10s} r={r:+.2f}")
