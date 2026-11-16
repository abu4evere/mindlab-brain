"""WI: imagination in the silent room (questions.md, WI-frozen). W3c's GYFR brain (gated class) lives 10,000 steps in
WQ's silent room, learning by W3's A2C; arm IM also dreams 200 imagined steps every 500 room steps in a world built
from its own map memory with food placed anew; afterwards it is tested on W3's 50 test lands.

  python wi.py run ARM SEED OUT_DIR      ARM in L, IM
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
sys.path.insert(0, str(HERE.parent / "W3c"))
sys.path.insert(0, str(HERE.parent / "WQ"))
import w3c  # noqa: E402  (gated class; W3b and W3 on the path)
import wq  # noqa: E402
from w3c import B, W, R3  # noqa: E402

ROOM, T_ROOM, WIN = 900001, 10_000, 1_000
DREAM_EVERY, DREAM_LEN = 500, 200
KIND = "D3"


def load(seed):
    w3c.configure("GYFR")                              # the gated class, as GYFR was trained
    net = B.DriveVIN(seed)
    with np.load(HERE.parent / "W3c" / "output" / f"GYFR_{seed}.npz") as z:
        for k in net.p:
            net.p[k] = z[k].copy()
    return net


class Segments:
    """W3's A2C bookkeeping: collect steps, update every SEG steps or at the end."""
    def __init__(self, net, rng):
        self.net, self.rng, self.seg = net, rng, {"maps": [], "levels": [], "cells": [], "acts": [], "rews": []}

    def add(self, m, lev, cell, a, r):
        for k, v in (("maps", m), ("levels", lev), ("cells", cell), ("acts", a), ("rews", r)):
            self.seg[k].append(v)

    def flush_if(self, w, end):
        if len(self.seg["acts"]) == B.SEG or (end and self.seg["acts"]):
            G = 0.0 if (end or w.dead) else self.net.act(w.obs_map(), R3.levels(w, KIND), w.pos, self.rng)[2]
            rets = []
            for rr in reversed(self.seg["rews"]):
                G = rr + B.GAMMA * G
                rets.append(G)
            self.net.update(self.seg["maps"], self.seg["levels"], self.seg["cells"], self.seg["acts"], rets[::-1])
            self.seg = {"maps": [], "levels": [], "cells": [], "acts": [], "rews": []}


def imagined_land(room, drng):
    """A world built from the brain's own map memory: remembered walls (unknown imagined open; border wall), the
    remembered shelter, three food patches placed anew, start where it stands."""
    walls = room.m_wall.copy()
    walls[0, :] = walls[-1, :] = walls[:, 0] = walls[:, -1] = True
    open_cells = [(x, y) for y in range(W.N) for x in range(W.N) if not walls[y, x]]
    ys, xs = np.nonzero(room.m_shelter)
    shelter = (int(xs[0]), int(ys[0])) if len(xs) else open_cells[int(drng.integers(len(open_cells)))]
    taken = {shelter, room.pos}
    patches = []
    for _ in range(3):
        cand = W._blocks(walls, taken)
        if not cand:
            break
        c = cand[int(drng.integers(len(cand)))]
        patches.append(c)
        taken |= set(W.block_cells(c))
    return {"walls": walls, "shelter": shelter, "patches": patches, "start": room.pos, "sched": [], "reloc_seed": 0}


def dream(net, room, drng, rng, R):
    land = imagined_land(room, drng)
    w = W.World(land, R)
    w.E, w.F = float(drng.uniform(40, 150)), float(drng.uniform(0, 150))
    seg = Segments(net, rng)
    eaten = 0
    for _ in range(DREAM_LEN):
        if w.done():
            break
        m, lev, cell = w.obs_map(), R3.levels(w, KIND), w.pos
        a = net.act(m, lev, cell, rng)[0]
        d0 = w.drive()
        cur, ate = w.step(a)
        eaten += int(ate)
        seg.add(m, lev, cell, a, R3.reward(KIND, d0, w.drive(), cur, w.dead))
        seg.flush_if(w, w.done())
    seg.flush_if(w, True)
    return {"eaten": eaten, "died": bool(w.dead), "steps": w.t}


def test_after(net, seed):
    """W3c/W3b's test (learning off), on W3's 50 test lands."""
    R = R3.regrowth()
    before = {k: v.copy() for k, v in net.p.items()}
    lives = []
    for ls in W.TEST_SEEDS:
        land = W.make_land(ls)
        rng = np.random.default_rng(ls)
        _, m = R3.run_life(lambda w: net.act(w.obs_map(), R3.levels(w, KIND), w.pos, rng)[0], land, R, rng)
        lives.append(m)
    assert all(np.array_equal(before[k], net.p[k]) for k in net.p)
    return lives


def run(arm, seed, test=True):
    net = load(seed)
    R = R3.regrowth()
    room = wq.Room(W.make_land(ROOM), R)
    rng = np.random.default_rng([seed, ROOM, 41])                 # WQ's acting stream
    drng = np.random.default_rng([seed, 51])
    seg = Segments(net, rng)
    moves, cells, dreams = [], [], []
    while not room.done():
        m, lev, cell = room.obs_map(), R3.levels(room, KIND), room.pos
        a = net.act(m, lev, cell, rng)[0]
        d0 = room.drive()
        before = room.pos
        cur, _ = room.step(a)
        moves.append(a if room.pos != before else 4)
        cells.append(room.pos)
        seg.add(m, lev, cell, a, R3.reward(KIND, d0, room.drive(), cur, False))
        seg.flush_if(room, room.done())
        if arm == "IM" and room.t % DREAM_EVERY == 0 and not room.done():
            seg.flush_if(room, True)                              # close the waking segment before dreaming
            dreams.append(dream(net, room, drng, rng, R))
    windows = []
    for i in range(T_ROOM // WIN):
        mv, cl = moves[i * WIN:(i + 1) * WIN], cells[i * WIN:(i + 1) * WIN]
        windows.append({"activity": float(np.mean([x != 4 for x in mv])), "reach": len(set(cl)),
                        "pattern": len(zlib.compress(bytes(mv), 9)) / len(mv)})
    out = {"arm": arm, "seed": seed, "windows": windows, "dreams": dreams}
    if test:
        out["after"] = test_after(net, seed)
    return out


if __name__ == "__main__":
    if sys.argv[1] == "run":
        arm, seed, outd = sys.argv[2], int(sys.argv[3]), Path(sys.argv[4])
        outd.mkdir(parents=True, exist_ok=True)
        (outd / f"{arm}_{seed}.json").write_text(json.dumps(run(arm, seed)), encoding="utf-8")
        print("done", arm, seed, flush=True)
