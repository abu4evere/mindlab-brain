"""WL checks, before any data. Prints All: PASS or the failures."""
import json
import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).parent))
import wl  # noqa: E402
import wn  # noqa: E402
import ws  # noqa: E402

fails = []


def check(name, ok):
    print(("PASS " if ok else "FAIL ") + name, flush=True)
    if not ok:
        fails.append(name)


# 1. L0 reproduces WN's M-n children (seeds 1, 2; sizes 32 and 128): own skill at 7, 15, 30, 60 and after a showing
WN = Path(__file__).parent.parent / "WN" / "output"
for n in (32, 128):
    for s in (1, 2):
        a = wl.run_child("L0", n, s)
        b = json.loads((WN / f"M{n}_seed_{s}.json").read_text())
        same = all(a["tests"][d] == b["tests"][str(d)]["success"] for d in wl.TEST_DAYS) and \
            a["show30"] == b["show_tests"]["30"]["success"]
        check(f"L0-{n} seed {s} reproduces WN's M{n}", same)

# 2. gradients through wait steps (finite differences), with fixed noise
rng = np.random.default_rng(0)
net = wn.Net(5, 16, True)
look = rng.normal(0, 1, ws.LOOK)
prefix = ws.show_steps(look, [(1, 2), (3, 0)]) + [wl.Wait(rng.normal(0, 0.6, 16)) for _ in range(3)]
xs_after = [ws.x_try(look, 0, None, 0), ws.x_try(look, 0, 1, 1)]
targets = {len(prefix): (1, 1.0), len(prefix) + 1: (2, 1.0)}


def loss():
    xs, hs, h = wl.run_prefix(net, prefix)
    L = 0.0
    for t, x in enumerate(xs_after):
        h, z = net.step(x, h)
        a, sc = targets[len(prefix) + t]
        L += -np.log(ws.softmax(z)[a]) * sc
    return L


xs, hs, h = wl.run_prefix(net, prefix)
for x in xs_after:
    h, _ = net.step(x, h)
    xs.append(x)
    hs.append(h)
g = net.grads(xs, hs, targets)
worst = 0.0
for k in ("Wx", "Wh", "b", "M"):
    for _ in range(6):
        idx = tuple(int(rng.integers(0, s)) for s in net.p[k].shape)
        old = net.p[k][idx]
        net.p[k][idx] = old + 1e-6
        lp = loss()
        net.p[k][idx] = old - 1e-6
        lm = loss()
        net.p[k][idx] = old
        num = (lp - lm) / 2e-6
        worst = max(worst, abs(num - g[k][idx]) / max(1e-8, abs(num) + abs(g[k][idx])))
check(f"gradients through noisy wait steps (worst relative error {worst:.1e})", worst < 1e-5)

# 3. episodes: L1 adds 4 wait steps, L2 8; noise sd as planned
e1 = wl.episode(look, [(1, 2), (3, 0)], 128, "L1", np.random.default_rng(1))
e2 = wl.episode(look, [(1, 2), (3, 0)], 128, "L2", np.random.default_rng(1))
sd = float(np.std(np.concatenate([w.eps for w in e2 if isinstance(w, wl.Wait)])))
check("L1 has 4 wait steps, L2 has 8", sum(isinstance(w, wl.Wait) for w in e1) == 4 and sum(isinstance(w, wl.Wait) for w in e2) == 8)
check(f"L2 noise sd about 0.6 ({sd:.3f})", 0.55 < sd < 0.65)

# 4. same child twice; L2 differs from L0
a1, a2 = wl.run_child("L2", 32, 3), wl.run_child("L2", 32, 3)
check("same child twice is the same", a1 == a2)
check("the leak changes the child", a1["food"] != wl.run_child("L0", 32, 3)["food"])
print("All: PASS" if not fails else f"FAILED: {fails}")
