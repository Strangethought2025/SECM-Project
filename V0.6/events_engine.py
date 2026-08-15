# -*- coding: utf-8 -*-
"""社会事件引擎: 曲线定时机/密度/严重度(G_disp), 事件库定内容, 真实锚点校验.
玩家看不到曲线, 只看到事件流. 事件≠骚乱: 大头是治安/教育/健康/经济/阶级距离/治理变难.
用法: py events_engine.py UK [年数]  (默认全部年份)
"""
import pandas as pd, numpy as np, os, io, sys, json, hashlib
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
from secm_model import compute, calibrate
HERE = os.path.dirname(os.path.abspath(__file__))
def load_P(profile="B"):
    """画像A: 校准+验证满分(可读性~1.1, 事件流平淡); 画像B: 尖峰版(可读性~20x, 危机年事件爆炸, 适合游戏)"""
    fn = "best_params.json" if profile=="A" else "best_params_spiky.json"
    return json.load(open(os.path.join(HERE,fn),encoding="utf-8"))
LIB = json.load(open(os.path.join(HERE,"event_library.json"),encoding="utf-8"))
REAL = json.load(open(os.path.join(HERE,"uk_events_real.json"),encoding="utf-8"))
TUNE_EV = {"USA":[1987,2001,2008,2020],"Argentina":[1982,1989,2001,2014,2020],
    "Mexico":[1982,1994,2008,2020],"Turkey":[1994,2001,2018,2020],
    "Russia":[1998,2008,2015,2020,2022],"Greece":[2010,2012,2020]}
VAL_EV = {"UK":[2008,2020],"Spain":[2008,2012,2020],"Portugal":[2011,2020],
    "Ireland":[2008,2010,2020],"Cyprus":[2013,2020],"Iceland":[2008,2020],"Brazil":[2015,2020],
    "Ukraine":[2009,2014,2020,2022],"Venezuela":[2013,2016,2020],"Egypt":[2011,2016,2020],
    "Pakistan":[2008,2019,2022],"SriLanka":[2022],"Ghana":[2022],"Lebanon":[2019,2020]}
CITIES = {"UK":["伦敦","曼彻斯特","伯明翰","格拉斯哥","利兹","利物浦","谢菲尔德"],
          "USA":["纽约","洛杉矶","芝加哥","底特律","费城","巴尔的摩"],
          "Spain":["马德里","巴塞罗那","瓦伦西亚","塞维利亚"],
          "default":["首都圈","工业城市","港口城市","大学城","北部城镇","卫星城"]}
SEV_LABEL = {1:"轻微",2:"一般",3:"严重",4:"非常严重",5:"爆发"}

def global_S(P):
    evG=[]
    for folder,EVS in [("tune",TUNE_EV),("oos2000",VAL_EV)]:
        for name,ev in EVS.items():
            df=pd.read_csv(os.path.join(HERE,folder,f"{name}.csv"),index_col="Year").ffill().bfill()
            yrs,Y,Yl=compute(df,P); yf,yls=calibrate(yrs,Y,Yl,ev[0]); G=yf*Y-yls*Yl
            for e in ev:
                if e in yrs: evG.append(G[np.where(yrs==e)[0][0]])
    return 1.0/float(np.median(evG))

S = global_S(load_P("B"))

def band_of(g): return "安全" if g<0 else ("紧张" if g>1 else "承压")

def expected_events(g):
    if g<0: return 1.2
    if g<=1: return 1.5+5.0*g
    return 6.5+12.0*((g-1)**1.5)

def pick_category(rng, band):
    cats=[]; ws=[]
    for c,cfg in LIB.items():
        if c.startswith("_"): continue
        w=cfg["权重"].get(band,0.0)
        if w>0: cats.append(c); ws.append(w)
    ws=np.array(ws,float); ws/=ws.sum()
    return cats[int(rng.choice(len(cats),p=ws))]

def fill(tpl, rng, sev, year, city, nums=None):
    def xnum(k):
        if nums is None: lo,hi=5+4*sev,20+9*sev
        elif isinstance(nums[0],list): lo,hi=nums[k]
        else: lo,hi=nums
        return str(int(rng.integers(lo,hi)))
    s=tpl; k=0
    while "{X}" in s:
        s=s.replace("{X}",xnum(k),1); k+=1
    s=s.replace("{city}",city).replace("{year}",str(year))
    return s

def gen_year(rng, year, g, city_list, state):
    band=band_of(g)
    lam=expected_events(g)
    n=min(int(rng.poisson(lam)),25)
    out=[]; used=set()
    for _ in range(n):
        cat=pick_category(rng,band)
        if cat=="骚乱类":                      # 现实频率≈1次/5年
            if year-state["last_riot"]<2: continue
        elif cat=="爆发类":                    # 金融/政治爆发≈1次/10年+
            if year-state["last_boom"]<5: continue
        cfg=LIB[cat]
        cand=[t for t in cfg["模板"] if band in t[3]]
        avail=[t for t in cand if id(t) not in used]
        if not avail: continue
        tpl=avail[int(rng.integers(len(avail)))]; used.add(id(tpl))
        lo,hi=tpl[1],tpl[2]
        sev=int(np.clip(round(1+1.2*g+rng.normal(0,0.6)),lo,hi))
        city=str(rng.choice(city_list))
        out.append((cat,sev,fill(tpl[0],rng,sev,year,city,tpl[4] if len(tpl)>4 else None)))
        if cat=="骚乱类": state["last_riot"]=year
        elif cat=="爆发类": state["last_boom"]=year
    out.sort(key=lambda x:-x[1])
    return out

def run(name, folder="oos2000", show_real=True, max_years=None, profile="B"):
    P=load_P(profile); S=global_S(P)
    df=pd.read_csv(os.path.join(HERE,folder,f"{name}.csv"),index_col="Year").ffill().bfill()
    ev=VAL_EV.get(name,TUNE_EV.get(name,[df.index[-1]]))
    yrs,Y,Yl=compute(df,P); yf,yls=calibrate(yrs,Y,Yl,ev[0]); G=yf*Y-yls*Yl
    Gd=S*G
    seed=int(hashlib.md5(name.encode()).hexdigest()[:8],16)
    cities=CITIES.get(name,CITIES["default"])
    years=yrs if max_years is None else yrs[-max_years:]
    state={"last_riot":-99,"last_boom":-99}
    print(f"== {name} 事件流 (画像{profile}, 显示增益S={S:.2f}) ==")
    for i,y in enumerate(yrs):
        if y not in years: continue
        rng=np.random.default_rng(seed+y*7919)
        g=Gd[i]; band=band_of(g)
        evs=gen_year(rng,int(y),g,cities,state)
        print(f"{y} G_disp={g:+.2f} [{band}] 事件{len(evs)}条:")
        for cat,sev,txt in evs:
            print(f"   [{sev}·{cat}] {txt}")
        if show_real and str(y) in REAL:
            for r in REAL[str(y)]:
                print(f"   [真实锚点] {r['text']}  ({r['source']})")
        print()

if __name__=="__main__":
    name=sys.argv[1] if len(sys.argv)>1 else "UK"
    max_years=int(sys.argv[2]) if len(sys.argv)>2 else None
    profile=sys.argv[3] if len(sys.argv)>3 else "B"
    run(name, max_years=max_years, profile=profile)
