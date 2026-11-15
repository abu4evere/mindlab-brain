"""WL4 checks, before any data. Prints All: PASS or the failures."""
import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).parent))
import wl4  # noqa: E402
import ws  # noqa: E402

fails = []


def check(name, ok):
    print(("PASS " if ok else "FAIL ") + name, flush=True)
    if not ok:
        fails.append(name)


look = np.zeros(16)
look[[2, 5, 8, 15]] = 1.0
check("rule code from arg-maxes", wl4.rule_code(look) == [(2, 1), (0, 3)])
h, g = wl4.Home(3, "RULE"), wl4.Home(3, "RAND")
check("same looks in both worlds", np.array_equal(h.looks, g.looks))
check("RULE codes follow the looks", all(h.pairs[k] == wl4.rule_code(h.looks[k]) for k in range(30)))
check("RAND codes: 2 different pairs per kind", all(len(p) == 2 and p[0] != p[1] for p in g.pairs))
d = h.day(1)
check("a day: 72 tries on the 24 practised kinds only", len(d) == 72 and max(k for k, _ in d) == 23)
r = wl4.run_child("RULE", "Linf", 32, 2)
check("tests at 15, 30, 60 with practised and held-out shares",
      sorted(r["tests"]) == [15, 30, 60] and set(r["tests"][15]) == {"practised", "heldout"})
check("same child twice is the same", wl4.run_child("RAND", "L2", 32, 2) == wl4.run_child("RAND", "L2", 32, 2))
# how often would a rule code differ between noisy encounters? (the noise rarely flips an arg-max)
rng = np.random.default_rng(0)
flips = np.mean([wl4.rule_code(h.looks[k]) != wl4.rule_code(h.looks[k] + rng.normal(0, 0.2, 16)) for k in range(30) for _ in range(20)])
print(f"INFO share of noisy encounters whose look's arg-max code differs from the kind's code: {flips:.3f}")
print("All: PASS" if not fails else f"FAILED: {fails}")
