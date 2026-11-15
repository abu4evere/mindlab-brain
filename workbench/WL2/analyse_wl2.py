"""WL2 analysis (descriptive; questions.md). 95% bootstrap intervals over 48 seeds (numpy seed 20261123, 10,000
resamples; paired by seed). Writes analysis.md and analysis.json."""
import json
import sys
from pathlib import Path

import numpy as np

sys.stdout.reconfigure(encoding="utf-8")
HERE = Path(__file__).parent
ARMS, SIZES, SEEDS, B = ("L0", "L2", "W8", "NS", "NP", "Linf"), (32, 128), range(1, 49), 10_000
IDX = np.random.default_rng(20261123).integers(0, len(SEEDS), (B, len(SEEDS)))
R = {(a, n): [json.loads((HERE / "output" / f"{a}_{n}_seed_{s}.json").read_text()) for s in SEEDS] for a in ARMS for n in SIZES}
KEYS = {"day 7": lambda r: r["tests"]["7"], "day 15": lambda r: r["tests"]["15"], "day 30": lambda r: r["tests"]["30"],
        "day 60": lambda r: r["tests"]["60"], "after showing 30": lambda r: r["show30"], "food": lambda r: r["food"]}


def ci(v):
    v = np.asarray(v, float)
    m = v[IDX].mean(axis=1)
    return [round(float(v.mean()), 3), round(float(np.percentile(m, 2.5)), 3), round(float(np.percentile(m, 97.5)), 3)]


def vals(a, n, k):
    return np.array([KEYS[k](r) for r in R[(a, n)]], float)


f = lambda t: f"{t[0]:.3f} [{t[1]:.3f}, {t[2]:.3f}]"
out = {"means": {}, "diffs": {}, "carries": {}}
L = ["# WL2 analysis (from analyse_wl2.py; 48 children per cell; means)", "",
     "| arm | size | " + " | ".join(KEYS) + " |", "|---|---|" + "---|" * len(KEYS)]
for n in SIZES:
    for a in ARMS:
        out["means"][f"{a}-{n}"] = {k: ci(vals(a, n, k)) for k in KEYS}
        L.append(f"| {a} | {n} | " + " | ".join(
            (f"{out['means'][f'{a}-{n}'][k][0]:.0f}" if k == "food" else f"{out['means'][f'{a}-{n}'][k][0]:.3f}") for k in KEYS) + " |")
L += ["", "| paired difference | day 30 | day 60 | after showing 30 |", "|---|---|---|---|"]
for n in SIZES:
    for ref in ("L0", "L2"):
        for a in ARMS:
            if a == ref or (ref == "L2" and a == "L0"):
                continue
            d = {k: ci(vals(a, n, k) - vals(ref, n, k)) for k in ("day 30", "day 60", "after showing 30")}
            out["diffs"][f"{a}-{n} − {ref}-{n}"] = d
            L.append(f"| {a}-{n} − {ref}-{n} | " + " | ".join(f(d[k]) for k in ("day 30", "day 60", "after showing 30")) + " |")
L += ["", "Carries the effect (arm's day-30 gain over L0 at least half of L2's gain, same size):", ""]
for n in SIZES:
    g2 = float((vals("L2", n, "day 30") - vals("L0", n, "day 30")).mean())
    for a in ("W8", "NS", "NP", "Linf"):
        g = float((vals(a, n, "day 30") - vals("L0", n, "day 30")).mean())
        out["carries"][f"{a}-{n}"] = {"gain": round(g, 3), "L2_gain": round(g2, 3), "share": round(g / g2, 3) if g2 else None}
        L.append(f"- {a}-{n}: gain {g:+.3f} of L2's {g2:+.3f} (share {g / g2:.2f}) -> {'carries' if g >= g2 / 2 else 'does not carry'}")
(HERE / "analysis.json").write_text(json.dumps(out, indent=1), encoding="utf-8")
(HERE / "analysis.md").write_text("\n".join(L) + "\n", encoding="utf-8")
print("\n".join(L))
