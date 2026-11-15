"""WL3 checks, before any data. Prints All: PASS or the failures."""
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
import wl3  # noqa: E402
import ws  # noqa: E402

fails = []


def check(name, ok):
    print(("PASS " if ok else "FAIL ") + name, flush=True)
    if not ok:
        fails.append(name)


WL2O = Path(__file__).parent.parent / "WL2" / "output"
for arm in ("L0", "Linf"):
    a = wl3.run_child("K6L2", arm, 32, 1)
    b = json.loads((WL2O / f"{arm}_32_seed_1.json").read_text())
    check(f"K6L2 {arm}-32 reproduces WL2", a["food"] == b["food"] and a["tests"] == {int(k): v for k, v in b["tests"].items()})
wl3.set_world("K24L2")
h = ws.Home(3)
check("K24L2: 24 kinds, 2 lids each, 72 tries a day", len(h.pairs) == 24 and all(len(p) == 2 for p in h.pairs) and len(h.day(1)) == 72)
wl3.set_world("K6L3")
h = ws.Home(3)
check("K6L3: 6 kinds, 3 different lids each", all(len(p) == 3 and len(set(p)) == 3 for p in h.pairs))
check("K6L3: a showing has 6 steps", len(ws.show_steps(h.looks[0], h.pairs[0])) == 6)
r = wl3.run_child("K6L3", "L2", 32, 2)
check("K6L3 child runs; tests at 7, 15, 30, 60", sorted(r["tests"]) == [7, 15, 30, 60])
check("same child twice is the same", wl3.run_child("K24L2", "Linf", 32, 2) == wl3.run_child("K24L2", "Linf", 32, 2))
wl3.set_world("K6L2")
print("All: PASS" if not fails else f"FAILED: {fails}")
