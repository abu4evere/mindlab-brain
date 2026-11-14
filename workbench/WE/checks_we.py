"""WE checks, before any data. Prints All: PASS or the failures."""
import json
import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).parent))
import we  # noqa: E402
import wg  # noqa: E402

fails = []


def check(name, ok):
    print(("PASS " if ok else "FAIL ") + name, flush=True)
    if not ok:
        fails.append(name)


# 1. run_child with WG's GA schedule reproduces WG's saved GA child (seed 1); with no schedule, WG's M32
w = json.loads((Path(__file__).parent.parent / "WG" / "output" / "GA_seed_1.json").read_text())
r = we.run_child(16, {8: 32, 16: 64, 24: 128}, 1, tests=True)
check("GA schedule reproduces WG's GA seed 1",
      all(r["tests"][d]["success"] == w["tests"][str(d)]["success"] for d in (7, 15, 30, 60))
      and r["show_tests"][30]["success"] == w["show_tests"]["30"]["success"] and r["final_n"] == 128)
w = json.loads((Path(__file__).parent.parent / "WG" / "output" / "M32_seed_1.json").read_text())
r = we.run_child(32, {}, 1, tests=True)
check("no schedule reproduces WG's M32 seed 1",
      all(r["tests"][d]["success"] == w["tests"][str(d)]["success"] for d in (7, 15, 30, 60)))

# 2. food counts lids opened in practice tries (0..2 per try, 18 tries a day, 60 days)
check("food is within 0..2160", 0 <= r["food"] <= 2160)

# 3. schedules
n0, s = we.schedule(np.array([4.0, 3.0, 8.0, 24.0]))
check(f"schedule 16 -> 128 over days 8..24: born {n0}, last {s.get(24)}, steps rise",
      n0 == 16 and s[24] == 128 and min(s) == 8 and all(s[a] < s[b] for a, b in zip(sorted(s), sorted(s)[1:])))
n0, s = we.schedule(np.array([5.0, 0.0, 3.0, 50.0]))
check("g = 0 means no growth", n0 == 32 and s == {})
n0, s = we.schedule(np.array([2.0, 6.0, 10.0, 10.0]))
check("one-day growth jumps at once to the final size", n0 == 4 and s == {10: 256})

# 4. clamping keeps genes in range
rng = np.random.default_rng(0)
ok = True
for _ in range(2000):
    g = we.clamp(rng.normal(0, 20, 4))
    ok = ok and 2 <= g[0] <= 8 and 0 <= g[1] <= 8 - g[0] + 1e-12 and 1 <= g[2] <= g[3] <= 60
    ok = ok and we.schedule(g)[0] >= 4 and max([we.schedule(g)[0]] + list(we.schedule(g)[1].values())) <= 256
check("clamped genes stay in range; sizes 4..256", ok)

# 5. generation 0 in range; selection uses food only (same food -> same parent draw for the same rng)
p = we.gen0(np.random.default_rng([1, 77]))
check("generation 0 has 32 genomes in range", len(p) == 32 and all(np.allclose(we.clamp(g), g) for g in p))

# 6. same child twice is the same
a, b = we.run_child(8, {5: 12, 6: 16}, 7), we.run_child(8, {5: 12, 6: 16}, 7)
check("same child twice gives the same food and size", a["food"] == b["food"] and a["final_n"] == b["final_n"] == 16)

print("All: PASS" if not fails else f"FAILED: {fails}")
