"""WG analysis (descriptive; questions.md). Means over 48 seeds with 95% bootstrap intervals (numpy seed 20261115,
10,000 resamples of seeds; paired differences resample seeds once for both brains). Writes analysis.md and .json."""
import json
from pathlib import Path

import numpy as np

HERE = Path(__file__).parent
BRAINS = ("M16", "M32", "M128", "G", "GA", "GF", "GA32")
SEEDS, DAYS, B = range(1, 49), (7, 15, 30, 60), 10_000
R = {b: [json.loads((HERE / "output" / f"{b}_seed_{s}.json").read_text()) for s in SEEDS] for b in BRAINS}
IDX = np.random.default_rng(20261115).integers(0, len(SEEDS), (B, len(SEEDS)))


def ci(v):
    v = np.asarray(v, float)
    m = v[IDX].mean(axis=1)
    return [round(float(v.mean()), 3), round(float(np.percentile(m, 2.5)), 3), round(float(np.percentile(m, 97.5)), 3)]


def skill(b, d):
    return np.array([r["tests"][str(d)]["success"] for r in R[b]])


def shown(b):
    return np.array([r["show_tests"]["30"]["success"] for r in R[b]])


out = {"n_children_per_brain": len(SEEDS), "skill": {}, "after_showing_30": {}, "out_weight_day60": {}, "diffs": {}}
for b in BRAINS:
    out["skill"][b] = {d: ci(skill(b, d)) for d in DAYS}
    out["after_showing_30"][b] = ci(shown(b))
    if b in ("G", "GA", "GF", "GA32"):
        born = [r["out_weight_day60"]["born"] for r in R[b]]
        added = [r["out_weight_day60"]["added"] for r in R[b]]
        out["out_weight_day60"][b] = {"born": ci(born), "added": ci(added),
                                      "added_over_born": ci(np.array(added) / np.array(born))}
for a, c in (("GA", "G"), ("GF", "G"), ("GA", "M128"), ("GF", "M128"), ("GA32", "M32")):
    for d in (30, 60):
        out["diffs"][f"{a}-{c} day {d}"] = ci(skill(a, d) - skill(c, d))
    out["diffs"][f"{a}-{c} after showing 30"] = ci(shown(a) - shown(c))

(HERE / "analysis.json").write_text(json.dumps(out, indent=1), encoding="utf-8")
f = lambda t: f"{t[0]:.3f} [{t[1]:.3f}, {t[2]:.3f}]"
L = ["# WG analysis (from analyse_wg.py; 48 children per brain; mean [95% bootstrap interval])", "",
     "| brain | day 7 | day 15 | day 30 | day 60 | after a showing, day 30 |", "|---|---|---|---|---|---|"]
for b in BRAINS:
    s = out["skill"][b]
    L.append(f"| {b} | " + " | ".join(f(s[d]) for d in DAYS) + f" | {f(out['after_showing_30'][b])} |")
L += ["", "Manipulation check: mean |outgoing weight to the hands| at day 60", "",
      "| brain | born neurons | added neurons | added / born |", "|---|---|---|---|"]
for b, u in out["out_weight_day60"].items():
    L.append(f"| {b} | {f(u['born'])} | {f(u['added'])} | {f(u['added_over_born'])} |")
L += ["", "| paired difference | mean [95% interval] |", "|---|---|"]
L += [f"| {k} | {f(v)} |" for k, v in out["diffs"].items()]
(HERE / "analysis.md").write_text("\n".join(L) + "\n", encoding="utf-8")
print("\n".join(L))
