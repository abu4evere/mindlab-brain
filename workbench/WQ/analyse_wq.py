"""WQ analysis (descriptive; questions.md). Per seed: the mean over its 3 stays; intervals: bootstrap over the 8 seeds
(numpy seed 20261131, 10,000 resamples; paired by seed). Script is deterministic (one run, no interval)."""
import json
import sys
from pathlib import Path

import numpy as np

sys.stdout.reconfigure(encoding="utf-8")
HERE = Path(__file__).parent
OUT = HERE / "output"
IDX = np.random.default_rng(20261131).integers(0, 8, (10_000, 8))
CELLS = [("D2", "still"), ("D2", "living"), ("D3", "still"), ("D3", "living"), ("Dc", "still"), ("Dc", "living"),
         ("GYFR", "still"), ("GYFR", "living"), ("Rand", "still")]
MEAS = ("activity", "reach", "pattern", "curiosity")


def ci(v):
    v = np.asarray(v, float)
    m = v[IDX].mean(axis=1)
    return [round(float(v.mean()), 3), round(float(np.percentile(m, 2.5)), 3), round(float(np.percentile(m, 97.5)), 3)]


def seedvals(b, mode, w, key):
    out = []
    for s in range(1, 9):
        r = json.loads((OUT / f"{b}_{mode}_{s}.json").read_text())
        out.append(np.mean([st["windows"][w][key] for st in r["stays"]]))
    return np.array(out)


f = lambda t: f"{t[0]:.3f} [{t[1]:.3f}, {t[2]:.3f}]"
res = {"cells": {}, "diffs": {}}
L = ["# WQ analysis (from analyse_wq.py; 8 seeds x 3 stays of 10,000 steps; mean [95% interval])", "",
     "| brain | mode | activity w1 | activity w10 | reach w10 | pattern w10 | curiosity w10 |", "|---|---|---|---|---|---|---|"]
for b, mode in CELLS:
    c = {k: {w: ci(seedvals(b, mode, w, k)) for w in (0, 9)} for k in MEAS}
    res["cells"][f"{b}-{mode}"] = c
    L.append(f"| {b} | {mode} | {f(c['activity'][0])} | {f(c['activity'][9])} | {c['reach'][9][0]:.1f} | "
             f"{f(c['pattern'][9])} | {c['curiosity'][9][0]:.0f} |")
sc = json.loads((OUT / "Script_still_1.json").read_text())
sw = {k: [float(np.mean([st["windows"][w][k] for st in sc["stays"]])) for w in range(10)] for k in MEAS}
res["script"] = sw
L.append(f"| Script | rule | {sw['activity'][0]:.3f} | {sw['activity'][9]:.3f} | {sw['reach'][9]:.1f} | {sw['pattern'][9]:.3f} | {sw['curiosity'][9]:.0f} |")
L += ["", "| paired difference | activity w10 | reach w10 | pattern w10 |", "|---|---|---|---|"]
pairs = [(("D3", "still"), ("D2", "still")), (("Dc", "still"), ("D2", "still")), (("GYFR", "still"), ("D2", "still")),
         (("D3", "still"), ("Rand", "still")), (("Dc", "still"), ("Rand", "still")), (("D2", "still"), ("Rand", "still"))]
pairs += [((b, "living"), (b, "still")) for b in ("D2", "D3", "Dc", "GYFR")]
pairs += [((b, "still"), (b, "still")) for b in ()]
for a, c in pairs:
    d = {k: ci(seedvals(*a, 9, k) - seedvals(*c, 9, k)) for k in ("activity", "reach", "pattern")}
    res["diffs"][f"{a[0]}-{a[1]} − {c[0]}-{c[1]}"] = d
    L.append(f"| {a[0]} {a[1]} − {c[0]} {c[1]} | {f(d['activity'])} | {f(d['reach'])} | {f(d['pattern'])} |")
L += ["", "Activity falls from window 1 to window 10 (w10 − w1, paired):", ""]
for b, mode in CELLS:
    d = ci(seedvals(b, mode, 9, "activity") - seedvals(b, mode, 0, "activity"))
    res["diffs"][f"{b}-{mode} w10-w1 activity"] = d
    L.append(f"- {b} {mode}: {f(d)}")
(HERE / "analysis.json").write_text(json.dumps(res, indent=1), encoding="utf-8")
(HERE / "analysis.md").write_text("\n".join(L) + "\n", encoding="utf-8")
print("\n".join(L))
