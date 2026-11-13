"""W3 runner (questions.md, W3-frozen).

  python run_w3.py calib                    the calibration (Script and Rand on the calibration lands) -> calib.json
  python run_w3.py train KIND SEED STEPS    train one learned brain (D3, D2, Dc, D3i) -> output/KIND_SEED.npz + log
  python run_w3.py test KIND SEED           test one trained brain on the 50 test lands (KIND may be D3- : the lesion)
  python run_w3.py refs                     Rand and Script on the 50 test lands -> output/Rand.json, output/Script.json
"""
from __future__ import annotations

import json
import math
import os
import sys
import time
from pathlib import Path

os.environ.setdefault("OPENBLAS_NUM_THREADS", "1")
os.environ.setdefault("OMP_NUM_THREADS", "1")
os.environ.setdefault("MKL_NUM_THREADS", "1")

import numpy as np  # noqa: E402

HERE = Path(__file__).parent
sys.path.insert(0, str(HERE))
import brains3 as B  # noqa: E402
import world3 as W  # noqa: E402

OUT = HERE / "output"
CALIB = HERE / "calib.json"
W_H = {"D3": 1.0, "D2": 1.0, "Dc": 0.0, "D3i": 1.0}
W_C = {"D3": 1.0, "D2": 0.0, "Dc": 1.0, "D3i": 1.0}
D_MAX = 2.0
HUNGRY, EXHAUSTED = 50, 100
NORM_EVERY = 50_000


def regrowth():
    return int(json.loads(CALIB.read_text())["R"])


def levels(w, kind):
    """The drive levels fed to the reward map (questions.md, Brains)."""
    s, f = w.deficits()
    c = w.curiosity_level()
    if kind == "D2":
        c = 0.0
    if kind == "Dc":
        s = f = 0.0
    if kind == "D3-":
        c = 0.0
    return (s, f, c)


def reward(kind, d_before, d_after, cur, died):
    """r = w_h * 10 * (D_t - D_t+1) + w_c * 0.05 * curiosity; at death the drive jumps to D_MAX."""
    if died:
        d_after = D_MAX
    return W_H[kind] * 10.0 * (d_before - d_after) + W_C[kind] * 0.05 * cur


def run_life(policy, land, R, rng, on_step=None):
    """One life; policy(world) -> action. Returns (world, per-life measures)."""
    w = W.World(land, R)
    known500, hungry, exhausted = None, 0, 0
    while not w.done():
        a = policy(w)
        d0 = w.drive()
        cur, _ = w.step(a)
        if on_step is not None:
            on_step(w, a, d0, cur)
        hungry += w.E < HUNGRY
        exhausted += w.F > EXHAUSTED
        if w.t == 500:
            known500 = w.land_known()
    m = W.life_measures(w)
    m.update({"known500": known500 if known500 is not None else w.land_known(), "known_end": w.land_known(),
              "hungry": hungry / max(1, w.t), "exhausted": exhausted / max(1, w.t)})
    return w, m


def train(kind, seed, steps):
    OUT.mkdir(exist_ok=True)
    with open(OUT / f"{kind}_{seed}.log", "w") as log:
        net, norms = train_net(kind, seed, steps, regrowth(), log)
    np.savez(OUT / f"{kind}_{seed}.npz", **net.p)
    (OUT / f"{kind}_{seed}_norms.json").write_text(json.dumps(norms))


def train_net(kind, seed, steps, R, log=None):
    net = B.DriveVIN(seed, fixed_map=(kind == "D3i"))
    rng = np.random.default_rng(10_000 + seed)
    norms, total, life, t0 = [], 0, 0, time.time()
    lives_survived, lives = 0, 0
    while total < steps:
        life += 1
        land = W.make_land(W.train_seed(seed, life))
        w = W.World(land, R)
        seg = {"maps": [], "levels": [], "cells": [], "acts": [], "rews": []}
        while not w.done() and total < steps:
            m, lev, cell = w.obs_map(), levels(w, kind), w.pos
            a, _, _ = net.act(m, lev, cell, rng)
            d0 = w.drive()
            cur, _ = w.step(a)
            r = reward(kind, d0, w.drive(), cur, w.dead)
            for k, v in (("maps", m), ("levels", lev), ("cells", cell), ("acts", a), ("rews", r)):
                seg[k].append(v)
            total += 1
            if total % NORM_EVERY == 0:
                norms.append({"step": total, **net.row_norms()})
            if len(seg["acts"]) == B.SEG or w.done() or total >= steps:
                if w.dead or w.t >= W.LIFE:
                    G = 0.0                                   # death (its jump is in the reward) or the cap
                else:
                    _, _, G = net.act(w.obs_map(), levels(w, kind), w.pos, rng)
                rets = []
                for rr in reversed(seg["rews"]):
                    G = rr + B.GAMMA * G
                    rets.append(G)
                net.update(seg["maps"], seg["levels"], seg["cells"], seg["acts"], rets[::-1])
                seg = {"maps": [], "levels": [], "cells": [], "acts": [], "rews": []}
        lives += 1
        lives_survived += int(w.t >= W.LIFE and not w.dead)
        if log is not None and life % 20 == 0:
            print(f"{kind} {seed} step {total} lives {lives} survived {lives_survived} last t {w.t} "
                  f"norms {net.row_norms()} {time.time() - t0:.0f}s", file=log, flush=True)
    if log is not None:
        print(f"done {kind} {seed} steps {total} lives {lives} survived {lives_survived} {time.time() - t0:.0f}s",
              file=log, flush=True)
    return net, norms


def load(kind, seed):
    base = "D3" if kind == "D3-" else kind
    net = B.DriveVIN(seed, fixed_map=(base == "D3i"))
    with np.load(OUT / f"{base}_{seed}.npz") as z:
        for k in net.p:
            net.p[k] = z[k].copy()
    return net


def test(kind, seed):
    """Learning off; the learned policy, sampled with a fixed generator per test land (the same for every brain)."""
    R = regrowth()
    net = load(kind, seed)
    before = {k: v.copy() for k, v in net.p.items()}
    lives = []
    for ls in W.TEST_SEEDS:
        land = W.make_land(ls)
        rng = np.random.default_rng(ls)
        _, m = run_life(lambda w: net.act(w.obs_map(), levels(w, kind), w.pos, rng)[0], land, R, rng)
        lives.append(m)
    assert all(np.array_equal(before[k], net.p[k]) for k in net.p), "weights changed in testing"
    (OUT / f"test_{kind}_{seed}.json").write_text(json.dumps(lives))


def rand_policy(rng):
    return lambda w: int(rng.integers(5))


def script_policy():
    s = W.Script()
    return lambda w: s.act(W.MapView(w))


def refs():
    R = regrowth()
    OUT.mkdir(exist_ok=True)
    for name in ("Rand", "Script"):
        lives = []
        for ls in W.TEST_SEEDS:
            rng = np.random.default_rng(ls)
            pol = rand_policy(rng) if name == "Rand" else script_policy()
            lives.append(run_life(pol, W.make_land(ls), R, rng)[1])
        (OUT / f"test_{name}.json").write_text(json.dumps(lives))


def calib():
    """questions.md, Calibration: the first R (scarcest first) with Script >= 0.90 and Rand <= 0.20."""
    rows = []
    chosen = None
    for R in W.R_LIST:
        res = {}
        for name in ("Script", "Rand"):
            surv = []
            for ls in W.CAL_SEEDS:
                rng = np.random.default_rng(ls)
                pol = rand_policy(rng) if name == "Rand" else script_policy()
                surv.append(run_life(pol, W.make_land(ls), R, rng)[1]["survived"])
            res[name] = float(np.mean(surv))
        rows.append({"R": R, **res})
        print(rows[-1], flush=True)
        if res["Script"] >= 0.90 and res["Rand"] <= 0.20:
            chosen = R
            break
    CALIB.write_text(json.dumps({"R": chosen, "rows": rows}, indent=1))
    print("chosen", chosen)


if __name__ == "__main__":
    cmd = sys.argv[1]
    if cmd == "calib":
        calib()
    elif cmd == "train":
        train(sys.argv[2], int(sys.argv[3]), int(sys.argv[4]))
    elif cmd == "test":
        test(sys.argv[2], int(sys.argv[3]))
    elif cmd == "refs":
        refs()
