"""WQ checks, before any data. Prints All: PASS or the failures."""
import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).parent))
import wq  # noqa: E402
from wq import W, R3  # noqa: E402

fails = []


def check(name, ok):
    print(("PASS " if ok else "FAIL ") + name, flush=True)
    if not ok:
        fails.append(name)


# 1. the room: needs always met, nothing eaten, no relocation, fixed contents, no death, 10,000-step stay
w = wq.Room(W.make_land(wq.ROOMS[0]), R3.regrowth())
food0, patches0 = dict(w.food), list(w.patches)
rng = np.random.default_rng(0)
ok = True
while not w.done():
    w.step(int(rng.integers(5)))
    ok = ok and w.deficits() == (0.0, 0.0) and not w.dead
check("needs always met and no death over a full stay", ok and w.t == wq.T_ROOM)
check("nothing eaten, nothing moved: food and patches unchanged", w.food == food0 and w.patches == patches0 and w.events == [])

# 2. a stay's measures are in range; the same stay twice is the same
r1 = wq.stay("D3", "still", 1, wq.ROOMS[0])
r2 = wq.stay("D3", "still", 1, wq.ROOMS[0])
check("same stay twice is the same", r1 == r2)
wd = r1["windows"]
check("10 windows; activity in [0,1]; reach 1..225; pattern positive",
      len(wd) == 10 and all(0 <= x["activity"] <= 1 and 1 <= x["reach"] <= 225 and x["pattern"] > 0 for x in wd))

# 3. still leaves the weights unchanged; living changes them (D3 has curiosity reward)
net = wq.load("D3", 1)
before = {k: v.copy() for k, v in net.p.items()}
_ = wq.stay("D3", "still", 1, wq.ROOMS[1])
check("still: the stored weights are untouched (a fresh load is used per stay)",
      all(np.array_equal(before[k], wq.load("D3", 1).p[k]) for k in before))
orig = wq.load
captured = {}


def spy(brain, seed):
    n = orig(brain, seed)
    captured["net"] = n
    return n


wq.load = spy
_ = wq.stay("D3", "living", 1, wq.ROOMS[1])
wq.load = orig
check("living: the weights change during the stay",
      not all(np.array_equal(before[k], captured["net"].p[k]) for k in before))
_ = wq.stay("D2", "living", 2, wq.ROOMS[1])
check("D2 living stay completes", True)

# 4. Rand and Script run; Script never reads the world's truth (W3's MapView)
check("Rand stay runs", len(wq.stay("Rand", "still", 1, wq.ROOMS[2])["windows"]) == 10)
check("Script stay runs", len(wq.stay("Script", "still", 1, wq.ROOMS[2])["windows"]) == 10)
print("All: PASS" if not fails else f"FAILED: {fails}")
