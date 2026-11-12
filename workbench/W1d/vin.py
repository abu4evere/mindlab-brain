"""W1d's value iteration network (Tamar et al. 2016), NumPy only, on W1b's 11 x 11 map.

Reward map r = 3x3 conv of the map (walls, food) + bias. Then q = conv(r; Wq) [+ conv(v; Wv)], v = max over the A
channels, K times in all. The agent's cell's q (A numbers) gives 5 action scores and a value.

The map does not change within an episode, so the planning part runs once per episode and each step reads the
agent's cell. It plugs into W1's learning code: step(x) -> (None, pos, logits, value); backward(xs, hps, hs, dlogits,
dvals) -> gradients; apply(g). x is W1b's full-view observation (walls, self, food).
"""
from __future__ import annotations

import sys
from pathlib import Path

import numpy as np
from numpy.lib.stride_tricks import sliding_window_view

HERE = Path(__file__).parent
sys.path.insert(0, str(HERE.parent / "W1b"))
sys.path.insert(0, str(HERE.parent / "W1"))
import brains as B1  # noqa: E402
import world_b as W  # noqa: E402

N = W.N
A = 8                       # action channels in the planner


def cols(m):
    """im2col for one or more maps (C, N, N), padding 1 -> (N*N, C*9)."""
    mp = np.pad(m, ((0, 0), (1, 1), (1, 1)))
    win = sliding_window_view(mp, (3, 3), axis=(1, 2))      # (C, N, N, 3, 3)
    return win.transpose(1, 2, 0, 3, 4).reshape(N * N, m.shape[0] * 9)


def uncols(d):
    """The gradient of (N*N, 9) one-channel columns back onto the (N, N) map."""
    out = np.zeros((N + 2, N + 2))
    dc = d.reshape(N, N, 3, 3)
    for ky in range(3):
        for kx in range(3):
            out[ky:ky + N, kx:kx + N] += dc[:, :, ky, kx]
    return out[1:-1, 1:-1]


class VIN:
    def __init__(self, seed, K, mode="max"):
        r = np.random.default_rng(seed)
        self.K = K
        self.mode = mode                                     # "max" (VIN) or "mean" (Vm: v = tanh(mean of q))
        self.rec = False
        self.p = {"Wr": r.normal(0, 0.3, (1, 2, 3, 3)), "br": np.zeros(1),
                  "Wq": r.normal(0, 0.3, (A, 1, 3, 3)), "Wv": r.normal(0, 0.3, (A, 1, 3, 3)),
                  "Wo": r.normal(0, 0.3, (5, A)), "bo": np.zeros(5), "wv": r.normal(0, 0.1, A), "bv": np.zeros(1)}
        self.reset()

    def reset(self):
        self.key = None
        self.fw = None

    def _forward(self, m):
        p = self.p
        c_x = cols(m)                                            # (121, 18)
        r = (c_x @ p["Wr"].reshape(1, 18).T).ravel() + p["br"][0]   # (121,)
        c_r = cols(r.reshape(1, N, N))                           # (121, 9)
        Rq = c_r @ p["Wq"].reshape(A, 9).T                       # (121, A)
        q = Rq
        trace = []                                               # per iteration: (columns of v, argmax of q before)
        for _ in range(self.K - 1):
            if self.mode == "max":
                am = q.argmax(1)
                v = q[np.arange(N * N), am]
            else:
                v = np.tanh(q.mean(1))
                am = v                                       # kept for the backward pass (1 - v^2)
            c_v = cols(v.reshape(1, N, N))
            trace.append((c_v, am))
            q = Rq + c_v @ p["Wv"].reshape(A, 9).T
        self.fw = (c_x, c_r, trace, q)

    def step(self, x):
        o = x.reshape(3, N, N)
        m = np.stack([o[0], o[2]])
        key = m.tobytes()
        if key != self.key:
            self._forward(m)
            self.key = key
        pos = int(np.argmax(o[1]))
        qa = self.fw[3][pos]
        return None, pos, self.p["Wo"] @ qa + self.p["bo"], float(self.p["wv"] @ qa + self.p["bv"][0])

    def backward(self, xs, hps, hs, dlogits, dvals):
        """hs holds the agent's cell index per step (all steps share one map within an episode)."""
        p = self.p
        g = {k: np.zeros_like(v) for k, v in p.items()}
        c_x, c_r, trace, q = self.fw
        dq = np.zeros((N * N, A))
        for pos, dl, dv in zip(hs, dlogits, dvals):
            qa = q[pos]
            g["Wo"] += np.outer(dl, qa)
            g["bo"] += dl
            g["wv"] += dv * qa
            g["bv"] += dv
            dq[pos] += p["Wo"].T @ dl + dv * p["wv"]
        dRq = np.zeros_like(dq)
        Wv9 = p["Wv"].reshape(A, 9)
        for c_v, am in reversed(trace):
            dRq += dq
            g["Wv"] += (dq.T @ c_v).reshape(A, 1, 3, 3)
            dv_map = uncols(dq @ Wv9).ravel()                    # (121,)
            dq = np.zeros((N * N, A))
            if self.mode == "max":
                dq[np.arange(N * N), am] = dv_map
            else:
                dq[:] = (dv_map * (1.0 - am ** 2) / A)[:, None]
        dRq += dq
        g["Wq"] += (dRq.T @ c_r).reshape(A, 1, 3, 3)
        dr = uncols(dRq @ p["Wq"].reshape(A, 9)).ravel()
        g["Wr"] += (dr @ c_x).reshape(1, 2, 3, 3)
        g["br"] += dr.sum()
        return g

    def apply(self, g):
        n = float(np.sqrt(sum(float((v * v).sum()) for v in g.values())))
        s = min(1.0, B1.CLIP / n) if n > 0 else 1.0
        for k in self.p:
            self.p[k] -= B1.LR * s * g[k]
