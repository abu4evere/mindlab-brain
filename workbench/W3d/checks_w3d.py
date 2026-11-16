"""W3d checks, before any data. Prints All: PASS or the failures."""
import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).parent))
import w3d  # noqa: E402
from w3d import w3b, W, R3  # noqa: E402

fails = []


def check(name, ok):
    print(("PASS " if ok else "FAIL ") + name, flush=True)
    if not ok:
        fails.append(name)


R = R3.regrowth()
# 1. no parent (childhood 0, not always): the loop reproduces W3b's D3 training exactly
w3d.CFG.update(child=0, always=False)
a, sa, _ = w3d.train_net_parent("D3", 3, 2500, R, hours=1.0)
b, sb, _ = w3b.train_net("D3", 3, 2500, R, hours=1.0)
check("no parent reproduces W3b's D3 training exactly", all(np.array_equal(a.p[k], b.p[k]) for k in a.p))

# 2. weights: P fades 0.5 -> 0 over childhood; PA constant 0.5
w3d.CFG.update(child=400_000, always=False)
check("P weight: 0.5 at 0, 0.25 at 200k, 0 at 400k and after",
      w3d.copy_weight(0) == 0.5 and abs(w3d.copy_weight(200_000) - 0.25) < 1e-12 and w3d.copy_weight(400_000) == 0.0
      and not w3d.parent_present(400_000))
w3d.CFG.update(always=True)
check("PA weight 0.5 always", w3d.copy_weight(1_999_999) == 0.5 and w3d.parent_present(1_999_999))

# 3. copies happen on every 4th step while the parent is present (short childhood 2,000), none after
w3d.CFG.update(child=2000, always=False)
n, s, _ = w3d.train_net_parent("P", 4, 3000, R, hours=1.0)
check(f"P copies only during childhood, every 4th step ({s['updates'].get('copy')} copies; expected 500)",
      s["updates"].get("copy") == 500)
w3d.CFG.update(always=True)
n2, s2, _ = w3d.train_net_parent("PA", 4, 3000, R, hours=1.0)
check(f"PA copies every 4th step for the whole run ({s2['updates'].get('copy')} copies; expected 750)",
      s2["updates"].get("copy") == 750)
w3d.CFG.update(child=2000, always=False)
n3, _, _ = w3d.train_net_parent("P", 3, 2500, R, hours=1.0)
check("the parent changes learning (P differs from no parent, same seed)",
      not all(np.array_equal(n3.p[k], a.p[k]) for k in n3.p))

# 4. the parent sees only the map view (W3's Script on a MapView)
import inspect  # noqa: E402
check("the parent is W3's Script acting on a MapView", "parent.act(W.MapView(w))" in w3d._src)

# 5. split = unsplit, and the same seed twice (PYFR, short childhood)
w3d.CFG.update(child=2000, always=False)
w3d.configure  # noqa: B018
p1, q1, _ = w3d.train_net_parent("PYFR", 5, 3000, R, hours=1.0)
pa, qa, _ = w3d.train_net_parent("PYFR", 5, 3000, R, hours=1.0, pause_after=1400)
pb, qb, _ = w3d.train_net_parent("PYFR", 5, 3000, R, hours=1.0, state=qa)
check("PYFR: a split run equals an unsplit run", all(np.array_equal(p1.p[k], pb.p[k]) for k in p1.p))
p2, _, _ = w3d.train_net_parent("PYFR", 5, 3000, R, hours=1.0)
check("PYFR: the same seed twice is the same", all(np.array_equal(p1.p[k], p2.p[k]) for k in p1.p))
print("All: PASS" if not fails else f"FAILED: {fails}")
