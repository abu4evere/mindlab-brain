"""W3b (questions.md, W3b-frozen; IMPLEMENTATION.md). W3's world, body, drives, planner and actor-critic unchanged
(../W3/world3.py, ../W3/brains3.py, ../W3/run_w3.py), plus the parts Y ("that worked!"), FR (a store of successful
paths replayed on shelter steps), RR (the control: random windows replayed on shelter steps) and F (the engineered
ceiling: walk to the place where the need was last relieved; test only, on W3's trained D3 weights).

  python w3b.py step0 KIND SEED              KIND in D3i, D3 (W3's weights) -> output/step0_KIND_SEED.json
  python w3b.py train ARM SEED [HOURS]       ARM in Y, FR, YFR, RR (D3 = no parts, for checks); resumable; HOURS = the
                                             time guard (default 4.5): the run pauses at a life boundary after it
  python w3b.py test ARM SEED                ARM in Y, FR, YFR, RR, D3 (own weights) or F (W3's D3 weights)
  python w3b.py run ARM SEED [HOURS]         train (resume if paused), then test when finished
"""
from __future__ import annotations

import json
import os
import pickle
import sys
import time
from collections import deque
from pathlib import Path

os.environ.setdefault("OPENBLAS_NUM_THREADS", "1")
os.environ.setdefault("OMP_NUM_THREADS", "1")
os.environ.setdefault("MKL_NUM_THREADS", "1")

import numpy as np  # noqa: E402

HERE = Path(__file__).parent
W3 = HERE.parent / "W3"
sys.path.insert(0, str(W3))
import brains3 as B  # noqa: E402
import world3 as W  # noqa: E402
import run_w3 as R3  # noqa: E402

OUT = HERE / "output"
STEPS = 2_000_000
# the parts' numbers (questions.md; pre-data correction 1 in IMPLEMENTATION.md for HIGH)
HIGH = {"s": 0.2, "f": 0.4}                     # "the need is high": Script's lines (E < 120; F > 80)
REL_MIN, SD_MULT, WARMUP = 0.05, 2.0, 1_000
WIN, DECAY, W_MAX = 15, 0.9, 3.0
STORE_CAP, REPLAY_CAP = 256, 64
NEEDS = ("s", "f")


def parts_of(arm):
    return {"D3": "", "Y": "Y", "FR": "R", "YFR": "YR", "RR": "X", "F": ""}[arm]


class Stats:
    """Running mean and sd of relief per need, from past steps only (count, sum, sum of squares)."""
    def __init__(self):
        self.n = {c: 0 for c in NEEDS}
        self.s1 = {c: 0.0 for c in NEEDS}
        self.s2 = {c: 0.0 for c in NEEDS}

    def mean_sd(self, c):
        if self.n[c] == 0:
            return 0.0, 0.0
        m = self.s1[c] / self.n[c]
        v = max(0.0, self.s2[c] / self.n[c] - m * m)
        return m, float(np.sqrt(v))

    def add(self, c, r):
        self.n[c] += 1
        self.s1[c] += r
        self.s2[c] += r * r


def relief(before, after):
    """(s, f) deficits before and after a step -> relief per need (positive drops only)."""
    return {"s": max(0.0, before[0] - after[0]), "f": max(0.0, before[1] - after[1])}


def event(stats, need_before, rel, total):
    """Y's trigger (questions.md): the need was high, the relief beats the running mean + 2 sd and the floor; after the
    warm-up. Returns the weight at k = 0 (0.0 = no event) and the need."""
    if total < WARMUP:
        return 0.0, None
    best, which = 0.0, None
    for i, c in enumerate(NEEDS):
        if need_before[i] >= HIGH[c] and rel[c] >= REL_MIN:
            m, sd = stats.mean_sd(c)
            if rel[c] >= m + SD_MULT * sd:
                w = min(W_MAX, (rel[c] - m) / (sd + 1e-6))
                if w > best:
                    best, which = w, c
    return best, which


def window(records, since_event, w0):
    """The last min(WIN, since_event) records (k = 0 is the latest) with weights w0 * DECAY^k."""
    n = min(WIN, since_event, len(records))
    recs = list(records)[-n:]
    weights = [w0 * DECAY ** k for k in range(n - 1, -1, -1)]          # oldest first, matching recs
    return recs, weights


def imitate(net, recs, weights):
    """One supervised step toward the taken actions (the planner and head learn; the critic is untouched)."""
    maps = np.asarray([r[0] for r in recs])
    levels = np.asarray([r[1] for r in recs], float)
    cells = [r[2] for r in recs]
    acts = [r[3] for r in recs]
    fw = net.plan(maps, levels)
    rows = np.arange(len(cells)) * B.N * B.N + np.array([c[1] * B.N + c[0] for c in cells])
    z, v = net.head(fw, rows)
    dl = np.zeros_like(z)
    for t in range(len(acts)):
        pi = B.softmax(z[t])
        d = pi.copy()
        d[acts[t]] -= 1.0
        dl[t] = d * weights[t]
    net.apply(net.backprop(fw, rows, dl, np.zeros(len(acts))))


def ckpt_path(arm, seed):
    return OUT / f"{arm}_{seed}.ckpt.pkl"


def should_replay(w, replays, store):
    """FR/RR replay one stored path on each step spent on the shelter cell, under the per-life cap."""
    return w.pos == w.shelter and replays < REPLAY_CAP and len(store) > 0


def train_net(arm, seed, steps, R, hours=4.5, log=None, state=None, stop_lives=None, pause_after=None):
    """W3's training loop (run_w3.train_net) with the parts. Returns (net, state, finished)."""
    parts = parts_of(arm)
    Y, FR, RR = "Y" in parts, "R" in parts, "X" in parts
    kind = "D3"
    if state is None:
        net = B.DriveVIN(seed, fixed_map=False)
        rng = np.random.default_rng(10_000 + seed)
        state = {"p": None, "rng": None, "rrng": np.random.default_rng([seed, 21]).bit_generator.state,
                 "total": 0, "life": 0, "lives": 0, "lives_survived": 0, "norms": [], "stats": Stats(),
                 "store": deque(maxlen=STORE_CAP), "lives_log": [],
                 "updates": {"ac": 0, "y": 0, "replay": 0}}
    else:
        net = B.DriveVIN(seed, fixed_map=False)
        for k in net.p:
            net.p[k] = state["p"][k].copy()
        rng = np.random.default_rng()
        rng.bit_generator.state = state["rng"]
    rrng = np.random.default_rng()
    rrng.bit_generator.state = state["rrng"]
    stats, store, upd = state["stats"], state["store"], state["updates"]
    total, life, lives, lives_survived = state["total"], state["life"], state["lives"], state["lives_survived"]
    norms, t0 = state["norms"], time.time()
    recent = deque(maxlen=WIN)                                 # RR's window source (its own recent experience)
    finished = False
    while total < steps:
        life += 1
        land = W.make_land(W.train_seed(seed, life))
        w = W.World(land, R)
        seg = {"maps": [], "levels": [], "cells": [], "acts": [], "rews": []}
        records, since_event, replays, events, wsum, off_shelter = deque(maxlen=WIN), 0, 0, 0, 0.0, 0
        recent.clear()
        while not w.done() and total < steps:
            m, lev, cell = w.obs_map(), R3.levels(w, kind), w.pos
            a, _, _ = net.act(m, lev, cell, rng)
            d0 = w.drive()
            nb = w.deficits()
            cur, _ = w.step(a)
            na = w.deficits()
            r = R3.reward(kind, d0, w.drive(), cur, w.dead)
            for k, v in (("maps", m), ("levels", lev), ("cells", cell), ("acts", a), ("rews", r)):
                seg[k].append(v)
            total += 1
            rec = (m, lev, cell, a)
            records.append(rec)
            recent.append(rec)
            since_event += 1
            if total % R3.NORM_EVERY == 0:
                norms.append({"step": total, **net.row_norms()})
            if len(seg["acts"]) == B.SEG or w.done() or total >= steps:
                if w.dead or w.t >= W.LIFE:
                    G = 0.0
                else:
                    _, _, G = net.act(w.obs_map(), R3.levels(w, kind), w.pos, rng)
                rets = []
                for rr in reversed(seg["rews"]):
                    G = rr + B.GAMMA * G
                    rets.append(G)
                net.update(seg["maps"], seg["levels"], seg["cells"], seg["acts"], rets[::-1])
                upd["ac"] += 1
                seg = {"maps": [], "levels": [], "cells": [], "acts": [], "rews": []}
            if Y or FR:
                rel = relief(nb, na)
                w0, which = event(stats, nb, rel, total)
                for c in NEEDS:
                    stats.add(c, rel[c])
                if which is not None:
                    recs, weights = window(records, since_event, w0)
                    events += 1
                    wsum += float(np.mean(weights))
                    since_event = 0
                    if Y:
                        imitate(net, recs, weights)
                        upd["y"] += 1
                    if FR:
                        store.append((recs, weights))
            if RR and len(recent) == WIN and w.t % WIN == 0:
                store.append((list(recent), [1.0] * WIN))
            if (FR or RR) and should_replay(w, replays, store):
                recs, weights = store[int(rrng.integers(len(store)))]
                imitate(net, recs, weights)
                upd["replay"] += 1
                replays += 1
        lives += 1
        lives_survived += int(w.t >= W.LIFE and not w.dead)
        state["lives_log"].append({"life": life, "t": w.t, "events": events, "replays": replays,
                                   "mean_w": (wsum / events) if events else 0.0})
        if log is not None and life % 20 == 0:
            print(f"{arm} {seed} step {total} lives {lives} survived {lives_survived} last t {w.t} "
                  f"norms {net.row_norms()} {time.time() - t0:.0f}s", file=log, flush=True)
        if stop_lives is not None and lives >= stop_lives:
            break
        if total < steps and (time.time() - t0 > hours * 3600 or (pause_after is not None and total >= pause_after)):
            break
    finished = total >= steps
    if log is not None and finished:
        print(f"done {arm} {seed} steps {total} lives {lives} survived {lives_survived} {time.time() - t0:.0f}s "
              f"updates {upd}", file=log, flush=True)
    state.update(p={k: v.copy() for k, v in net.p.items()}, rng=rng.bit_generator.state,
                 rrng=rrng.bit_generator.state, total=total, life=life, lives=lives, lives_survived=lives_survived)
    return net, state, finished


def train(arm, seed, hours=4.5, steps=STEPS):
    """Train, resuming from a checkpoint if one exists. Returns True when the run is finished."""
    OUT.mkdir(exist_ok=True)
    cp = ckpt_path(arm, seed)
    state = pickle.loads(cp.read_bytes()) if cp.exists() else None
    with open(OUT / f"{arm}_{seed}.log", "a") as log:
        if state is not None:
            print(f"resume {arm} {seed} at step {state['total']} life {state['life']}", file=log, flush=True)
        net, state, finished = train_net(arm, seed, steps, R3.regrowth(), hours, log, state)
    if finished:
        np.savez(OUT / f"{arm}_{seed}.npz", **net.p)
        (OUT / f"{arm}_{seed}_norms.json").write_text(json.dumps(state["norms"]))
        (OUT / f"{arm}_{seed}_lives.json").write_text(json.dumps({"lives": state["lives_log"],
                                                                    "updates": state["updates"]}))
        if cp.exists():
            cp.unlink()
    else:
        cp.write_bytes(pickle.dumps(state))
        print("paused", arm, seed, "at step", state["total"], flush=True)
    return finished


def load(arm, seed):
    if arm in ("F", "D3"):                       # W3's trained D3 (D3 is cited from W3, never retrained here)
        return R3.load("D3", seed)
    net = B.DriveVIN(seed, fixed_map=False)
    with np.load(OUT / f"{arm}_{seed}.npz") as z:
        for k in net.p:
            net.p[k] = z[k].copy()
    return net


class FPolicy:
    """The engineered ceiling: a place per need (the food cell last eaten at; the shelter); when the need is high and the
    place is known, the shortest path on the map memory; otherwise the learned brain."""
    def __init__(self, net, rng):
        self.net, self.rng, self.place, self.walks = net, rng, {"s": None, "f": None}, 0

    def reset(self):
        self.place = {"s": None, "f": None}

    def act(self, w):
        if w.m_shelter.any():
            ys, xs = np.nonzero(w.m_shelter)
            self.place["f"] = (int(xs[0]), int(ys[0]))
        s, f = w.deficits()
        for c, need in (("s", s), ("f", f)):
            if need >= HIGH[c] and self.place[c] is not None and self.place[c] != w.pos:
                a = W.bfs_path(lambda cell: not w.m_wall[cell[1], cell[0]], w.pos, [self.place[c]])
                if a is not None:
                    self.walks += 1
                    return a
        return self.net.act(w.obs_map(), R3.levels(w, "D3"), w.pos, self.rng)[0]

    def after(self, w, ate):
        if ate:
            self.place["s"] = w.pos


def run_life_f(pol, land, R, rng):
    """run_w3.run_life for F (it needs the 'ate' flag after each step)."""
    w = W.World(land, R)
    known500, hungry, exhausted = None, 0, 0
    while not w.done():
        a = pol.act(w)
        _, ate = w.step(a)
        pol.after(w, ate)
        hungry += w.E < R3.HUNGRY
        exhausted += w.F > R3.EXHAUSTED
        if w.t == 500:
            known500 = w.land_known()
    m = W.life_measures(w)
    m.update({"known500": known500 if known500 is not None else w.land_known(), "known_end": w.land_known(),
              "hungry": hungry / max(1, w.t), "exhausted": exhausted / max(1, w.t)})
    return w, m


def test(arm, seed):
    """Learning off; W3's test (the same lands, the same generator per land)."""
    R = R3.regrowth()
    net = load(arm, seed)
    before = {k: v.copy() for k, v in net.p.items()}
    lives = []
    for ls in W.TEST_SEEDS:
        land = W.make_land(ls)
        rng = np.random.default_rng(ls)
        if arm == "F":
            pol = FPolicy(net, rng)
            _, m = run_life_f(pol, land, R, rng)
            m["f_walks"] = pol.walks
        else:
            _, m = R3.run_life(lambda w: net.act(w.obs_map(), R3.levels(w, "D3"), w.pos, rng)[0], land, R, rng)
        lives.append(m)
    assert all(np.array_equal(before[k], net.p[k]) for k in net.p), "weights changed in testing"
    OUT.mkdir(exist_ok=True)
    (OUT / f"test_{arm}_{seed}.json").write_text(json.dumps(lives))
    return lives


# ---- step 0: the diagnostic on W3's saved weights --------------------------------------------------------------
def cell_values(net, w, kind):
    fw = net.plan(w.obs_map()[None], np.asarray(R3.levels(w, kind), float)[None])
    return fw, fw[5].max(1).reshape(B.N, B.N)                     # [y, x]


def open_neighbours(w):
    out = []
    for a, (dx, dy) in enumerate(W.MOVES[:4]):
        x, y = w.pos[0] + dx, w.pos[1] + dy
        if 0 <= x < B.N and 0 <= y < B.N and not w.m_wall[y, x]:
            out.append((a, x, y))
    return out


def greedy_action(v, w):
    """(b): the open neighbour with the highest value; stay if none beats the own cell."""
    best, bv = 4, v[w.pos[1], w.pos[0]]
    for a, x, y in open_neighbours(w):
        if v[y, x] > bv:
            best, bv = a, v[y, x]
    return best


def lookahead_action(v, w):
    """(c): the open neighbour whose own best open neighbour (or itself) has the highest value; stay if none beats
    the own cell."""
    best, bv = 4, v[w.pos[1], w.pos[0]]
    for a, x, y in open_neighbours(w):
        sc = v[y, x]
        for dx, dy in W.MOVES[:4]:
            x2, y2 = x + dx, y + dy
            if 0 <= x2 < B.N and 0 <= y2 < B.N and not w.m_wall[y2, x2]:
                sc = max(sc, v[y2, x2])
        if sc > bv:
            best, bv = a, sc
    return best


def contributions(net, fw, w):
    """At one step: the mean |part| over open cells for W0, s*Ws, f*Wf, c*Wc, and the reward-map value at the remembered
    food cells minus the mean over the other open cells (None if no food is remembered)."""
    T, c_x, lev_cells, c_r, trace, q = fw
    p = net.p
    Wstack = np.stack([p["W0"].reshape(-1), p["Ws"].reshape(-1), p["Wf"].reshape(-1), p["Wc"].reshape(-1)], 1)
    parts = (c_x @ Wstack) * lev_cells                              # (N*N, 4)
    r = parts.sum(1) + p["br"][0]
    open_ = ~w.m_wall.reshape(-1)
    food = w.m_food.reshape(-1) & open_
    out = {"W0": float(np.abs(parts[open_, 0]).mean()), "sWs": float(np.abs(parts[open_, 1]).mean()),
           "fWf": float(np.abs(parts[open_, 2]).mean()), "cWc": float(np.abs(parts[open_, 3]).mean())}
    out["food_minus_rest"] = float(r[food].mean() - r[open_ & ~food].mean()) if food.any() and (open_ & ~food).any() else None
    return out


def step0(kind, seed):
    R = R3.regrowth()
    net = R3.load(kind, seed)
    res = {"kind": kind, "seed": seed, "a": [], "b": [], "c": [], "agree": [], "hungry": []}
    for ls in W.TEST_SEEDS:
        land = W.make_land(ls)
        # (a) W3's walk, re-run, with the agreement log and the hungry-step contributions
        rng = np.random.default_rng(ls)
        agree, steps, hung = 0, 0, []

        def pol_a(w):
            nonlocal agree, steps
            fw, v = cell_values(net, w, kind)
            z, _ = net.head(fw, np.array([w.pos[1] * B.N + w.pos[0]]))
            pi = B.softmax(z[0])
            a = int(rng.choice(5, p=pi))
            agree += int(int(pi.argmax()) == greedy_action(v, w))
            steps += 1
            if w.deficits()[0] >= 0.5:
                hung.append(contributions(net, fw, w))
            return a
        _, m = R3.run_life(pol_a, land, R, rng)
        res["a"].append(m)
        res["agree"].append(agree / max(1, steps))
        if hung:
            keys = ("W0", "sWs", "fWf", "cWc")
            h = {k: float(np.mean([x[k] for x in hung])) for k in keys}
            fm = [x["food_minus_rest"] for x in hung if x["food_minus_rest"] is not None]
            h["food_minus_rest"] = float(np.mean(fm)) if fm else None
            h["n_steps"] = len(hung)
            res["hungry"].append(h)
        # (b) and (c): no action head
        for key, choose in (("b", greedy_action), ("c", lookahead_action)):
            rng2 = np.random.default_rng(ls)
            _, m = R3.run_life(lambda w: choose(cell_values(net, w, kind)[1], w), land, R, rng2)
            res[key].append(m)
    OUT.mkdir(exist_ok=True)
    (OUT / f"step0_{kind}_{seed}.json").write_text(json.dumps(res))
    print("step0", kind, seed, {k: round(float(np.mean([x["survived"] for x in res[k]])), 3) for k in "abc"},
          "agree", round(float(np.mean(res["agree"])), 3), flush=True)
    return res


if __name__ == "__main__":
    cmd = sys.argv[1]
    if cmd == "step0":
        step0(sys.argv[2], int(sys.argv[3]))
    elif cmd == "train":
        train(sys.argv[2], int(sys.argv[3]), float(sys.argv[4]) if len(sys.argv) > 4 else 4.5)
    elif cmd == "test":
        test(sys.argv[2], int(sys.argv[3]))
    elif cmd == "run":
        arm, seed = sys.argv[2], int(sys.argv[3])
        if train(arm, seed, float(sys.argv[4]) if len(sys.argv) > 4 else 4.5):
            test(arm, seed)
            print("done", arm, seed, flush=True)
