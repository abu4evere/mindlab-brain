"""WN analysis (descriptive; questions.md). Means over the 24 seeds with 95% bootstrap intervals (numpy seed 20261114,
10,000 resamples of seeds; paired differences resample seeds once for both brains). Writes analysis.md and .json."""
import json
from pathlib import Path

import numpy as np

HERE = Path(__file__).parent
BRAINS = ("M8", "M16", "M32", "M64", "M128", "M256", "F8", "F32", "F128", "G")
SEEDS, DAYS, B = range(1, 25), (7, 15, 30, 60), 10_000
R = {b: [json.loads((HERE / "output" / f"{b}_seed_{s}.json").read_text()) for s in SEEDS] for b in BRAINS}
rng = np.random.default_rng(20261114)
IDX = rng.integers(0, len(SEEDS), (B, len(SEEDS)))


def ci(v):
    v = np.asarray(v, float)
    m = v[IDX].mean(axis=1)
    return [round(float(v.mean()), 3), round(float(np.percentile(m, 2.5)), 3), round(float(np.percentile(m, 97.5)), 3)]


def skill(b, d):
    return [r["tests"][str(d)]["success"] for r in R[b]]


out = {"n_children_per_brain": len(SEEDS), "skill": {}, "after_showing_30": {}, "cpu_secs": {}, "diffs": {}}
for b in BRAINS:
    out["skill"][b] = {d: ci(skill(b, d)) for d in DAYS}
    out["after_showing_30"][b] = ci([r["show_tests"]["30"]["success"] for r in R[b]])
    out["cpu_secs"][b] = round(float(np.mean([r["cpu_secs"] for r in R[b]])), 2)
pairs = [("G", "M128"), ("G", "M16"), ("M8", "F8"), ("M32", "F32"), ("M128", "F128")]
for a, c in pairs:
    for d in (30, 60):
        out["diffs"][f"{a}-{c} day {d}"] = ci(np.array(skill(a, d)) - np.array(skill(c, d)))
    out["diffs"][f"{a}-{c} after showing 30"] = ci(
        np.array([r["show_tests"]["30"]["success"] for r in R[a]]) -
        np.array([r["show_tests"]["30"]["success"] for r in R[c]]))

(HERE / "analysis.json").write_text(json.dumps(out, indent=1), encoding="utf-8")
L = ["# WN analysis (from analyse_wn.py; 24 children per brain; mean [95% bootstrap interval])", "",
     "| brain | day 7 | day 15 | day 30 | day 60 | after a showing, day 30 | CPU s per child |", "|---|---|---|---|---|---|---|"]
f = lambda t: f"{t[0]:.3f} [{t[1]:.3f}, {t[2]:.3f}]"
for b in BRAINS:
    s = out["skill"][b]
    L.append(f"| {b} | " + " | ".join(f(s[d]) for d in DAYS) + f" | {f(out['after_showing_30'][b])} | {out['cpu_secs'][b]} |")
L += ["", "| paired difference | mean [95% interval] |", "|---|---|"]
L += [f"| {k} | {f(v)} |" for k, v in out["diffs"].items()]
(HERE / "analysis.md").write_text("\n".join(L) + "\n", encoding="utf-8")
print("\n".join(L))
