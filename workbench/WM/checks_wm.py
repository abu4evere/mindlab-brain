"""WM checks, before any data. Prints All: PASS or the failures."""
import json
import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).parent))
import wm  # noqa: E402
import ws  # noqa: E402
import wn  # noqa: E402

fails = []


def check(name, ok):
    print(("PASS " if ok else "FAIL ") + name, flush=True)
    if not ok:
        fails.append(name)


WC_OUT = Path(__file__).parent.parent / "WC" / "output"
# 1. Base reproduces WC's children exactly (sizes 128 and 32, seed 1001)
for n in (128, 32):
    a = wm.run_child("Base", n, 1001)
    b = json.loads((WC_OUT / f"M{n}_seed_1001.json").read_text())
    same = a["food"] == b["food"] and all(a["tests"][d]["success"] == b["tests"][str(d)]["success"]
                                          and a["tests"][d]["stale"] == b["tests"][str(d)]["stale"] for d in a["tests"])
    check(f"Base-{n} reproduces WC's M{n} seed 1001 (food and every test)", same)

# 2. blocked pairs are never drawn
net = wn.Net(3, 32, True)
rng = np.random.default_rng(0)
look = np.random.default_rng(1).normal(0, 1, ws.LOOK)
tabu = {0: {(0, b) for b in range(4)} | {(1, 2)}, 1: set()}
ok = True
for _ in range(400):
    _, ch = wm.try_box(net, look, [(3, 3), (2, 2)], [], rng, True, tabu=tabu)
    ok = ok and ch[0][0] != 0 and tuple(ch[0]) != (1, 2)
check("blocked pairs never chosen (a fully blocked first act, and one blocked pair)", ok)

# 3. the surprise trace: e and u follow the plan's formulas over r = 1, 1, 0
e = u = 0.0
for r in (1.0, 1.0, 0.0):
    u = 0.7 * u + 0.3 * max(0.0, e - r)
    e += 0.2 * (r - e)
check(f"surprise trace after 1, 1, 0: u = {u:.3f} (expected 0.108)", abs(u - 0.3 * 0.36) < 1e-12)
s = wm.run_child("SU", 32, 1001)
check(f"SU: surprise rises in the changing world (max u {s['u_max']:.2f} > 0.2)", s["u_max"] > 0.2)

# 4. LSi senses: 10 more inputs; the original 29 columns are the base network's
a, b = wm.make_net(5, 32, True), wn.Net(5, 32, True)
check("LSi network has 39 inputs and keeps the base 29 columns",
      a.p["Wx"].shape == (32, 39) and np.array_equal(a.p["Wx"][:, :29], b.p["Wx"]))
last = {(2, 0): (1, 3, False)}
x = wm.extra(last, 2, 0)
check("LSi sense of a failed (1, 3) try", list(x) == [0, 1, 0, 0, 0, 0, 0, 1, 0, 1])
check("LSi sense with no try yet is zeros", not wm.extra(last, 2, 1).any())

# 5. every arm runs, and the same child twice is the same
for arm in wm.ARMS:
    r1, r2 = wm.run_child(arm, 32, 1002), wm.run_child(arm, 32, 1002)
    check(f"{arm}: same child twice is the same", r1 == r2 and sorted(r1["tests"]) == [30, 33, 38, 45, 48, 53, 60])
print("All: PASS" if not fails else f"FAILED: {fails}")
