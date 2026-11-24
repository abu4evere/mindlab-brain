"""W3r checks, before any data. Prints All: PASS or the failures."""
import json
import os
import shutil
import sys
from pathlib import Path

HERE = Path(__file__).parent
sys.path.insert(0, str(HERE))
import w3r  # noqa: E402
import numpy as np  # noqa: E402
from w3r import w3k, w3m, w3n, w3o, W  # noqa: E402
from w3k import w3d, R3  # noqa: E402

fails = []


def check(name, ok):
    print(("PASS " if ok else "FAIL ") + name, flush=True)
    if not ok:
        fails.append(name)


R = R3.regrowth()
tmp = HERE / "tmp_checks"
OTHER = [HERE.parent / d / "output" for d in ("W3n", "W3o")]
before_other = {str(d): {p.name for p in d.iterdir()} if d.exists() else set() for d in OTHER}


def fresh():
    if tmp.exists():
        shutil.rmtree(tmp)
    tmp.mkdir()
    w3k.OUT = w3m.OUT = w3n.OUT = w3o.OUT = w3r.OUT = tmp


def short(arm, seed, fade=1500, steps=3000, src="w3r"):
    w3k.RUNS[arm] = {"steps": steps, "fade": fade}
    if src == "w3r":
        w3r.configure(arm, seed)
    elif src == "w3o":
        w3o.configure(arm, seed)
    else:
        w3n.configure(arm, seed)
    w3k.w3b.OUT = w3k.w3i.OUT = tmp


def train(arm, seed, steps=3000, **kw):
    return w3m.train_net_w3m(arm, seed, steps, R, hours=1.0, **kw)


def same(a, b):
    return all(np.array_equal(a.p[k], b.p[k]) for k in a.p)


# 0. the numerical settings (W3k's)
from numpy._core._multiarray_umath import __cpu_targets_info__  # noqa: E402
in_use = sorted({v["current"] for fn in __cpu_targets_info__.values() for v in fn.values()})
check(f"determinism settings in place before numpy loads (paths {in_use})",
      os.environ.get("OPENBLAS_CORETYPE") == ("Zen" if w3k.GOOD_MACHINE else None)
      and os.environ.get("NPY_DISABLE_CPU_FEATURES") == "AVX512_SPR AVX512_ICL X86_V4"
      and not any(t.startswith(("X86_V4", "AVX512")) for t in in_use))

# 1. the arms: W3n's HR body and schedule; CY as W3n's; the eyes and module set; the pilot's rate in place
ok = True
for arm, spec in w3r.ARMS.items():
    w3r.configure(arm, 3)
    cw = w3d._ns["copy_weight"]
    ok &= w3k.RUNS[arm] == {"steps": 4_000_000, "fade": 2_400_000} and cw(0) == 0.5 and cw(2_400_000) == 0.0
    ok &= w3m.PART == {"reflex": "walk", "urge": False} and w3n.BODY == {"cheap": False, "hunger": True}
    ok &= w3k.CFG["cy_step"] == int(np.random.default_rng(20261211 + 3).integers(2_600_000, 4_000_000))
    ok &= W.World is w3r.MeaningWorld and w3o.EYES == {"mode": spec["eyes"], "swap": False}
    ok &= w3r.MOD == {"module": spec["module"], "oracle": False} and w3r.TEST == {"midswap": False, "soft": False}
calib = json.loads((HERE / "calib_w3r.json").read_text())
check(f"arms: W3n's HR body and schedule, both reflexes, CY as W3n's, eyes and module set; the ensemble's rate from the "
      f"pilot ({w3r.ENS['lr']}, pilot seeds {calib['pilot_seeds']})",
      bool(ok) and w3r.ENS["lr"] == calib["lr"] == 0.3 and calib["pilot_seeds"] == [9001, 9002, 9003, 9004])

# 2. W3r's RV trains W3o's RV bit for bit; W3r's HR trains W3n's HR bit for bit
w3k.CS_WINDOW, w3k.CS_START = 400, 200
fresh()
short("RV", 4)
a, _, _ = train("RV", 4)
short("RV", 4, src="w3o")
b, _, _ = train("RV", 4)
short("HR", 4)
c, _, _ = train("HR", 4)
short("HR", 4, src="w3n")
d, _, _ = train("HR", 4)
check(f"W3r's RV = W3o's RV [{same(a, b)}]; W3r's HR = W3n's HR [{same(c, d)}] (bit for bit)", same(a, b) and same(c, d))

# 3. RM with the oracle colour-to-kind map trains HR bit for bit (the defined check); the real RM differs
short("RM", 4)
w3r.MOD["oracle"] = True
e, _, _ = train("RM", 4)
short("RM", 4)
f, _, _ = train("RM", 4)
check(f"RM with the oracle map = HR bit for bit [{same(e, c)}]; RM with its table differs from HR [{not same(f, c)}] "
      f"and from RV [{not same(f, a)}]", same(e, c) and not same(f, c) and not same(f, a))

# 4. the labels, on a land with W3o's changing colours and the table
w3r.configure("RM", 1)


def world(seed=5):
    return W.World(W.make_land(seed), R)


w = world()
codes = [w3r.code_of(r) for r in w.codes()]                     # wall, food, shelter
assert len(set(codes)) == 3 and 0 not in codes
N = W.N


def put(w, pos):
    w.pos = pos
    w.write_view()


def next_to(w, kind):
    """A walkable cell next to a cell of the kind (wall / food / shelter), and the move into it."""
    cells = {"wall": [(x, y) for y in range(N) for x in range(N) if w.walls[y, x]],
             "food": [c for c in w.food if w.food_full(c)], "shelter": [w.shelter]}[kind]
    for (tx, ty) in cells:
        for a, (dx, dy) in enumerate(W.MOVES[:4]):
            sx, sy = tx - dx, ty - dy
            if 0 < sx < N - 1 and 0 < sy < N - 1 and not w.walls[sy, sx] and (sx, sy) not in w.food \
                    and (sx, sy) != w.shelter:
                return (sx, sy), a
    raise RuntimeError(kind)


w.E, w.F = 100.0, 50.0
p, a = next_to(w, "wall")
put(w, p)
t0 = w.mod.pos.copy(), w.mod.neg.copy()
w.step(a)
d_pos, d_neg = w.mod.pos - t0[0], w.mod.neg - t0[1]
ok_block = d_pos[codes[0], 0] == 1 and d_pos.sum() == 1 and d_neg[0, 1] == 1 and d_neg[0, 2] == 1 and d_neg.sum() == 2
p, a = next_to(w, "food")
put(w, p)
w.E = 100.0
t0 = w.mod.pos.copy(), w.mod.neg.copy()
_, ate = w.step(a)
d_pos, d_neg = w.mod.pos - t0[0], w.mod.neg - t0[1]
ok_fed = ate and d_pos[codes[1], 1] == 1 and d_neg[codes[1], 0] == 1 and d_neg[codes[1], 2] == 1 and d_pos.sum() == 1 \
    and d_neg.sum() == 2
p, a = next_to(w, "shelter")
put(w, p)
w.F = 50.0
t0 = w.mod.pos.copy(), w.mod.neg.copy()
w.step(a)
d_pos, d_neg = w.mod.pos - t0[0], w.mod.neg - t0[1]
ok_rest = d_pos[codes[2], 2] == 1 and d_neg[codes[2], 0] == 1 and d_neg[codes[2], 1] == 1 and d_pos.sum() == 1 \
    and d_neg.sum() == 2
put(w, next_to(w, "wall")[0])
w.F = 0.0
t0 = w.mod.pos.copy(), w.mod.neg.copy()
w.step(4)                                                        # stay on floor, not tired: rest could not happen
d_pos, d_neg = w.mod.pos - t0[0], w.mod.neg - t0[1]
ok_none = d_pos.sum() == 0 and d_neg[:, 2].sum() == 0 and d_neg[:, 0].sum() == 0 and d_neg[0, 1] == 1
check(f"labels: a bump gives 1 blocked positive on the wall colour [{ok_block}]; a meal 1 fed positive on the food "
      f"colour [{ok_fed}]; rest at the shelter 1 rested positive on its colour [{ok_rest}]; staying put untired "
      f"teaches nothing about blocked or rest [{ok_none}]", ok_block and ok_fed and ok_rest and ok_none)

# 5. a fresh world starts with an empty module; with no lessons the brain's wall/food/shelter layers are all 0 (the
#    true kinds never leak); the sham credits a colour in view; the ensemble starts seeded and the same per land
w2 = world()
m0 = w2.obs_map()
leak_free = not (m0[W.CH_WALL].any() or m0[W.CH_FOOD].any() or m0[W.CH_SHELTER].any())
w3r.configure("RMX", 1)
w3 = world()
p, a = next_to(w3, "food")
put(w3, p)
view_codes = {int(w3.code_map()[y, x]) for x, y in w3.view_cells()}
w3.step(a)
credited = {int(c) for c in np.nonzero(w3.mod.pos[:, 1] + w3.mod.neg[:, 1])[0]}
w3r.configure("RE5", 1)
e1, e2, e3 = world(5).mod.w, world(5).mod.w, world(6).mod.w
check(f"a new life starts empty (table zero [{not w2.mod.pos.any() and not w2.mod.neg.any()}]); no lesson, no layer "
      f"[{leak_free}]; the sham credits colours in view {credited} of {view_codes}; the ensemble's start is the same "
      f"per land and differs between lands",
      not w2.mod.pos.any() and not w2.mod.neg.any() and leak_free and credited <= view_codes
      and np.array_equal(e1, e2) and not np.array_equal(e1, e3))

# 6. the probes: mid-swap exchanges the wall and food colours from LIFE/2; soft gives 0.85/0.15 on seen cells
w3r.configure("RV", 1)
w4 = world()
w3r.TEST["midswap"] = True
c_early = w4.codes().copy()
w4.t = W.LIFE // 2
c_late = w4.codes().copy()
w3r.TEST["midswap"] = False
w3r.configure("HR", 1)
w5 = world()
hard = w5.obs_map()
w3r.TEST["soft"] = True
soft = w5.obs_map()
w3r.TEST["soft"] = False
seen = w5.m_seen
ok_soft = (np.allclose(soft[W.CH_WALL][seen], np.where(hard[W.CH_WALL][seen] > 0, 0.85, 0.15))
           and not soft[W.CH_FOOD][~seen].any() and np.array_equal(soft[W.CH_UNC], hard[W.CH_UNC]))
check(f"mid-swap exchanges wall and food from LIFE/2 [{np.array_equal(c_late, c_early[[1, 0, 2]])}]; soft layers "
      f"[{ok_soft}]", np.array_equal(c_early, w4.codes0) and np.array_equal(c_late, c_early[[1, 0, 2]]) and ok_soft)

# 7. RM and RE5: split = unsplit; repeatable
fresh()
res = {}
for arm in ("RM", "RE5"):
    short(arm, 6, fade=1500, steps=6000)
    x1, _, _ = train(arm, 6, 6000)
    _, q, _ = train(arm, 6, 6000, pause_after=3500)
    x2, _, _ = train(arm, 6, 6000, state=q)
    x3, _, _ = train(arm, 6, 6000)
    res[arm] = (same(x1, x2), same(x1, x3))
check(f"split = unsplit and repeatable: {res}", all(a and b for a, b in res.values()))

# 8. a whole staged RM run and HR run: copies saved, every test plus the probe; module measures recorded; settings back
fresh()
seeds0, fresh0 = W.TEST_SEEDS, w3k.w3i.FRESH_SEEDS
W.TEST_SEEDS, w3k.w3i.FRESH_SEEDS = range(900001, 900003), range(910001, 910003)
w3k.right_machine = lambda: True
for arm in ("RM", "HR"):
    short(arm, 7, fade=1500, steps=12000)
    w3k.CFG["cy_step"] = 2200
    w3r.run(arm, 7, 1.0)
names = {p.name for p in tmp.iterdir()}
need = {"RM_7.npz", "RM_CS_7.npz", "RM_CY_7.npz", "HR_7.npz", "HR_CS_7.npz"}
need |= {f"test_{t}_7.json" for t in ("RM", "RMS", "RMY", "RMS-off", "RMS-bare", "RMS-midswap", "HR", "HRS",
                                       "HRS-bare", "HRS-soft")}
lives = json.loads((tmp / "test_RMS_7.json").read_text())
has_mod = all("food_first" in x for x in lives)
new_other = {str(d): ({p.name for p in d.iterdir()} if d.exists() else set()) - before_other[str(d)] for d in OTHER}
check(f"staged RM and HR runs save copies and run every test plus the probe (missing: {sorted(need - names)}); module "
      f"measures recorded [{has_mod}]; settings back after the probe; nothing new in W3n's or W3o's folders",
      need <= names and has_mod and w3r.TEST == {"midswap": False, "soft": False}
      and w3m.PART["reflex"] == "walk" and not any(new_other.values()))
W.TEST_SEEDS, w3k.w3i.FRESH_SEEDS = seeds0, fresh0
shutil.rmtree(tmp)
print("All: PASS" if not fails else f"FAILED: {fails}")
