"""W1c's networks: the egocentric view, a flat network on it (E), and a small convolutional network (C). NumPy only.
They plug into W1's learning code (brains.episode_ac, brains.episode_imit): step(x) -> (h_prev, h, logits, value),
backward(xs, hps, hs, dlogits, dvals) -> gradients, apply(g)."""
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

R = 10                      # egocentric window radius: 21 x 21 covers the whole 11 x 11 area from anywhere
S = 2 * R + 1
HID = 64


class EgoEnv(W.Env):
    """W1b's world, seen from the agent: two 21 x 21 channels (walls, food); cells outside the area are walls."""

    def obs(self):
        o = np.zeros((2, S, S))
        x0, y0 = self.pos
        for j in range(S):
            for i in range(S):
                x, y = x0 + i - R, y0 + j - R
                if W.blocked(self.walls, x, y):
                    o[0, j, i] = 1.0
                elif (x, y) == self.goal:
                    o[1, j, i] = 1.0
        return o.ravel()


class FlatNet(B1.Net):
    """E: W1's flat network, 882 inputs -> 64 tanh -> 5 action scores and a value."""

    def __init__(self, seed, n_in=2 * S * S):
        r = np.random.default_rng(seed)
        self.rec = False
        self.p = {"Wx": r.normal(0, 0.1, (HID, n_in)), "b": np.zeros(HID), "Wa": r.normal(0, 0.1, (5, HID)),
                  "ba": np.zeros(5), "Wv": r.normal(0, 0.1, HID), "bv": np.zeros(1)}

    def reset(self):
        self.h = np.zeros(HID)

    def backward(self, xs, hps, hs, dlogits, dvals):
        keep = B1.H
        B1.H = HID
        try:
            return super().backward(xs, hps, hs, dlogits, dvals)
        finally:
            B1.H = keep


class ConvNet:
    """C: conv 3x3 (2 -> 8, padding 1) + ReLU; conv 3x3 stride 2 (8 -> 8) + ReLU (21 -> 10); 800 -> 64 tanh; heads."""

    def __init__(self, seed):
        r = np.random.default_rng(seed)
        self.p = {"K1": r.normal(0, 0.3, (8, 2, 3, 3)), "b1": np.zeros(8),
                  "K2": r.normal(0, 0.15, (8, 8, 3, 3)), "b2": np.zeros(8),
                  "Wf": r.normal(0, 0.05, (HID, 800)), "bf": np.zeros(HID),
                  "Wa": r.normal(0, 0.1, (5, HID)), "ba": np.zeros(5), "Wv": r.normal(0, 0.1, HID), "bv": np.zeros(1)}
        self.rec = False
        self.cache = []

    def reset(self):
        self.cache = []

    @staticmethod
    def _cols1(x):
        xp = np.pad(x.reshape(2, S, S), ((0, 0), (1, 1), (1, 1)))
        win = sliding_window_view(xp, (3, 3), axis=(1, 2))          # (2, 21, 21, 3, 3)
        return win.transpose(1, 2, 0, 3, 4).reshape(S * S, 18)       # rows: positions; cols: (channel, ky, kx)

    @staticmethod
    def _cols2(a1):
        win = sliding_window_view(a1, (3, 3), axis=(1, 2))[:, ::2, ::2]   # (8, 10, 10, 3, 3)
        return win.transpose(1, 2, 0, 3, 4).reshape(100, 72)

    def step(self, x):
        p = self.p
        c1 = self._cols1(x)
        z1 = c1 @ p["K1"].reshape(8, 18).T + p["b1"]                 # (441, 8)
        a1 = np.maximum(z1, 0.0).T.reshape(8, S, S)
        c2 = self._cols2(a1)
        z2 = c2 @ p["K2"].reshape(8, 72).T + p["b2"]                 # (100, 8)
        a2 = np.maximum(z2, 0.0).ravel()                             # (800,), position-major
        h = np.tanh(p["Wf"] @ a2 + p["bf"])
        self.cache.append((c1, z1, c2, z2, a2))
        return None, h, p["Wa"] @ h + p["ba"], float(p["Wv"] @ h + p["bv"][0])

    def backward(self, xs, hps, hs, dlogits, dvals):
        p = self.p
        g = {k: np.zeros_like(v) for k, v in p.items()}
        K2m = p["K2"].reshape(8, 72)
        for t in range(len(hs)):
            c1, z1, c2, z2, a2 = self.cache[t]
            h = hs[t]
            g["Wa"] += np.outer(dlogits[t], h)
            g["ba"] += dlogits[t]
            g["Wv"] += dvals[t] * h
            g["bv"] += dvals[t]
            dh = p["Wa"].T @ dlogits[t] + dvals[t] * p["Wv"]
            dpre = dh * (1.0 - h ** 2)
            g["Wf"] += np.outer(dpre, a2)
            g["bf"] += dpre
            dz2 = (p["Wf"].T @ dpre).reshape(100, 8) * (z2 > 0)
            g["K2"] += (dz2.T @ c2).reshape(8, 8, 3, 3)
            g["b2"] += dz2.sum(0)
            dc2 = (dz2 @ K2m).reshape(10, 10, 8, 3, 3)               # back to the 8 x 21 x 21 map
            da1 = np.zeros((8, S, S))
            for ky in range(3):
                for kx in range(3):
                    da1[:, ky:ky + 19:2, kx:kx + 19:2] += dc2[:, :, :, ky, kx].transpose(2, 0, 1)
            dz1 = da1.reshape(8, S * S).T * (z1 > 0)                 # (441, 8)
            g["K1"] += (dz1.T @ c1).reshape(8, 2, 3, 3)
            g["b1"] += dz1.sum(0)
        return g

    def apply(self, g):
        n = float(np.sqrt(sum(float((v * v).sum()) for v in g.values())))
        s = min(1.0, B1.CLIP / n) if n > 0 else 1.0
        for k in self.p:
            self.p[k] -= B1.LR * s * g[k]
