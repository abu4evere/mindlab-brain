"""W2's learning brains (questions.md, W2-frozen).

  MapVIN  V+ (W1e's plus-shaped VIN, K = 30, max), on a 3-channel map (known wall, unknown, food). The map changes
          during an episode, so the planner runs on every distinct map; in learning, all the episode's maps are planned
          in one batch (the same arithmetic as one map at a time).
  RNet    the learned memory: the 3 x 3 view (9), its cell (11 + 11), the food's cell (11 + 11), the food's offset (2)
          -> 64 tanh with an Elman state -> 5 action scores and a value. (A convolution on a 3 x 3 view is a dense layer
          on its 9 cells, so W1c's convolution reduces to this.) Truncated backprop through time, 16 steps.
"""
from __future__ import annotations

import sys
from pathlib import Path

import numpy as np
from numpy.lib.stride_tricks import sliding_window_view

HERE = Path(__file__).parent
sys.path.insert(0, str(HERE.parent / "W1d"))
import vin as V  # noqa: E402

B1 = V.B1
N, A, C = V.N, V.A, 3


def cols(m):
    """im2col for a batch of maps (T, Cin, N, N), padding 1 -> (T*N*N, Cin*9)."""
    T, ci = m.shape[0], m.shape[1]
    mp = np.pad(m, ((0, 0), (0, 0), (1, 1), (1, 1)))
    win = sliding_window_view(mp, (3, 3), axis=(2, 3))          # (T, Cin, N, N, 3, 3)
    return win.transpose(0, 2, 3, 1, 4, 5).reshape(T * N * N, ci * 9)


def uncols(d, T):
    """The gradient of (T*N*N, 9) one-channel columns back onto the (T, N, N) maps."""
    out = np.zeros((T, N + 2, N + 2))
    dc = d.reshape(T, N, N, 3, 3)
    for ky in range(3):
        for kx in range(3):
            out[:, ky:ky + N, kx:kx + N] += dc[:, :, :, ky, kx]
    return out[:, 1:-1, 1:-1]


class MapVIN:
    rec = False

    def __init__(self, seed, K=30):
        r = np.random.default_rng(seed)
        self.K = K
        self.mask = np.ones((A, 1, 3, 3))
        self.mask[:, :, [0, 0, 2, 2], [0, 2, 0, 2]] = 0.0
        self.p = {"Wr": r.normal(0, 0.3, (1, C, 3, 3)), "br": np.zeros(1),
                  "Wq": r.normal(0, 0.3, (A, 1, 3, 3)), "Wv": r.normal(0, 0.3, (A, 1, 3, 3)),
                  "Wo": r.normal(0, 0.3, (5, A)), "bo": np.zeros(5), "wv": r.normal(0, 0.1, A), "bv": np.zeros(1)}
        self.p["Wv"] = self.p["Wv"] * self.mask
        self.reset()

    def reset(self):
        self.key, self.fw = None, None

    def plan(self, maps):
        """maps (T, C, N, N) -> the forward trace; q of every cell of every map is fw[3] (T*N*N, A)."""
        p, T = self.p, maps.shape[0]
        c_x = cols(maps)
        r = (c_x @ p["Wr"].reshape(1, C * 9).T).ravel() + p["br"][0]
        c_r = cols(r.reshape(T, 1, N, N))
        Rq = c_r @ p["Wq"].reshape(A, 9).T
        q, trace, idx = Rq, [], np.arange(T * N * N)
        Wv9 = p["Wv"].reshape(A, 9).T
        for _ in range(self.K - 1):
            am = q.argmax(1)
            c_v = cols(q[idx, am].reshape(T, 1, N, N))
            trace.append((c_v, am))
            q = Rq + c_v @ Wv9
        return (T, c_x, c_r, trace, q)

    def step(self, maps, pos):
        """One map (C, N, N) and the brain's cell index -> (None, pos, logits, value)."""
        key = maps.tobytes()
        if key != self.key:
            self.fw, self.key = self.plan(maps[None]), key
        qa = self.fw[4][pos]
        return None, pos, self.p["Wo"] @ qa + self.p["bo"], float(self.p["wv"] @ qa + self.p["bv"][0])

    def backprop(self, fw, poss, dlogits, dvals):
        """Gradients for a whole episode (fw = plan(maps)): step t read map t at cell poss[t]."""
        p = self.p
        T, c_x, c_r, trace, q = fw
        g = {k: np.zeros_like(v) for k, v in p.items()}
        rows = np.arange(T) * N * N + np.asarray(poss)
        qa = q[rows]                                              # (T, A)
        dl, dv = np.asarray(dlogits), np.asarray(dvals, float)
        g["Wo"] += dl.T @ qa
        g["bo"] += dl.sum(0)
        g["wv"] += dv @ qa
        g["bv"] += dv.sum()
        dq = np.zeros((T * N * N, A))
        np.add.at(dq, rows, dl @ p["Wo"] + dv[:, None] * p["wv"][None, :])
        dRq = np.zeros_like(dq)
        Wv9 = p["Wv"].reshape(A, 9)
        idx = np.arange(T * N * N)
        for c_v, am in reversed(trace):
            dRq += dq
            g["Wv"] += (dq.T @ c_v).reshape(A, 1, 3, 3)
            dv_map = uncols(dq @ Wv9, T).ravel()
            dq = np.zeros((T * N * N, A))
            dq[idx, am] = dv_map
        dRq += dq
        g["Wv"] *= self.mask
        g["Wq"] += (dRq.T @ c_r).reshape(A, 1, 3, 3)
        dr = uncols(dRq @ p["Wq"].reshape(A, 9), T).ravel()
        g["Wr"] += (dr @ c_x).reshape(1, C, 3, 3)
        g["br"] += dr.sum()
        return g

    def imitate(self, maps, poss, acts):
        """One imitation update: cross-entropy toward the teacher's action at every step."""
        fw = self.plan(maps)
        rows = np.arange(len(poss)) * N * N + np.asarray(poss)
        z = fw[4][rows] @ self.p["Wo"].T + self.p["bo"]
        e = np.exp(z - z.max(1, keepdims=True))
        d = e / e.sum(1, keepdims=True)
        d[np.arange(len(acts)), acts] -= 1.0
        self.apply(self.backprop(fw, poss, d, np.zeros(len(acts))))

    def apply(self, g):
        n = float(np.sqrt(sum(float((v * v).sum()) for v in g.values())))
        s = min(1.0, B1.CLIP / n) if n > 0 else 1.0
        for k in self.p:
            self.p[k] -= B1.LR * s * g[k]


H, NIN = 64, 55


def r_input(env_walls, pos, goal):
    """R's input: the 3 x 3 view (1 = wall or outside), its cell, the food's cell, the food's offset / 10."""
    v = [1.0 if V.W.blocked(env_walls, pos[0] + dx, pos[1] + dy) else 0.0 for dy in (-1, 0, 1) for dx in (-1, 0, 1)]
    x = np.zeros(NIN)
    x[:9] = v
    x[9 + pos[0]] = 1.0
    x[20 + pos[1]] = 1.0
    x[31 + goal[0]] = 1.0
    x[42 + goal[1]] = 1.0
    x[53], x[54] = (goal[0] - pos[0]) / 10.0, (goal[1] - pos[1]) / 10.0
    return x


class RNet:
    """W1's Elman network (the same arithmetic), 55 inputs and 64 units."""
    rec = True

    def __init__(self, seed):
        r = np.random.default_rng(seed)
        self.p = {"Wx": r.normal(0, 0.1, (H, NIN)), "b": np.zeros(H), "Wa": r.normal(0, 0.1, (5, H)),
                  "ba": np.zeros(5), "Wv": r.normal(0, 0.1, H), "bv": np.zeros(1), "Wh": r.normal(0, 0.1, (H, H))}
        self.reset()

    def reset(self):
        self.h = np.zeros(H)

    def step(self, x):
        p = self.p
        hp = self.h
        self.h = np.tanh(p["Wx"] @ x + p["b"] + p["Wh"] @ hp)
        return hp, self.h, p["Wa"] @ self.h + p["ba"], float(p["Wv"] @ self.h + p["bv"][0])

    def backward(self, xs, hps, hs, dlogits, dvals):
        p = self.p
        g = {k: np.zeros_like(v) for k, v in p.items()}
        dh_next = np.zeros(H)
        for t in reversed(range(len(xs))):
            g["Wa"] += np.outer(dlogits[t], hs[t])
            g["ba"] += dlogits[t]
            g["Wv"] += dvals[t] * hs[t]
            g["bv"] += dvals[t]
            dh = p["Wa"].T @ dlogits[t] + dvals[t] * p["Wv"]
            if (t + 1) % B1.TRUNC != 0:
                dh = dh + dh_next
            dpre = dh * (1.0 - hs[t] ** 2)
            g["Wx"] += np.outer(dpre, xs[t])
            g["b"] += dpre
            g["Wh"] += np.outer(dpre, hps[t])
            dh_next = p["Wh"].T @ dpre
        return g

    apply = MapVIN.apply
