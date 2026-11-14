"""WN checks, before any data. Prints All: PASS or the failures."""
import json
import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).parent))
import wn  # noqa: E402
import ws  # noqa: E402

fails = []


def check(name, ok):
    print(("PASS " if ok else "FAIL ") + name, flush=True)
    if not ok:
        fails.append(name)


# 1. M-32 is WS's memory child (Bm) exactly, from WS's saved output
for s in (1, 2):
    a = wn.run("M32", s)
    b = json.loads((Path(__file__).parent.parent / "WS" / "output" / f"Bm_seed_{s}.json").read_text())
    same = all(a["tests"][d]["success"] == b["tests"][str(d)]["success"] for d in wn.TEST_DAYS)
    same = same and a["show_tests"][30]["success"] == b["show_tests"]["30"]["success"]
    check(f"M32 seed {s} reproduces WS Bm (days 7,15,30,60 and after a showing at 30)", same)

# 2. gradients through time against finite differences, at several sizes
rng = np.random.default_rng(0)
for n, rec in ((8, True), (64, True), (8, False), (128, False)):
    net = wn.Net(5, n, rec)
    xs_in = [rng.normal(0, 1, ws.N_IN) for _ in range(7)]
    targets = {2: (1, 1.0), 4: (3, -0.4), 6: (0, 0.7)}

    def loss():
        h, L = np.zeros(net.n), 0.0
        for t, x in enumerate(xs_in):
            h, z = net.step(x, h)
            if t in targets:
                a, sc = targets[t]
                L += sc * -np.log(ws.softmax(z)[a])
        return L

    xs, hs = wn.run_prefix(net, xs_in)[:2]
    g = net.grads(xs, hs, targets)
    worst = 0.0
    for k in ("Wx", "Wh", "M", "b", "c"):
        if k == "Wh" and not rec:
            continue
        for _ in range(5):
            idx = tuple(int(rng.integers(0, s)) for s in net.p[k].shape)
            old = net.p[k][idx]
            net.p[k][idx] = old + 1e-6
            lp = loss()
            net.p[k][idx] = old - 1e-6
            lm = loss()
            net.p[k][idx] = old
            num = (lp - lm) / 2e-6
            worst = max(worst, abs(num - g[k][idx]) / max(1e-8, abs(num) + abs(g[k][idx])))
    check(f"gradients n={n} recurrent={rec} (worst relative error {worst:.1e})", worst < 1e-5)

# 3. growing keeps what the child does at that moment (act scores identical before and after)
net = wn.Net(7, 16, True)
seq = [rng.normal(0, 1, ws.N_IN) for _ in range(10)]


def scores(net):
    h, out = np.zeros(net.n), []
    for x in seq:
        h, z = net.step(x, h)
        out.append(z)
    return np.array(out)


before = scores(net)
ok = True
for m in (32, 64, 128):
    net.grow(m)
    ok = ok and np.allclose(before, scores(net), atol=1e-12) and net.p["Wh"].shape == (m, m)
check("growth 16->32->64->128 leaves the act scores unchanged", ok)
check("new neurons' outgoing weights start at zero",
      np.all(net.p["M"][:, 16:] == 0) and np.all(net.p["Wh"][:16, 16:] == 0))

# 4. the growing child's sizes, and the same seed twice
g1, g2 = wn.run("G", 3), wn.run("G", 3)
check("G sizes at days 7, 15, 30, 60 are 16, 32, 128, 128", g1["sizes"] == {7: 16, 15: 32, 30: 128, 60: 128})
check("same seed twice gives the same results", g1["tests"] == g2["tests"] and g1["show_tests"] == g2["show_tests"])

# 5. the no-memory brain gets no showing in its state (its after-showing test is a plain test on the same looks).
# (First version compared it with the plain day-30 test, which draws different look noise: a wrong check, fixed
# before any data; see IMPLEMENTATION.md.)
home, net = ws.Home(1), wn.Net(1, 8, False)
r = np.random.default_rng([1, 6, 30, 1])
manual = []
for k in range(ws.KINDS):
    look = home.looks[k] + r.normal(0, 0.2, ws.LOOK)
    manual.append(1.0 if ws.try_box(net, look, home.pairs[k], [], None, False)[0] == ws.LIDS else 0.0)
check("F-n after-showing test uses no showing prefix",
      ws.test(home, net, 1, 30, showing=True)["success"] == float(np.mean(manual)))

print("All: PASS" if not fails else f"FAILED: {fails}")
