# -*- coding: utf-8 -*-
"""G函数计算模块: 由 Y/Ylimit 距离(G) 连续导出 问题量(事件频率) 与 事件类型分布(按严重分数排行表偏移)
核心公式:
  λ(G)  = 1 + 19·σ((G−0.2)/0.4)            # 事件频率: G单调上升, -0.3比-0.8多, 3比0多
  p_c(G) ∝ w_c · exp(θ·s_c·G)              # 类型概率: 严重分数s_c越高, G越大越被选中
  sev    = clip(round(1+1.2G+N(0,0.6)), lo, hi)
"""
import numpy as np, json, os

LMAX=20.0; G0=0.2; S=0.4; THETA=0.12

# 事件类型严重分数排行表 (分数越高: G越大时被选中概率越往这里偏移)
CATEGORY_SCORES = {
    "缓和类":        1.0,
    "无序与集体犯罪": 1.5,
    "家庭与社会":     2.0,
    "治安":           2.3,
    "教育退化":       2.5,
    "健康压力":       2.6,
    "治理变难":       2.7,
    "经济紧张":       2.8,
    "阶级距离":       3.0,
    "政治与制度":     3.2,
    "骚乱类":         5.0,
    "爆发类":         5.5,
}

def sigmoid(x): return 1.0/(1.0+np.exp(-x))

def lambda_G(G, D=1.0):
    """年事件期望数: G 单调上升. D=难度系数: 1.0=现实(最高难度), 0.4=简单.
    G=-0.8→2.4条, -0.3→5.2, 0→8.2, 1→17.7, 3→20 (D=1.0时)"""
    return 1.0 + D*(LMAX-1.0)*sigmoid((G-G0)/S)

def base_weight(cfg):
    """以'承压'带权重为基准权重(G=0附近的参考值)"""
    w=cfg.get("权重",{})
    return float(w.get("承压", w.get("安全", w.get("紧张", 0.0))))

def type_probs(G, lib, D=1.0):
    """事件类型概率分布: p_c ∝ w_c·exp(D·θ·s_c·G). G越高, 高分数(严重)类型越被抬升.
    D<1 时偏移减弱 → 低难度下严重类型不轻易出现"""
    cats=[]; ws=[]
    for c,cfg in lib.items():
        if c.startswith("_"): continue
        w=base_weight(cfg)
        if w<=0: continue
        s=CATEGORY_SCORES.get(c,2.5)
        cats.append(c); ws.append(w*np.exp(D*THETA*s*G))
    ws=np.array(ws,float); ws/=ws.sum()
    return cats, ws

def sample_severity(rng, G, lo, hi, D=1.0):
    """严重度抽样: G越高越严重; D<1 时整体降档"""
    return int(np.clip(round(1+1.2*G*(0.4+0.6*D)+rng.normal(0,0.6)), lo, hi))

if __name__=="__main__":
    import io, sys
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
    print("== λ(G) 事件频率函数 ==")
    for G in [-2.0,-1.0,-0.8,-0.3,0.0,0.5,1.0,2.0,3.0,5.0]:
        print(f"  G={G:+5.1f} → λ={lambda_G(G):5.1f} 条/年")
    print("\n== 事件类型严重分数排行表 ==")
    rank=sorted(CATEGORY_SCORES.items(), key=lambda x:-x[1])
    for c,s in rank: print(f"  {s:4.1f}  {c}")
    print("\n== 类型分布随G偏移示例 (p_c) ==")
    lib=json.load(open(os.path.join(os.path.dirname(os.path.abspath(__file__)),"event_library.json"),encoding="utf-8"))
    for G in [-1.0,0.0,1.0,3.0]:
        cats,ws=type_probs(G,lib)
        top=sorted(zip(cats,ws),key=lambda x:-x[1])[:6]
        print(f"  G={G:+.1f}: " + ", ".join(f"{c}{w*100:.0f}%" for c,w in top))
