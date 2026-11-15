"""WC analysis (descriptive; questions.md). Gene paths; the final test with 95% bootstrap intervals over 48 seeds
(numpy seed 20261118, 10,000 resamples; paired differences resample seeds once). Writes analysis.md and .json."""
import json
import sys
from pathlib import Path

import numpy as np

sys.stdout.reconfigure(encoding="utf-8")
HERE = Path(__file__).parent
BRAINS = ("E1", "E2", "T1", "T2", "GA", "M32", "M128", "M256")
SEEDS, B = range(1001, 1049), 10_000
DAYS = (30, 33, 38, 45, 48, 53, 60)
IDX = np.random.default_rng(20261118).integers(0, len(SEEDS), (B, len(SEEDS)))
A, Bk = (0, 1, 2), (3, 4, 5)


def ci(v):
    v = np.asarray(v, float)
    m = v[IDX].mean(axis=1)
    return [round(float(v.mean()), 3), round(float(np.percentile(m, 2.5)), 3), round(float(np.percentile(m, 97.5)), 3)]


f = lambda t: f"{t[0]:.3f} [{t[1]:.3f}, {t[2]:.3f}]"
g = lambda t: f"{t[0]:.2f}"
R = {b: [json.loads((HERE / "output" / f"{b}_seed_{s}.json").read_text()) for s in SEEDS] for b in BRAINS}


def grp(r, d, ks, key="success"):
    return float(np.mean([r["tests"][str(d)][key][k] for k in ks]))


out = {"paths": {}, "evolved": json.loads((HERE / "evolved.json").read_text()), "skill": {}, "stale": {}, "food": {},
       "diffs": {}}
L = ["# WC analysis (from analyse_wc.py)", "", "## Gene paths (population 32; means; born/final medians)", "",
     "| run | gen | mean food | a | g | s | e | born | final |", "|---|---|---|---|---|---|---|---|---|"]
for run in (1, 2):
    out["paths"][run] = []
    for h in json.loads((HERE / f"evo_run{run}.json").read_text()):
        m = np.mean(np.array(h["genes"]), axis=0)
        row = {"gen": h["gen"], "food": float(np.mean(h["food"])), "a": float(m[0]), "g": float(m[1]), "s": float(m[2]),
               "e": float(m[3]), "born": float(np.median(h["born"])), "final": float(np.median(h["final"]))}
        out["paths"][run].append(row)
        if h["gen"] in (0, 4, 9, 14, 19, 24, 29):
            L.append(f"| {run} | {row['gen']} | {row['food']:.0f} | {row['a']:.2f} | {row['g']:.2f} | {row['s']:.1f} | "
                     f"{row['e']:.1f} | {row['born']:.0f} | {row['final']:.0f} |")
L += ["", "## Evolved schedules (median genes of the last generation)", ""]
for k, v in out["evolved"].items():
    L.append(f"- {k}: born {v['born']}, schedule {v['schedule']}, genes {[round(x, 2) for x in v['median_genes']]}")

L += ["", "## Own skill by group and day (means; 48 children each). Group A changes at day 31, group B at day 46.", "",
      "| brain | A30 | A33 | A38 | A45 | A60 | B30 | B45 | B48 | B53 | B60 | food |", "|---|---|---|---|---|---|---|---|---|---|---|---|"]
for b in BRAINS:
    out["skill"][b] = {f"{n}{d}": ci([grp(r, d, ks) for r in R[b]]) for n, ks in (("A", A), ("B", Bk)) for d in DAYS}
    out["food"][b] = ci([r["food"] for r in R[b]])
    s = out["skill"][b]
    L.append(f"| {b} | " + " | ".join(g(s[k]) for k in ("A30", "A33", "A38", "A45", "A60", "B30", "B45", "B48", "B53", "B60"))
             + f" | {out['food'][b][0]:.0f} |")
L += ["", "## Stale habit: share of changed kinds whose first lid still gets the old pair", "",
      "| brain | A33 | A38 | B48 | B53 |", "|---|---|---|---|---|"]
for b in BRAINS:
    out["stale"][b] = {f"A{d}": ci([grp(r, d, A, "stale") for r in R[b]]) for d in (33, 38)}
    out["stale"][b].update({f"B{d}": ci([grp(r, d, Bk, "stale") for r in R[b]]) for d in (48, 53)})
    L.append(f"| {b} | " + " | ".join(f(out['stale'][b][k]) for k in ("A33", "A38", "B48", "B53")) + " |")

L += ["", "## Paired differences (mean [95% interval])", "", "| difference | A45 | B60 | food |", "|---|---|---|---|"]
pairs = [("M256", "M32"), ("M128", "M32"), ("E1", "T1"), ("E1", "T2"), ("E2", "T1"), ("E2", "T2"), ("E1", "M128"),
         ("E2", "M128"), ("E1", "GA"), ("E2", "GA")]
for a, c in pairs:
    d = {"A45": ci(np.array([grp(r, 45, A) for r in R[a]]) - np.array([grp(r, 45, A) for r in R[c]])),
         "B60": ci(np.array([grp(r, 60, Bk) for r in R[a]]) - np.array([grp(r, 60, Bk) for r in R[c]])),
         "food": ci(np.array([r["food"] for r in R[a]]) - np.array([r["food"] for r in R[c]]))}
    out["diffs"][f"{a}-{c}"] = d
    L.append(f"| {a} − {c} | {f(d['A45'])} | {f(d['B60'])} | {f(d['food'])} |")
L += ["", "Full intervals for every cell: analysis.json."]
(HERE / "analysis.json").write_text(json.dumps(out, indent=1), encoding="utf-8")
(HERE / "analysis.md").write_text("\n".join(L) + "\n", encoding="utf-8")
print("\n".join(L))
