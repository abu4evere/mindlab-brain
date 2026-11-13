"""W3's frozen code checks (questions.md, Validity) -> checks.log. Run after calibration (check 9 needs calib.json).

  python checks_w3.py
"""
from __future__ import annotations

import json
import os
import sys
from pathlib import Path

os.environ.setdefault("OPENBLAS_NUM_THREADS", "1")

import numpy as np  # noqa: E402

HERE = Path(__file__).parent
sys.path.insert(0, str(HERE))
import brains3 as B  # noqa: E402
import run_w3 as Rn  # noqa: E402
import world3 as W  # noqa: E402

RES = []


def check(name, ok, detail=""):
    RES.append((name, bool(ok), detail))
    print(("PASS " if ok else "FAIL ") + name + (f"  ({detail})" if detail else ""), flush=True)


def c1_writer_only_view():
    """The map writer never writes a cell outside the 3 x 3 view."""
    w = W.World(W.make_land(700101), 100)
    rng = np.random.default_rng(1)
    bad = 0
    while not w.done() and w.t < 1500:
        before = [a.copy() for a in (w.m_wall, w.m_seen, w.m_food, w.m_shelter, w.m_last)]
        w.step(int(rng.integers(5)))
        view = set(w.view_cells())
        for b, a in zip(before, (w.m_wall, w.m_seen, w.m_food, w.m_shelter, w.m_last)):
            ys, xs = np.nonzero(b != a)
            bad += sum((int(x), int(y)) not in view for x, y in zip(xs, ys))
    check("1 map writer writes only the view", bad == 0, f"{bad} cells outside the view changed")


def c2_batch_equals_single():
    net = B.DriveVIN(3)
    rng = np.random.default_rng(2)
    w = W.World(W.make_land(700102), 100)
    maps, levs = [], []
    for _ in range(12):
        maps.append(w.obs_map())
        levs.append(Rn.levels(w, "D3"))
        w.step(int(rng.integers(5)))
    fb = net.plan(np.array(maps), np.array(levs))
    worst = 0.0
    for t in range(12):
        fs = net.plan(np.array(maps[t])[None], np.array(levs[t])[None])
        qb = fb[5][t * B.N * B.N:(t + 1) * B.N * B.N]
        worst = max(worst, float(np.abs(qb - fs[5]).max()))
    check("2 batched planner equals one map at a time", worst < 1e-9, f"max |diff| {worst:.2e}")


def c3_gradient():
    """A numerical gradient check of f = sum(dl*z) + sum(dv*v); Ws, Wf, Wc get non-zero gradients from zero."""
    net = B.DriveVIN(5)
    rng = np.random.default_rng(3)
    w = W.World(W.make_land(700103), 100)
    maps, levs, cells = [], [], []
    for _ in range(6):
        maps.append(w.obs_map())
        levs.append((0.3 + 0.1 * rng.random(), 0.2 + 0.1 * rng.random(), 0.5 + 0.1 * rng.random()))
        cells.append(w.pos)
        w.step(int(rng.integers(5)))
    maps, levs = np.array(maps), np.array(levs)
    rows = np.arange(6) * B.N * B.N + np.array([c[1] * B.N + c[0] for c in cells])
    dl, dv = rng.normal(size=(6, 5)), rng.normal(size=6)

    def f():
        z, v = net.head(net.plan(maps, levs), rows)
        return float((dl * z).sum() + (dv * v).sum())

    g = net.backprop(net.plan(maps, levs), rows, dl, dv)
    worst, nonzero = 0.0, {}
    for k in ("W0", "Ws", "Wf", "Wc", "Wq", "Wo", "br"):
        flat = net.p[k].reshape(-1)
        for i in rng.choice(flat.size, size=min(6, flat.size), replace=False):
            if k == "Wq" and False:
                continue
            old = flat[i]
            flat[i] = old + 1e-6
            fp = f()
            flat[i] = old - 1e-6
            fm = f()
            flat[i] = old
            num = (fp - fm) / 2e-6
            ana = float(g[k].reshape(-1)[i])
            worst = max(worst, abs(num - ana) / max(1.0, abs(num)))
        nonzero[k] = float(np.abs(g[k]).sum())
    ok = worst < 1e-4 and all(nonzero[k] > 0 for k in ("Ws", "Wf", "Wc"))
    check("3 numerical gradient (drive-weighted map)", ok,
          f"worst rel err {worst:.2e}; |g| Ws {nonzero['Ws']:.3g} Wf {nonzero['Wf']:.3g} Wc {nonzero['Wc']:.3g}")


def c4_death_bound():
    """Dying now is never better than any continuation (homeostatic part), on 10,000 random continuations."""
    rng = np.random.default_rng(4)
    worst = np.inf
    for _ in range(10_000):
        d_t = rng.uniform(0, Rn.D_MAX)
        T = int(rng.integers(1, 200))
        ds = rng.uniform(0, Rn.D_MAX, size=T)
        die = bool(rng.integers(0, 2))
        seq = [d_t] + list(ds)
        G, disc = 0.0, 1.0
        for k in range(T):
            nxt = seq[k + 1]
            if die and k == T - 1:
                nxt = Rn.D_MAX
            G += disc * 10.0 * (seq[k] - nxt)
            disc *= B.GAMMA
        worst = min(worst, G - 10.0 * (d_t - Rn.D_MAX))
    check("4 death bound holds", worst >= -1e-9, f"min(continuation - die now) = {worst:.3g}")


def c5_lands_identical():
    same = True
    for s in list(W.TEST_SEEDS)[:5]:
        a, b = W.make_land(s), W.make_land(s)
        same &= np.array_equal(a["walls"], b["walls"]) and a["sched"] == b["sched"] and a["patches"] == b["patches"]
        wa, wb = W.World(a, 100), W.World(b, 100)
        for t in range(2800):
            act = (t * 7) % 5
            wa.step(act)
            wb.step(act)
            if wa.done() or wb.done():
                break
        same &= [e[:3] for e in wa.events] == [e[:3] for e in wb.events]
    check("5 test lands and relocations identical across brains", same)


def c6_test_no_learning():
    net = B.DriveVIN(6)
    before = {k: v.copy() for k, v in net.p.items()}
    rng = np.random.default_rng(6)
    Rn.run_life(lambda w: net.act(w.obs_map(), Rn.levels(w, "D3"), w.pos, rng)[0], W.make_land(700106), 100, rng)
    check("6 weights unchanged by testing", all(np.array_equal(before[k], net.p[k]) for k in net.p))


def c7_script_reads_memory_only():
    w = W.World(W.make_land(700107), 100)
    mv = W.MapView(w)
    attrs = set(vars(mv))
    allowed = {"pos", "E", "F", "m_wall", "m_seen", "m_food", "shelter_known", "u"}
    check("7 Script reads only the map memory", attrs == allowed, f"attributes {sorted(attrs)}")


def c8_same_seed_same_result():
    a, _ = Rn.train_net("D3", 7, 400, 100)
    b, _ = Rn.train_net("D3", 7, 400, 100)
    c, _ = Rn.train_net("D3i", 7, 400, 100)
    same = all(np.array_equal(a.p[k], b.p[k]) for k in a.p)
    fixed = c.p["Ws"][0, W.CH_FOOD, 1, 1] == 1.0 and float(np.abs(c.p["Ws"]).sum()) == 1.0
    moved = float(np.abs(a.p["Ws"]).sum()) > 0
    check("8 same seed gives the same result; D3i's link stays fixed; D3's link learns", same and fixed and moved,
          f"same {same}, D3i fixed {fixed}, D3 Ws moved {moved}")


def c8b_levels():
    w = W.World(W.make_land(700108), 100)
    for _ in range(30):
        w.step(4)
    s, f, c = Rn.levels(w, "D3")
    ok = Rn.levels(w, "D2") == (s, f, 0.0) and Rn.levels(w, "Dc") == (0.0, 0.0, c) and Rn.levels(w, "D3-") == (s, f, 0.0)
    check("8b drive levels per brain (D2 no c; Dc no s, f; the lesion zeroes c only)", ok and c > 0)


def c9_calibration_reproduces():
    cal = json.loads((HERE / "calib.json").read_text())
    R = cal["R"]
    row = [r for r in cal["rows"] if r["R"] == R][0]
    res = {}
    for name in ("Script", "Rand"):
        surv = []
        for ls in W.CAL_SEEDS:
            rng = np.random.default_rng(ls)
            pol = Rn.rand_policy(rng) if name == "Rand" else Rn.script_policy()
            surv.append(Rn.run_life(pol, W.make_land(ls), R, rng)[1]["survived"])
        res[name] = float(np.mean(surv))
    check("9 Rand and Script reproduce their calibration numbers", res["Script"] == row["Script"]
          and res["Rand"] == row["Rand"], f"R {R}: {res} vs {row}")


if __name__ == "__main__":
    for fn in (c1_writer_only_view, c2_batch_equals_single, c3_gradient, c4_death_bound, c5_lands_identical,
               c6_test_no_learning, c7_script_reads_memory_only, c8_same_seed_same_result, c8b_levels,
               c9_calibration_reproduces):
        fn()
    allok = all(ok for _, ok, _ in RES)
    with open(HERE / "checks.log", "w") as fh:
        for name, ok, d in RES:
            fh.write(("PASS " if ok else "FAIL ") + name + (f"  ({d})" if d else "") + "\n")
        fh.write(f"All: {'PASS' if allok else 'FAIL'}\n")
    print("All:", "PASS" if allok else "FAIL")
