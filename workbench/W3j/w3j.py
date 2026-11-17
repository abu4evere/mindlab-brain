"""W3j: keep what the parent taught (questions.md, W3j-frozen). W3i's C (W3d's PYFR, 1.2M fade, no pain) with:
CK the learning rate x 0.1 after the fade; CV a quiet parent (copy weight 0.05) after the fade; C4 4M steps; C2 4M
steps with a 2.4M fade. CF is the end-of-fade snapshot. Snapshots at the fade end and every 400,000 steps after it.

  python w3j.py run ARM SEED [HOURS]    ARM in CK, CV, C4, C2 (train in stages, resumable; then the tests)
  python w3j.py repro SEED [HOURS]      C again with this code; compare with W3i's saved weights
"""
from __future__ import annotations

import json
import os
import pickle
import sys
import time
from pathlib import Path

os.environ.setdefault("OPENBLAS_NUM_THREADS", "1")
import numpy as np  # noqa: E402

HERE = Path(__file__).parent
sys.path.insert(0, str(HERE.parent / "W3i"))
import w3i  # noqa: E402
from w3i import w3d, w3b, B, W, R3  # noqa: E402

OUT = HERE / "output"
ARMS = {"CK": {"steps": 2_800_000, "fade": 1_200_000}, "CV": {"steps": 2_800_000, "fade": 1_200_000},
        "C4": {"steps": 4_000_000, "fade": 1_200_000}, "C2": {"steps": 4_000_000, "fade": 2_400_000},
        "C": {"steps": 2_800_000, "fade": 1_200_000}}
EVERY_SNAP = 400_000
LR0 = B.LR
CK_FACTOR, CV_WEIGHT = 0.1, 0.05
_orig_copy, _orig_present = w3d._ns["copy_weight"], w3d._ns["parent_present"]


def snaps(arm):
    a = ARMS[arm]
    return tuple(range(a["fade"], a["steps"], EVERY_SNAP))


def configure(arm):
    w3i.install()
    w3d.ARMS[arm] = {"parts": "YR", "always": False}
    w3d.configure(arm)
    fade = ARMS[arm]["fade"]
    w3d.CFG.update(child=fade, always=False)
    w3b.OUT = w3i.OUT = OUT
    B.LR = LR0
    if arm == "CV":                         # after the fade the parent stays, at copy weight 0.05 (every 4th step)
        w3d._ns["copy_weight"] = lambda total: _orig_copy(total) if total < fade else CV_WEIGHT
        w3d._ns["parent_present"] = lambda total: True
    else:
        w3d._ns["copy_weight"], w3d._ns["parent_present"] = _orig_copy, _orig_present


def tag_of(arm, seed, step):
    return f"{arm}_{seed}_{step // 1000}k"


def load_npz(path, seed):
    net = B.DriveVIN(seed, fixed_map=False)
    with np.load(path) as z:
        for k in net.p:
            net.p[k] = z[k].copy()
    return net


def train_staged(arm, seed, hours=4.5, steps=None, snapshot_at=None):
    """W3d's training, paused at the first life boundary after each snapshot (tested and saved), resumable.
    CK: from the fade snapshot on, every update uses the learning rate x 0.1."""
    OUT.mkdir(exist_ok=True)
    steps = steps or ARMS[arm]["steps"]
    snapshot_at = snaps(arm) if snapshot_at is None else snapshot_at
    fade = ARMS[arm]["fade"]
    R = R3.regrowth()
    cp = w3b.ckpt_path(arm, seed)
    state = pickle.loads(cp.read_bytes()) if cp.exists() else None
    t0 = time.time()
    with open(OUT / f"{arm}_{seed}.log", "a") as log:
        while True:
            total = state["total"] if state else 0
            pending = [x for x in snapshot_at if not (OUT / f"{tag_of(arm, seed, x)}.npz").exists()]
            nxt = min(pending) if pending else None
            if nxt is not None and total >= nxt:
                net = B.DriveVIN(seed, fixed_map=False)
                for k in net.p:
                    net.p[k] = state["p"][k].copy()
                tag = tag_of(arm, seed, nxt)
                w3i.test_all(net, tag, W.TEST_SEEDS)
                np.savez(OUT / f"{tag}.npz", **net.p)
                print(f"snapshot {tag} at step {total}", file=log, flush=True)
                cp.write_bytes(pickle.dumps(state))
                continue
            left = hours - (time.time() - t0) / 3600
            if left <= 0:
                break
            B.LR = LR0 * CK_FACTOR if (arm == "CK" and total >= fade and total > 0) else LR0
            net, state, finished = w3d.train_net_parent(arm, seed, steps, R, left, log, state, pause_after=nxt)
            if finished:
                np.savez(OUT / f"{arm}_{seed}.npz", **net.p)
                (OUT / f"{arm}_{seed}_norms.json").write_text(json.dumps(state["norms"]))
                (OUT / f"{arm}_{seed}_lives.json").write_text(json.dumps({"lives": state["lives_log"],
                                                                            "updates": state["updates"]}))
                if cp.exists():
                    cp.unlink()
                B.LR = LR0
                return True
            if nxt is not None and state["total"] >= nxt:
                continue
            break
    B.LR = LR0
    cp.write_bytes(pickle.dumps(state))
    print("paused", arm, seed, "at step", state["total"], flush=True)
    return False


def drift_and_parent(final, snap, seeds, R):
    """On the final brain's own test lives (the test's generator): the share of steps where its greedy move differs
    from the end-of-fade brain's greedy move, and the share where it equals W3's Script on the same map view."""
    out = []
    for ls in seeds:
        rng = np.random.default_rng(ls)
        land = W.make_land(ls)
        script = W.Script()
        rec = {"n": 0, "differ": 0, "parent": 0}

        def policy(w):
            m, lev = w.obs_map(), R3.levels(w, "D3")
            a, pi, _ = final.act(m, lev, w.pos, rng)
            _, pi_s, _ = snap.act(m, lev, w.pos, None, greedy=True)
            pa = script.act(W.MapView(w))
            rec["n"] += 1
            rec["differ"] += int(int(np.argmax(pi)) != int(np.argmax(pi_s)))
            rec["parent"] += int(int(np.argmax(pi)) == pa)
            return a
        R3.run_life(policy, land, R, rng)
        out.append({"drift": rec["differ"] / max(1, rec["n"]), "parent_agree": rec["parent"] / max(1, rec["n"])})
    return out


def run(arm, seed, hours):
    configure(arm)
    if train_staged(arm, seed, hours):
        final = load_npz(OUT / f"{arm}_{seed}.npz", seed)
        w3i.test_all(final, f"{arm}_{seed}", W.TEST_SEEDS)
        w3i.test_all(final, f"fresh_{arm}_{seed}", w3i.FRESH_SEEDS)
        snap = load_npz(OUT / f"{tag_of(arm, seed, ARMS[arm]['fade'])}.npz", seed)
        dp = drift_and_parent(final, snap, W.TEST_SEEDS, R3.regrowth())
        (OUT / f"drift_{arm}_{seed}.json").write_text(json.dumps(dp))
        print("done", arm, seed, flush=True)


def repro(seed, hours):
    """W3i's C seed again with this code (no snapshots, as W3i trained it); compare with W3i's saved weights."""
    configure("C")
    if train_staged("C", seed, hours, snapshot_at=()):
        a = OUT / f"C_{seed}.npz"
        b = HERE.parent / "W3i" / "output" / f"C_{seed}.npz"
        with np.load(a) as x, np.load(b) as y:
            exact = all(np.array_equal(x[k], y[k]) for k in y.files)
            diff = max(float(np.abs(x[k] - y[k]).max()) for k in y.files)
        (OUT / f"repro_{seed}.json").write_text(json.dumps({"exact": exact, "max_abs_diff": diff}))
        print("repro", seed, "exact", exact, flush=True)


if __name__ == "__main__":
    if sys.argv[1] == "run":
        run(sys.argv[2], int(sys.argv[3]), float(sys.argv[4]) if len(sys.argv) > 4 else 4.5)
    elif sys.argv[1] == "repro":
        repro(int(sys.argv[2]), float(sys.argv[3]) if len(sys.argv) > 3 else 4.5)
