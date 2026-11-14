"""WG checks, before any data. Prints All: PASS or the failures."""
import json
import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).parent))
import wg  # noqa: E402
import wn  # noqa: E402
import ws  # noqa: E402

fails = []


def check(name, ok):
    print(("PASS " if ok else "FAIL ") + name, flush=True)
    if not ok:
        fails.append(name)


# 1. the references and G are WN's children (seed 1, compared with WN's saved output)
for b in ("M32", "G"):
    a = wg.run(b, 1)
    w = json.loads((Path(__file__).parent.parent / "WN" / "output" / f"{b}_seed_1.json").read_text())
    check(f"{b} seed 1 equals WN's", all(a["tests"][d]["success"] == w["tests"][str(d)]["success"] for d in wn.TEST_DAYS)
          and a["show_tests"][30]["success"] == w["show_tests"]["30"]["success"])

# 2. growth modes: awake_in keeps the act scores; awake changes them; sizes and starting scales are as planned
rng = np.random.default_rng(0)
seq = [rng.normal(0, 1, ws.N_IN) for _ in range(10)]


def scores(net):
    h, out = np.zeros(net.n), []
    for x in seq:
        h, z = net.step(x, h)
        out.append(z)
    return np.array(out)


net = wn.Net(7, 16, True)
before = scores(net)
ok = True
for m in (32, 64, 128):
    wg.grow(net, m, "awake_in")
    ok = ok and np.allclose(before, scores(net), atol=1e-12) and net.p["Wh"].shape == (m, m) and net.n == m
check("awake_in growth 16->128 leaves the act scores unchanged", ok)
check("awake_in: new outgoing zero", np.all(net.p["M"][:, 16:] == 0) and np.all(net.p["Wh"][:16, 16:] == 0))
sd = float(net.p["Wx"][64:].std())
check(f"awake_in: new incoming scale about 0.1 (sd {sd:.3f})", 0.09 < sd < 0.11)
net2 = wn.Net(7, 16, True)
wg.grow(net2, 32, "awake")
check("awake growth changes the act scores", not np.allclose(before, scores(net2)))
sd2 = float(net2.p["M"][:, 16:].std())
check(f"awake: new outgoing scale about 0.1 (sd {sd2:.3f})", 0.07 < sd2 < 0.13)

# 3. sizes over a life, and the same seed twice
r1, r2 = wg.run("GA32", 2), wg.run("GA32", 2)
check("GA32 sizes 8, 16, 32, 32 at days 7, 15, 30, 60", r1["sizes"] == {7: 8, 15: 16, 30: 32, 60: 32})
check("same seed twice gives the same results", r1["tests"] == r2["tests"] and r1["out_weight_day60"] == r2["out_weight_day60"])
r3 = wg.run("GF", 2)
check("GF sizes 16, 32, 128, 128", r3["sizes"] == {7: 16, 15: 32, 30: 128, 60: 128})
check("M128 has no added neurons", wg.run("M128", 2)["out_weight_day60"]["added"] is None)

print("All: PASS" if not fails else f"FAILED: {fails}")
