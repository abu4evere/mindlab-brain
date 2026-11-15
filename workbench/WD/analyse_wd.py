"""WD analysis (descriptive; questions.md). 95% bootstrap intervals over 48 seeds (numpy seed 20261127, 10,000
resamples; paired by seed). Writes analysis.md and analysis.json."""
import json
import sys
from pathlib import Path

import numpy as np

sys.stdout.reconfigure(encoding="utf-8")
HERE = Path(__file__).parent
ARMS, SIZES, SEEDS, B = ("Naive", "Doubt", "Alone"), (32, 128), range(1, 49), 10_000
BAD, GOOD, DAYS = (0, 1, 2), (3, 4, 5), (15, 30, 45, 60)
IDX = np.random.default_rng(20261127).integers(0, len(SEEDS), (B, len(SEEDS)))
R = {(a, n): [json.loads((HERE / "output" / f"{a}_{n}_seed_{s}.json").read_text()) for s in SEEDS] for a in ARMS for n in SIZES}


def ci(v):
    v = np.asarray(v, float)
    m = v[IDX].mean(axis=1)
    return [round(float(v.mean()), 3), round(float(np.percentile(m, 2.5)), 3), round(float(np.percentile(m, 97.5)), 3)]


def val(r, key):
    if key == "food":
        return r["food"]
    g, d = key.split("@")
    d = str(d)
    if g == "believe":
        return float(np.mean([r["tests"][d]["believe"][k] for k in BAD]))
    ks = BAD if g == "bad" else GOOD
    return float(np.mean([r["tests"][d]["success"][k] for k in ks]))


KEYS = [f"bad@{d}" for d in DAYS] + [f"good@{d}" for d in DAYS] + ["believe@15", "believe@30", "believe@60", "food"]
f = lambda t: f"{t[0]:.3f} [{t[1]:.3f}, {t[2]:.3f}]"
out = {"means": {}, "diffs": {}, "trust30": {}}
L = ["# WD analysis (from analyse_wd.py; 48 children per cell; means)", "",
     "| arm | size | " + " | ".join(KEYS) + " |", "|---|---|" + "---|" * len(KEYS)]
for n in SIZES:
    for a in ARMS:
        m = {k: ci([val(r, k) for r in R[(a, n)]]) for k in KEYS}
        out["means"][f"{a}-{n}"] = m
        L.append(f"| {a} | {n} | " + " | ".join((f"{m[k][0]:.0f}" if k == "food" else f"{m[k][0]:.2f}") for k in KEYS) + " |")
L += ["", "Doubt's trust at day 30 (mean over kinds):", ""]
for n in SIZES:
    tb = ci([np.mean(r["trust30"][:3]) for r in R[("Doubt", n)]])
    tg = ci([np.mean(r["trust30"][3:]) for r in R[("Doubt", n)]])
    out["trust30"][n] = {"bad": tb, "good": tg}
    L.append(f"- size {n}: bad kinds {f(tb)}; good kinds {f(tg)}")
L += ["", "| paired difference | bad@30 | bad@60 | good@30 | good@60 | believe@30 |", "|---|---|---|---|---|---|"]
for n in SIZES:
    for a, c in (("Doubt", "Naive"), ("Doubt", "Alone"), ("Naive", "Alone")):
        d = {k: ci(np.array([val(r, k) for r in R[(a, n)]]) - np.array([val(r, k) for r in R[(c, n)]]))
             for k in ("bad@30", "bad@60", "good@30", "good@60", "believe@30")}
        out["diffs"][f"{a}-{n} − {c}-{n}"] = d
        L.append(f"| {a}-{n} − {c}-{n} | " + " | ".join(f(d[k]) for k in ("bad@30", "bad@60", "good@30", "good@60", "believe@30")) + " |")
(HERE / "analysis.json").write_text(json.dumps(out, indent=1), encoding="utf-8")
(HERE / "analysis.md").write_text("\n".join(L) + "\n", encoding="utf-8")
print("\n".join(L))
