# -*- coding: utf-8 -*-
"""幅度相关：模型 G 与真实暴力强度(凶杀率)的 Pearson 相关（统一列名/单位）"""
import pandas as pd, numpy as np, os, io, sys, requests
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
BASE = r"E:\AI-Personal\SECM-Project\Data\DATAsource\1980_2020 Source"
WB = r"E:\AI-Personal\SECM-Project\V0.6"
OOS = r"E:\AI-Personal\SECM-Project\V0.6\oos"

def sign_log(z): return np.sign(z)*np.log(1+np.abs(z))
def mov_avg(x,w): return pd.Series(x).rolling(w,center=True,min_periods=1).mean().to_numpy()

def model(df, P):
    pop=df["Population"].to_numpy(float); patent=df["Patent"].to_numpy(float)
    edu=df["EduRate"].to_numpy(float); gini=df["Gini"].to_numpy(float)
    mil=df["Military"].to_numpy(float)      # 比例 0~1
    arable=df["Arable"].to_numpy(float); unemp=df["unemployment"].to_numpy(float)
    mcap=df["mcap_gdp"].to_numpy(float)
    if "GDP" in df.columns:
        X=df["GDP"].to_numpy(float)
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
    fZ=sign_log(Z); popP=np.zeros(len(df))
    if np.nanmax(arable)>0:
        popP=np.clip((pop/arable)/np.nanmedian(pop/arable)-1,0,3)
    Y=np.zeros(len(df)); Y[0]=P["Y0"]
    for t in range(1,len(df)): Y[t]=Y[t-1]+P["kX"]*dX[t]*(1+popP[t])+P["kZ"]*fZ[t]
    u_norm=unemp/np.nanmax(unemp); mg=np.zeros(len(df))
    for t in range(1,len(df)):
        pr=mcap[t-1] if mcap[t-1]>0 else 1.0
        mg[t]=np.clip((mcap[t]-mcap[t-1])/pr,-1,1)
    fstress=np.clip(P["wU"]*u_norm+P["wC"]*np.clip(-mg,0,1),0,0.8)
    t=np.arange(len(df))
    Yl=P["kL"]*(Xn**P["beta"])*(1-mil)*(1-fstress)-P["b0"]*(1+P["bG"]*t)
    return Y-Yl

def fetch_homicide(cc):
    url=f"https://api.worldbank.org/v2/country/{cc}/indicator/VC.IHR.PSRC.P5?format=json&date=1980:2022&per_page=100"
    try:
        d=requests.get(url,timeout=30).json()
        return {int(x["date"]):x["value"] for x in (d[1] or []) if x.get("value") is not None}
    except: return {}

P = dict(kX=1.0,kZ=0.3,kL=1.5,beta=0.6,b0=0.12,bG=0.003,Y0=1.0,wU=0.5,wC=0.5)
COUNTRIES = [
    ("USA","US",False),("Japan","JP",False),("Argentina","AR",False),("Greece","GR",False),
    ("SouthKorea","KR",True),("Mexico","MX",True),("Turkey","TR",True),("Indonesia","ID",True),
    ("Thailand","TH",True),("Brazil","BR",True),("Chile","CL",True),("Russia","RU",True),
    ("India","IN",True),("SouthAfrica","ZA",True),
]
rows=[]
for name, cc, use_gdp in COUNTRIES:
    if use_gdp:
        df = pd.read_csv(os.path.join(OOS,f"{name}.csv"), index_col="Year").ffill().bfill()
        df = df.rename(columns={"Military":"Military_pct"}); df["Military"]=df["Military_pct"]/100
        df = df.rename(columns={"Patent":"Patent"}); df["EduRate"]=df["EduRate"]
        df["Arable"]=df["Arable"]
        years = df.index.to_numpy(int)
    else:
        df = pd.read_excel(os.path.join(BASE,f"SECM_V24_{name}.xlsx"), sheet_name=0).ffill()
        wb = pd.read_csv(os.path.join(WB,f"wb_{name}.csv"), index_col="Year")
        df = df.join(wb, on="Year", how="left").ffill().bfill()
        df = df.rename(columns={"PatentCount":"Patent","MilitaryRatio":"Military","ArableLandTotal":"Arable"})
        years = df["Year"].to_numpy(int)
    G = model(df, P)
    hom = fetch_homicide(cc)
    gv=[]; hv=[]
    for i,y in enumerate(years):
        if y in hom and not np.isnan(G[i]):
            gv.append(G[i]); hv.append(hom[y])
    r = float(np.corrcoef(gv,hv)[0,1]) if len(gv)>=8 else float('nan')
    rows.append((name,len(gv),r))
    print(f"{name:12s} n={len(gv):3d}  r={r:+.3f}" if not np.isnan(r) else f"{name:12s} n={len(gv):3d}  r=NaN(样本不足)")
valid=[r for _,_,r in rows if not np.isnan(r)]
print(f"\n平均 G↔凶杀率 相关: {np.mean(valid):+.3f} (跨{len(valid)}国)")
print(f"正相关国家数: {sum(1 for r in valid if r>0)}/{len(valid)}")
