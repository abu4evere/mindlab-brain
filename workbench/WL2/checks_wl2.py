"""WL2 checks, before any data. Prints All: PASS or the failures."""
import json
import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).parent))
import wl2  # noqa: E402
import wl  # noqa: E402
import ws  # noqa: E402

fails = []


def check(name, ok):
    print(("PASS " if ok else "FAIL ") + name, flush=True)
    if not ok:
        fails.append(name)


WLO = Path(__file__).parent.parent / "WL" / "output"
# 1. L0 and L2 reproduce WL's saved children (sizes 32 and 128, seed 1)
for arm in ("L0", "L2"):
    for n in (32, 128):
        a = wl2.run_child(arm, n, 1)
        b = json.loads((WLO / f"{arm}_{n}_seed_1.json").read_text())
        check(f"{arm}-{n} reproduces WL", a["tests"] == {int(k): v for k, v in b["tests"].items()}
              and a["show30"] == b["show30"] and a["food"] == b["food"])

# 2. episodes
look = np.zeros(ws.LOOK)
pairs = [(1, 2), (3, 0)]
r = np.random.default_rng(0)
e = {a: wl2.episode(a, look, pairs, 16, r) for a in wl2.ARMS}
check("W8: 4 showing steps + 8 silent waits",
      len(e["W8"]) == 12 and all(isinstance(x, wl.Wait) and not x.eps.any() for x in e["W8"][4:]))
check("NS: 4 noisy showing steps, no wait", len(e["NS"]) == 4 and all(isinstance(x, wl2.Noisy) and x.eps.std() > 0.2 for x in e["NS"]))
check("NP and L0: the plain showing", len(e["NP"]) == 4 and len(e["L0"]) == 4)
check("Linf: a blank memory", e["Linf"] == [])

# 3. NP noise only while noise_on (practice), none in tests
net = wl2.Net(3, 16, True, np_noise=True)
x = np.ones(ws.N_IN)
net.noise_on = False
h1, _ = net.step(x, np.zeros(16))
h2, _ = net.step(x, np.zeros(16))
net.noise_on = True
h3, _ = net.step(x, np.zeros(16))
check("NP: no noise when off, noise when on", np.array_equal(h1, h2) and not np.allclose(h1, h3))

# 4. every arm runs; the same child twice is the same; arms differ
res = {a: wl2.run_child(a, 32, 2) for a in wl2.ARMS}
check("same child twice is the same (NP)", wl2.run_child("NP", 32, 2) == res["NP"])
check("all six arms give different lives", len({r["food"] for r in res.values()}) == 6)
check("Linf: after-showing test equals a plain test at day 30 setup (blank memory)", res["Linf"]["show30"] is not None)
print("All: PASS" if not fails else f"FAILED: {fails}")
