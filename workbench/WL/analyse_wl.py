"""WL analysis (descriptive; questions.md). 95% bootstrap intervals over 48 seeds (numpy seed 20261122, 10,000
resamples; paired by seed). Writes analysis.md and analysis.json."""
import json
import sys
from pathlib import Path

import numpy as np

sys.stdout.reconfigure(encoding="utf-8")
HERE = Path(__file__).parent
LEVELS, SIZES, SEEDS, B = ("L0", "L1", "L2"), (32, 128, 256), range(1, 49), 10_000
IDX = np.random.default_rng(20261122).integers(0, len(SEEDS), (B, len(SEEDS)))
R = {(l, n): [json.loads((HERE / "output" / f"{l}_{n}_seed_{s}.json").read_text()) for s in SEEDS]
     for l in LEVELS for n in SIZES}
KEYS = {"day 7": lambda r: r["tests"]["7"], "day 15": lambda r: r["tests"]["15"], "day 30": lambda r: r["tests"]["30"],
        "day 60": lambda r: r["tests"]["60"], "after showing 30": lambda r: r["show30"], "food": lambda r: r["food"]}


def ci(v):
    v = np.asarray(v, float)
    m = v[IDX].mean(axis=1)
    return [round(float(v.mean()), 3), round(float(np.percentile(m, 2.5)), 3), round(float(np.percentile(m, 97.5)), 3)]


def vals(l, n, k):
    return np.array([KEYS[k](r) for r in R[(l, n)]], float)


f = lambda t: f"{t[0]:.3f} [{t[1]:.3f}, {t[2]:.3f}]"
out = {"means": {}, "diffs": {}}
L = ["# WL analysis (from analyse_wl.py; 48 children per cell; mean [95% interval])", "",
     "| level | size | " + " | ".join(KEYS) + " |", "|---|---|" + "---|" * len(KEYS)]
for n in SIZES:
    for l in LEVELS:
        out["means"][f"{l}-{n}"] = {k: ci(vals(l, n, k)) for k in KEYS}
        L.append(f"| {l} | {n} | " + " | ".join(
            (f"{out['means'][f'{l}-{n}'][k][0]:.0f}" if k == "food" else f"{out['means'][f'{l}-{n}'][k][0]:.3f}") for k in KEYS) + " |")
L += ["", "| paired difference | day 30 | day 60 | after showing 30 | food |", "|---|---|---|---|---|"]
pairs = [(("L1", n), ("L0", n)) for n in SIZES] + [(("L2", n), ("L0", n)) for n in SIZES] + \
        [(("L2", 128), ("L0", 32)), (("L2", 256), ("L0", 32)), (("L1", 128), ("L0", 32)), (("L1", 256), ("L0", 32))]
for a, c in pairs:
    d = {k: ci(vals(*a, k) - vals(*c, k)) for k in ("day 30", "day 60", "after showing 30", "food")}
    out["diffs"][f"{a[0]}-{a[1]} − {c[0]}-{c[1]}"] = d
    L.append(f"| {a[0]}-{a[1]} − {c[0]}-{c[1]} | " + " | ".join(f(d[k]) for k in ("day 30", "day 60", "after showing 30", "food")) + " |")
(HERE / "analysis.json").write_text(json.dumps(out, indent=1), encoding="utf-8")
(HERE / "analysis.md").write_text("\n".join(L) + "\n", encoding="utf-8")
print("\n".join(L))
