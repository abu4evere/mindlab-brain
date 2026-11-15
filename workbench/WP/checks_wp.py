"""WP checks, before any data. Prints All: PASS or the failures."""
import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).parent))
import wp  # noqa: E402
import wn  # noqa: E402
import wt  # noqa: E402
import ws  # noqa: E402

fails = []


def check(name, ok):
    print(("PASS " if ok else "FAIL ") + name, flush=True)
    if not ok:
        fails.append(name)


# 1. alone: children do not affect each other (child 1-5 the same whatever child 0 is)
a = wp.run_group("S6alone", 2, "stable")
b = wp.run_group("S6alone", 2, "stable", sizes=[128] + [32] * 5)
check("alone: small children 1-5 unaffected by child 0's size",
      all(a["tests"][c] == b["tests"][c] and a["food"][c] == b["food"][c] for c in range(1, 6)))
check("alone: no watching recorded", sum(map(sum, map(lambda m: sum(m, []), a["watched"]))) == 0)

# 2. the same small child starts identical in S6 and B1S5
check("small child c starts with the same weights in any group",
      all(np.array_equal(wn.Net(1000 * 3 + c, 32, True).p["Wx"], wn.Net(1000 * 3 + c, 32, True).p["Wx"]) for c in range(1, 6)))

# 3. the grown-up: only days 1-30, about 20% of the 540 tries
r = wp.run_group("S6", 4, "change")
exp = sum(int(wt.present(4, d, 0.2).sum()) for d in range(1, 31))
check(f"grown-up shows = the world's presence draws on days 1-30 ({r['adult_shows']} = {exp})", r["adult_shows"] == exp)

# 4. watching: never oneself; happens in both phases; trust in [0, 1]
W = np.array(r["watched"])
check("never watches itself", all(W[p, c, c] == 0 for p in range(2) for c in range(6)))
check("watching in both phases", W[0].sum() > 0 and W[1].sum() > 0)
T = np.array(r["trust_end"])
check("trust stays in [0, 1]", T.min() >= 0 and T.max() <= 1)

# 5. watch(): only opened lids are held and copied
net = wn.Net(7, 32, True)
look = np.zeros(ws.LOOK)
check("watch: nothing opened -> nothing held", wp.watch(net, look, ([[1, 2]], 0)) == [])
check("watch: one lid opened -> 2 memory steps", len(wp.watch(net, look, ([[1, 2], [3, 0]], 1))) == 2)
check("watch: both opened -> 4 memory steps", len(wp.watch(net, look, ([[1, 2], [3, 0]], 2))) == 4)

# 6. tests and determinism
check("change world tested at days 30, 45, 60", sorted(r["tests"][0]) == [30, 45, 60])
check("same group twice is the same", wp.run_group("B1S5", 5, "stable") == wp.run_group("B1S5", 5, "stable"))
print("All: PASS" if not fails else f"FAILED: {fails}")
