"""WE analysis (descriptive; questions.md). Gene paths per run; the final test with 95% bootstrap intervals over 48
seeds (numpy seed 20261116, 10,000 resamples; paired differences resample seeds once). Writes analysis.md and .json."""
import json
from pathlib import Path

import numpy as np

HERE = Path(__file__).parent
BRAINS = ("E1", "E2", "GA", "M32", "M128")
SEEDS, B = range(1001, 1049), 10_000
IDX = np.random.default_rng(20261116).integers(0, len(SEEDS), (B, len(SEEDS)))


def ci(v):
    v = np.asarray(v, float)
    m = v[IDX].mean(axis=1)
    return [round(float(v.mean()), 3), round(float(np.percentile(m, 2.5)), 3), round(float(np.percentile(m, 97.5)), 3)]


f = lambda t: f"{t[0]:.3f} [{t[1]:.3f}, {t[2]:.3f}]"
out = {"paths": {}, "final": {}, "diffs": {}, "evolved": json.loads((HERE / "evolved.json").read_text())}
L = ["# WE analysis (from analyse_we.py)", "", "## Gene paths (population 32 per generation; means, born/final medians)", "",
     "| run | gen | mean food | a | g | s | e | born (median) | final (median) |", "|---|---|---|---|---|---|---|---|---|"]
for run in (1, 2):
    hist = json.loads((HERE / f"evo_run{run}.json").read_text())
    out["paths"][run] = []
    for h in hist:
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

R = {b: [json.loads((HERE / "output" / f"{b}_seed_{s}.json").read_text()) for s in SEEDS] for b in BRAINS}
meas = {"day 30": lambda r: r["tests"]["30"]["success"], "day 60": lambda r: r["tests"]["60"]["success"],
        "after showing 30": lambda r: r["show_tests"]["30"]["success"], "food": lambda r: r["food"]}
L += ["", "## Final test (48 fresh children each; mean [95% interval])", "",
      "| brain | day 30 | day 60 | after a showing, day 30 | lifetime food |", "|---|---|---|---|---|"]
for b in BRAINS:
    out["final"][b] = {k: ci([fn(r) for r in R[b]]) for k, fn in meas.items()}
    L.append(f"| {b} | " + " | ".join(f(out['final'][b][k]) for k in meas) + " |")
L += ["", "| paired difference | day 30 | day 60 | after a showing | food |", "|---|---|---|---|---|"]
for e in ("E1", "E2"):
    for c in ("GA", "M32", "M128"):
        d = {k: ci(np.array([fn(r) for r in R[e]]) - np.array([fn(r) for r in R[c]])) for k, fn in meas.items()}
        out["diffs"][f"{e}-{c}"] = d
        L.append(f"| {e} − {c} | " + " | ".join(f(d[k]) for k in meas) + " |")
(HERE / "analysis.json").write_text(json.dumps(out, indent=1), encoding="utf-8")
(HERE / "analysis.md").write_text("\n".join(L) + "\n", encoding="utf-8")
print("\n".join(L))
