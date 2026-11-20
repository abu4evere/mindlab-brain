"""W3o checks, before any data. Prints All: PASS or the failures."""
import json
import os
import shutil
import sys
from pathlib import Path

HERE = Path(__file__).parent
sys.path.insert(0, str(HERE))
import w3o  # noqa: E402
import numpy as np  # noqa: E402
from w3o import w3k, w3m, w3n, W  # noqa: E402
from w3k import w3d, R3  # noqa: E402

fails = []


def check(name, ok):
    print(("PASS " if ok else "FAIL ") + name, flush=True)
    if not ok:
        fails.append(name)


R = R3.regrowth()
tmp = HERE / "tmp_checks"
W3N_OUT = HERE.parent / "W3n" / "output"
n3n = {p.name for p in W3N_OUT.iterdir()}


def fresh():
    if tmp.exists():
        shutil.rmtree(tmp)
    tmp.mkdir()
    w3k.OUT = w3m.OUT = w3n.OUT = w3o.OUT = tmp


def short(arm, seed, fade=1500, steps=3000, mode=None):
    w3k.RUNS[arm] = {"steps": steps, "fade": fade}
    if arm in w3o.ARMS:
        w3o.configure(arm, seed)
        if mode:
            w3o.EYES["mode"] = mode
    else:
        w3n.configure(arm, seed)
    w3k.w3b.OUT = w3k.w3i.OUT = tmp


def same(a, b):
    return all(np.array_equal(a.p[k], b.p[k]) for k in a.p)


def known_world(seed=5):
    w = W.World(W.make_land(seed), R)
    w.m_seen[:] = True
    w.m_wall[:] = w.walls
    w.m_shelter[:] = False
    w.m_shelter[w.shelter[1], w.shelter[0]] = True
    for (x, y) in list(w.food):
        w.m_food[y, x] = w.food_full((x, y))
    return w


# 0. the numerical settings (W3k's)
from numpy._core._multiarray_umath import __cpu_targets_info__  # noqa: E402
in_use = sorted({v["current"] for fn in __cpu_targets_info__.values() for v in fn.values()})
check(f"determinism settings in place before numpy loads (paths {in_use})",
      os.environ.get("OPENBLAS_CORETYPE") == ("Zen" if w3k.GOOD_MACHINE else None)
      and os.environ.get("NPY_DISABLE_CPU_FEATURES") == "AVX512_SPR AVX512_ICL X86_V4"
      and not any(t.startswith(("X86_V4", "AVX512")) for t in in_use))

# 1. the arms: W3n's HR body and schedule, the eyes set, CY drawn as W3n's (so each seed pairs with HR's)
ok = True
for arm, mode in (("RE", "fixed"), ("RV", "vary")):
    w3o.configure(arm, 3)
    cw = w3d._ns["copy_weight"]
    ok &= w3k.RUNS[arm] == {"steps": 4_000_000, "fade": 2_400_000} and cw(0) == 0.5 and cw(2_400_000) == 0.0
    ok &= w3m.PART == {"reflex": "walk", "urge": False} and w3n.BODY == {"cheap": False, "hunger": True}
    ok &= w3k.CFG["cy_step"] == int(np.random.default_rng(20261211 + 3).integers(2_600_000, 4_000_000))
    ok &= W.World is w3o.RawWorld and w3o.EYES == {"mode": mode, "swap": False}
check("arms: W3n's HR body and schedule (2.4M fade of 4.0M), sleep and hunger reflexes; CY as W3n's; the eyes set",
      bool(ok))

# 2. with sorted eyes, W3o trains W3n's HR bit for bit
w3k.CS_WINDOW, w3k.CS_START = 400, 200
fresh()
short("RE", 4, mode="sorted")
a, _, _ = w3m.train_net_w3m("RE", 4, 3000, R, hours=1.0)
short("HR", 4)
b, _, _ = w3m.train_net_w3m("HR", 4, 3000, R, hours=1.0)
check("sorted eyes: W3o's training equals W3n's HR bit for bit", same(a, b))

# 3. the colours: each layer is on for two kinds; the sorted layers come back exactly by the inverse mix; unseen and
#    staleness unchanged; the body (which reads the world's memory) acts the same whatever the eyes
w3o.configure("RE", 1)
w = known_world()
rows = slice(W.N - 3, W.N) if w.shelter[1] < W.N - 3 else slice(0, 3)   # pre-data fix: never blank the shelter's row
w.m_seen[rows, :] = False
w.m_wall[rows, :] = w.m_food[rows, :] = w.m_shelter[rows, :] = False
assert w.m_food.any() and w.m_shelter.any()
w3o.EYES["mode"] = "sorted"
s = w.obs_map()
w3o.EYES["mode"] = "fixed"
m = w.obs_map()
back = np.tensordot(np.linalg.inv(w3o.CODES.T), m[:3], axes=1)
layer_kinds = [int(x) for x in (w3o.CODES > 0).sum(0)]
w.E = w3n.H_LINE
acts = []
for mode in ("sorted", "fixed", "vary"):
    w3o.EYES["mode"] = mode
    bd = w3n.Body()
    acts.append((bd.act(w, 4), bd.hungry))
w3o.EYES["mode"] = "fixed"
sorted3 = s[[W.CH_WALL, W.CH_FOOD, W.CH_SHELTER]]
check(f"colours: each layer on for {layer_kinds} kinds; the sorted layers come back exactly "
      f"[{np.allclose(back, sorted3)}]; no colour layer equals a sorted one; unseen and staleness the same; "
      f"the body acts the same with any eyes {acts}",
      layer_kinds == [2, 2, 2] and np.allclose(back, sorted3)
      and not any(np.array_equal(m[i], sorted3[j]) for i in range(3) for j in range(3))
      and np.array_equal(m[3], s[W.CH_UNSEEN]) and np.array_equal(m[4], s[W.CH_UNC])
      and len(set(acts)) == 1 and acts[0][1])

# 4. RV: the colours change from land to land (all six dealings appear), the same land always the same; RE fixed
w3o.EYES["mode"] = "vary"
lands = list(W.TEST_SEEDS) + [W.train_seed(1, k) for k in range(10)]
deals = {tuple(w3o.codes_for(ls).ravel()) for ls in lands}
again = all(np.array_equal(w3o.codes_for(ls), w3o.codes_for(ls)) for ls in W.TEST_SEEDS)
w3o.EYES["mode"] = "fixed"
fixed = {tuple(w3o.codes_for(ls).ravel()) for ls in lands}
check(f"RV: {len(deals)} different dealings of the colours over {len(lands)} lands; the same land, the same colours; "
      f"RE fixed ({len(fixed)})", len(deals) == 6 and again and len(fixed) == 1)

# 5. RE and RV train differently from HR; a split run equals an unsplit one; the same seed twice
fresh()
short("RE", 6, fade=1500, steps=6000)
e1, _, _ = w3m.train_net_w3m("RE", 6, 6000, R, hours=1.0)
_, q, _ = w3m.train_net_w3m("RE", 6, 6000, R, hours=1.0, pause_after=3500)
e2, _, _ = w3m.train_net_w3m("RE", 6, 6000, R, hours=1.0, state=q)
e3, _, _ = w3m.train_net_w3m("RE", 6, 6000, R, hours=1.0)
short("RV", 6, fade=1500, steps=6000)
v1, _, _ = w3m.train_net_w3m("RV", 6, 6000, R, hours=1.0)
short("HR", 6, fade=1500, steps=6000)
h1, _, _ = w3m.train_net_w3m("HR", 6, 6000, R, hours=1.0)
check(f"RE differs from HR [{not same(e1, h1)}]; RV differs from RE [{not same(v1, e1)}]; split = unsplit "
      f"[{same(e1, e2)}]; repeatable [{same(e1, e3)}]",
      not same(e1, h1) and not same(v1, e1) and same(e1, e2) and same(e1, e3))

# 6. a whole staged RE run: copies saved; every test, plus the swapped-colour test; the eyes and body back after;
#    nothing written into W3n's folder
fresh()
short("RE", 7, fade=1500, steps=12000)
w3k.CFG["cy_step"] = 2200
seeds0, fresh0 = W.TEST_SEEDS, w3k.w3i.FRESH_SEEDS
W.TEST_SEEDS, w3k.w3i.FRESH_SEEDS = range(900001, 900003), range(910001, 910003)
w3k.right_machine = lambda: True
w3o.OUT = tmp
w3o.run("RE", 7, 1.0)
names = {p.name for p in tmp.iterdir()}
need = {"RE_7.npz", "RE_CS_7.npz", "RE_CY_7.npz", "test_RE_7.json", "test_RES_7.json", "test_REY_7.json",
        "test_RES-off_7.json", "test_RES-bare_7.json", "test_RES-swap_7.json", "test_fresh_RES-swap_7.json"}
ls_s = json.loads((tmp / "test_RES_7.json").read_text())
ls_w = json.loads((tmp / "test_RES-swap_7.json").read_text())
w3o.EYES["swap"] = True
sw = w3o.codes_for(900001)
w3o.EYES["swap"] = False
new3n = {p.name for p in W3N_OUT.iterdir()} - n3n
check(f"a staged RE run saves its copies and runs every test, plus the swap test (missing: {sorted(need - names)}); "
      f"swap exchanges the wall and food colours; lifespans {[l['lifespan'] for l in ls_s]} vs swapped "
      f"{[l['lifespan'] for l in ls_w]}; eyes and body back; nothing new in W3n's folder from W3o "
      f"({sorted(x for x in new3n if x.startswith(('RE', 'RV', 'test_RE', 'test_RV')))})",
      need <= names and np.array_equal(sw, w3o.CODES[[1, 0, 2]]) and w3o.EYES == {"mode": "fixed", "swap": False}
      and w3n.BODY == {"cheap": False, "hunger": True} and w3m.PART["reflex"] == "walk"
      and not any(x.startswith(("RE", "RV", "test_RE", "test_RV")) for x in new3n))
W.TEST_SEEDS, w3k.w3i.FRESH_SEEDS = seeds0, fresh0
shutil.rmtree(tmp)
print("All: PASS" if not fails else f"FAILED: {fails}")
