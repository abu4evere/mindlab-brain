"""WF checks, before any data. Prints All: PASS or the failures."""
import json
import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).parent))
import wf  # noqa: E402
import wn  # noqa: E402
import ws  # noqa: E402

fails = []


def check(name, ok):
    print(("PASS " if ok else "FAIL ") + name, flush=True)
    if not ok:
        fails.append(name)


WYO = Path(__file__).parent.parent / "WY" / "output"
# 1. Base and TBYS reproduce WY's saved children (seed 1001, size 32)
for arm in ("Base", "TBYS"):
    a = wf.run_child(arm, 32, 1001)
    b = json.loads((WYO / f"{arm}32_seed_1001.json").read_text())
    check(f"{arm}-32 reproduces WY", a["food"] == b["food"] and
          all(a["tests"][d]["success"] == b["tests"][str(d)]["success"] for d in a["tests"]))

# 2. wf.try_box with no extras and no forcing equals wm.try_box (same draws, same learning)
import wm  # noqa: E402
look = np.random.default_rng(1).normal(0, 1, ws.LOOK)
n1, n2 = wn.Net(3, 32, True), wn.Net(3, 32, True)
r1, r2 = np.random.default_rng(5), np.random.default_rng(5)
same = True
for _ in range(30):
    same = same and wf.try_box(n1, look, [(1, 2), (0, 3)], [], r1, True) == wm.try_box(n2, look, [(1, 2), (0, 3)], [], r2, True)
check("wf.try_box = wm.try_box without extras", same and np.array_equal(n1.p["M"], n2.p["M"]))

# 3. forcing: forced pairs are done
net = wn.Net(4, 32, True)
op, ch = wf.try_box(net, look, [(1, 2), (0, 3)], [], None, False, force={0: (1, 2), 1: (0, 3)})
check("forced pairs are done (both lids open)", op == 2 and ch == [[1, 2], [0, 3]])

# 4. store sense
store = {(2, 1): ((3, 0), True)}
check("FM sense of a fresh (3, 0)", list(wf.fm_sense(store, 2, 1)) == [0, 0, 0, 1, 1, 0, 0, 0, 1])
check("FM sense empty is zeros", not wf.fm_sense(store, 2, 0).any())

# 5. new arms run; replay happens; WSLS relearns in the moment (food above TBYS); same child twice
res = {a: wf.run_child(a, 32, 1002) for a in ("RP", "FMin", "WSLS")}
check(f"RP replays ({res['RP']['replays']})", res["RP"]["replays"] > 0)
check("same child twice is the same (WSLS)", wf.run_child("WSLS", 32, 1002) == res["WSLS"])
check("FMin runs a full life with its 9 extra senses", sorted(res["FMin"]["tests"]) == [30, 33, 38, 45, 48, 53, 60])
print("All: PASS" if not fails else f"FAILED: {fails}")
