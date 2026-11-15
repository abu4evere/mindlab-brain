"""WC checks, before any data. Prints All: PASS or the failures."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
import wc  # noqa: E402
import we  # noqa: E402
import wt  # noqa: E402
import ws  # noqa: E402

fails = []


def check(name, ok):
    print(("PASS " if ok else "FAIL ") + name, flush=True)
    if not ok:
        fails.append(name)


GA = (16, {8: 32, 16: 64, 24: 128})
# 1. with no change, WC is WT (p = 0.5) and WE (p = 1) exactly
check("no change, p = 0.5 reproduces WT's child food",
      wc.run_child(*GA, 3, change=False)["food"] == wt.run_child(*GA, 3, 0.5)["food"])
check("no change, p = 1 reproduces WE's child food",
      wc.run_child(32, {}, 4, p=1.0, change=False)["food"] == we.run_child(32, {}, 4)["food"])

# 2. the new codes
ok = True
for s in range(1, 200):
    h = ws.Home(s)
    nc = wc.new_codes(h, s)
    for k in range(ws.KINDS):
        ok = ok and nc[k][0] != nc[k][1] and all(nc[k][j] != tuple(h.pairs[k][j]) for j in range(2))
        ok = ok and all(0 <= a < 4 and 0 <= b < 4 for a, b in nc[k])
check("new codes differ from the old on every lid; a kind's two lids differ", ok)
check("new codes are the same each time for a world", wc.new_codes(ws.Home(9), 9) == wc.new_codes(ws.Home(9), 9))

# 3. the codes switch: group A and B end on their new codes
r = wc.run_child(16, {}, 5, tests=True)
nc = wc.new_codes(ws.Home(5), 5)
check("by day 60 every kind runs on its new code", r["final_pairs"] == [list(map(list, pr)) for pr in nc])
t = r["tests"]
check("stale habit measured only on changed kinds",
      all(v is None for v in t[30]["stale"]) and t[33]["stale"][:3] != [None] * 3 and t[33]["stale"][3:] == [None] * 3
      and all(v is not None for v in t[48]["stale"]))
check("tests at days 30, 33, 38, 45, 48, 53, 60", sorted(t) == [30, 33, 38, 45, 48, 53, 60])
# 4. same child twice
check("same child twice is the same", wc.run_child(8, {3: 16}, 6, tests=True) == wc.run_child(8, {3: 16}, 6, tests=True))
print("All: PASS" if not fails else f"FAILED: {fails}")
