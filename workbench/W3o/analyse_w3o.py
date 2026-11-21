"""W3o's frozen analysis (questions.md), written before any data.

  python analyse_w3o.py        -> analysis.json, analysis.md
"""
import json
import math
import sys
from pathlib import Path

import numpy as np

sys.stdout.reconfigure(encoding="utf-8")
HERE = Path(__file__).parent
OUT = HERE / "output"
W3N = HERE.parent / "W3n" / "output"
SEEDS = list(range(1, 9))
N = len(SEEDS)
IDX = np.random.default_rng(20261220).integers(0, N, (10_000, N))
MARGIN = -200.0


def ci(v, level=95.0):
    v = np.asarray(v, float)
    m = v[IDX].mean(axis=1)
    lo = (100 - level) / 2
    return [round(float(v.mean()), 3), round(float(np.percentile(m, lo)), 3), round(float(np.percentile(m, 100 - lo)), 3)]


def f3(t):
    return f"{t[0]:.3f} [{t[1]:.3f}, {t[2]:.3f}]"


def mean(xs):
    xs = [x for x in xs if x is not None and not (isinstance(x, float) and math.isnan(x))]
    return float(np.mean(xs)) if xs else float("nan")


def summ(path):
    L = json.loads(path.read_text())
    return {"lifespan": mean([l["lifespan"] for l in L]), "survived": mean([l["survived"] for l in L]),
            "to1000": mean([float(l["lifespan"] >= 1000) for l in L]),
            "deaths_per_1000": mean([1000.0 * (1.0 - l["survived"]) / max(1, l["lifespan"]) for l in L]),
            "hungry": mean([l["hungry"] for l in L]), "exhausted": mean([l["exhausted"] for l in L])}


ARMS = {"HR": (W3N, "HR"), "HRS": (W3N, "HRS"), "HRS-bare": (W3N, "HRS-bare"), "HRS-off": (W3N, "HRS-off"),
        "RE": (OUT, "RE"), "RES": (OUT, "RES"), "REY": (OUT, "REY"), "RES-bare": (OUT, "RES-bare"),
        "RES-off": (OUT, "RES-off"), "RES-swap": (OUT, "RES-swap"),
        "RV": (OUT, "RV"), "RVS": (OUT, "RVS"), "RVY": (OUT, "RVY"), "RVS-bare": (OUT, "RVS-bare"),
        "RVS-off": (OUT, "RVS-off"), "RVS-swap": (OUT, "RVS-swap")}


def main():
    checks = (HERE / "checks.log").read_text() if (HERE / "checks.log").exists() else ""
    files = {a: [d / f"test_{lab}_{s}.json" for s in SEEDS] for a, (d, lab) in ARMS.items()}
    fresh = {a: [d / f"test_fresh_{lab}_{s}.json" for s in SEEDS] for a, (d, lab) in ARMS.items()}
    missing = [p.name for ps in list(files.values()) + list(fresh.values()) for p in ps if not p.exists()]
    L = ["# W3o analysis (the frozen analysis, analyse_w3o.py)", "",
         f"- Checks All: PASS: **{'yes' if 'All: PASS' in checks else 'NO'}**",
         f"- All runs present: **{'yes' if not missing else 'NO, missing ' + ', '.join(missing[:12])}**", ""]
    if missing:
        (HERE / "analysis.md").write_text("\n".join(L) + "\n", encoding="utf-8")
        print("\n".join(L))
        return
    S = {a: [summ(p) for p in ps] for a, ps in files.items()}
    F = {a: [summ(p) for p in ps] for a, ps in fresh.items()}
    life = {a: np.array([x["lifespan"] for x in S[a]]) for a in ARMS}
    res = {"table": {}}
    L += ["| arm | lifespan | survived | fresh lands: survived | steps hungry |", "|---|---|---|---|---|"]
    for a in ARMS:
        row = {"lifespan": ci(life[a]), "survived": ci([x["survived"] for x in S[a]]),
               "fresh": ci([x["survived"] for x in F[a]]), "hungry": ci([x["hungry"] for x in S[a]])}
        res["table"][a] = row
        L.append(f"| {a}{' (W3n)' if ARMS[a][0] == W3N else ''} | {f3(row['lifespan'])} | {f3(row['survived'])} | "
                 f"{f3(row['fresh'])} | {f3(row['hungry'])} |")

    def diff(a, b, level):
        return ci(life[a] - life[b], level)

    prim = {"RES-bare − HRS-bare": diff("RES-bare", "HRS-bare", 97.5), "RES − HRS": diff("RES", "HRS", 97.5)}
    ceiling = {k: diff(*k.split(" − "), 95) for k in ("RVS-bare − HRS-bare", "RVS − HRS")}
    sec = {k: diff(*k.split(" − "), 95) for k in ("RE − HR", "RV − HR", "RVS − RES", "RES-swap − RES")}
    res["ceiling_RV"] = ceiling
    res["deaths_per_1000"] = {a: ci([x["deaths_per_1000"] for x in S[a]]) for a in ARMS}
    res.update(primary=prim, secondary=sec,
               seeds_positive={k: int((life[k.split(" − ")[0]] - life[k.split(" − ")[1]] > 0).sum()) for k in prim})

    def verdict(t):
        if t[2] < 0:
            return "a real loss" + (" (but small: lower bound above −200)" if t[1] > MARGIN else "")
        if t[1] > 0:
            return "a real gain"
        return "small: within the margin" if t[1] > MARGIN else "unclear (the interval reaches below −200)"
    res["verdicts"] = {k: verdict(v) for k, v in prim.items()}
    L += ["", "## Readings (lifespan on the test lands, paired by seed with W3n's HR)", "",
          "**1. Primary, RE (97.5% intervals, Bonferroni; margin −200 steps):**"]
    for k, v in prim.items():
        L.append(f"- **{k}:** {f3(v)} -> **{res['verdicts'][k]}**; {res['seeds_positive'][k]} of {N} seeds above 0")
    L.append("**2. RV, the ceiling test (95%):**")
    for k, v in ceiling.items():
        L.append(f"- {k}: {f3(v)}")
    L.append("**3. Secondary (95%):**")
    for k, v in sec.items():
        L.append(f"- {k}: {f3(v)}" + (" (the manipulation check: expected below 0)" if k == "RES-swap − RES" else ""))
    sw = sec["RES-swap − RES"]
    res["manipulation_check"] = bool(sw[2] < 0)
    L.append(f"- Manipulation check passed (RE's brain uses what the colours mean): **{'yes' if sw[2] < 0 else 'NO'}**")
    L.append("- Deaths per 1,000 steps: " + "; ".join(f"{a} {f3(res['deaths_per_1000'][a])}" for a in ARMS))
    L += ["**4. Toward the bar (fresh-land survival, 0.80):** " + "; ".join(
        f"{a} {f3(res['table'][a]['fresh'])}" for a in ("HRS", "RES", "RVS", "HRS-bare", "RES-bare", "RVS-bare")), ""]
    L.append("- Median lifespan: " + "; ".join(f"{a} {float(np.median(life[a])):.0f}" for a in ARMS))
    L.append("- Share of lives past step 1,000: " + "; ".join(
        f"{a} {np.mean([x['to1000'] for x in S[a]]):.3f}" for a in ARMS))
    pj = HERE / "probe.json"
    if pj.exists():                                   # the probe (probe_w3o.py, frozen): first moves toward what it needs
        P = json.loads(pj.read_text())
        res["probe"] = {}
        L += ["", "**The probe** (no reflex, memory fully known; share of first moves toward food when hungry, toward the "
              "shelter when tired):"]
        for st in ("hungry", "tired"):
            tw = {b: np.array([P[b][str(s)][st]["toward"] for s in SEEDS]) for b in P}
            ch = np.mean([P["HRS"][str(s)][st]["chance"] for s in SEEDS])
            d = {f"{b} − HRS": ci(tw[b] - tw["HRS"]) for b in ("RES", "RVS", "RES-swap")}
            res["probe"][st] = {"means": {b: float(v.mean()) for b, v in tw.items()}, "chance": float(ch), "diff": d}
            L.append(f"- {st}: " + "; ".join(f"{b} {v.mean():.3f}" for b, v in tw.items()) + f" (chance {ch:.3f}); "
                     + "; ".join(f"{k} {f3(v)}" for k, v in d.items()))
    (HERE / "analysis.json").write_text(json.dumps(res, indent=1), encoding="utf-8")
    (HERE / "analysis.md").write_text("\n".join(L) + "\n", encoding="utf-8")
    print("\n".join(L))


if __name__ == "__main__":
    main()
