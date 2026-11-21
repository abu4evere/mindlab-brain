"""Exploratory: MoveVIN's planning loop compiled with Numba (run in the separate environment D:\\venvs\\numba_lab only;
never in the Python that runs the frozen studies). Compares speed and agreement with brain_mv.MoveVIN.

  D:\\venvs\\numba_lab\\Scripts\\python numba_mv.py
"""
import sys
import time
from pathlib import Path

import numpy as np
from numba import njit

HERE = Path(__file__).parent
sys.path.insert(0, str(HERE.parent))
sys.path.insert(0, str(HERE.parents[1] / "W3"))
import brain_mv as M  # noqa: E402

N, K = M.N, M.K
DX = np.array([0, 0, 1, -1])
DY = np.array([-1, 1, 0, 0])


@njit(cache=True)
def plan_k(r, pas, gam, K):
    T, N, _ = r.shape
    V = np.empty((K + 1, T, N, N))
    AM = np.empty((K, T, N, N), np.int8)
    q = np.empty((5, T, N, N))
    V[0] = r
    for k in range(K):
        for t in range(T):
            for y in range(N):
                for x in range(N):
                    v0 = V[k, t, y, x]
                    best, ba = -1e300, 0
                    for a in range(5):
                        if a == 4:
                            m = v0
                        else:
                            nx, ny = x + DX[a], y + DY[a]
                            if 0 <= nx < N and 0 <= ny < N:
                                p = pas[t, ny, nx]
                                m = p * V[k, t, ny, nx] + (1.0 - p) * v0
                            else:
                                m = v0
                        qa = r[t, y, x] + gam * m
                        if k == K - 1:
                            q[a, t, y, x] = qa
                        if qa > best:
                            best, ba = qa, a
                    V[k + 1, t, y, x] = best
                    AM[k, t, y, x] = ba
    return V, AM, q


@njit(cache=True)
def back_k(dq_last, dv_last, r, pas, gam, V, AM, K):
    T, N, _ = r.shape
    dr = np.zeros((T, N, N))
    dpas = np.zeros((T, N, N))
    dgam = 0.0
    dv = dv_last.copy()
    for k in range(K - 1, -1, -1):
        dvp = np.zeros((T, N, N))
        for t in range(T):
            for y in range(N):
                for x in range(N):
                    v0 = V[k, t, y, x]
                    for a in range(5):
                        g = dq_last[a, t, y, x] if k == K - 1 else 0.0
                        if AM[k, t, y, x] == a:
                            g += dv[t, y, x]
                        if g == 0.0:
                            continue
                        dr[t, y, x] += g
                        if a == 4:
                            dgam += g * v0
                            dvp[t, y, x] += gam * g
                        else:
                            nx, ny = x + DX[a], y + DY[a]
                            if 0 <= nx < N and 0 <= ny < N:
                                p = pas[t, ny, nx]
                                vn = V[k, t, ny, nx]
                                dgam += g * (p * vn + (1.0 - p) * v0)
                                dvp[t, y, x] += gam * g * (1.0 - p)
                                dvp[t, ny, nx] += gam * g * p
                                dpas[t, ny, nx] += gam * g * (vn - v0)
                            else:
                                dgam += g * v0
                                dvp[t, y, x] += gam * g
        dv = dvp
    dr += dv
    return dr, dpas, dgam


rng = np.random.default_rng(4)
net = M.MoveVIN(2)
for k in net.p:
    net.p[k] = net.p[k] + rng.normal(0, 0.3, net.p[k].shape)
for T in (1, 64):
    maps = (rng.random((T, M.C, N, N)) < 0.3).astype(float)
    maps[:, 4] = rng.random((T, N, N))
    lev = rng.random((T, 3))
    fw = net.plan(maps, lev)
    r, pas, gam, q_ref, v_ref = fw[3], fw[4], fw[6], fw[8], fw[9]
    V, AM, q = plan_k(r, pas, gam, K)                      # compile
    print(f"T={T}: plan agrees (max |q diff| {np.abs(q - q_ref).max():.1e}, argmax same "
          f"{bool((q.argmax(0) == q_ref.argmax(0)).all())})")
    t0 = time.time(); n = 200 if T == 1 else 20
    for _ in range(n):
        net.plan(maps, lev)
    t_np = (time.time() - t0) / n
    t0 = time.time()
    for _ in range(n):
        plan_k(r, pas, gam, K)
    t_nb = (time.time() - t0) / n
    print(f"   planning loop: numpy MoveVIN (whole plan) {t_np * 1000:.2f} ms, numba loop {t_nb * 1000:.3f} ms")
    rows = np.arange(T) * N * N + rng.integers(0, N * N, T)
    dl, dvv = rng.normal(size=(T, 5)), rng.normal(size=T)
    g_ref = net.backprop(fw, rows, dl, dvv)
    beta = np.exp(net.p["lb"][0])
    dq = np.zeros((5, T * N * N)); np.add.at(dq.T, rows, beta * dl)
    dvl = np.zeros(T * N * N); np.add.at(dvl, rows, net.p["wv"][0] * dvv)
    dr, dpas, dgam = back_k(dq.reshape(5, T, N, N), dvl.reshape(T, N, N), r, pas, gam, V, AM, K)
    g_nb_g = dgam * gam * (1 - gam)
    print(f"   backprop agrees: d gamma {g_nb_g:.6e} vs {g_ref['g'][0]:.6e}")
    t0 = time.time()
    for _ in range(n):
        net.backprop(fw, rows, dl, dvv)
    t_bnp = (time.time() - t0) / n
    t0 = time.time()
    for _ in range(n):
        back_k(dq.reshape(5, T, N, N), dvl.reshape(T, N, N), r, pas, gam, V, AM, K)
    t_bnb = (time.time() - t0) / n
    print(f"   backprop: numpy {t_bnp * 1000:.2f} ms, numba loop {t_bnb * 1000:.3f} ms")
