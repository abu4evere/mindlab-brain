"""W3n checks, before any data. Prints All: PASS or the failures. Imports w3n first (it imports W3m and W3k, which set
the numerical settings before numpy loads)."""
import json
import os
import shutil
import sys
from pathlib import Path

HERE = Path(__file__).parent
sys.path.insert(0, str(HERE))
import w3n  # noqa: E402
import numpy as np  # noqa: E402
from w3n import w3k, w3m, W  # noqa: E402
from w3k import w3d, R3  # noqa: E402

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
    w3k.OUT = w3m.OUT = w3n.OUT = tmp


def short(arm, seed, fade=1500, steps=3000):
    w3k.RUNS[arm] = {"steps": steps, "fade": fade}
    (w3n.configure if arm in w3n.ARMS else w3m.configure)(arm, seed)
    w3k.w3b.OUT = w3k.w3i.OUT = tmp


def same(a, b):
    return all(np.array_equal(a.p[k], b.p[k]) for k in a.p)


def known_world(seed=5):
    """A world whose map memory knows the walls, the shelter and every food cell (a hand-made test body)."""
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
check(f"determinism settings in place before numpy loads (verified machine: {w3k.GOOD_MACHINE}; paths {in_use})",
      os.environ.get("OPENBLAS_CORETYPE") == ("Zen" if w3k.GOOD_MACHINE else None)
      and os.environ.get("NPY_DISABLE_CPU_FEATURES") == "AVX512_SPR AVX512_ICL X86_V4"
      and not any(t.startswith(("X86_V4", "AVX512")) for t in in_use))

# 1. the arms: W3k's run R schedule, W3m's sleep reflex on, the arm's parts; CY drawn with the new seed
ok = True
for arm, body in (("CR", (True, False)), ("HR", (False, True)), ("HC", (True, True))):
    w3n.configure(arm, 3)
    cw, pp = w3d._ns["copy_weight"], w3d._ns["parent_present"]
    ok &= w3k.RUNS[arm] == {"steps": 4_000_000, "fade": 2_400_000} and cw(0) == 0.5 and cw(2_400_000) == 0.0
    ok &= w3m.PART == {"reflex": "walk", "urge": False} and (w3n.BODY["cheap"], w3n.BODY["hunger"]) == body
    ok &= w3k.CFG["cy_step"] == int(np.random.default_rng(20261211 + 3).integers(2_600_000, 4_000_000))
    ok &= W.World is w3n.CheapWorld
check("arms: W3k's run R (2.4M fade of 4.0M), W3m's sleep reflex on, the arm's parts; CY drawn (seed 20261211)", bool(ok))

# 2. with both new parts off, W3n trains W3m's SL bit for bit
w3k.CS_WINDOW, w3k.CS_START = 400, 200
fresh()
short("HR", 4)
w3n.BODY.update(cheap=False, hunger=False)
a, _, _ = w3m.train_net_w3m("HR", 4, 3000, R, hours=1.0)
short("SL", 4)
b, _, _ = w3m.train_net_w3m("SL", 4, 3000, R, hours=1.0)
check("parts off: W3n's training equals W3m's SL bit for bit", same(a, b))

# 3. cheaper rest: a step resting at the shelter costs 0.5 (on) or 1 (off); elsewhere unchanged
costs = {}
W.World = w3n.CheapWorld                    # as configure() installs it for every W3n arm
for on in (True, False):
    w3n.BODY["cheap"] = on
    w = known_world()
    w.pos, w.E, w.F = w.shelter, 100.0, 50.0
    e0 = w.E; w.step(4); rest = e0 - w.E
    nb = next((w.shelter[0] + dx, w.shelter[1] + dy) for dx, dy in W.MOVES[:4] if not w.walls[w.shelter[1] + dy, w.shelter[0] + dx])
    w.pos = nb
    e0 = w.E; w.step(4); away = e0 - w.E
    costs[on] = (rest, away)
check(f"cheaper rest: resting at the shelter costs {costs[True][0]} (on) / {costs[False][0]} (off); away {costs[True][1]}",
      costs[True] == (0.5, 1.0) and costs[False] == (1.0, 1.0))

# 4. the hunger reflex on a hand-made body: silent above the line; at the line walks to the nearest remembered food;
#    hands back after eating; nothing remembered: silent; it wins over the sleep reflex
w3n.BODY.update(cheap=False, hunger=True)
w3m.PART.update(reflex="walk")
w = known_world()
body = w3n.Body()
w.E, w.F = w3n.H_LINE + 1, 0.0
quiet = body.act(w, 2) == 2 and not body.hungry
w.E = w3n.H_LINE
steps, ate = 0, False
while steps < 80:
    act = body.act(w, 0)
    if not body.hungry:
        ate = True
        break
    _, got = w.step(act)
    steps += 1
check(f"hunger reflex: silent above the line; at the line walks to remembered food and hands back after eating "
      f"({steps} steps)", quiet and ate)
w2 = known_world(); w2.m_food[:] = False; w2.E = 10.0
b2 = w3n.Body()
none = b2.act(w2, 3) == 3 and not b2.hungry
w3 = known_world(); w3.E, w3.F = w3n.H_LINE, 95.0
b3 = w3n.Body()
first = b3.act(w3, 1)
wins = b3.hungry and not b3.on
check("hunger reflex: nothing remembered, nothing happens; when both are due, hunger wins over sleep", none and wins)

# 5. HR trains differently from SL, takes over some steps; a split run equals an unsplit one; the same seed twice
fresh()
short("HR", 6, fade=1500, steps=6000)
w3n.HC.update(steps=0, hunger=0, meals=0)
h1, s1, _ = w3m.train_net_w3m("HR", 6, 6000, R, hours=1.0)
took = dict(w3n.HC)
_, q, _ = w3m.train_net_w3m("HR", 6, 6000, R, hours=1.0, pause_after=3500)
h2, s2, _ = w3m.train_net_w3m("HR", 6, 6000, R, hours=1.0, state=q)
h3, _, _ = w3m.train_net_w3m("HR", 6, 6000, R, hours=1.0)
short("SL", 6, fade=1500, steps=6000)
w3n.BODY.update(cheap=False, hunger=False)  # plain SL: W3m's body only
l1, _, _ = w3m.train_net_w3m("SL", 6, 6000, R, hours=1.0)
check(f"HR: the hunger reflex took {took['hunger']} of {took['steps']} training steps ({took['meals']} meals) "
      f"[{took['hunger'] > 0}]; differs from SL [{not same(h1, l1)}]; split = unsplit [{same(h1, h2)}]; "
      f"repeatable [{same(h1, h3)}]", took["hunger"] > 0 and not same(h1, l1) and same(h1, h2) and same(h1, h3))
fresh()
short("CR", 6, fade=1500, steps=6000)
c1, _, _ = w3m.train_net_w3m("CR", 6, 6000, R, hours=1.0)
check("CR: training differs from SL (the cheaper rest changes the body's energy)", not same(c1, l1))

# 6. a whole staged HC run: copies saved; tests with both reflexes counted; the S-off test without the hunger reflex
fresh()
short("HC", 7, fade=1500, steps=12000)   # long enough that a life ends after the snapshot point (lives now last long)
w3k.CFG["cy_step"] = 2200
seeds0, fresh0 = W.TEST_SEEDS, w3k.w3i.FRESH_SEEDS
W.TEST_SEEDS, w3k.w3i.FRESH_SEEDS = range(900001, 900003), range(910001, 910003)
w3k.right_machine = lambda: True
w3n.run("HC", 7, 1.0)
names = {p.name for p in tmp.iterdir()}
h_on = json.loads((tmp / "hunger_HCS_7.json").read_text())
h_off = json.loads((tmp / "hunger_HCS-off_7.json").read_text())
bare_r = json.loads((tmp / "reflex_HCS-bare_7.json").read_text())
bare_h = json.loads((tmp / "hunger_HCS-bare_7.json").read_text())
check(f"a staged HC run saves its copies and tests HC, HCS, HCY, HCS-off, HCS-old and HCS-bare; hunger counted ({h_on}); "
      f"off in HCS-off ({h_off['hunger']}); bare: no sleep ({bare_r['forced']}) or hunger ({bare_h['hunger']}) take-over; "
      f"the body back as trained after", {"HC_7.npz", "HC_CS_7.npz", "HC_CY_7.npz", "test_HCS_7.json", "test_HCS-off_7.json",
      "test_HCS-old_7.json", "test_HCS-bare_7.json", "reflex_HCS_7.json", "hunger_HCS_7.json"} <= names
      and h_off["hunger"] == 0 and bare_r["forced"] == 0 and bare_h["hunger"] == 0
      and w3n.BODY == {"cheap": True, "hunger": True} and w3m.PART["reflex"] == "walk")
W.TEST_SEEDS, w3k.w3i.FRESH_SEEDS = seeds0, fresh0
shutil.rmtree(tmp)
print("All: PASS" if not fails else f"FAILED: {fails}")
