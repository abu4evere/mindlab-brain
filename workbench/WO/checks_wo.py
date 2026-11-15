"""WO checks, before any data. Prints All: PASS or the failures."""
import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).parent))
import wo  # noqa: E402
import ws  # noqa: E402

fails = []


def check(name, ok):
    print(("PASS " if ok else "FAIL ") + name, flush=True)
    if not ok:
        fails.append(name)


looks, codes = wo.boxes(3)
check("60 kinds, each with 2 different lid codes in range",
      len(codes) == 60 and all(c[0] != c[1] and all(0 <= a < 4 and 0 <= b < 4 for a, b in c) for c in codes))
check("kinds of day 1 are 0,1; day 30 are 58,59; day 0 and 31 none",
      wo.kinds_of(1) == [0, 1] and wo.kinds_of(30) == [58, 59] and wo.kinds_of(0) == [] and wo.kinds_of(31) == [])
r = wo.run_child("L0", 32, 2)
check("every kind gets an immediate test (60)", sorted(r["immediate"]) == list(range(60)))
check("retention 1 day for kinds of days 1-29 (58); 7 days for days 1-23 (46)",
      len(r["retain1"]) == 58 and len(r["retain7"]) == 46)
ma = (30 * 2 * 3) * 2 + sum(len(wo.kinds_of(d - a)) for d in range(1, 31) for a in wo.REVIEW_AGO) * 2
check(f"food within its maximum ({r['food']} <= {ma})", 0 <= r["food"] <= ma)
check("same child twice is the same", wo.run_child("L2", 32, 4) == wo.run_child("L2", 32, 4))
a, b, c = (wo.run_child(x, 32, 5) for x in wo.ARMS)
check("the three arms give different lives", len({a["food"], b["food"], c["food"]}) == 3)
print("All: PASS" if not fails else f"FAILED: {fails}")
