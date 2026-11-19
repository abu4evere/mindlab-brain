"""W3m checks, before any data. Prints All: PASS or the failures. Imports w3m first (it imports w3k, which sets the
numerical settings before numpy loads)."""
import json
import os
import shutil
import sys
from pathlib import Path

HERE = Path(__file__).parent
sys.path.insert(0, str(HERE))
import w3m  # noqa: E402
import numpy as np  # noqa: E402
from w3m import w3k, w3d, W, R3  # noqa: E402

fails = []


def check(name, ok):
    print(("PASS " if ok else "FAIL ") + name, flush=True)
    if not ok:
        fails.append(name)


R = R3.regrowth()
tmp = HERE / "tmp_checks"


def fresh():
    if tmp.exists():
        shutil.rmtree(tmp)
    tmp.mkdir()
    w3k.OUT = w3m.OUT = tmp


def short(arm, seed, fade=1500, steps=3000):
    w3k.RUNS[arm] = {"steps": steps, "fade": fade}
    (w3m.configure if arm in w3m.ARMS else w3k.configure)(arm, seed)
    w3k.w3b.OUT = w3k.w3i.OUT = tmp


def same(a, b):
    return all(np.array_equal(a.p[k], b.p[k]) for k in a.p)


# 0. the numerical settings (W3k's)
from numpy._core._multiarray_umath import __cpu_targets_info__  # noqa: E402
in_use = sorted({v["current"] for fn in __cpu_targets_info__.values() for v in fn.values()})
check(f"determinism settings in place before numpy loads (verified machine: {w3k.GOOD_MACHINE}; paths {in_use})",
      os.environ.get("OPENBLAS_CORETYPE") == ("Zen" if w3k.GOOD_MACHINE else None)
      and os.environ.get("NPY_DISABLE_CPU_FEATURES") == "AVX512_SPR AVX512_ICL X86_V4"
      and not any(t.startswith(("X86_V4", "AVX512")) for t in in_use))

# 1. schedules: both arms are W3k's run R (4.0M steps, 2.4M fade); CY's steps drawn with the new seed
ok = True
for arm in ("SL", "SR", "UR"):
    w3m.configure(arm, 3)
    cw, pp = w3d._ns["copy_weight"], w3d._ns["parent_present"]
    ok &= w3k.RUNS[arm] == {"steps": 4_000_000, "fade": 2_400_000}
    ok &= cw(0) == 0.5 and cw(2_400_000) == 0.0 and pp(2_399_999) and not pp(2_400_000)
    ok &= w3k.CFG["cy_step"] == int(np.random.default_rng(20261201 + 3).integers(2_600_000, 4_000_000))
ok &= w3m.PART == {"reflex": False, "urge": True}
check("schedules: SL and UR are W3k's run R (2.4M fade of 4.0M); CY drawn in advance (seed 20261201 + run seed); "
      "the arm's part set", bool(ok))

# 2. with both parts off, W3m's training is W3k's run R exactly (short runs: the copy window shrunk as W3k's checks)
w3k.CS_WINDOW, w3k.CS_START = 400, 200
fresh()
short("SL", 4)
w3m.PART.update(reflex=False, urge=False)
a, _, _ = w3m.train_net_w3m("SL", 4, 3000, R, hours=1.0)
short("R", 4)
b, _, _ = w3k.train_net_w3k("R", 4, 3000, R, hours=1.0)
check("parts off: W3m's training equals W3k's run R bit for bit", same(a, b))

# 3. the urge: 0 at or below the line, 0.75 at the cap, linear between; 0 in the reflex arm
w = W.World(W.make_land(5), R)
w3m.PART.update(reflex=False, urge=True)
vals = []
for F in (0, 90, 145, 200, 260):
    w.F = float(F)
    vals.append(round(w3m.urge(w), 6))
w3m.PART.update(reflex=False, urge=False)
w.F = 200.0
check(f"the urge: {vals} at F = 0, 90, 145, 200, 260; 0 when off", vals == [0, 0, 0.375, 0.75, 0.75] and w3m.urge(w) == 0)

# 4. the reflex on a hand-made body: it takes over at F 90 with E >= 60 and the shelter known, walks there, stays
#    until F is 0; hunger (E < 60) lets go; below the line it never acts; off, it never acts
w3m.PART.update(reflex="walk", urge=False)
land = W.make_land(5)
w = W.World(land, R)
w.m_shelter[:] = False
w.m_shelter[w.shelter[1], w.shelter[0]] = True
w.m_seen[:] = True
w.m_wall[:] = w.walls
rf = w3m.Reflex()
w.F, w.E = w3m.F_LINE - 1, 150.0
below = rf.act(w, 2) == 2
w.F = w3m.F_LINE
path, steps = [], 0
while w.pos != w.shelter and steps < 60:
    act = rf.act(w, 4)
    path.append(act)
    w.step(act)
    steps += 1
arrived = w.pos == w.shelter
held = all(rf.act(w, 0) == 4 for _ in range(3))
w.E = w3m.E_HUNGER - 1
lets_go = rf.act(w, 1) == 1 and not rf.on
w.E, w.F = 150.0, 0.0
rf2 = w3m.Reflex()
rf2.on = True
done_resting = rf2.act(w, 3) == 3 and not rf2.on
w3m.PART["reflex"] = False
off = w3m.Reflex().act(w, 2) == 2
check(f"the reflex: silent below the line; at the line walks to the shelter ({steps} steps, arrived {arrived}), "
      f"holds there; hunger lets go; lets go at F 0; off never acts", below and arrived and held and lets_go
      and done_resting and off)

# 4b. SR, rest only: the same lines, but it never walks; it holds the brain only once it stands on the shelter
w3m.PART.update(reflex="rest", urge=False)
w = W.World(land, R)
w.m_shelter[:] = False
w.m_shelter[w.shelter[1], w.shelter[0]] = True
w.m_seen[:] = True
w.m_wall[:] = w.walls
rf = w3m.Reflex()
w.F, w.E = w3m.F_LINE + 5, 150.0
away = w.pos != w.shelter and all(rf.act(w, a0) == a0 for a0 in (0, 1, 2, 3)) and not rf.on
w.pos = w.shelter
holds = rf.act(w, 2) == 4 and rf.on
w.F = 0.0
release = rf.act(w, 2) == 2 and not rf.on
check("SR: never moves the brain away from the shelter; holds it there once it arrives tired; lets go at F 0",
      away and holds and release)

# 5. SL trains differently from R (the reflex acts), takes over some steps; a split run equals an unsplit one
fresh()
short("SL", 6, fade=1500, steps=6000)
w3m.COUNT.update(steps=0, forced=0)
s1, st1, _ = w3m.train_net_w3m("SL", 6, 6000, R, hours=1.0)
forced = dict(w3m.COUNT)
_, q, _ = w3m.train_net_w3m("SL", 6, 6000, R, hours=1.0, pause_after=3500)
s2, st2, _ = w3m.train_net_w3m("SL", 6, 6000, R, hours=1.0, state=q)
s3, _, _ = w3m.train_net_w3m("SL", 6, 6000, R, hours=1.0)
short("R", 6, fade=1500, steps=6000)
r1, _, _ = w3k.train_net_w3k("R", 6, 6000, R, hours=1.0)
check(f"SL: the reflex took over {forced['forced']} of {forced['steps']} training steps; training differs from R; "
      f"split = unsplit; the same seed twice is the same",
      forced["forced"] > 0 and not same(s1, r1) and same(s1, s2) and same(s1, s3) and st1["cs_step"] == st2["cs_step"])

# 6. UR trains differently from R (the urge changes the reward) and never forces a move
fresh()
short("UR", 6, fade=1500, steps=6000)
w3m.COUNT.update(steps=0, forced=0)
u1, _, _ = w3m.train_net_w3m("UR", 6, 6000, R, hours=1.0)
check(f"UR: training differs from R; no step forced ({w3m.COUNT['forced']})",
      not same(u1, r1) and w3m.COUNT["forced"] == 0)

# 7. a whole staged SL run: the copies are saved; the tests run with the reflex (counted) and the S-off test without
fresh()
short("SL", 7, fade=1500, steps=3000)
w3k.CFG["cy_step"] = 2200
seeds0 = W.TEST_SEEDS
W.TEST_SEEDS = range(900001, 900003)
w3k.w3i.FRESH_SEEDS, fresh0 = range(910001, 910003), w3k.w3i.FRESH_SEEDS
w3k.right_machine = lambda: True
w3m.run("SL", 7, 1.0)
names = {p.name for p in tmp.iterdir()}
rx = json.loads((tmp / "reflex_SLS_7.json").read_text())
rx_off = json.loads((tmp / "reflex_SLS-off_7.json").read_text())
check(f"a staged SL run saves its copies and tests SL, SLS, SLY and SLS-off; the reflex acts in the tests "
      f"({rx['forced']} of {rx['steps']} steps) and not in SLS-off ({rx_off['forced']})",
      {"SL_7.npz", "SL_CS_7.npz", "SL_CY_7.npz", "test_SL_7.json", "test_SLS_7.json", "test_SLY_7.json",
       "test_SLS-off_7.json", "test_fresh_SLS_7.json"} <= names and rx["forced"] >= 0 and rx_off["forced"] == 0
      and w3m.PART["reflex"])
W.TEST_SEEDS, w3k.w3i.FRESH_SEEDS = seeds0, fresh0
shutil.rmtree(tmp)
print("All: PASS" if not fails else f"FAILED: {fails}")
