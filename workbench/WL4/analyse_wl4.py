"""WL4 analysis (descriptive; questions.md). 95% bootstrap intervals over 24 seeds (numpy seed 20261128, 10,000
resamples; paired by seed). Writes analysis.md and analysis.json."""
import json
import sys
from pathlib import Path

import numpy as np

sys.stdout.reconfigure(encoding="utf-8")
HERE = Path(__file__).parent
WORLDS, ARMS, SIZES, SEEDS, B = ("RULE", "RAND"), ("L0", "L2", "Linf"), (32, 128), range(1, 25), 10_000
IDX = np.random.default_rng(20261128).integers(0, len(SEEDS), (B, len(SEEDS)))
R = {(w, a, n): [json.loads((HERE / "output" / f"{w}_{a}_{n}_seed_{s}.json").read_text()) for s in SEEDS]
     for w in WORLDS for a in ARMS for n in SIZES}


def ci(v):
    v = np.asarray(v, float)
    m = v[IDX].mean(axis=1)
    return [round(float(v.mean()), 3), round(float(np.percentile(m, 2.5)), 3), round(float(np.percentile(m, 97.5)), 3)]


def vals(w, a, n, g, d):
    return np.array([r["tests"][str(d)][g] for r in R[(w, a, n)]], float)


f = lambda t: f"{t[0]:.3f} [{t[1]:.3f}, {t[2]:.3f}]"
out = {"means": {}, "diffs": {}}
cols = [(g, d) for g in ("practised", "heldout") for d in (15, 30, 60)]
L = ["# WL4 analysis (from analyse_wl4.py; 24 children per cell; means)", "",
     "| world | arm | size | " + " | ".join(f"{g} d{d}" for g, d in cols) + " | food |", "|---|---|---|" + "---|" * (len(cols) + 1)]
for w in WORLDS:
    for n in SIZES:
        for a in ARMS:
            m = {f"{g}@{d}": ci(vals(w, a, n, g, d)) for g, d in cols}
            m["food"] = ci([r["food"] for r in R[(w, a, n)]])
            out["means"][f"{w}-{a}-{n}"] = m
            L.append(f"| {w} | {a} | {n} | " + " | ".join(f"{m[f'{g}@{d}'][0]:.3f}" for g, d in cols) + f" | {m['food'][0]:.0f} |")
L += ["", "| paired difference | practised d30 | practised d60 | held-out d30 | held-out d60 |", "|---|---|---|---|---|"]
for w in WORLDS:
    for n in SIZES:
        for a in ("Linf", "L2"):
            d = {f"{g}@{dd}": ci(vals(w, a, n, g, dd) - vals(w, "L0", n, g, dd)) for g in ("practised", "heldout") for dd in (30, 60)}
            out["diffs"][f"{w} {a}-{n} − L0-{n}"] = d
            L.append(f"| {w} {a}-{n} − L0-{n} | " + " | ".join(f(d[k]) for k in ("practised@30", "practised@60", "heldout@30", "heldout@60")) + " |")
L += ["", "| RULE − RAND, held-out d60 | mean [95% interval] |", "|---|---|"]
for n in SIZES:
    for a in ARMS:
        d = ci(vals("RULE", a, n, "heldout", 60) - vals("RAND", a, n, "heldout", 60))
        out["diffs"][f"RULE-RAND heldout60 {a}-{n}"] = d
        L.append(f"| {a}-{n} | {f(d)} |")
(HERE / "analysis.json").write_text(json.dumps(out, indent=1), encoding="utf-8")
(HERE / "analysis.md").write_text("\n".join(L) + "\n", encoding="utf-8")
print("\n".join(L))
