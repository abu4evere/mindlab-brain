"""W3k: a longer childhood still, and keeping the adult's best (questions.md, W3k-frozen).

W3d's training with a parent (as W3j's C2), plus three things, added at anchors in W3d's training source:
  - CS / CY: at the end of each training life the brain may keep a copy of itself (its own-lives rule; a step drawn in
    advance). They never change training: R2, CS and CY are one run ("R").
  - CR: in the second half of the fade, the parent's examples are kept (reservoir, at most 20,000); after the fade,
    every 4th step, one is replayed as a copy step at weight 0.05.
  - Numerical determinism: OpenBLAS's Zen kernels and NumPy without AVX-512 paths, set before numpy loads; only on
    processors verified to train bit-identically (amendment 2).

  python w3k.py run RUN SEED [HOURS]     RUN in R, C3, CR (train in stages, resumable; then the tests)
  python w3k.py det NAME SEED [HOURS]    the determinism job: run "R" again into output/NAME_<seed>*, then compare
"""
from __future__ import annotations

import os

def _cpu():
    try:
        return next(l.split(":", 1)[1].strip() for l in open("/proc/cpuinfo") if l.startswith("model name"))
    except (OSError, StopIteration):
        import platform
        return platform.processor()


CPU = _cpu()
# Amendment 2: the processors verified (tools/diag_seg.py, 18 Nov) to train bit-identically with these settings are
# GitHub's Intel Xeons (6975P, 6973P, 8370C) and AMD EPYC 7763. The newer AMD EPYCs (9V74, 9V45) crash with any forced
# OpenBLAS core and differ without one: a job that lands there hands itself back (wrong_machine.flag) and is re-queued.
GOOD_MACHINE = ("Intel" in CPU) or ("EPYC 7" in CPU) or not os.path.exists("/proc/cpuinfo")
# the same numerical path on every verified machine: set before numpy is loaded anywhere
if GOOD_MACHINE:
    os.environ["OPENBLAS_CORETYPE"] = "Zen"
os.environ["NPY_DISABLE_CPU_FEATURES"] = "AVX512_SPR AVX512_ICL X86_V4"   # amendment 1: all AVX-512 groups
os.environ["OPENBLAS_NUM_THREADS"] = os.environ["OMP_NUM_THREADS"] = os.environ["MKL_NUM_THREADS"] = "1"

import json  # noqa: E402
import pickle  # noqa: E402
import platform  # noqa: E402
import sys  # noqa: E402
import time  # noqa: E402
from collections import deque  # noqa: E402
from pathlib import Path  # noqa: E402

import numpy as np  # noqa: E402

HERE = Path(__file__).parent
sys.path.insert(0, str(HERE.parent / "W3i"))
import w3i  # noqa: E402
from w3i import w3d, w3b, B, W, R3  # noqa: E402

OUT = HERE / "output"
RUNS = {"R": {"steps": 4_000_000, "fade": 2_400_000}, "C3": {"steps": 5_200_000, "fade": 3_600_000},
        "CR": {"steps": 4_000_000, "fade": 2_400_000}}
EVERY_SNAP = 400_000
CS_WINDOW, CS_START = 200_000, 200_000      # CS: mean length of lives ended in the last 200k steps, from fade + 200k
CY_SEED = 20261181
PSTORE_CAP, REPLAY_W = 20_000, 0.05
CFG = {"run": "R", "fade": 2_400_000, "steps": 4_000_000, "cy_step": None, "seed": 1}


# ── the hooks (called from inside the training loop; they never touch the training generator) ─────────────────────
def cy_step_for(seed, run=None):
    """CY's step, drawn in advance: uniform between fade + 200k and the end of training."""
    a = RUNS[run or "R"]
    rng = np.random.default_rng(CY_SEED + seed)
    return int(rng.integers(a["fade"] + CS_START, a["steps"]))


def _pack(m):
    """Store a map compactly when that is exact (the maps are 0/1); otherwise keep it as it is."""
    u = m.astype(np.uint8)
    return u if np.array_equal(u.astype(m.dtype), m) else m.copy()


def parent_hook(state, total, ex):
    """CR only: keep the parent's example, by reservoir sampling, during the second half of the fade."""
    if CFG["run"] != "CR" or total < CFG["fade"] // 2:
        return
    ps = state.setdefault("pstore", [])
    state["pseen"] = state.get("pseen", 0) + 1
    rng = np.random.default_rng()
    rng.bit_generator.state = state.setdefault("prng", np.random.default_rng([CFG["seed"], 77]).bit_generator.state)
    m, lev, cell, pa = ex
    item = (_pack(m), lev, cell, pa)
    if len(ps) < PSTORE_CAP:
        ps.append(item)
    else:
        j = int(rng.integers(state["pseen"]))
        if j < PSTORE_CAP:
            ps[j] = item
    state["prng"] = rng.bit_generator.state


def adult_hook(net, state, total):
    """CR only: after the fade, every 4th step, one copy step at weight 0.05 toward a stored parent example."""
    if CFG["run"] != "CR" or total % w3d.EVERY != 0 or not state.get("pstore"):
        return False
    rng = np.random.default_rng()
    rng.bit_generator.state = state["prng"]
    m, lev, cell, pa = state["pstore"][int(rng.integers(len(state["pstore"])))]
    state["prng"] = rng.bit_generator.state
    w3b.imitate(net, [(m.astype(np.float64), lev, cell, pa)], [REPLAY_W])
    return True


def life_hook(net, state, total, t):
    """At the end of every training life: CS keeps a copy when its recent lives are the longest so far; CY keeps the
    copy at its pre-drawn step. Both only read; training is unchanged."""
    ends = state.setdefault("cs_ends", deque())
    ends.append((total, t))
    while ends and ends[0][0] <= total - CS_WINDOW:
        ends.popleft()
    if total >= CFG["fade"] + CS_START and ends:
        mean = sum(x[1] for x in ends) / len(ends)
        if mean > state.get("cs_best", -1.0):
            state["cs_best"], state["cs_step"] = mean, total
            state["cs_p"] = {k: v.copy() for k, v in net.p.items()}
    if CFG["cy_step"] is not None and "cy_p" not in state and total >= CFG["cy_step"]:
        state["cy_at"] = total
        state["cy_p"] = {k: v.copy() for k, v in net.p.items()}


# W3d's training source (already with the parent), with the three hooks inserted at anchors (checked to be present)
_src = w3d._src
_anchors = [
    ("                    upd['copy'] = upd.get('copy', 0) + 1\n",
     "                    upd['copy'] = upd.get('copy', 0) + 1\n"
     "                    parent_hook(state, total, (m, lev, cell, pa))\n"
     "            elif adult_hook(net, state, total):\n"
     "                upd['replay_parent'] = upd.get('replay_parent', 0) + 1\n"),
    ("        lives_survived += int(w.t >= W.LIFE and not w.dead)\n",
     "        lives_survived += int(w.t >= W.LIFE and not w.dead)\n"
     "        life_hook(net, state, total, w.t)\n"),
    ("def train_net_parent(", "def train_net_w3k("),
]
for a, b in _anchors:
    assert _src.count(a) == 1, a
    _src = _src.replace(a, b)
_ns = dict(w3d._ns)
_ns.update(parent_hook=parent_hook, adult_hook=adult_hook, life_hook=life_hook)
exec(compile(_src, "w3k_train_net", "exec"), _ns)
train_net_w3k = _ns["train_net_w3k"]


def configure(run, seed):
    w3i.install()
    w3d.ARMS[run] = {"parts": "YR", "always": False}
    w3d.configure(run)
    a = RUNS[run]
    w3d.CFG.update(child=a["fade"], always=False)
    w3b.OUT = w3i.OUT = OUT
    CFG.update(run=run, fade=a["fade"], steps=a["steps"], seed=seed, cy_step=cy_step_for(seed, run) if run == "R" else None)


def snaps(run):
    a = RUNS[run]
    return tuple(range(a["fade"], a["steps"], EVERY_SNAP))


def tag_of(name, seed, step):
    return f"{name}_{seed}_{step // 1000}k"


def load_npz(path, seed):
    net = B.DriveVIN(seed, fixed_map=False)
    with np.load(path) as z:
        for k in net.p:
            net.p[k] = z[k].copy()
    return net


def train_staged(run, seed, hours=4.5, name=None, snapshot_at=None):
    """Train in stages (paused at the first life boundary after each snapshot; tested and saved); resumable.
    Returns True when finished. `name` labels the files (the determinism job trains run "R" under another name)."""
    name = name or run
    OUT.mkdir(exist_ok=True)
    a = RUNS[run]
    snapshot_at = snaps(run) if snapshot_at is None else snapshot_at
    R = R3.regrowth()
    cp = OUT / f"{name}_{seed}.ckpt.pkl"
    state = pickle.loads(cp.read_bytes()) if cp.exists() else None
    t0 = time.time()
    with open(OUT / f"{name}_{seed}.log", "a") as log:
        while True:
            total = state["total"] if state else 0
            pending = [x for x in snapshot_at if not (OUT / f"{tag_of(name, seed, x)}.npz").exists()]
            nxt = min(pending) if pending else None
            if nxt is not None and total >= nxt:
                net = B.DriveVIN(seed, fixed_map=False)
                for k in net.p:
                    net.p[k] = state["p"][k].copy()
                tag = tag_of(name, seed, nxt)
                w3i.test_all(net, tag, W.TEST_SEEDS)
                np.savez(OUT / f"{tag}.npz", **net.p)
                print(f"snapshot {tag} at step {total}", file=log, flush=True)
                cp.write_bytes(pickle.dumps(state))
                continue
            left = hours - (time.time() - t0) / 3600
            if left <= 0:
                break
            net, state, finished = train_net_w3k(run, seed, a["steps"], R, left, log, state, pause_after=nxt)
            if finished:
                np.savez(OUT / f"{name}_{seed}.npz", **net.p)
                if run == "R":
                    np.savez(OUT / f"{name}_CS_{seed}.npz", **(state.get("cs_p") or net.p))
                    np.savez(OUT / f"{name}_CY_{seed}.npz", **(state.get("cy_p") or net.p))
                meta = {k: state.get(k) for k in ("cs_step", "cs_best", "cy_at", "pseen")}
                meta.update(cy_step=CFG["cy_step"], pstore=len(state.get("pstore", [])), updates=state["updates"])
                (OUT / f"{name}_{seed}_meta.json").write_text(json.dumps(meta))
                (OUT / f"{name}_{seed}_lives.json").write_text(json.dumps({"lives": state["lives_log"],
                                                                            "updates": state["updates"]}))
                if cp.exists():
                    cp.unlink()
                return True
            if nxt is not None and state["total"] >= nxt:
                continue
            break
    cp.write_bytes(pickle.dumps(state))
    print("paused", name, seed, "at step", state["total"], flush=True)
    return False


def machine(name, seed):
    """The processor and the numerical library this run used (the determinism record)."""
    cpu = CPU
    from numpy._core._multiarray_umath import __cpu_features__, __cpu_dispatch__, __cpu_targets_info__
    rec = {"cpu": cpu, "machine": platform.machine(), "python": platform.python_version(), "numpy": np.__version__,
           "env": {k: os.environ.get(k) for k in ("OPENBLAS_CORETYPE", "NPY_DISABLE_CPU_FEATURES", "OPENBLAS_NUM_THREADS")},
           "cpu_dispatch": list(__cpu_dispatch__),
           "targets_in_use": sorted({v["current"] for fn in __cpu_targets_info__.values() for v in fn.values()}),
           "avx512": bool(__cpu_features__.get("AVX512F")), "time": time.strftime("%Y-%m-%d %H:%M:%S")}
    p = OUT / f"machine_{name}_{seed}.json"
    old = json.loads(p.read_text()) if p.exists() else []
    p.write_text(json.dumps(old + [rec], indent=1))


def drift_and_parent(final, snap, seeds, R):
    """As W3j: on the final brain's own test lives, the share of steps where its greedy move differs from the
    end-of-fade brain's, and the share where it equals W3's Script on the same map view."""
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


def test_brain(label, path, seed, snap):
    net = load_npz(path, seed)
    w3i.test_all(net, label, W.TEST_SEEDS)
    w3i.test_all(net, f"fresh_{label}", w3i.FRESH_SEEDS)
    (OUT / f"drift_{label}.json").write_text(json.dumps(drift_and_parent(net, snap, W.TEST_SEEDS, R3.regrowth())))


def right_machine():
    """On an unverified processor, leave a flag (the manager re-queues the job, keeping any checkpoint) and stop."""
    OUT.mkdir(exist_ok=True)
    flag = OUT / "wrong_machine.flag"
    if not GOOD_MACHINE:
        flag.write_text(CPU)
        print("wrong machine:", CPU, flush=True)
        return False
    if flag.exists():
        flag.unlink()
    return True


def run(run_name, seed, hours):
    if not right_machine():
        return
    configure(run_name, seed)
    machine(run_name, seed)
    if train_staged(run_name, seed, hours):
        snap = load_npz(OUT / f"{tag_of(run_name, seed, RUNS[run_name]['fade'])}.npz", seed)
        if run_name == "R":
            test_brain(f"R2_{seed}", OUT / f"R_{seed}.npz", seed, snap)
            test_brain(f"CS_{seed}", OUT / f"R_CS_{seed}.npz", seed, snap)
            test_brain(f"CY_{seed}", OUT / f"R_CY_{seed}.npz", seed, snap)
        else:
            test_brain(f"{run_name}_{seed}", OUT / f"{run_name}_{seed}.npz", seed, snap)
        print("done", run_name, seed, flush=True)


def det(name, seed, hours):
    """The determinism job: run "R" trained again under another name (no snapshots, no tests). The comparison with
    R's own weights is made by the analysis, once both have finished."""
    if not right_machine():
        return
    configure("R", seed)
    machine(name, seed)
    if train_staged("R", seed, hours, name=name, snapshot_at=()):
        print("det done", name, seed, flush=True)


if __name__ == "__main__":
    if sys.argv[1] == "run":
        run(sys.argv[2], int(sys.argv[3]), float(sys.argv[4]) if len(sys.argv) > 4 else 4.5)
    elif sys.argv[1] == "det":
        det(sys.argv[2], int(sys.argv[3]), float(sys.argv[4]) if len(sys.argv) > 4 else 4.5)
