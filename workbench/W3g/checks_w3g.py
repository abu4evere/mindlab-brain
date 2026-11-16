"""W3g checks, before any data. Prints All: PASS or the failures."""
import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).parent))
import w3g  # noqa: E402
from w3g import w3d, w3b, B, W, R3  # noqa: E402

fails = []


def check(name, ok):
    print(("PASS " if ok else "FAIL ") + name, flush=True)
    if not ok:
        fails.append(name)


R = R3.regrowth()
# W3d's PYFR training for reference (5 channels), a short childhood
w3d.CFG.update(child=2000, always=False)
ref, _, _ = w3d.train_net_parent("PYFR", 3, 2500, R, hours=1.0)

w3g.configure()
w3d.CFG.update(child=2000, always=False)
# 1. new channel weights start at zero; the first 5 channels are W3's own draw
n0 = B.DriveVIN(3)
b5 = w3g.BaseVIN.__new__(w3g.BaseVIN)
B.C = 5
w3g.BaseVIN.__init__(b5, 3)
B.C = 6
check("the 6th channel's weights start at zero; channels 1-5 equal W3's draw",
      all(not n0.p[k][:, 5].any() and np.array_equal(n0.p[k][:, :5], b5.p[k]) for k in ("W0", "Ws", "Wf", "Wc")))

# 2. with the new channel held at zero, training reproduces W3d's PYFR (allclose: one extra zero column in the sums)
w3g.CFG["zero"] = True
z, _, _ = w3d.train_net_parent("FM", 3, 2500, R, hours=1.0)
same = all(np.allclose(z.p[k][:, :5] if k in ("W0", "Ws", "Wf", "Wc") else z.p[k], ref.p[k], atol=1e-10) for k in ref.p)
exact = all(np.array_equal(z.p[k][:, :5] if k in ("W0", "Ws", "Wf", "Wc") else z.p[k], ref.p[k]) for k in ref.p)
check(f"channel held at zero reproduces W3d's PYFR training (allclose; bit-exact: {exact})", same)
w3g.CFG["zero"] = False

# 3. the channel marks exactly the cells eaten at
w = W.World(W.make_land(W.TEST_SEEDS[0]), R)
rng = np.random.default_rng(0)
eaten = set()
for _ in range(1500):
    if w.done():
        break
    _, ate = w.step(int(rng.integers(5)))
    if ate:
        eaten.add(w.pos)
marked = {(x, y) for y in range(W.N) for x in range(W.N) if w.m_fed[y, x]}
check(f"the channel marks exactly the cells eaten at ({len(eaten)} cells)", marked == eaten and w.obs_map().shape[0] == 6)

# 4. split = unsplit; same seed twice
p1, _, _ = w3d.train_net_parent("FM", 4, 3000, R, hours=1.0)
pa, qa, _ = w3d.train_net_parent("FM", 4, 3000, R, hours=1.0, pause_after=1400)
pb, _, _ = w3d.train_net_parent("FM", 4, 3000, R, hours=1.0, state=qa)
check("a split run equals an unsplit run", all(np.array_equal(p1.p[k], pb.p[k]) for k in p1.p))
p2, _, _ = w3d.train_net_parent("FM", 4, 3000, R, hours=1.0)
check("the same seed twice is the same", all(np.array_equal(p1.p[k], p2.p[k]) for k in p1.p))
check("the brain learns to use the new channel (its weights move from zero)", any(p1.p[k][:, 5].any() for k in ("W0", "Ws", "Wf", "Wc")))
print("All: PASS" if not fails else f"FAILED: {fails}")
