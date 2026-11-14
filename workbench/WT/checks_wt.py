"""WT checks, before any data. Prints All: PASS or the failures."""
import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).parent))
import wt  # noqa: E402
import we  # noqa: E402

fails = []


def check(name, ok):
    print(("PASS " if ok else "FAIL ") + name, flush=True)
    if not ok:
        fails.append(name)


GA = (16, {8: 32, 16: 64, 24: 128})
# 1. p = 1 is WE exactly
a, b = wt.run_child(*GA, 3, 1.0, tests=True), we.run_child(*GA, 3, tests=True)
check("p = 1 reproduces WE's child (food, tests)", a["food"] == b["food"] and a["tests"] == b["tests"]
      and a["show_tests"] == b["show_tests"] and a["shows"] == 540)
# 2. p = 0: no showings at all
check("p = 0: no showings", wt.run_child(32, {}, 3, 0.0)["shows"] == 0)
# 3. presence rate and sameness across brains
rate = np.mean([wt.present(s, d, 0.2).mean() for s in range(1, 41) for d in range(1, 31)])
check(f"p = 0.2 presence rate about 0.2 ({rate:.3f})", 0.18 < rate < 0.22)
check("the same world gives the same absences to every brain",
      wt.run_child(8, {}, 5, 0.5)["shows"] == wt.run_child(64, {3: 128}, 5, 0.5)["shows"])
r = wt.run_child(16, {}, 5, 0.5)
check(f"p = 0.5 shows over 30 days about 270 ({r['shows']})", 230 < r["shows"] < 310)
# 4. the same child twice
check("same child twice is the same", wt.run_child(16, {4: 24}, 9, 0.2) == wt.run_child(16, {4: 24}, 9, 0.2))

print("All: PASS" if not fails else f"FAILED: {fails}")
