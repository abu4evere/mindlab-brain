"""W3h's frozen analysis (questions.md), written before any data.

  python analyse_w3h.py        -> analysis.json, analysis.md
"""
import json
import math
import sys
from pathlib import Path

import numpy as np

sys.stdout.reconfigure(encoding="utf-8")
HERE = Path(__file__).parent
OUT = HERE / "output"
ARMS = ("TH", "THP", "THw", "THPw")
SEEDS = range(1, 9)
IDX = np.random.default_rng(20261137).integers(0, 8, (10_000, 8))
KEYS = ("thorn_per_1000", "entries_per_opp", "bout", "lifespan", "survived", "near_meal_share", "near_food_share",
        "harm", "pain")


def ci(v):
    v = np.asarray(v, float)
    m = v[IDX].mean(axis=1)
    return [round(float(v.mean()), 3), round(float(np.percentile(m, 2.5)), 3), round(float(np.percentile(m, 97.5)), 3)]


def nanmean(xs):
    xs = [x for x in xs if not (isinstance(x, float) and math.isnan(x))]
    return float(np.mean(xs)) if xs else float("nan")


def per_seed(arm, s):
    L = json.loads((OUT / f"test_{arm}_{s}.json").read_text())
    return {k: nanmean([l[k] for l in L]) for k in KEYS}


def main():
    checks = (HERE / "checks.log").read_text() if (HERE / "checks.log").exists() else ""
    missing = [f"{a}_{s}" for a in ARMS for s in SEEDS if not (OUT / f"test_{a}_{s}.json").exists()]
    L = ["# W3h analysis (the frozen analysis, analyse_w3h.py)", "",
         f"- Checks All: PASS: **{'yes' if 'All: PASS' in checks else 'NO'}**",
         f"- All 32 runs present: **{'yes' if not missing else 'NO, missing ' + ', '.join(missing)}**", ""]
    if missing:
        (HERE / "analysis.md").write_text("\n".join(L) + "\n", encoding="utf-8")
        print("\n".join(L))
        return
    d = {a: [per_seed(a, s) for s in SEEDS] for a in ARMS}
    out = {a: {k: ci([r[k] for r in d[a]]) for k in KEYS} for a in ARMS}

    def diff(a, b, k):
        return ci([x[k] - y[k] for x, y in zip(d[a], d[b])])
    f3 = lambda t: f"{t[0]:.3f} [{t[1]:.3f}, {t[2]:.3f}]"  # noqa: E731
    L += ["| arm | thorn steps / 1,000 | entries / opportunity | bout | lifespan | survived | near-thorn meal share "
          "(food there) |", "|---|---|---|---|---|---|---|"]
    for a in ARMS:
        o = out[a]
        L.append(f"| {a} | {f3(o['thorn_per_1000'])} | {f3(o['entries_per_opp'])} | {o['bout'][0]:.2f} | "
                 f"{f3(o['lifespan'])} | {f3(o['survived'])} | {o['near_meal_share'][0]:.3f} "
                 f"({o['near_food_share'][0]:.3f}) |")
    reads = {"1. Pain teaches avoidance (THP - TH, thorn steps / 1,000; upper < 0)": ("THP", "TH", "thorn_per_1000", "lt"),
             "2. Pain helps it live (THP - TH, lifespan; lower > 0)": ("THP", "TH", "lifespan", "gt"),
             "3. Watching teaches avoidance (THw - TH, thorn steps / 1,000; upper < 0)": ("THw", "TH", "thorn_per_1000",
                                                                                          "lt"),
             "4. Pain adds to watching (THPw - THw, thorn steps / 1,000; upper < 0)": ("THPw", "THw", "thorn_per_1000",
                                                                                       "lt")}
    L += ["", "## Readings", ""]
    out["readings"] = {}
    for name, (a, b, k, sign) in reads.items():
        t = diff(a, b, k)
        yes = t[2] < 0 if sign == "lt" else t[1] > 0
        out["readings"][name] = {"diff": t, "yes": bool(yes)}
        L.append(f"- **{name}:** {f3(t)} -> **{'yes' if yes else 'no'}**")
    L += ["", "## Secondary (paired differences, no gate)", ""]
    for a, b in (("THP", "TH"), ("THw", "TH"), ("THPw", "THw"), ("THPw", "THP")):
        L.append(f"- {a} - {b}: entries/opportunity {f3(diff(a, b, 'entries_per_opp'))}; survived "
                 f"{f3(diff(a, b, 'survived'))}; near-thorn meal share {f3(diff(a, b, 'near_meal_share'))}")
    # training curves and the thorn channel's norm
    L += ["", "## Training (means over seeds)", ""]
    for a in ARMS:
        curves = [json.loads((OUT / f"{a}_{s}_curve.json").read_text()) for s in SEEDS
                  if (OUT / f"{a}_{s}_curve.json").exists()]
        norms = [json.loads((OUT / f"{a}_{s}_norms.json").read_text()) for s in SEEDS
                 if (OUT / f"{a}_{s}_norms.json").exists()]
        if curves:
            n = min(len(c) for c in curves)
            pts = [round(float(np.mean([c[i]["thorn_per_1000"] for c in curves])), 1) for i in range(n)]
            L.append(f"- {a}: thorn steps / 1,000 per 100,000-step block: {pts}")
        if norms:
            fin = [nn[-1].get("thorn", float("nan")) for nn in norms if nn]
            L.append(f"  - the thorn channel's final weight norm: {nanmean(fin):.3f} (seeds: "
                     f"{[round(x, 3) for x in fin]})")
    (HERE / "analysis.json").write_text(json.dumps(out, indent=1), encoding="utf-8")
    (HERE / "analysis.md").write_text("\n".join(L) + "\n", encoding="utf-8")
    print("\n".join(L))


if __name__ == "__main__":
    main()
