"""WQ: the silent room (questions.md, WQ-frozen). W3's world with the body held satisfied (E = 150, F = 0), no food
relocations and no eating, for 10,000 steps; W3's and W3c's trained brains, still (weights fixed) or living (W3's
A2C continues with the curiosity reward only).

  python wq.py run BRAIN MODE OUT_DIR      BRAIN in D2, D3, Dc, GYFR, Rand, Script; MODE still | living
"""
from __future__ import annotations

import json
import os
import sys
import zlib
from pathlib import Path

os.environ.setdefault("OPENBLAS_NUM_THREADS", "1")
import numpy as np  # noqa: E402

HERE = Path(__file__).parent
sys.path.insert(0, str(HERE.parent / "W3"))
import brains3 as B  # noqa: E402
import world3 as W  # noqa: E402
import run_w3 as R3  # noqa: E402

T_ROOM, WIN = 10_000, 1_000
ROOMS = (900001, 900002, 900003)
SEEDS = range(1, 9)
KIND = {"D2": "D2", "D3": "D3", "Dc": "Dc", "GYFR": "D3"}
WEIGHTS = {"D2": HERE.parent / "W3" / "output", "D3": HERE.parent / "W3" / "output", "Dc": HERE.parent / "W3" / "output",
           "GYFR": HERE.parent / "W3c" / "output"}


class Room(W.World):
    """The silent room: needs always met, nothing moves, nothing is eaten, no death, 10,000 steps."""
    def __init__(self, land, R):
        super().__init__(land, R)
        self.sched = []
        self.E, self.F = float(W.E_SET), 0.0

    def step(self, a):
        self.E = float(W.EMAX) + 1.0              # after the step's cost (1) it is EMAX, so nothing is eaten
        self.F = 0.0
        cur, ate = super().step(a)
        assert not ate
        self.E, self.F, self.dead = float(W.E_SET), 0.0, False
        return cur, ate

    def done(self):
        return self.t >= T_ROOM


def load(brain, seed):
    net = B.DriveVIN(seed, fixed_map=False)
    with np.load(WEIGHTS[brain] / f"{brain}_{seed}.npz") as z:
        for k in net.p:
            net.p[k] = z[k].copy()
    return net


def stay(brain, mode, seed, room):
    """One 10,000-step stay. Returns per-window measures and the path."""
    w = Room(W.make_land(room), R3.regrowth())
    rng = np.random.default_rng([seed, room, 41])
    net = load(brain, seed) if brain in KIND else None
    script = W.Script() if brain == "Script" else None
    kind = KIND.get(brain, "D3")
    seg = {"maps": [], "levels": [], "cells": [], "acts": [], "rews": []}
    moves, cells, curs = [], [], []
    while not w.done():
        m, lev, cell = w.obs_map(), R3.levels(w, kind), w.pos
        if brain == "Rand":
            a = int(rng.integers(5))
        elif brain == "Script":
            a = script.act(W.MapView(w))
        else:
            a = net.act(m, lev, cell, rng)[0]
        d0 = w.drive()
        before = w.pos
        cur, _ = w.step(a)
        moves.append(a if w.pos != before else 4)
        cells.append(w.pos)
        curs.append(cur)
        if mode == "living" and net is not None:
            r = R3.reward(kind, d0, w.drive(), cur, False)
            for k, v in (("maps", m), ("levels", lev), ("cells", cell), ("acts", a), ("rews", r)):
                seg[k].append(v)
            if len(seg["acts"]) == B.SEG or w.done():
                G = 0.0 if w.done() else net.act(w.obs_map(), R3.levels(w, kind), w.pos, rng)[2]
                rets = []
                for rr in reversed(seg["rews"]):
                    G = rr + B.GAMMA * G
                    rets.append(G)
                net.update(seg["maps"], seg["levels"], seg["cells"], seg["acts"], rets[::-1])
                seg = {"maps": [], "levels": [], "cells": [], "acts": [], "rews": []}
    windows = []
    for i in range(T_ROOM // WIN):
        mv, cl, cu = moves[i * WIN:(i + 1) * WIN], cells[i * WIN:(i + 1) * WIN], curs[i * WIN:(i + 1) * WIN]
        raw = bytes(mv)
        windows.append({"activity": float(np.mean([x != 4 for x in mv])), "reach": len(set(cl)),
                        "pattern": len(zlib.compress(raw, 9)) / len(raw), "curiosity": float(np.sum(cu))})
    return {"windows": windows, "known": w.land_known()}


def run(brain, mode, out):
    out = Path(out)
    out.mkdir(parents=True, exist_ok=True)
    seeds = [1] if brain == "Script" else SEEDS
    for s in seeds:
        res = {"brain": brain, "mode": mode, "seed": s, "stays": [stay(brain, mode, s, r) for r in ROOMS]}
        (out / f"{brain}_{mode}_{s}.json").write_text(json.dumps(res), encoding="utf-8")
        print("done", brain, mode, s, flush=True)


if __name__ == "__main__":
    if sys.argv[1] == "run":
        run(sys.argv[2], sys.argv[3], sys.argv[4])
