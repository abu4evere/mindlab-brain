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


LAYERS = [(2, 8, 1, 1), (8, 8, 2, 0), (8, 16, 2, 0)]     # (in channels, out channels, stride, padding); 3 x 3 kernels


def _cols(a, stride, pad):
    """im2col: a (C, H, W) -> (positions, C * 9), positions row-major."""
    if pad:
        a = np.pad(a, ((0, 0), (pad, pad), (pad, pad)))
    win = sliding_window_view(a, (3, 3), axis=(1, 2))[:, ::stride, ::stride]   # (C, Ho, Wo, 3, 3)
    C, Ho, Wo = win.shape[:3]
    return win.transpose(1, 2, 0, 3, 4).reshape(Ho * Wo, C * 9), Ho, Wo


def _uncols(dcols, C, H, W, Ho, Wo, stride, pad):
    """col2im: the gradient of the columns back onto the (C, H, W) map."""
    d = np.zeros((C, H + 2 * pad, W + 2 * pad))
    dc = dcols.reshape(Ho, Wo, C, 3, 3)
    for ky in range(3):
        for kx in range(3):
            d[:, ky:ky + stride * (Ho - 1) + 1:stride, kx:kx + stride * (Wo - 1) + 1:stride] +=                 dc[:, :, :, ky, kx].transpose(2, 0, 1)
    return d[:, pad:pad + H, pad:pad + W] if pad else d


class ConvNet:
    """C: conv 3x3 (2 -> 8, padding 1) + ReLU; 3x3 stride 2 (8 -> 8) + ReLU; 3x3 stride 2 (8 -> 16) + ReLU
    (21 -> 21 -> 10 -> 4); 256 -> 64 tanh; 5 action scores and a value."""

    def __init__(self, seed):
        r = np.random.default_rng(seed)
        self.p = {}
        for i, (ci, co, _, _) in enumerate(LAYERS, 1):
            self.p[f"K{i}"] = r.normal(0, np.sqrt(2.0 / (ci * 9)), (co, ci, 3, 3))
            self.p[f"b{i}"] = np.zeros(co)
        self.p.update({"Wf": r.normal(0, 0.1, (HID, 256)), "bf": np.zeros(HID), "Wa": r.normal(0, 0.1, (5, HID)),
                       "ba": np.zeros(5), "Wv": r.normal(0, 0.1, HID), "bv": np.zeros(1)})
        self.rec = False
        self.cache = []

    def reset(self):
        self.cache = []

    def step(self, x):
        p = self.p
        a = x.reshape(2, S, S)
        layers = []
        for i, (ci, co, st, pd) in enumerate(LAYERS, 1):
            cols, Ho, Wo = _cols(a, st, pd)
            z = cols @ p[f"K{i}"].reshape(co, ci * 9).T + p[f"b{i}"]
            layers.append((cols, z, a.shape, Ho, Wo))
            a = np.maximum(z, 0.0).T.reshape(co, Ho, Wo)
        flat = a.ravel()                                          # channel-major
        h = np.tanh(p["Wf"] @ flat + p["bf"])
        self.cache.append((layers, flat))
        return None, h, p["Wa"] @ h + p["ba"], float(p["Wv"] @ h + p["bv"][0])

    def backward(self, xs, hps, hs, dlogits, dvals):
        p = self.p
        g = {k: np.zeros_like(v) for k, v in p.items()}
        for t in range(len(hs)):
            layers, flat = self.cache[t]
            h = hs[t]
            g["Wa"] += np.outer(dlogits[t], h)
            g["ba"] += dlogits[t]
            g["Wv"] += dvals[t] * h
            g["bv"] += dvals[t]
            dh = p["Wa"].T @ dlogits[t] + dvals[t] * p["Wv"]
            dpre = dh * (1.0 - h ** 2)
            g["Wf"] += np.outer(dpre, flat)
            g["bf"] += dpre
            da = (p["Wf"].T @ dpre)
            for i in range(len(LAYERS), 0, -1):
                ci, co, st, pd = LAYERS[i - 1]
                cols, z, in_shape, Ho, Wo = layers[i - 1]
                dz = da.reshape(co, Ho * Wo).T * (z > 0)              # (positions, co)
                g[f"K{i}"] += (dz.T @ cols).reshape(co, ci, 3, 3)
                g[f"b{i}"] += dz.sum(0)
                if i > 1:
                    da = _uncols(dz @ p[f"K{i}"].reshape(co, ci * 9), ci, in_shape[1], in_shape[2], Ho, Wo, st, pd)
        return g

    def apply(self, g):
        n = float(np.sqrt(sum(float((v * v).sum()) for v in g.values())))
        s = min(1.0, B1.CLIP / n) if n > 0 else 1.0
        for k in self.p:
            self.p[k] -= B1.LR * s * g[k]
