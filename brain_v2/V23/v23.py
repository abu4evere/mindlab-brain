"""V2-3 Keep learning for life, with protection (questions.md, V23-frozen).

The walker (RMS, W3n's DriveVIN) keeps learning as an adult in a new world B, with W3's actor-critic and the drive
reward unchanged, in W3r's own world (MeaningWorld, the RM table live), the walker's reflexes acting (w3m.Reflex).
Worlds: A = W3r's lands (regrowth R). B1 = R x2. B2 = R x2 and the shelter moved to the open cell farthest (by path)
from its place, not a food-patch cell or the start. The pilot (seeds 1-2) decides B (questions.md).
Arms: FREE; SLOW (learning rate x0.1); ANCHOR (EWC-style: grad += lam * F * (p - p0), F = mean squared policy
gradients over 20 home lives before learning, every 10th step; lam = 1 / mean(F)); REHEARSE (after each B life one home
life with learning on; B steps as every arm, home steps extra); REPLAY (20,000 home transitions in 64-step segments
with bootstrapped returns, recorded before learning; after each B update one update on a random home segment).
  python v23.py train ARM SEED STEPS WORLD [pilot]   -> output/net_{ARM}_{SEED}[_pilot].npz, snapshots, a log
  python v23.py test KIND ARM SEED WORLD [pilot|snap250k|snap500k]  KIND: B (B test lands) | H (home: W3r fresh lands) | P (pilot lands)
  python v23.py bp TEST ARM SEED                     the Bob Profile test (W3r's bp_w3r unchanged but the loading)
"""
from __future__ import annotations

import json
import os
import platform
import sys
import time
from pathlib import Path

HERE = Path(__file__).parent
sys.path.insert(0, str(HERE.parents[1] / "body" / "CW1"))
import cw1  # noqa: E402  (W3r's chain first)
import numpy as np  # noqa: E402
from cw1 import W, w3k, R3  # noqa: E402

B = w3k.B
w3r, w3m = cw1.w3r, cw1.w3r.w3m
w3i = w3r.w3n.w3i
OUT, BP_OUT = Path(os.environ.get("V23_OUT", HERE / "output")), HERE / "bp_output"
BRAINS = HERE.parents[1] / "body" / "CW1" / "brains"
W3R = HERE.parents[1] / "workbench" / "W3r"
V23_SEED = 20261201
B_TEST, PILOT_LANDS, HOME_TEST = range(997001, 997051), range(999001, 999021), w3i.FRESH_SEEDS
SNAPS = (250_000, 500_000)
LOG_EVERY = 100_000
ARMS = ("FREE", "SLOW", "ANCHOR", "REHEARSE", "REPLAY")


def machine():
    return {"platform": platform.platform(), "python": platform.python_version(), "numpy": np.__version__,
            "node": platform.node()}


def world_land(ls, world):
    """The land and its regrowth in world A, B1 or B2."""
    land, R = W.make_land(ls), R3.regrowth()
    if world == "A":
        return land, R
    if world == "B250":  # the amended B (amendment.md): regrowth x1.25, nothing else changed
        return land, int(round(1.25 * R))
    if world == "B2":
        walls = land["walls"]
        taken = {land["start"]}
        for c in land["patches"]:
            taken |= set(W.block_cells(c))
        d = {land["shelter"]: 0}
        q = [land["shelter"]]
        while q:
            c = q.pop(0)
            for dx, dy in W.MOVES[:4]:
                n = (c[0] + dx, c[1] + dy)
                if 0 <= n[0] < W.N and 0 <= n[1] < W.N and not walls[n[1], n[0]] and n not in d:
                    d[n] = d[c] + 1
                    q.append(n)
        far = max((k, cell) for cell, k in d.items() if cell not in taken)[1]
        land = dict(land, shelter=far)
    return land, 2 * R


def configure(seed):
    w3r.configure("RM", seed)
    W.World = w3r.MeaningWorld


def load_rms(seed):
    return w3k.load_npz(BRAINS / f"RM_CS_{seed}.npz", seed)


def returns(net, seg, w, rng):
    if w.dead or w.t >= W.LIFE:
        G = 0.0
    else:
        _, _, G = net.act(w.obs_map(), R3.levels(w, "D3"), w.pos, rng)
    rets = []
    for rr in reversed(seg["rews"]):
        G = rr + B.GAMMA * G
        rets.append(G)
    return rets[::-1]


def update(learn, net, seg, w, rng):
    net.update(seg["maps"], seg["levels"], seg["cells"], seg["acts"], returns(net, seg, w, rng))
    learn["updates"] += 1
    if learn["arm"] == "REPLAY" and learn["counts_steps"]:
        h = learn["buffer"][int(learn["brng"].integers(len(learn["buffer"])))]
        net.update(h["maps"], h["levels"], h["cells"], h["acts"], h["rets"])


def life(net, seed, ls, world, learn=None, rng=None):
    """One life; learn: None (test) or the training state (A2C on 64-step segments, as W3's train_net)."""
    configure(seed)
    land, R = world_land(ls, world)
    rng = rng if rng is not None else np.random.default_rng(ls)
    rfx = w3m.Reflex()

    def pol(w):
        return rfx.act(w, net.act(w.obs_map(), R3.levels(w, "D3"), w.pos, rng)[0])
    if learn is None:
        w, m = R3.run_life(pol, land, R, rng)
        return {"survived": m["survived"], "lifespan": m["lifespan"]}
    w = W.World(land, R)
    seg = {"maps": [], "levels": [], "cells": [], "acts": [], "rews": []}
    while not w.done() and learn["total"] < learn["steps"]:
        m, lev, cell = w.obs_map(), R3.levels(w, "D3"), w.pos
        a = pol(w)
        d0 = w.drive()
        cur, _ = w.step(a)
        r = R3.reward("D3", d0, w.drive(), cur, w.dead)
        for k, v in (("maps", m), ("levels", lev), ("cells", cell), ("acts", a), ("rews", r)):
            seg[k].append(v)
        learn["count"] += 1
        if learn["counts_steps"]:
            learn["total"] += 1
        snap = learn["counts_steps"] and learn["total"] in SNAPS
        if len(seg["acts"]) == B.SEG or w.done() or learn["total"] >= learn["steps"] or snap:
            update(learn, net, seg, w, rng)
            seg = {"maps": [], "levels": [], "cells": [], "acts": [], "rews": []}
        if snap and learn["total"] < learn["steps"]:
            np.savez(OUT / f"snap{learn['total'] // 1000}k_{learn['name']}.npz", **net.p)
    return {"survived": float(w.t >= W.LIFE and not w.dead), "lifespan": w.t}


class Anchored:
    """Wraps net.apply: adds lam * F * (p - p0) to the gradient before W3's clipping and step."""

    def __init__(self, net, F, p0):
        self.net, self.F, self.p0 = net, F, p0
        mean = float(np.mean(np.concatenate([v.ravel() for v in F.values()])))
        self.lam = 1.0 / mean if mean > 0 else 0.0
        self.orig = net.apply
        net.apply = self

    def penalty(self):
        return {k: self.lam * self.F[k] * (self.net.p[k] - self.p0[k]) for k in self.F}

    def __call__(self, g):
        pen = self.penalty()
        return self.orig({k: g[k] + pen[k] if k in pen else g[k] for k in g})


def fisher(net, seed):
    """Mean squared gradient of log pi(a|s) over 20 home lives, every 10th step (before any learning)."""
    acc = {k: np.zeros_like(v) for k, v in net.p.items()}
    n = 0
    for i in range(20):
        configure(seed)
        land, R = world_land(82_000_000 + 1000 * seed + i, "A")
        rng = np.random.default_rng([V23_SEED, seed, i])
        rfx = w3m.Reflex()
        w = W.World(land, R)
        while not w.done():
            m, lev = w.obs_map(), R3.levels(w, "D3")
            a = rfx.act(w, net.act(m, lev, w.pos, rng)[0])
            if w.t % 10 == 0:
                fw = net.plan(m[None], np.asarray(lev, float)[None])
                rows = np.array([w.pos[1] * B.N + w.pos[0]])
                z, v = net.head(fw, rows)
                dl = B.softmax(z[0])
                dl[a] -= 1.0
                g = net.backprop(fw, rows, dl[None], np.zeros(1))
                for k in acc:
                    acc[k] += g[k] ** 2
                n += 1
            w.step(a)
    return {k: v / max(1, n) for k, v in acc.items()}


def home_buffer(net, seed, size=20_000):
    """Home segments (64 steps) with bootstrapped returns from the frozen walker, recorded before learning."""
    buf, i = [], 0
    while sum(len(s["acts"]) for s in buf) < size:
        configure(seed)
        land, R = world_land(83_000_000 + 1000 * seed + i, "A")
        rng = np.random.default_rng([V23_SEED, seed, 100 + i])
        rfx = w3m.Reflex()
        w = W.World(land, R)
        seg = {"maps": [], "levels": [], "cells": [], "acts": [], "rews": []}
        while not w.done():
            m, lev, cell = w.obs_map(), R3.levels(w, "D3"), w.pos
            a = rfx.act(w, net.act(m, lev, w.pos, rng)[0])
            d0 = w.drive()
            cur, _ = w.step(a)
            for k, v in (("maps", m), ("levels", lev), ("cells", cell), ("acts", a),
                         ("rews", R3.reward("D3", d0, w.drive(), cur, w.dead))):
                seg[k].append(v)
            if len(seg["acts"]) == B.SEG or w.done():
                seg["rets"] = returns(net, seg, w, rng)
                buf.append(seg)
                seg = {"maps": [], "levels": [], "cells": [], "acts": [], "rews": []}
        i += 1
    return buf


def train(arm, seed, steps, world, tag=""):
    assert arm in ARMS
    OUT.mkdir(exist_ok=True)
    name = f"{arm}_{seed}{tag}"
    net = load_rms(seed)
    p0 = {k: v.copy() for k, v in net.p.items()}
    configure(seed)
    learn = {"arm": arm, "name": name, "total": 0, "count": 0, "updates": 0, "steps": steps, "life": 0, "home_steps": 0,
             "counts_steps": True}
    keep_lr = B.LR
    if arm == "SLOW":
        B.LR = keep_lr * 0.1
    if arm == "ANCHOR":
        Anchored(net, fisher(net, seed), p0)
    if arm == "REPLAY":
        learn["buffer"] = home_buffer(net, seed)
        learn["brng"] = np.random.default_rng([V23_SEED, seed, 9])
    rng = np.random.default_rng([V23_SEED, seed, 7])
    log, t0, next_log = [], time.time(), LOG_EVERY
    try:
        while learn["total"] < steps:
            learn["life"] += 1
            learn["counts_steps"] = True
            life(net, seed, 80_000_000 + 1000 * seed + learn["life"], world, learn, rng)
            if arm == "REHEARSE" and learn["total"] < steps:
                c0 = learn["count"]
                learn["counts_steps"] = False
                life(net, seed, 81_000_000 + 1000 * seed + learn["life"], "A", learn, rng)
                learn["home_steps"] += learn["count"] - c0
            if learn["total"] >= next_log or learn["total"] >= steps:
                row = {"step": learn["total"], "life": learn["life"], "home_steps": learn["home_steps"],
                       "drift": float(np.sqrt(sum(((net.p[k] - p0[k]) ** 2).sum() for k in net.p))),
                       "seconds": round(time.time() - t0, 1)}
                log.append(row)
                print(json.dumps(row), flush=True)
                next_log += LOG_EVERY
    finally:
        B.LR = keep_lr
    np.savez(OUT / f"net_{name}.npz", **net.p)
    (OUT / f"trainlog_{name}.json").write_text(json.dumps({"log": log, "machine": machine(), "world": world}))
    print("trained", arm, seed, steps, world, flush=True)


def load(arm, seed, tag=""):
    net = load_rms(seed)
    if arm == "FROZEN":
        return net
    f = f"{tag[1:]}_{arm}_{seed}.npz" if tag.startswith("_snap") else f"net_{arm}_{seed}{tag}.npz"
    with np.load(OUT / f) as z:
        for k in net.p:
            net.p[k] = z[k].copy()
    return net


def test(kind, arm, seed, world, tag=""):
    net = load(arm, seed, tag)
    lands, w = {"B": (B_TEST, world), "H": (HOME_TEST, "A"), "P": (PILOT_LANDS, world)}[kind]
    path = OUT / f"{kind}_{arm}_{seed}{tag}.jsonl"
    done = set()
    if path.exists():
        done = {json.loads(x)["land"] for x in path.read_text().splitlines() if x.strip()}
    with open(path, "a") as f:
        for ls in lands:
            if ls in done:
                continue
            m = life(net, seed, ls, w)
            m.update({"land": ls, "arm": arm, "seed": seed, "world": w, "machine": machine()})
            f.write(json.dumps(m) + "\n")
            f.flush()
    print("tested", kind, arm, seed, flush=True)


def bob_profile(test_name, arm, seed):
    sys.path.insert(0, str(W3R))
    sys.argv = ["bp_w3r.py", test_name, "RM", str(seed)]
    import bp_w3r
    T = bp_w3r.T

    def load_brain(_arm, s):
        w3r.configure("RM", s)
        return load("FROZEN" if arm == "RMS" else arm, s)
    T.load_brain = bp_w3r.load_brain = load_brain
    T.OUT = BP_OUT
    BP_OUT.mkdir(exist_ok=True)
    agent = load_brain("RM", seed)
    prev = T.body(test_name not in T.BARE)
    res = T.TESTS[test_name](agent, T.R3.regrowth())
    T.body(prev[0] == "walk")
    res.update(test=test_name, agent=f"{arm}_{seed}")
    (BP_OUT / f"{test_name}_{arm}_{seed}.json").write_text(json.dumps(res, indent=1))
    print("bp", test_name, arm, seed, flush=True)


if __name__ == "__main__":
    a = sys.argv
    if a[1] == "train":
        train(a[2], int(a[3]), int(a[4]), a[5], "_pilot" if len(a) > 6 and a[6] == "pilot" else "")
    elif a[1] == "test":
        test(a[2], a[3], int(a[4]), a[5], "_" + a[6] if len(a) > 6 else "")  # pilot | snap250k | snap500k
    elif a[1] == "bp":
        bob_profile(a[2], a[3], int(a[4]))
