"""W3p's frozen analysis (questions.md), written before any data. MBS (W3p's MoveVIN learning from bumps) against HRS (W3n), seeds 1-8, paired.
Bob Profile files from scorecard/bp/output (written by bp_tests.py for HR and bp_mv.py for MV); W3 test files from each
study's output. Bootstrap over seeds, numpy seed 20261122, one-sided 95% lower bounds.

  python analyse_w3p.py        -> analysis.json, analysis.md
"""
import json
import math
import sys
from pathlib import Path

import numpy as np

sys.stdout.reconfigure(encoding="utf-8")
HERE = Path(__file__).parent
BP = HERE.parent.parent / "scorecard" / "bp" / "output"
OUTS = {"MB": HERE / "output", "MBb": HERE / "output", "MV": HERE / "output", "HR": HERE.parent / "W3n" / "output"}
ARMS = ("MB", "MBb", "MV", "HR")
SEEDS = list(range(1, 9))
IDX = np.random.default_rng(20261122).integers(0, len(SEEDS), (10_000, len(SEEDS)))


def ci(v):
    v = np.asarray(v, float)
    m = v[IDX].mean(axis=1)
    return [round(float(v.mean()), 3), round(float(np.percentile(m, 5)), 3), round(float(np.percentile(m, 95)), 3)]


def f3(t):
    return f"{t[0]:.3f} [{t[1]:.3f}, {t[2]:.3f}]"


def bp(test, arm, key):
    out = []
    for s in SEEDS:
        p = BP / f"{test}_{arm}S_{s}.json"
        out.append(json.loads(p.read_text())[key] if p.exists() else None)
    return out


def w3(arm, label, key):
    out = []
    for s in SEEDS:
        p = OUTS[arm] / f"test_{label}_{s}.json"
        if not p.exists():
            out.append(None)
            continue
        L = json.loads(p.read_text())
        out.append(float(np.mean([l[key] for l in L])))
    return out


def main():
    checks = (HERE / "checks.log").read_text() if (HERE / "checks.log").exists() else ""
    tbl = {
        "R2 detour success": ("R2", "success"), "R5d long-detour success": ("R5d", "success"),
        "M2 memory success": ("M2", "success"), "M2e memory erased": ("M2e", "success"),
        "A2 tracks need": ("A2", "tracks"), "A5s bare fresh survival": ("A5s", "survived"),
        "L2 test lifespan": ("L2", "lifespan"), "G2 new-land ratio": ("G2", "ratio"),
        "value map uphill reaches food": ("PLAN", "uphill")}
    vals = {k: {a: bp(t, a, key) for a in ARMS} for k, (t, key) in tbl.items()}
    for lab, key in (("S", "lifespan"), ("S-bare", "lifespan")):
        vals[f"lifespan ({'reflexes' if lab == 'S' else 'bare'})"] = {a: w3(a, f"{a}{lab}", key) for a in ARMS}
    vals["fresh-land survival"] = {a: w3(a, f"fresh_{a}S", "survived") for a in ARMS}
    vals["can I enter here? (open minus walls)"] = {a: (bp("WALLS", a, "gap") if a != "HR" else [0.0] * len(SEEDS)) for a in ARMS}
    missing = [f"{k}/{a}/seed {SEEDS[i]}" for k, d in vals.items() for a, v in d.items() for i, x in enumerate(v)
               if x is None]
    L = ["# W3p analysis (the frozen analysis, analyse_w3p.py)", "",
         f"- Checks All: PASS: **{'yes' if 'All: PASS' in checks else 'NO'}**",
         f"- All files present: **{'yes' if not missing else 'NO, missing ' + ', '.join(missing[:10])}**", ""]
    if missing:
        (HERE / "analysis.md").write_text("\n".join(L) + "\n", encoding="utf-8")
        print("\n".join(L))
        return
    res = {"table": {}, "diff": {}}
    L += ["| measure | MBS (bumps) | MBbS (balanced bumps) | MVS (no bumps) | HRS (old brain) | MBS − HRS | MBbS − MBS | MBS − MVS |",
          "|---|---|---|---|---|---|---|---|"]
    for k, d in vals.items():
        a = {x: np.array(d[x], float) for x in ARMS}
        res["table"][k] = {x: ci(a[x]) for x in ARMS}
        res["diff"][k] = {"MB-HR": ci(a["MB"] - a["HR"]), "MBb-MB": ci(a["MBb"] - a["MB"]), "MB-MV": ci(a["MB"] - a["MV"]),
                          "MBb-HR": ci(a["MBb"] - a["HR"]), "MV-HR": ci(a["MV"] - a["HR"])}
        L.append(f"| {k} | " + " | ".join(f3(ci(a[x])) for x in ARMS) + f" | {f3(res['diff'][k]['MB-HR'])} | "
                 f"{f3(res['diff'][k]['MBb-MB'])} | {f3(res['diff'][k]['MB-MV'])} |")
    r2 = res["diff"]["R2 detour success"]["MB-HR"]
    mv_r2 = res["table"]["R2 detour success"]["MB"]
    mbb_r2 = res["table"]["R2 detour success"]["MBb"]
    res["primary"] = {"MBS − HRS on R2, lower bound > 0": bool(r2[1] > 0), "MBbS passes": bool(mbb_r2[1] >= 0.80),
                      "MBS passes Reasoning 2 (lower bound >= 0.80)": bool(mv_r2[1] >= 0.80)}
    L += ["", "## Primary", "",
          f"- **MoveVIN with bump learning detours better than DriveVIN (R2, MBS − HRS):** {f3(r2)} -> **{'yes' if r2[1] > 0 else 'no'}**",
          f"- **MBS passes the Bob Profile's Reasoning 2 (success lower bound ≥ 0.80):** {f3(mv_r2)} -> "
          f"**{'yes' if mv_r2[1] >= 0.80 else 'no'}**", "",
          "**Secondary:** MBbS passes Reasoning 2: " + f"{f3(mbb_r2)} -> {'yes' if mbb_r2[1] >= 0.80 else 'no'}; "
          f"MBbS − MBS on R2 {f3(res['diff']['R2 detour success']['MBb-MB'])}; MBS − MVS (what the bumps add) "
          f"{f3(res['diff']['R2 detour success']['MB-MV'])}; MVS − HRS (the planner alone) "
          f"{f3(res['diff']['R2 detour success']['MV-HR'])}.", "",
          "The full Bob Profile of MBS: `python ../../scorecard/bp/bp_score.py MB` (its Memory 5 line reads 'not built' "
          "for MB; MB, like HR, has no learned memory of its own, so Memory 5 fails by construction)."]
    (HERE / "analysis.json").write_text(json.dumps(res, indent=1), encoding="utf-8")
    (HERE / "analysis.md").write_text("\n".join(L) + "\n", encoding="utf-8")
    print("\n".join(L))


if __name__ == "__main__":
    main()
