"""W3i: more practice, a longer childhood (questions.md, W3i-frozen). W3d's PYFR with a different number of training
steps and a different fade length; snapshots for L and LC; stale-food measures and WX's death labels in the test; a
test on fresh lands; and the reproduction job.

  python w3i.py run ARM SEED [HOURS]    ARM in L, LC, C (train in stages, resumable; then the tests)
  python w3i.py repro SEED [HOURS]      W3d's PYFR again (2,000,000 steps); compare with W3d's saved weights
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
import numpy as np  # noqa: E402

HERE = Path(__file__).parent
sys.path.insert(0, str(HERE.parent / "W3d"))
sys.path.insert(0, str(HERE.parent / "WX"))
import w3d  # noqa: E402
from w3d import w3b, B, W, R3  # noqa: E402
import wx  # noqa: E402

OUT = HERE / "output"
ARMS = {"L": {"steps": 6_000_000, "fade": 400_000, "snaps": (2_000_000, 4_000_000)},
        "LC": {"steps": 6_000_000, "fade": 1_200_000, "snaps": (2_000_000, 4_000_000)},
        "C": {"steps": 2_800_000, "fade": 1_200_000, "snaps": ()},
        "PYFR": {"steps": 2_000_000, "fade": 400_000, "snaps": ()}}
FRESH_SEEDS = range(910001, 910051)
BaseWorld, base_life_measures = W.World, W.life_measures


class StaleWorld(BaseWorld):
    """W3's World plus two counters (read-only for the brain): arrivals at a cell the memory shows as full food that is
    really empty, and the step of the last meal."""
    def __init__(self, land, R):
        super().__init__(land, R)
        self.stale, self.last_meal = 0, None

    def step(self, a):
        dx, dy = W.MOVES[a]
        nx, ny = self.pos[0] + dx, self.pos[1] + dy
        remembered = a != 4 and 0 <= nx < W.N and 0 <= ny < W.N and bool(self.m_food[ny, nx]) and not self.walls[ny, nx]
        really_full = self.food_full((nx, ny)) if remembered else False
        cur, ate = super().step(a)
        if remembered and self.pos == (nx, ny) and not really_full:
            self.stale += 1
        if ate:
            self.last_meal = self.t
        return cur, ate


def life_measures(w):
    m = base_life_measures(w)
    m.update({"stale": w.stale, "stale_per_1000": 1000.0 * w.stale / max(1, w.t),
              "since_meal_end": w.t - (w.last_meal or 0)})
    return m


def install():
    W.World = StaleWorld
    W.life_measures = life_measures


def configure(arm):
    install()
    w3d.ARMS[arm] = {"parts": "YR", "always": False}
    w3d.configure(arm)
    w3d.CFG.update(child=ARMS[arm]["fade"], always=False)
    w3b.OUT = OUT


def policy(net, rng):
    return lambda w: net.act(w.obs_map(), R3.levels(w, "D3"), w.pos, rng)[0]


def test_life(net, ls, R):
    """One test life (the test's own generator), with WX's recorder for the death labels."""
    land = W.make_land(ls)
    rng = np.random.default_rng(ls)
    tail = deque(maxlen=100)

    def on_step(w, a, d0, cur):
        tail.append((wx.nearest_food(w), w.F > W.F_TIRED))
    w, m = R3.run_life(policy(net, rng), land, R, rng, on_step=on_step)
    if w.dead:
        t = list(tail)
        m["labels"] = {"no_food_known": not (t and t[-1][0] is not None),
                       "food_known_not_reached": any(d is not None and d <= 30 for d, _ in t),
                       "exhaustion": sum(x for _, x in t) >= 50}
    return m


def test_all(net, tag, seeds):
    R = R3.regrowth()
    before = {k: v.copy() for k, v in net.p.items()}
    lives = [test_life(net, ls, R) for ls in seeds]
    assert all(np.array_equal(before[k], net.p[k]) for k in net.p), "weights changed in testing"
    (OUT / f"test_{tag}.json").write_text(json.dumps(lives))
    return lives


def train_staged(arm, seed, hours=4.5, steps=None, snaps=None):
    """W3d's training, paused at the first life boundary after each snapshot; resumable. Returns True when finished."""
    OUT.mkdir(exist_ok=True)
    steps = steps or ARMS[arm]["steps"]
    snaps = ARMS[arm]["snaps"] if snaps is None else snaps
    R = R3.regrowth()
    cp = w3b.ckpt_path(arm, seed)
    state = pickle.loads(cp.read_bytes()) if cp.exists() else None
    t0 = time.time()
    with open(OUT / f"{arm}_{seed}.log", "a") as log:
        while True:
            total = state["total"] if state else 0
            pending = [x for x in snaps if not (OUT / f"{arm}_{seed}_{x // 1_000_000}M.npz").exists()]
            nxt = min(pending) if pending else None
            if nxt is not None and total >= nxt:                     # snapshot (at the life boundary just passed)
                net = B.DriveVIN(seed, fixed_map=False)
                for k in net.p:
                    net.p[k] = state["p"][k].copy()
                tag = f"{arm}_{seed}_{nxt // 1_000_000}M"
                test_all(net, tag, W.TEST_SEEDS)
                np.savez(OUT / f"{tag}.npz", **net.p)
                print(f"snapshot {tag} at step {total}", file=log, flush=True)
                cp.write_bytes(pickle.dumps(state))
                continue
            left = hours - (time.time() - t0) / 3600
            if left <= 0:
                break
            net, state, finished = w3d.train_net_parent(arm, seed, steps, R, left, log, state, pause_after=nxt)
            if finished:
                np.savez(OUT / f"{arm}_{seed}.npz", **net.p)
                (OUT / f"{arm}_{seed}_norms.json").write_text(json.dumps(state["norms"]))
                (OUT / f"{arm}_{seed}_lives.json").write_text(json.dumps({"lives": state["lives_log"],
                                                                            "updates": state["updates"]}))
                if cp.exists():
                    cp.unlink()
                return True
            if nxt is not None and state["total"] >= nxt:
                continue
            break
    cp.write_bytes(pickle.dumps(state))
    print("paused", arm, seed, "at step", state["total"], flush=True)
    return False


def load(arm, seed):
    net = B.DriveVIN(seed, fixed_map=False)
    with np.load(OUT / f"{arm}_{seed}.npz") as z:
        for k in net.p:
            net.p[k] = z[k].copy()
    return net


def run(arm, seed, hours):
    configure(arm)
    if train_staged(arm, seed, hours):
        net = load(arm, seed)
        test_all(net, f"{arm}_{seed}", W.TEST_SEEDS)
        test_all(net, f"fresh_{arm}_{seed}", FRESH_SEEDS)
        print("done", arm, seed, flush=True)


def repro(seed, hours):
    """W3d's PYFR again, exactly as W3d trained it (w3b.train, 2,000,000 steps); compare with W3d's saved weights."""
    configure("PYFR")
    w3d.CFG.update(child=w3d.CHILD, always=False)
    w3b.OUT = OUT / "repro"
    w3b.OUT.mkdir(parents=True, exist_ok=True)
    if w3b.train("PYFR", seed, hours):
        with np.load(w3b.OUT / f"PYFR_{seed}.npz") as a, np.load(HERE.parent / "W3d" / "output" / f"PYFR_{seed}.npz") as b:
            exact = all(np.array_equal(a[k], b[k]) for k in b.files)
            close = all(np.allclose(a[k], b[k], atol=1e-9) for k in b.files)
            diff = max(float(np.abs(a[k] - b[k]).max()) for k in b.files)
        (OUT / f"repro_{seed}.json").write_text(json.dumps({"exact": exact, "allclose_1e-9": close, "max_abs_diff": diff}))
        print("repro", seed, "exact", exact, "max diff", diff, flush=True)


if __name__ == "__main__":
    if sys.argv[1] == "run":
        run(sys.argv[2], int(sys.argv[3]), float(sys.argv[4]) if len(sys.argv) > 4 else 4.5)
    elif sys.argv[1] == "repro":
        repro(int(sys.argv[2]), float(sys.argv[3]) if len(sys.argv) > 3 else 4.5)
