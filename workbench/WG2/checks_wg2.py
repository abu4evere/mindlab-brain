"""WG2 checks, before any data. Prints All: PASS or the failures."""
import json
import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).parent))
import wg2  # noqa: E402
from wg2 import W, R3, wq, wi  # noqa: E402

fails = []


def check(name, ok):
    print(("PASS " if ok else "FAIL ") + name, flush=True)
    if not ok:
        fails.append(name)


# 1. IM re-run reproduces WI's IM seed 1 (room windows, dreams, after-room test)
a = wg2.run("IM", 1)
b = json.loads((Path(__file__).parent.parent / "WI" / "output" / "IM_1.json").read_text())
same_after = json.dumps(a["after"], sort_keys=True) == json.dumps(b["after"], sort_keys=True)   # NaN-safe (NaN != NaN)
# the pattern measure is zlib's compressed size; zlib can differ by a byte between platforms (Windows vs the cloud's
# Linux), so pattern is compared within 0.002 and activity and reach exactly
same_win = all(x["activity"] == y["activity"] and x["reach"] == y["reach"] and abs(x["pattern"] - y["pattern"]) <= 0.002
               for x, y in zip(a["windows"], b["windows"]))
check(f"IM reproduces WI's IM seed 1 (windows {same_win}, dreams {a['dreams'] == b['dreams']}, "
      f"after-room lives {same_after})", same_win and a["dreams"] == b["dreams"] and same_after)
check("IM tracks 19 random blocks", len(a["questions"]) == 19)

# 2. marking: after a question, its cells are long unseen (uncertainty about 1) until seen again
room = wq.Room(W.make_land(wi.ROOM), R3.regrowth())
rng = np.random.default_rng(0)
for _ in range(400):
    room.step(int(rng.integers(5)))
net = wi.load(2)
d, best = wg2.dream(net, room, np.random.default_rng(1), np.random.default_rng(2), R3.regrowth())
if best is None:
    best = [(5, 5), (6, 5), (5, 6), (6, 6)]
for x, y in best:
    room.m_last[y, x] = room.t - wg2.BACK
u = room.uncertainty()
check("a question's cells read as unknown (uncertainty > 0.99) unless walls",
      all(u[y, x] > 0.99 or room.m_wall[y, x] for x, y in best))
check("the dream's best patch lies on imagined-open cells", all(not room.m_wall[y, x] for x, y in best))

# 3. IQ runs, poses questions, and the same seed twice is the same
r1 = wg2.run("IQ", 3, test=False)
r2 = wg2.run("IQ", 3, test=False)
check(f"IQ poses questions ({len(r1['questions'])}, at most 19)", 1 <= len(r1["questions"]) <= 19)
check("IQ: the same seed twice is the same", r1 == r2)
check("IQ differs from IM in the room (the questions act)",
      r1["windows"] != wg2.run("IM", 3, test=False)["windows"])
print("All: PASS" if not fails else f"FAILED: {fails}")
