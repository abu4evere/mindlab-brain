"""WP analysis (descriptive; questions.md). 95% bootstrap intervals over the 48 groups (numpy seed 20261119, 10,000
resamples; paired differences resample groups once). Writes analysis.md and analysis.json."""
import json
import sys
from pathlib import Path

import numpy as np

sys.stdout.reconfigure(encoding="utf-8")
HERE = Path(__file__).parent
GROUPS = ("S6", "B1S5", "B6", "S6alone")
GS, B = range(1, 49), 10_000
IDX = np.random.default_rng(20261119).integers(0, len(GS), (B, len(GS)))
A, Bk = (0, 1, 2), (3, 4, 5)


def ci(v):
    v = np.asarray(v, float)
    m = v[IDX].mean(axis=1)
    return [round(float(v.mean()), 3), round(float(np.percentile(m, 2.5)), 3), round(float(np.percentile(m, 97.5)), 3)]


f = lambda t: f"{t[0]:.3f} [{t[1]:.3f}, {t[2]:.3f}]"
out, L = {}, ["# WP analysis (from analyse_wp.py; 48 groups of 6 per cell; mean [95% interval])"]
for world in ("stable", "change"):
    R = {n: [json.loads((HERE / f"output_{world}" / f"{n}_g{g}.json").read_text()) for g in GS] for n in GROUPS}
    reads = {"day 30": (30, range(6)), "day 60": (60, range(6))}
    if world == "change":
        reads.update({"A day 45": (45, A), "B day 60": (60, Bk)})

    def score(r, kids, key):
        d, ks = reads[key]
        return float(np.mean([np.mean([r["tests"][str(c)][str(d)][k] for k in ks]) for c in kids]))

    o = out[world] = {"small_1to5": {}, "group_mean": {}, "child0": {}, "diffs": {}, "watch_big": {}, "food": {}}
    L += ["", f"## World: {world}", "", "### Small children 1–5 (mean of the five), group mean, child 0", "",
          "| group | measure | small 1–5 | group mean (all 6) | child 0 |", "|---|---|---|---|---|"]
    for n in GROUPS:
        for key in reads:
            s = ci([score(r, range(1, 6), key) for r in R[n]])
            gm = ci([score(r, range(6), key) for r in R[n]])
            c0 = ci([score(r, [0], key) for r in R[n]])
            o["small_1to5"].setdefault(n, {})[key] = s
            o["group_mean"].setdefault(n, {})[key] = gm
            o["child0"].setdefault(n, {})[key] = c0
            L.append(f"| {n} | {key} | {f(s)} | {f(gm)} | {f(c0)} |")
        o["food"][n] = {"small_1to5": ci([np.mean(r["food"][1:]) for r in R[n]]),
                        "child0": ci([r["food"][0] for r in R[n]]), "group": ci([np.mean(r["food"]) for r in R[n]])}
    L += ["", "### Food per child", "", "| group | small 1–5 | child 0 | group mean |", "|---|---|---|---|"]
    for n in GROUPS:
        L.append(f"| {n} | {f(o['food'][n]['small_1to5'])} | {f(o['food'][n]['child0'])} | {f(o['food'][n]['group'])} |")
    L += ["", "### Paired differences", "", "| difference | " + " | ".join(reads) + " |", "|---" * (len(reads) + 1) + "|"]
    for a, c, kids, label in (("B1S5", "S6", range(1, 6), "small 1–5: B1S5 − S6"),
                              ("S6", "S6alone", range(1, 6), "small 1–5: S6 − S6alone"),
                              ("B1S5", "S6", range(6), "group mean: B1S5 − S6"),
                              ("B6", "B1S5", range(6), "group mean: B6 − B1S5"),
                              ("B1S5", "B6", [0], "child 0: B1S5 − B6")):
        d = {key: ci(np.array([score(r, kids, key) for r in R[a]]) - np.array([score(r, kids, key) for r in R[c]]))
             for key in reads}
        o["diffs"][label] = d
        L.append(f"| {label} | " + " | ".join(f(d[k]) for k in reads) + " |")
    # Q2: the small children's watching share going to the big child (child 0) in B1S5; chance 0.2
    for ph, nm in ((0, "days 1-30"), (1, "days 31-60")):
        sh = []
        for r in R["B1S5"]:
            W = np.array(r["watched"])[ph]
            tot = W[1:, :].sum()
            sh.append(W[1:, 0].sum() / tot if tot else np.nan)
        o["watch_big"][nm] = ci(np.array(sh)[~np.isnan(sh)])
    L += ["", "### Watching share of the small children going to the big child (B1S5; chance 0.20)", ""]
    L += [f"- {k}: {f(v)}" for k, v in o["watch_big"].items()]
(HERE / "analysis.json").write_text(json.dumps(out, indent=1), encoding="utf-8")
(HERE / "analysis.md").write_text("\n".join(L) + "\n", encoding="utf-8")
print("\n".join(L))
