"""W3c checks, before any data. Prints All: PASS or the failures."""
import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).parent))
import w3c  # noqa: E402
from w3c import B, W, R3, w3b  # noqa: E402

fails = []


def check(name, ok):
    print(("PASS " if ok else "FAIL ") + name, flush=True)
    if not ok:
        fails.append(name)


rng = np.random.default_rng(0)
land = W.make_land(W.TEST_SEEDS[0])
w = W.World(land, R3.regrowth())
for _ in range(40):
    w.step(int(rng.integers(5)))
maps = np.stack([w.obs_map()] * 3)
levels = np.array([[0.0, 0.0, 0.3], [0.5, 0.2, 0.4], [1.0, 0.1, 0.6]])

# 1. gate off, W0 random: the class equals W3's planner exactly
w3c.CFG.update(gate=False, z0=False, fixed=False)
a, b = w3c.GatedVIN(3), w3c.BaseVIN(3)
fa, fb = a.plan(maps, levels), b.plan(maps, levels)
check("gate off reproduces W3's planner", np.array_equal(fa[5], fb[5]) and all(np.array_equal(a.p[k], b.p[k]) for k in a.p))

# 2. gate on: g = 0 equals ungated; at g = 1, W0 and Wc have no effect
w3c.CFG.update(gate=True)
gnet = w3c.GatedVIN(3)
gnet.p["Ws"] = rng.normal(0, 0.3, gnet.p["Ws"].shape)
gnet.p["Wc"] = rng.normal(0, 0.3, gnet.p["Wc"].shape)
u = w3c.BaseVIN(3)
u.p = {k: v.copy() for k, v in gnet.p.items()}
lv0 = np.array([[0.0, 0.0, 0.5]])
check("gate on, no need (g = 0): equal to ungated", np.allclose(gnet.plan(maps[:1], lv0)[5], u.plan(maps[:1], lv0)[5]))
lv1 = np.array([[1.0, 0.2, 0.5]])
q1 = gnet.plan(maps[:1], lv1)[5]
saved = {k: gnet.p[k].copy() for k in ("W0", "Wc")}
gnet.p["W0"] += 1.0
gnet.p["Wc"] -= 1.0
q2 = gnet.plan(maps[:1], lv1)[5]
gnet.p.update(saved)
check("starving (g = 1): W0 and Wc have no effect on the plan", np.allclose(q1, q2))

# 3. gradients through the gated map: backprop vs finite differences on L = sum(z * U) + sum(v * k)
rows = np.array([w.pos[1] * B.N + w.pos[0] + i * B.N * B.N for i in range(3)])
U = rng.normal(0, 1, (3, 5))
kk = rng.normal(0, 1, 3)


def loss(net):
    fw = net.plan(maps, levels)
    z, v = net.head(fw, rows)
    return float((z * U).sum() + (v * kk).sum())


fw = gnet.plan(maps, levels)
g = gnet.backprop(fw, rows, U, kk)
worst = 0.0
for key in ("W0", "Ws", "Wc", "Wf"):
    for _ in range(4):
        idx = tuple(int(rng.integers(0, s)) for s in gnet.p[key].shape)
        old = gnet.p[key][idx]
        gnet.p[key][idx] = old + 1e-6
        lp = loss(gnet)
        gnet.p[key][idx] = old - 1e-6
        lm = loss(gnet)
        gnet.p[key][idx] = old
        num = (lp - lm) / 2e-6
        if abs(num) + abs(g[key][idx]) > 1e-9:
            worst = max(worst, abs(num - g[key][idx]) / (abs(num) + abs(g[key][idx])))
check(f"gated gradients match finite differences (worst relative error {worst:.1e})", worst < 1e-4)

# 4. Z0 starts at zero; Gi keeps the designer's links through training
w3c.configure("Z0")
check("Z0: W0 starts at zero", not B.DriveVIN(5).p["W0"].any())
w3c.configure("Gi")
gi = B.DriveVIN(5)
before = {k: gi.p[k].copy() for k in ("Ws", "Wf", "Wc")}
net, state, fin = w3b.train_net("Gi", 5, 3000, R3.regrowth(), hours=1.0)
check("Gi: the designer's links stay fixed through training",
      all(np.array_equal(before[k], net.p[k]) for k in before) and before["Ws"][0, W.CH_FOOD, 1, 1] == 1.0)
check("Gi: the gate is on", net.gate is True)

# 5. split run = unsplit run (G), and the same seed twice is the same
w3c.configure("G")
n1, s1, _ = w3b.train_net("G", 7, 2600, R3.regrowth(), hours=1.0)
na, sa, _ = w3b.train_net("G", 7, 2600, R3.regrowth(), hours=1.0, pause_after=1200)
nb, sb, _ = w3b.train_net("G", 7, 2600, R3.regrowth(), hours=1.0, state=sa)
check("G: a split run equals an unsplit run", all(np.array_equal(n1.p[k], nb.p[k]) for k in n1.p))
n2, _, _ = w3b.train_net("G", 7, 2600, R3.regrowth(), hours=1.0)
check("G: the same seed twice is the same", all(np.array_equal(n1.p[k], n2.p[k]) for k in n1.p))
w3c.configure("GYFR")
ny, sy, _ = w3b.train_net("GYFR", 7, 2600, R3.regrowth(), hours=1.0)
check("GYFR runs with the parts on (its updates logged)", "y" in sy["updates"])

# 6. F2 walks only to cells remembered as full food
B.DriveVIN = w3c.BaseVIN
pol = w3c.F2Policy(R3.load("D3", 1), np.random.default_rng(1))
w2 = W.World(W.make_land(W.TEST_SEEDS[1]), R3.regrowth())
ok, walked = True, 0
while not w2.done() and w2.t < 1500:
    s, f = w2.deficits()
    foods = [(x, y) for y in range(B.N) for x in range(B.N) if w2.m_food[y, x]]
    k0 = pol.walks
    a = pol.act(w2)
    if pol.walks > k0 and s >= w3b.HIGH["s"] and foods:
        walked += 1
        nxt = W.bfs_path(lambda c: not w2.m_wall[c[1], c[0]], w2.pos, foods)
        ok = ok and a == nxt
    _, ate = w2.step(a)
    pol.after(w2, ate)
check(f"F2's hungry walks head for remembered full food ({walked} walks checked)", ok and walked > 0)
print("All: PASS" if not fails else f"FAILED: {fails}")
