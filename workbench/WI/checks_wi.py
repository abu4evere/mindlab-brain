"""WI checks, before any data. Prints All: PASS or the failures."""
import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).parent))
import wi  # noqa: E402
from wi import W, R3, wq  # noqa: E402

fails = []


def check(name, ok):
    print(("PASS " if ok else "FAIL ") + name, flush=True)
    if not ok:
        fails.append(name)


# 1. the imagined land is built only from memory: walls = remembered walls (+ border), food placed on open cells
room = wq.Room(W.make_land(wi.ROOM), R3.regrowth())
rng = np.random.default_rng(0)
for _ in range(300):
    room.step(int(rng.integers(5)))
land = wi.imagined_land(room, np.random.default_rng(1))
inner = (slice(1, -1), slice(1, -1))
check("imagined walls are the remembered walls (inside the border)", np.array_equal(land["walls"][inner], room.m_wall[inner]))
cells = [c for p in land["patches"] for c in W.block_cells(p)]
check("imagined food sits on imagined-open cells, away from the shelter",
      len(land["patches"]) == 3 and all(not land["walls"][y, x] for x, y in cells) and land["shelter"] not in cells)
true_walls = W.make_land(wi.ROOM)["walls"]
unseen_true_walls = int((true_walls & ~room.m_seen).sum())
check(f"the imagination does not read unseen true walls ({unseen_true_walls} unseen true walls exist)",
      unseen_true_walls == 0 or not np.array_equal(land["walls"], true_walls))

# 2. a dream does not change the real room
net = wi.load(1)
pos, t, mem = room.pos, room.t, room.m_seen.copy()
d = wi.dream(net, room, np.random.default_rng(2), np.random.default_rng(3), R3.regrowth())
check("a dream leaves the real room untouched", room.pos == pos and room.t == t and np.array_equal(room.m_seen, mem))
check(f"a dream lasts at most 200 steps ({d['steps']})", 1 <= d["steps"] <= 200)

# 3. a dream changes the brain (it learns in imagination)
before = {k: v.copy() for k, v in net.p.items()}
wi.dream(net, room, np.random.default_rng(4), np.random.default_rng(5), R3.regrowth())
check("learning happens in a dream", not all(np.array_equal(before[k], net.p[k]) for k in before))

# 4. L without dreams reproduces WQ's GYFR living stay on room 900001 (the same streams and updates)
a = wi.run("L", 2, test=False)
b = wq.stay("GYFR", "living", 2, wi.ROOM)
check("L reproduces WQ's GYFR living stay (room 900001)",
      all(x["activity"] == y["activity"] and x["reach"] == y["reach"] for x, y in zip(a["windows"], b["windows"])))

# 5. IM dreams 19 times (every 500 steps, not at the end); same seed twice is the same
r1 = wi.run("IM", 3, test=False)
r2 = wi.run("IM", 3, test=False)
check(f"IM dreams 19 times ({len(r1['dreams'])})", len(r1["dreams"]) == 19)
check("IM: the same seed twice is the same", r1 == r2)
print("All: PASS" if not fails else f"FAILED: {fails}")
