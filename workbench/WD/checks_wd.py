"""WD checks, before any data. Prints All: PASS or the failures."""
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
import wd  # noqa: E402

fails = []


def check(name, ok):
    print(("PASS " if ok else "FAIL ") + name, flush=True)
    if not ok:
        fails.append(name)


# 1. with no bad kinds, Naive is WR's recipe: day-30 test equals WR's change-world LTYR (identical up to day 30)
wd.BAD = ()
a = wd.run_child("Naive", 32, 1001)
b = json.loads((Path(__file__).parent.parent / "WR" / "output" / "change_LTYR_32_seed_1001.json").read_text())
check("no bad kinds: Naive = WR's LTYR at day 30 (seed 1001, size 32)", a["tests"][30]["success"] == b["tests"]["30"]["success"])
wd.BAD = (0, 1, 2)

# 2. trust outcomes
check("same pair, opened -> 1", wd.trust_updates([[1, 2]], 1, [(1, 2), (0, 0)]) == [1.0])
check("same pair, failed -> 0", wd.trust_updates([[1, 2]], 0, [(1, 2), (0, 0)]) == [0.0])
check("different pair, opened -> 0", wd.trust_updates([[3, 3], [0, 1]], 1, [(1, 2), (0, 1)]) == [0.0, 0.0])
check("different pair, failed -> no update", wd.trust_updates([[3, 3]], 0, [(1, 2), (0, 0)]) == [])

# 3. pilot seed 901 (outside the study): trust moves the right way; the arms run; the same child twice
d = wd.run_child("Doubt", 32, 901)
t = d["trust30"]
check(f"pilot: trust at day 30 lower on bad kinds than good ({[round(x, 2) for x in t]})", max(t[:3]) < min(t[3:]) or sum(t[:3]) < sum(t[3:]))
check("same child twice is the same", wd.run_child("Alone", 32, 902) == wd.run_child("Alone", 32, 902))
check("Alone never trusts-updates (trust stays 1.0)", wd.run_child("Alone", 32, 903)["trust30"] == [1.0] * 6)
print("All: PASS" if not fails else f"FAILED: {fails}")
