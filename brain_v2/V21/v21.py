"""V2-1 Revise (questions.md, V21-frozen): a revision rule for Bob's count tables, on frozen brains.

Test A: W3r's RM kept copy (RMS), W3r's native MeaningWorld; W3r's meaning table replaced by RevTable (mode PLAIN,
SURPRISE, WINDOW or SHAM); conditions 'swap' (w3r.TEST midswap: from step 1,500 wall and food colours exchanged) and
'stable'. Test B: CW1's world and consequence model (K = 4) with RevModel; from step 1,500 the joining operation
becomes another (seeded per land).
  SURPRISE: on an event contradicting a confident prediction (n >= 3, |y - p| >= 0.75; CW1: usual next hand state with
            n >= 3, share >= 0.75, a different one observed) the whole look (key) is reset to 0 before the event.
  WINDOW:   every event first multiplies the touched cell (key) by 0.95.
  SHAM:     at the moments SURPRISE would reset, a different look (key) with counts, drawn at random, is reset.
  PLAIN:    W3r's / CW1's counts unchanged.
  python v21.py A ARM COND SEED [test|pilot]   -> output/A_{ARM}_{COND}_{SEED}.jsonl
  python v21.py B ARM SEED [test|pilot]        -> output/B_{ARM}_{SEED}.jsonl
"""
from __future__ import annotations

import json
import platform
import sys
import time
from pathlib import Path

HERE = Path(__file__).parent
sys.path.insert(0, str(HERE.parents[1] / "body" / "CW1"))
import cw1  # noqa: E402  (W3r's chain first: the numerical settings before numpy loads)
import numpy as np  # noqa: E402
from cw1 import W, w3k, R3  # noqa: E402

w3r, w3m = cw1.w3r, cw1.w3r.w3m
BRAINS, OUT = HERE.parents[1] / "body" / "CW1" / "brains", HERE / "output"
V21_SEED = 20261129
SWAP_T = W.LIFE // 2
LANDS = {"A": range(960001, 960051), "B": range(970001, 970051), "pilot": range(980001, 980006)}
ARMS = ("PLAIN", "SURPRISE", "WINDOW", "SHAM")
N_MIN, GAP, KEEP_W = 3, 0.75, 0.95
CFG = {"mode": "PLAIN", "change": True, "life_seed": 0}


class RevTable(w3r.Table):
    def __init__(self, mode, rng):
        super().__init__()
        self.mode, self.rng, self.resets = mode, rng, 0

    def add(self, code, j, y):
        if self.mode == "WINDOW":
            self.pos[code, j] *= KEEP_W
            self.neg[code, j] *= KEEP_W
        elif self.mode in ("SURPRISE", "SHAM"):
            n = self.pos[code, j] + self.neg[code, j]
            if n >= N_MIN and abs(float(y) - self.pos[code, j] / n) >= GAP - 1e-12:
                if self.mode == "SURPRISE":
                    target = code
                else:
                    others = [c for c in range(8) if c != code and (self.pos[c] + self.neg[c]).sum() > 0]
                    target = others[int(self.rng.integers(len(others)))] if others else None
                if target is not None:
                    self.pos[target, :] = 0.0
                    self.neg[target, :] = 0.0
                    self.resets += 1
        super().add(code, j, y)


class V21World(w3r.MeaningWorld):
    def __init__(self, land, R):
        super().__init__(land, R)
        self.mod = RevTable(CFG["mode"], np.random.default_rng([V21_SEED, int(land["seed"])]))


def ranks_right(w):
    """Does the table rank the true food colour first for fed and the true wall colour first for blocked?"""
    p = w.mod.pred()
    c = [w3r.code_of(r) for r in w.codes()]
    land = set(c) | {0}
    food_ok = all(p[c[1], 1] > p[x, 1] for x in land if x != c[1])
    wall_ok = all(p[c[0], 0] > p[x, 0] for x in land if x != c[0])
    return food_ok, wall_ok


def life_a(net, seed, ls, mode, swap, on_step=None):
    w3r.configure("RM", seed)
    W.World = V21World
    CFG["mode"] = mode
    w3r.TEST["midswap"] = swap
    land, R, rng = W.make_land(ls), R3.regrowth(), np.random.default_rng(ls)
    rfx = w3m.Reflex()                                   # = w3m.policy, built here to read the hunger reflex
    state = {"hungry": False}

    def pol(w):
        a = rfx.act(w, net.act(w.obs_map(), R3.levels(w, "D3"), w.pos, rng)[0])
        state["hungry"] = rfx.hungry
        return a
    rec = {"meals_post": 0, "meals_post_reflex": 0, "latency": None}

    def step_hook(w, a, d0, cur):
        if w.t > SWAP_T and w.last_meal == w.t:
            rec["meals_post"] += 1
            rec["meals_post_reflex"] += state["hungry"]
        if swap and w.t >= SWAP_T and rec["latency"] is None and all(ranks_right(w)):
            rec["latency"] = w.t - SWAP_T
        if on_step is not None:
            on_step(w, a, d0, cur)
    try:
        w, m = R3.run_life(pol, land, R, rng, on_step=step_hook)
    finally:
        w3r.TEST["midswap"] = False
    fo, wo = ranks_right(w)
    m.update({"land": ls, "resets": w.mod.resets, "acc_food": fo, "acc_wall": wo, **rec})
    return w, m


# --- Test B: CW1 with the join changed mid-life --------------------------------------------------------------------
class RevModel(cw1.Model):
    def __init__(self, K, rng):
        super().__init__(K, rng)
        self.mode, self.resets = CFG["mode"], 0
        self.srng = np.random.default_rng([V21_SEED, CFG["life_seed"], 3])   # never touches the model's own stream
        CFG["last_model"] = self

    def _drop(self, k):
        self.n.pop(k, None)
        self.gain.pop(k, None)
        self.nxt.pop(k, None)

    def learn(self, h, u, v, h2, gain):
        k = self.key(h, u, v)
        if k in self.n:
            if self.mode == "WINDOW":
                self.n[k] *= KEEP_W
                self.gain[k] *= KEEP_W
                self.nxt[k] = {o: c * KEEP_W for o, c in self.nxt[k].items()}
            elif self.mode in ("SURPRISE", "SHAM"):
                top, c = max(self.nxt[k].items(), key=lambda kv: kv[1])
                if self.n[k] >= N_MIN and c / self.n[k] >= GAP - 1e-12 and h2 != top:
                    if self.mode == "SURPRISE":
                        self._drop(k)
                        self.resets += 1
                    else:
                        others = sorted((x for x in self.n if x != k), key=repr)
                        if others:
                            self._drop(others[int(self.srng.integers(len(others)))])
                            self.resets += 1
        super().learn(h, u, v, h2, gain)


class ChangeWorld(cw1.CW1World):
    def __init__(self, land, R):
        super().__init__(land, R)
        self.chain_times = []
        self.join2 = None
        if cw1.CFG["things"] and self.K > 1 and CFG["change"]:
            r = np.random.default_rng([V21_SEED, int(land["seed"]), 2])
            opts = [k for k in range(self.K) if k != self.join_op]
            self.join2 = int(opts[int(r.integers(len(opts)))])

    def hand_step(self, verb):
        if self.join2 is not None and self.t + 1 >= SWAP_T:      # from the step that ends at t >= 1,500
            self.join_op = self.join2
        c0 = self.stats["chains"]
        out = super().hand_step(verb)
        if self.stats["chains"] > c0:
            self.chain_times.append(self.t)
        return out


def life_b(net, seed, ls, mode, change=True):
    cw1.configure("LEARN", seed)
    W.World = ChangeWorld
    CFG.update(mode=mode, change=change, life_seed=int(ls))
    orig = cw1.Model
    cw1.Model = RevModel
    try:
        w, m = cw1.life(net, seed, ls, "LEARN")
    finally:
        cw1.Model = orig
    ct = w.chain_times
    m.update({"chains_before": sum(t < SWAP_T for t in ct), "chains_after": sum(t >= SWAP_T for t in ct),
              "join_changed": w.join2 is not None, "resets": CFG["last_model"].resets})
    return w, m


def machine():
    return {"platform": platform.platform(), "python": platform.python_version(), "numpy": np.__version__,
            "node": platform.node()}


def run(test, arm, cond, seed, which):
    assert arm in ARMS
    OUT.mkdir(exist_ok=True)
    lands = LANDS["pilot"] if which == "pilot" else LANDS[test]
    name = f"{'pilot_' if which == 'pilot' else ''}{test}_{arm}" + (f"_{cond}" if test == "A" else "") + f"_{seed}.jsonl"
    path = OUT / name
    done = set()
    if path.exists():
        done = {json.loads(x)["land"] for x in path.read_text().splitlines() if x.strip()}
    net = w3k.load_npz(BRAINS / f"RM_CS_{seed}.npz", seed)
    mach = machine()
    with open(path, "a") as f:
        for ls in lands:
            if ls in done:
                continue
            t0 = time.time()
            if test == "A":
                _, m = life_a(net, seed, ls, arm, cond == "swap")
            else:
                _, m = life_b(net, seed, ls, arm)
            m.pop("acts_by_verb", None)
            m.update({"test": test, "arm": arm, "cond": cond, "seed": seed, "seconds": round(time.time() - t0, 2),
                      "machine": mach})
            f.write(json.dumps(m, default=float) + "\n")
            f.flush()
    print("done", test, arm, cond, seed, flush=True)


if __name__ == "__main__":
    a = sys.argv
    if a[1] == "A":
        run("A", a[2], a[3], int(a[4]), a[5] if len(a) > 5 else "test")
    elif a[1] == "B":
        run("B", a[2], "change", int(a[3]), a[4] if len(a) > 4 else "test")
