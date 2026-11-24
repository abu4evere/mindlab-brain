"""W3r's frozen analysis (questions.md, W3r-frozen), written before any study data.

Primary: fresh-land survival of the kept copy (S), RMS − RVS, the paired difference over the 16 training seeds with a
95% bootstrap interval (10,000 resamples of seeds, seed 1). Secondary: RMS − RMXS (the sham), RE5S − RVS, RMS − HRS,
lifespans, the bare test, the module's speed (fair trials and steps until "fed" ranks food first, after a meal), the
mid-swap probe (S-midswap − S) and the soft probe (HRS-soft − HRS).

  python analyse_w3r.py        -> analysis.json, analysis.md
"""
import json
import math
import sys
from pathlib import Path

import numpy as np

sys.stdout.reconfigure(encoding="utf-8")
HERE = Path(__file__).parent
OUT = HERE / "output"
SEEDS = list(range(1, 17))
N = len(SEEDS)
IDX = np.random.default_rng(1).integers(0, N, (10_000, N))
LABELS = ["RVS", "RMS", "RMXS", "RE5S", "HRS", "RVS-bare", "RMS-bare", "RMXS-bare", "RE5S-bare", "HRS-bare",
          "RVS-midswap", "RMS-midswap", "RMXS-midswap", "RE5S-midswap", "HRS-soft", "RV", "RM", "RMX", "RE5", "HR"]


def ci(v):
    v = np.asarray(v, float)
    m = v[IDX].mean(axis=1)
    return [round(float(v.mean()), 4), round(float(np.percentile(m, 2.5)), 4), round(float(np.percentile(m, 97.5)), 4)]


def f(t):
    return f"{t[0]:.3f} [{t[1]:.3f}, {t[2]:.3f}]"


def mean(xs):
    xs = [x for x in xs if x is not None and not (isinstance(x, float) and math.isnan(x))]
    return float(np.mean(xs)) if xs else float("nan")


def summ(path):
    L = json.loads(path.read_text())
    s = {"survived": mean([l["survived"] for l in L]), "lifespan": mean([l["lifespan"] for l in L]), "n": len(L)}
    if L and "food_first" in L[0]:
        s["found_share"] = mean([float(l["food_first"] is not None) for l in L])
        s["food_first_steps"] = mean([l["food_first"] for l in L])
        s["food_first_trials"] = mean([l["food_first_trials"] for l in L])
    return s


def main():
    checks = "".join(p.read_text() for p in HERE.glob("checks_*.log") if p.name != "checks_pc_trial.log")
    paths = {(k, a): [OUT / f"test_{'fresh_' if k == 'fresh' else ''}{a}_{s}.json" for s in SEEDS]
             for a in LABELS for k in ("test", "fresh")}
    missing = sorted(p.name for ps in paths.values() for p in ps if not p.exists())
    L = ["# W3r analysis (the frozen analysis, analyse_w3r.py)", "",
         f"- Checks All: PASS on every study machine: **{'yes' if checks.count('All: PASS') >= 2 else 'see logs'}**",
         f"- All runs present: **{'yes' if not missing else 'NO, missing ' + str(len(missing)) + ': ' + ', '.join(missing[:10])}**",
         ""]
    if missing:
        (HERE / "analysis.md").write_text("\n".join(L) + "\n", encoding="utf-8")
        print("\n".join(L))
        return
    S = {key: [summ(p) for p in ps] for key, ps in paths.items()}
    surv = {a: np.array([x["survived"] for x in S[("fresh", a)]]) for a in LABELS}
    life = {a: np.array([x["lifespan"] for x in S[("test", a)]]) for a in LABELS}
    res = {"n_seeds": N, "lives_per_test": S[("fresh", "RMS")][0]["n"], "table": {}}
    L += [f"Each cell: the mean over {N} seeds [95% bootstrap]; fresh lands: {res['lives_per_test']} lives per seed.", "",
          "| arm | fresh-land survival | test-land survival | lifespan |", "|---|---|---|---|"]
    for a in LABELS:
        row = {"fresh": ci(surv[a]), "survived": ci([x["survived"] for x in S[("test", a)]]), "lifespan": ci(life[a])}
        res["table"][a] = row
        L.append(f"| {a} | {f(row['fresh'])} | {f(row['survived'])} | {row['lifespan'][0]:.0f} "
                 f"[{row['lifespan'][1]:.0f}, {row['lifespan'][2]:.0f}] |")
    prim = ci(surv["RMS"] - surv["RVS"])
    res["primary"] = {"RMS − RVS (fresh-land survival)": prim, "seeds_above_0": int((surv["RMS"] > surv["RVS"]).sum())}
    verdict = "a real gain" if prim[1] > 0 else "a real loss" if prim[2] < 0 else "unclear (the interval includes 0)"
    res["verdict"] = verdict
    sec_s = {k: ci(surv[k.split(" − ")[0]] - surv[k.split(" − ")[1]]) for k in
             ("RMS − RMXS", "RE5S − RVS", "RMS − HRS", "RMS-bare − RVS-bare", "RMS-midswap − RMS",
              "RVS-midswap − RVS", "HRS-soft − HRS")}
    sec_l = {k: ci(life[k.split(" − ")[0]] - life[k.split(" − ")[1]]) for k in
             ("RMS − RVS", "RMS − RMXS", "RE5S − RVS", "RMS − HRS")}
    res.update(secondary_survival=sec_s, secondary_lifespan=sec_l)
    L += ["", "## Readings", "",
          f"**1. Primary, RMS − RVS (fresh-land survival):** {f(prim)} -> **{verdict}**; "
          f"{res['primary']['seeds_above_0']} of {N} seeds above 0", "",
          "**2. Secondary, fresh-land survival (95%):**"]
    L += [f"- {k}: {f(v)}" for k, v in sec_s.items()]
    L.append("**3. Secondary, test-land lifespan (95%):**")
    L += [f"- {k}: {v[0]:.0f} [{v[1]:.0f}, {v[2]:.0f}]" for k, v in sec_l.items()]
    mod = {}
    for a in ("RMS", "RMXS", "RE5S"):
        rows = S[("fresh", a)]
        mod[a] = {"found_share": mean([r["found_share"] for r in rows]),
                  "food_first_steps": mean([r["food_first_steps"] for r in rows]),
                  "food_first_trials": mean([r["food_first_trials"] for r in rows])}
    res["module"] = mod
    L.append("**4. The module on fresh lands** (share of lives where 'fed' came to rank the food colour first after a "
             "meal; mean step and fair trials when it did):")
    L += [f"- {a}: {m['found_share']:.3f} of lives; step {m['food_first_steps']:.0f}; trials "
          f"{m['food_first_trials']:.0f}" for a, m in mod.items()]
    pj = HERE / "probe.json"
    if pj.exists():
        res["probe"] = json.loads(pj.read_text())
        L.append("**5. The learning curve** (probe_w3r.py): see probe.json")
    (HERE / "analysis.json").write_text(json.dumps(res, indent=1), encoding="utf-8")
    (HERE / "analysis.md").write_text("\n".join(L) + "\n", encoding="utf-8")
    print("\n".join(L))


if __name__ == "__main__":
    main()
