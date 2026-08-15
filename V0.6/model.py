# -*- coding: utf-8 -*-
"""SECM V0.6 历史验证器 —— 核心模型（改进版 v4）
关键修复：Ylimit 由"能源周期"(PE+AP, 衰退下探)驱动，Y 由"全量产能趋势"累加。
"""
import pandas as pd
import numpy as np

def sign_log(z):
    return np.sign(z) * np.log(1 + np.abs(z))

def mov_avg(x, w):
    s = pd.Series(x).rolling(w, center=True, min_periods=1).mean().to_numpy()
    return s

def compute(df, p):
    pop = df["Population"].to_numpy(float)
    pe  = df["PrimaryEnergy"].to_numpy(float)
    ap  = df["AnimalPower"].to_numpy(float)
    edu = df["EduRate"].to_numpy(float)
    gini = df["Gini"].to_numpy(float)
    mil = df["MilitaryRatio"].to_numpy(float)
    arable = df["ArableLandTotal"].to_numpy(float)
    patent = df["PatentCount"].to_numpy(float)
    tfp = df["TFPGrowth"].to_numpy(float)
    n = len(df)

    # X 全量（趋势，含人力项，平滑）
    X_full = pe + ap + pop * 130.0 / 1e6
    Xn = X_full / (X_full[0] if X_full[0] > 0 else 1.0)
    dX = np.diff(Xn, prepend=Xn[0])

    # X 能源（周期，衰退年会下探）
    Xe = pe + ap
    Xe_norm = Xe / (Xe[0] if Xe[0] > 0 else 1.0)
    Xe_trend = mov_avg(Xe_norm, p.get("win", 5))
    cycle = Xe_norm / np.maximum(Xe_trend, 1e-6)   # 衰退<1, 繁荣>1

    # Z 四因代理 + 平滑（慢创新周期）
    pg = np.zeros(n)
    for t in range(1, n):
        pr = patent[t-1] if patent[t-1] > 0 else 1.0
        pg[t] = np.clip((patent[t] - patent[t-1]) / pr, -1, 1)
    edu_n = edu / (np.nanmax(edu) if np.nanmax(edu) > 0 else 1.0)
    z_raw = 0.25 * pg + 0.8 * tfp + 0.15 * (0.4 - gini/100.0) + 0.05 * (edu_n - 0.5)
    Z = np.clip(mov_avg(z_raw, 3), -0.5, 0.5)
    fZ = sign_log(Z)

    # 土地压力
    kwpe = X_full * 1e6 / pop
    popP = np.clip((pop / arable) / (kwpe / 15.0), 0, 3)

    # Y：累加全量趋势 + 加法式 Z 缓解
    Y = np.zeros(n); Y[0] = p["Y0"]
    for t in range(1, n):
        Y[t] = Y[t-1] + p["kX"] * dX[t] * (1 + popP[t]) + p["kZ"] * fZ[t]

    # Ylimit：长期趋势(β<1) × 能源周期(衰退下探) × 军事两难 − 增长负担
    t = np.arange(n)
    Yl = (p["kL"] * (Xn ** p["beta"]) * cycle * (1 - mil)
          - p["b0"] * (1 + p["bG"] * t))

    return Y, Yl, Y - Yl, Z, cycle, Xn
