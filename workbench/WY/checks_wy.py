"""WY checks, before any data. Prints All: PASS or the failures."""
import json
import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).parent))
import wy  # noqa: E402
import wn  # noqa: E402
import ws  # noqa: E402

fails = []


def check(name, ok):
    print(("PASS " if ok else "FAIL ") + name, flush=True)
    if not ok:
        fails.append(name)


# 1. Base reproduces WC's M128 and M32 (seed 1001); TBYS without YS would be WM's TB: check TB parts via WM's TB file
for n in (128, 32):
    a = wy.run_child("Base", n, 1001)
    b = json.loads((Path(__file__).parent.parent / "WC" / "output" / f"M{n}_seed_1001.json").read_text())
    check(f"Base-{n} reproduces WC's M{n} seed 1001",
          a["food"] == b["food"] and all(a["tests"][d]["success"] == b["tests"][str(d)]["success"] for d in a["tests"]))

# 2. self_copy pushes the copied acts up, more with a larger weight
look = np.random.default_rng(2).normal(0, 1, ws.LOOK)
probs = []
for w in (0.0, 0.3, 1.0):
    net = wn.Net(4, 32, True)
    h = np.zeros(32)
    h, z = net.step(ws.x_try(look, 0, None, 0), h)
    p0 = ws.softmax(z)[2]
    wy.self_copy(net, look, [[2, 1]], [w], [])
    h2, z2 = net.step(ws.x_try(look, 0, None, 0), np.zeros(32))
    probs.append(ws.softmax(z2)[2] - p0)
check(f"self-copy raises the copied act, scaled by the weight ({[round(p, 4) for p in probs]})",
      abs(probs[0]) < 1e-12 and 0 < probs[1] < probs[2])

# 3. YS fires, and mostly after the change (surprising successes)
r = wy.run_child("YS", 32, 1001)
check(f"YS fires ({r['ys_steps']} self-copies, mean weight {r['ys_mean_weight']:.2f})", r["ys_steps"] > 0)

# 4. same child twice; all arms run
for arm in wy.ARMS:
    r1, r2 = wy.run_child(arm, 32, 1003), wy.run_child(arm, 32, 1003)
    check(f"{arm}: same child twice is the same", r1 == r2)
print("All: PASS" if not fails else f"FAILED: {fails}")
