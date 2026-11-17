"""W3i checks, before any data. Prints All: PASS or the failures."""
import shutil
import sys
from pathlib import Path

import numpy as np

HERE = Path(__file__).parent
sys.path.insert(0, str(HERE))
import w3i  # noqa: E402
from w3i import w3d, w3b, B, W, R3  # noqa: E402

fails = []


def check(name, ok):
    print(("PASS " if ok else "FAIL ") + name, flush=True)
    if not ok:
        fails.append(name)


R = R3.regrowth()

# 1. the world is W3's: StaleWorld follows the same trajectory as W3's World under the same actions
land = W.make_land(W.TEST_SEEDS[3])
a_w, b_w = w3i.BaseWorld(land, R), w3i.StaleWorld(land, R)
rng = np.random.default_rng(5)
same = True
for _ in range(1500):
    if a_w.done():
        break
    act = int(rng.integers(5))
    a_w.step(act)
    b_w.step(act)
    same &= a_w.pos == b_w.pos and a_w.E == b_w.E and a_w.F == b_w.F and np.array_equal(a_w.m_food, b_w.m_food)
check("the counters do not change W3's world", same)

# 2. the stale counter: only arrivals on remembered-full, really-empty cells
w = w3i.StaleWorld(land, R)
cell = W.block_cells(land["patches"][0])[0]
nb = None
for a, (dx, dy) in enumerate(W.MOVES[:4]):
    p = (cell[0] - dx, cell[1] - dy)
    if 0 <= p[0] < W.N and 0 <= p[1] < W.N and not land["walls"][p[1], p[0]] and p not in w.food:
        nb, act = p, a
        break
w.pos = nb
w.m_food[cell[1], cell[0]] = True
w.food[cell] = w.t + 500                                   # really empty, remembered full
w.step(act)
ok1 = w.stale == 1
w2 = w3i.StaleWorld(land, R)
w2.pos = nb
w2.m_food[cell[1], cell[0]] = True
w2.E = 100.0
_, ate = w2.step(act)                                      # remembered full and really full: a meal, not stale
ok2 = w2.stale == 0 and ate and w2.last_meal == w2.t
w3_ = w3i.StaleWorld(land, R)
w3_.pos = nb
w3_.m_food[cell[1], cell[0]] = False
w3_.food[cell] = w3_.t + 500
w3_.step(act)                                              # not remembered: not stale
ok3 = w3_.stale == 0
check("stale arrivals: counted when remembered full and really empty; not for a meal; not when not remembered",
      ok1 and ok2 and ok3)

# 3. the fade per arm
okf = True
for arm, cfg in w3i.ARMS.items():
    w3i.configure(arm)
    f = cfg["fade"]
    okf &= w3d.copy_weight(0) == 0.5 and abs(w3d.copy_weight(f // 2) - 0.25) < 1e-12 and w3d.copy_weight(f) == 0.0 \
        and not w3d.parent_present(f) and w3d.parent_present(f - 1)
check("the fade: 0.5 at 0, 0.25 halfway, 0 from the arm's fade on (L 400k, LC 1.2M, C 1.2M, PYFR 400k)", okf)
check("nothing scheduled on the total steps: learning rate, entropy and clip are constants",
      (B.LR, B.ENT, B.CLIP) == (0.01, 0.01, 1.0))

# 4. split = unsplit; the same seed twice (LC's config, a short fade)
w3i.configure("LC")
w3d.CFG.update(child=2000, always=False)
p1, _, _ = w3d.train_net_parent("LC", 4, 3000, R, hours=1.0)
pa, qa, _ = w3d.train_net_parent("LC", 4, 3000, R, hours=1.0, pause_after=1400)
pb, _, _ = w3d.train_net_parent("LC", 4, 3000, R, hours=1.0, state=qa)
check("a split run equals an unsplit run", all(np.array_equal(p1.p[k], pb.p[k]) for k in p1.p))
p2, _, _ = w3d.train_net_parent("LC", 4, 3000, R, hours=1.0)
check("the same seed twice is the same", all(np.array_equal(p1.p[k], p2.p[k]) for k in p1.p))

# 5. a snapshot does not change the run (train_staged with and without a snapshot; a temporary folder)
tmp = HERE / "tmp_checks"
res = {}
for name, snaps in (("snap", (1500,)), ("plain", ())):
    if tmp.exists():
        shutil.rmtree(tmp)
    tmp.mkdir()
    w3i.OUT = tmp
    w3b.OUT = tmp
    w3d.CFG.update(child=2000, always=False)
    done = w3i.train_staged("LC", 4, hours=1.0, steps=3000, snaps=snaps)
    with np.load(tmp / "LC_4.npz") as z:
        res[name] = {k: z[k].copy() for k in z.files}
    res[name + "_files"] = sorted(p.name for p in tmp.iterdir())
shutil.rmtree(tmp)
check(f"a snapshot does not change the run (snapshot files: {[f for f in res['snap_files'] if '0M' in f]})",
      all(np.array_equal(res["snap"][k], res["plain"][k]) for k in res["plain"]) and
      any(f.startswith("test_LC_4_0M") for f in res["snap_files"]))
check("the staged run equals the plain W3d loop", all(np.array_equal(res["plain"][k], p1.p[k]) for k in p1.p))
print("All: PASS" if not fails else f"FAILED: {fails}")
