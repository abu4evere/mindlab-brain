"""W3e checks, before any data. Prints All: PASS or the failures."""
import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).parent))
import w3e  # noqa: E402
from w3e import w3b, w3d, B, W, R3  # noqa: E402

fails = []


def check(name, ok):
    print(("PASS " if ok else "FAIL ") + name, flush=True)
    if not ok:
        fails.append(name)


R = R3.regrowth()
w3e.configure("G2", 3)
parent_before = {k: v.copy() for k, v in w3e._P["net"].p.items()}

# 1. no parent present (childhood 0): reproduces W3b's YFR training (the same parts) exactly
w3d.CFG.update(child=0, always=False)
a, _, _ = w3e.train_net_gen("G2", 3, 2500, R, hours=1.0)
b, _, _ = w3b.train_net("YFR", 3, 2500, R, hours=1.0)
check("no parent reproduces W3b's YFR training exactly", all(np.array_equal(a.p[k], b.p[k]) for k in a.p))

# 2. with a short childhood: copies every 4th step during it; the parent's weights never change
w3d.CFG.update(child=2000, always=False)
n, s, _ = w3e.train_net_gen("G2", 3, 3000, R, hours=1.0)
check(f"copies every 4th step during childhood ({s['updates'].get('copy')}; expected 500)", s["updates"].get("copy") == 500)
check("the parent's weights never change", all(np.array_equal(parent_before[k], w3e._P["net"].p[k]) for k in parent_before))
check("the learned parent changes learning (differs from no parent)", not all(np.array_equal(n.p[k], a.p[k]) for k in n.p))

# 3. the parent gives its argmax act on the child's view
w = W.World(W.make_land(W.TEST_SEEDS[0]), R)
m, lev = w.obs_map(), R3.levels(w, "D3")
fw = w3e._P["net"].plan(m[None], np.asarray(lev, float)[None])
z, _ = w3e._P["net"].head(fw, np.array([w.pos[1] * B.N + w.pos[0]]))
check("parent_act is the parent's argmax", w3e.parent_act(m, lev, w.pos) == int(np.argmax(z[0])))

# 4. split = unsplit; same seed twice
p1, _, _ = w3e.train_net_gen("G2", 4, 3000, R, hours=1.0)
pa, qa, _ = w3e.train_net_gen("G2", 4, 3000, R, hours=1.0, pause_after=1400)
pb, _, _ = w3e.train_net_gen("G2", 4, 3000, R, hours=1.0, state=qa)
check("a split run equals an unsplit run", all(np.array_equal(p1.p[k], pb.p[k]) for k in p1.p))
p2, _, _ = w3e.train_net_gen("G2", 4, 3000, R, hours=1.0)
check("the same seed twice is the same", all(np.array_equal(p1.p[k], p2.p[k]) for k in p1.p))

# 5. fidelity: a brain against itself agrees 1.0; states are collected
par = w3e._P["net"]
f_self, nst = w3e.fidelity(par, par, 3)
check(f"fidelity of the parent with itself is 1.0 ({f_self}; {nst} states)", f_self == 1.0 and nst > 50)
print("All: PASS" if not fails else f"FAILED: {fails}")
