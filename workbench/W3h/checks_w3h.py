"""W3h checks, before any data. Prints All: PASS or the failures."""
import json
import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).parent))
import w3h  # noqa: E402
from w3h import w3d, w3b, B, W, R3  # noqa: E402

fails = []


def check(name, ok):
    print(("PASS " if ok else "FAIL ") + name, flush=True)
    if not ok:
        fails.append(name)


R = R3.regrowth()
cal = json.loads(w3h.CALIB.read_text())
check(f"the calibration rule is met (patches {cal['patches']}, harm {cal['harm']})", cal["harm"] is not None)
HARM, PATCHES = cal["harm"], cal["patches"]

# reference: W3d's PYFR training, short childhood, before anything is installed
w3d.CFG.update(child=2000, always=False)
ref, _, _ = w3d.train_net_parent("PYFR", 3, 2500, R, hours=1.0)
base_land = W.make_land(W.TEST_SEEDS[0])

# 1. thorn layout: from the land's seed only; W3's land unchanged
w3h.install(HARM, PATCHES)
land = W.make_land(W.TEST_SEEDS[0])
t1 = w3h.thorn_corners(land, PATCHES)
t2 = w3h.thorn_corners(W.make_land(W.TEST_SEEDS[0]), PATCHES)
food = {c for p in land["patches"] for c in W.block_cells(p)}
tcells = {c for p in t1 for c in W.block_cells(p)}
check("the thorns come from the land's seed alone, off food, shelter and start; W3's land unchanged",
      t1 == t2 and not (tcells & (food | {land["shelter"], land["start"]})) and
      all(np.array_equal(base_land[k], land[k]) if isinstance(land[k], np.ndarray) else base_land[k] == land[k]
          for k in land))

# 2. harm and pain only on thorns; pain only when on
rng = np.random.default_rng(1)
ok_harm, ok_pain, n_on = True, True, 0
for pain in (False, True):
    w3h.CFG["pain"] = pain
    w = W.World(land, R)
    for _ in range(3000):
        if w.done():
            break
        tcells = [(x, y) for y in range(W.N) for x in range(W.N) if w.thorn[y, x]]
        a = W.bfs_path(lambda c: not w.walls[c[1], c[0]], w.pos, tcells) if rng.random() < 0.5 else None
        a = int(rng.integers(5)) if a is None else a
        d0, E0 = w.drive(), w.E
        w.step(a)
        on = bool(w.thorn[w.pos[1], w.pos[0]])
        n_on += on
        ok_harm &= (w3h.CFG["last_harm"] == (HARM if on else 0.0))
        r = R3.reward("D3", d0, w.drive(), 0.0, w.dead)
        base = w3h.base_reward("D3", d0, w.drive(), 0.0, w.dead)
        ok_pain &= abs((base - r) - ((HARM / 8.0) if (on and pain) else 0.0)) < 1e-12
check(f"harm only on thorn cells ({n_on} thorn steps)", ok_harm and n_on > 0)
check("pain = harm / 8 on thorn steps, only in the pain arms", ok_pain)
w3h.CFG["pain"] = False

# 3. the sixth channel shows only thorns seen; its weights start at zero
w = W.World(land, R)
for _ in range(400):
    w.step(int(rng.integers(5)))
m = w.obs_map()
check("the sixth channel = thorns AND seen", m.shape[0] == 6 and np.array_equal(m[5] > 0, w.thorn & w.m_seen))
n0 = B.DriveVIN(3)
check("the thorn channel's weights start at zero", all(not n0.p[k][:, 5].any() for k in ("W0", "Ws", "Wf", "Wc")))

# 4. the parents
w3h.CFG["careful"] = True
stepped = 0
for ls in list(W.TEST_SEEDS)[:10]:
    w = W.World(W.make_land(ls), R)
    s = W.Script()
    while not w.done():
        x0, y0 = w.pos
        a = s.act(W.MapView(w))
        dx, dy = W.MOVES[a]
        nx, ny = x0 + dx, y0 + dy
        stepped += int(w.m_thorn[ny, nx] and not w.walls[ny, nx] and a != 4)
        w.step(a)
check(f"the careful parent never steps onto a thorn it has seen (10 lives; {stepped})", stepped == 0)
w3h.CFG["careful"] = False
w = W.World(land, R)
for _ in range(300):
    w.step(int(rng.integers(5)))
v = W.MapView(w)
check("the thorn-blind parent's view equals W3's MapView", np.array_equal(v.m_wall, w.m_wall))

# 5. no thorns: the loop reproduces W3d's PYFR training (allclose)
w3h.install(HARM, 0)
w3h.CFG.update(pain=False, careful=False)
w3d.CFG.update(child=2000, always=False)
z, _, _ = w3d.train_net_parent("PYFR", 3, 2500, R, hours=1.0)
same = all(np.allclose(z.p[k][:, :5] if k in ("W0", "Ws", "Wf", "Wc") else z.p[k], ref.p[k], atol=1e-10) for k in ref.p)
check("with no thorns, training reproduces W3d's PYFR (allclose)", same)

# 6. split = unsplit; the same seed twice (THP, short childhood)
w3h.install(HARM, PATCHES)
w3h.CFG.update(pain=True, careful=False)
w3d.ARMS["THP"] = {"parts": "YR", "always": False}
w3d.configure("THP")
w3d.CFG.update(child=2000, always=False)
p1, _, _ = w3d.train_net_parent("THP", 4, 3000, R, hours=1.0)
pa, qa, _ = w3d.train_net_parent("THP", 4, 3000, R, hours=1.0, pause_after=1400)
pb, _, _ = w3d.train_net_parent("THP", 4, 3000, R, hours=1.0, state=qa)
check("a split run equals an unsplit run", all(np.array_equal(p1.p[k], pb.p[k]) for k in p1.p))
p2, _, _ = w3d.train_net_parent("THP", 4, 3000, R, hours=1.0)
check("the same seed twice is the same", all(np.array_equal(p1.p[k], p2.p[k]) for k in p1.p))
print("All: PASS" if not fails else f"FAILED: {fails}")
