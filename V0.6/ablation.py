# -*- coding: utf-8 -*-
"""消融实验：逐个关闭模块，看命中率掉多少（10样本外国，GDP作X）"""
import pandas as pd, numpy as np, os, io, sys
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
OOS = r"E:\AI-Personal\SECM-Project\V0.6\oos"
CRISIS = {"SouthKorea":[1997],"Mexico":[1982,1994],"Turkey":[2000,2001],"Indonesia":[1997],
          "Thailand":[1997],"Brazil":[1983,1990,1994],"Chile":[1982],"Russia":[1998],
          "India":[1991],"SouthAfrica":[]}
def sign_log(z): return np.sign(z)*np.log(1+np.abs(z))
def mov_avg(x,w): return pd.Series(x).rolling(w,center=True,min_periods=1).mean().to_numpy()

def run(f, P, on):
    df = pd.read_csv(os.path.join(OOS,f), index_col="Year").ffill().bfill()
    pop=df["Population"].to_numpy(float); gdp=df["GDP"].to_numpy(float)
    patent=df["Patent"].to_numpy(float); edu=df["EduRate"].to_numpy(float)
    gini=df["Gini"].to_numpy(float); mil=df["Military"].to_numpy(float)/100
    arable=df["Arable"].to_numpy(float); unemp=df["unemployment"].to_numpy(float)
    mcap=df["mcap_gdp"].to_numpy(float)
    Xn=gdp/gdp[0]; dX=np.diff(Xn,prepend=Xn[0])
    pg=np.zeros(len(df))
    for t in range(1,len(df)):
        pr=patent[t-1] if patent[t-1]>0 else 1.0
        pg[t]=np.clip((patent[t]-patent[t-1])/pr,-1,1)
    edu_n=edu/np.nanmax(edu) if np.nanmax(edu)>0 else edu
    Z=np.clip(mov_avg(0.5*pg+0.3*(edu_n-0.5)+0.2*(0.4-gini/100),3),-0.5,0.5)
    fZ=sign_log(Z) if on["Z"] else np.zeros(len(df))
    popP=np.zeros(len(df))
    if on["land"] and np.nanmax(arable)>0:
        popP=np.clip((pop/arable)/np.nanmedian(pop/arable)-1,0,3)
    Y=np.zeros(len(df)); Y[0]=P["Y0"]
    for t in range(1,len(df)): Y[t]=Y[t-1]+P["kX"]*dX[t]*(1+popP[t])+P["kZ"]*fZ[t]
    fstress=np.zeros(len(df))
    if on["fin"]:
        u_norm=unemp/np.nanmax(unemp); mg=np.zeros(len(df))
        for t in range(1,len(df)):
            pr=mcap[t-1] if mcap[t-1]>0 else 1.0
            mg[t]=np.clip((mcap[t]-mcap[t-1])/pr,-1,1)
        fstress=np.clip(P["wU"]*u_norm+P["wC"]*np.clip(-mg,0,1),0,0.8)
    t=np.arange(len(df))
    mil_term = mil if on["mil"] else np.zeros(len(df))
    bg = P["bG"] if on["burden"] else 0.0
    Yl=P["kL"]*(Xn**P["beta"])*(1-mil_term)*(1-fstress)-P["b0"]*(1+bg*t)
    return df.index.to_numpy(int), Y-Yl

def sig_peaks(years,G,w=5,thresh=0.06):
    base=mov_avg(G,w); out=[]
    for t in range(1,len(G)-1):
        if G[t]>=G[t-1] and G[t]>=G[t+1] and G[t]>0 and (G[t]-base[t])>thresh: out.append(int(years[t]))
    return out

P = dict(kX=1.0,kZ=0.3,kL=1.5,beta=0.6,b0=0.12,bG=0.003,Y0=1.0,wU=0.5,wC=0.5)
ALL=dict(Z=True,land=True,fin=True,mil=True,burden=True)

def score(on):
    tot_hit=tot_ev=0
    for name in CRISIS:
        yrs,G=run(name+".csv",P,on); pk=sig_peaks(yrs,G)
        hits=[e for e in CRISIS[name] if any(abs(e-p)<=1 for p in pk)]
        tot_hit+=len(hits); tot_ev+=len(CRISIS[name])
    return tot_hit,tot_ev

base_h,base_e=score(ALL)
print(f"完整模型: {base_h}/{base_e}")
ablas = {
    "无金融压力": dict(ALL, fin=False),
    "无创新Z":    dict(ALL, Z=False),
    "无土地压力": dict(ALL, land=False),
    "无军事两难": dict(ALL, mil=False),
    "无固定负担": dict(ALL, burden=False),
}
for name,on in ablas.items():
    h,e=score(on)
    print(f"{name:8s}: {h}/{e}  (比完整 -{base_h-h})")
