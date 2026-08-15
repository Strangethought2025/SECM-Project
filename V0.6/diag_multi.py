# -*- coding: utf-8 -*-
"""多国 Y/Ylimit 曲线诊断: 逐国打印紧张带段 + 关键年 Y/Yl + 对照真实危机史"""
import pandas as pd, numpy as np, os, io, sys, json
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
from secm_model import compute, calibrate
HERE = os.path.dirname(os.path.abspath(__file__))
PA = json.load(open(os.path.join(HERE,"best_params.json"),encoding="utf-8"))
PB = json.load(open(os.path.join(HERE,"best_params_spiky.json"),encoding="utf-8"))

# 国家: (文件夹, 首个事件, 真实危机史)
COUNTRIES = {
 "UK":       ("oos2000", 2008, "2008金融危机/2011骚乱/2016脱欧/2017-19刀犯罪/2020新冠/2022生活成本"),
 "France":   ("oos2000", 2005, "2005郊区骚乱/2015恐袭/2018-19黄背心/2023养老金骚乱"),
 "Germany":  ("oos2000", 2003, "2003-05哈茨抗议/2015难民危机/2017G20骚乱/2020新冠(总体温和)"),
 "Argentina":("tune",    1982, "1982债务/1989恶性通胀/2001大骚乱/2014违约/2018-19危机/2020(常年紧张)"),
 "Brazil":   ("oos2000", 2013, "2013百万游行/2015-16弹劾反腐/2018卡车罢工/2020新冠/2023暴动"),
 "USA":      ("tune",    1987, "1987股灾/1992洛杉矶/2001九一一/2008金融/2011占领/2016撕裂/2020BLM/2021国会山"),
 "Japan":    ("oos2000", 2008, "2008金融/2011福岛/2020新冠(1990s危机不在数据内; 失落的年代=长期停滞但有序)"),
 "Singapore":("oos2000", 1985, "1985衰退/1997亚洲金融/2003非典/2008/2020(高度有序, 承载力强)"),
 "Malaysia": ("oos2000", 1985, "1985衰退/1997亚洲金融+安华事件/1998资本管制/2008/2018政权更迭/2020喜来登政变"),
}

def global_S(P):
    evG=[]
    TUNE_EV={"USA":[1987,2001,2008,2020],"Argentina":[1982,1989,2001,2014,2020],
        "Mexico":[1982,1994,2008,2020],"Turkey":[1994,2001,2018,2020],
        "Russia":[1998,2008,2015,2020,2022],"Greece":[2010,2012,2020]}
    VAL_EV={"UK":[2008,2020],"Spain":[2008,2012,2020],"Portugal":[2011,2020],
        "Ireland":[2008,2010,2020],"Cyprus":[2013,2020],"Iceland":[2008,2020],"Brazil":[2015,2020],
        "Ukraine":[2009,2014,2020,2022],"Venezuela":[2013,2016,2020],"Egypt":[2011,2016,2020],
        "Pakistan":[2008,2019,2022],"SriLanka":[2022],"Ghana":[2022],"Lebanon":[2019,2020]}
    for folder,EVS in [("tune",TUNE_EV),("oos2000",VAL_EV)]:
        for name,ev in EVS.items():
            df=pd.read_csv(os.path.join(HERE,folder,f"{name}.csv"),index_col="Year").ffill().bfill()
            yrs,Y,Yl=compute(df,P); yf,yls=calibrate(yrs,Y,Yl,ev[0]); G=yf*Y-yls*Yl
            for e in ev:
                if e in yrs: evG.append(G[np.where(yrs==e)[0][0]])
    return 1.0/float(np.median(evG))

SA, SB = global_S(PA), global_S(PB)

def bands_of(yrs,Gd):
    segs=[]; start=None; prev=None
    for i in range(len(yrs)):
        b = "安全" if Gd[i]<0 else ("紧张" if Gd[i]>1 else "承压")
        if b!=prev:
            if start is not None: segs.append((start,yrs[i-1],prev))
            start=yrs[i]; prev=b
    if start is not None: segs.append((start,yrs[-1],prev))
    return segs

for name,(folder,first_ev,real) in COUNTRIES.items():
    df=pd.read_csv(os.path.join(HERE,folder,f"{name}.csv"),index_col="Year").ffill().bfill()
    print(f"\n=== {name} ({df.index[0]}-{df.index[-1]}) === 真实史: {real}")
    for tag,P,S in [("A",PA,SA),("B",PB,SB)]:
        yrs,Y,Yl=compute(df,P); yf,yls=calibrate(yrs,Y,Yl,first_ev); G=yf*Y-yls*Yl; Gd=S*G
        segs=bands_of(yrs,Gd)
        print(f" [{tag}] yf={yf:.2f} yls={yls:.2f} 紧张带段: " +
              ", ".join(f"{a}-{b}{c}" for a,b,c in segs))
        imax=int(np.argmax(Gd)); imin=int(np.argmin(Gd))
        print(f"      Y范围 {np.min(Y):.2f}~{np.max(Y):.2f} | Yl范围 {np.min(Yl):.2f}~{np.max(Yl):.2f}"
              f" | G最高 {yrs[imax]}年Gd={Gd[imax]:+.1f}(Y={Y[imax]:.2f}/Yl={Yl[imax]:.2f})"
              f" | G最低 {yrs[imin]}年Gd={Gd[imin]:+.1f}")
    # 画像B逐5年概览(只看B)
    yrs,Y,Yl=compute(df,PB); yf,yls=calibrate(yrs,Y,Yl,first_ev); G=yf*Y-yls*Yl; Gd=SB*G
    print(f" [B逐年] " + " ".join(
        f"{y}:{Gd[i]:+.1f}" for i,y in enumerate(yrs) if (y%5==0 or abs(Gd[i])>1.5)))
