"""W3j's frozen analysis (questions.md), written before any data.

  python analyse_w3j.py        -> analysis.json, analysis.md
"""
import json
import math
import sys
from pathlib import Path

import numpy as np

sys.stdout.reconfigure(encoding="utf-8")
HERE = Path(__file__).parent
OUT = HERE / "output"
W3I = HERE.parent / "W3i" / "output"
SEEDS = range(1, 9)
IDX = np.random.default_rng(20261139).integers(0, 8, (10_000, 8))


def ci(v):
    v = np.asarray(v, float)
    m = v[IDX].mean(axis=1)
    return [round(float(v.mean()), 3), round(float(np.percentile(m, 2.5)), 3), round(float(np.percentile(m, 97.5)), 3)]


def f3(t):
    return f"{t[0]:.3f} [{t[1]:.3f}, {t[2]:.3f}]"


def mean(xs):
    xs = [x for x in xs if x is not None and not (isinstance(x, float) and math.isnan(x))]
    return float(np.mean(xs)) if xs else float("nan")


def summ(path):
    if not path.exists():
        return None
    L = json.loads(path.read_text())
    return {"lifespan": mean([l["lifespan"] for l in L]), "survived": mean([l["survived"] for l in L]),
            "to1000": mean([float(l["lifespan"] >= 1000) for l in L])}


def main():
    checks = (HERE / "checks.log").read_text() if (HERE / "checks.log").exists() else ""
    files = {
        "C": [W3I / f"test_C_{s}.json" for s in SEEDS],
        "CF": [OUT / f"test_CK_{s}_1200k.json" for s in SEEDS],
        **{a: [OUT / f"test_{a}_{s}.json" for s in SEEDS] for a in ("CK", "CV", "C4", "C2")},
    }
    missing = [p.name for ps in files.values() for p in ps if not p.exists()]
    rp = OUT / "repro_1.json"
    L = ["# W3j analysis (the frozen analysis, analyse_w3j.py)", "",
         f"- Checks All: PASS: **{'yes' if 'All: PASS' in checks else 'NO'}**",
         f"- All runs present: **{'yes' if not missing else 'NO, missing ' + ', '.join(missing[:12])}**",
         f"- The reproduction job (W3i's C seed 1 with W3j's code): {rp.read_text() if rp.exists() else 'NOT PRESENT'}", ""]
    if missing:
        (HERE / "analysis.md").write_text("\n".join(L) + "\n", encoding="utf-8")
        print("\n".join(L))
        return
    S = {a: [summ(p) for p in ps] for a, ps in files.items()}
    fresh = {"C": [summ(W3I / f"test_fresh_C_{s}.json") for s in SEEDS],
             **{a: [summ(OUT / f"test_fresh_{a}_{s}.json") for s in SEEDS] for a in ("CK", "CV", "C4", "C2")}}
    out = {"test": {a: {k: ci([r[k] for r in S[a]]) for k in ("lifespan", "survived", "to1000")} for a in S},
           "fresh": {a: ci([r["survived"] for r in fresh[a]]) for a in fresh}}
    drift = {a: [json.loads((OUT / f"drift_{a}_{s}.json").read_text()) for s in SEEDS] for a in ("CK", "CV", "C4", "C2")}
    out["drift"] = {a: ci([mean([x["drift"] for x in d]) for d in drift[a]]) for a in drift}
    out["parent_agree"] = {a: ci([mean([x["parent_agree"] for x in d]) for d in drift[a]]) for a in drift}
    L += ["| arm | lifespan | survived | to 1,000 | fresh lands: survived | drift from the end of childhood | agrees with the parent |",
          "|---|---|---|---|---|---|---|"]
    for a in ("C", "CF", "CK", "CV", "C4", "C2"):
        o = out["test"][a]
        L.append(f"| {a} | {f3(o['lifespan'])} | {f3(o['survived'])} | {f3(o['to1000'])} | "
                 f"{f3(out['fresh'][a]) if a in out['fresh'] else '–'} | {f3(out['drift'][a]) if a in out['drift'] else '–'} | "
                 f"{f3(out['parent_agree'][a]) if a in out['parent_agree'] else '–'} |")

    def d(a, b):
        return ci([x["lifespan"] - y["lifespan"] for x, y in zip(S[a], S[b])])
    rd = {"1 (primary) CK - C": d("CK", "C"), "CF - C": d("CF", "C"), "CV - C": d("CV", "C"), "C2 - C4": d("C2", "C4"),
          "C4 - C": d("C4", "C"), "CK - CF": d("CK", "CF")}
    out["readings"] = rd
    best = max(("CK", "CV", "C4", "C2"), key=lambda a: out["test"][a]["lifespan"][0])
    L += ["", "## Readings (lifespan, paired by seed)", "",
          f"- **1. Primary, settling down keeps it (CK − C):** {f3(rd['1 (primary) CK - C'])} -> "
          f"**{'yes' if rd['1 (primary) CK - C'][1] > 0 else 'no'}**",
          f"- Secondary: adult learning hurts (CF − C): {f3(rd['CF - C'])} -> {'yes' if rd['CF - C'][1] > 0 else 'no'}",
          f"- Secondary: a quiet parent keeps it (CV − C): {f3(rd['CV - C'])} -> {'yes' if rd['CV - C'][1] > 0 else 'no'}",
          f"- Secondary: a longer childhood at equal steps (C2 − C4): {f3(rd['C2 - C4'])} -> {'yes' if rd['C2 - C4'][1] > 0 else 'no'}",
          f"- Secondary: more steps, the same childhood (C4 − C): {f3(rd['C4 - C'])}",
          f"- CK against CF: {f3(rd['CK - CF'])} "
          f"({'slow adult learning adds something' if rd['CK - CF'][1] > 0 else 'CF at least as good: the adult learning itself is the problem' if rd['CK - CF'][2] <= 0 else 'not separated'})",
          f"- **Toward the bar:** the best final arm by test lifespan is {best}; fresh-land survival {f3(out['fresh'][best])} (bar 0.80)",
          "", "## The learning curves (exploratory; snapshot tests, mean lifespan over seeds)", ""]
    for a in ("CK", "CV", "C4", "C2"):
        pts = []
        for k in sorted({int(p.stem.split("_")[-1][:-1]) for p in OUT.glob(f"test_{a}_*_*k.json")}):
            ss = [summ(OUT / f"test_{a}_{s}_{k}k.json") for s in SEEDS]
            if all(ss):
                pts.append(f"{k / 1000:.1f}M {np.mean([x['lifespan'] for x in ss]):.0f}")
        pts.append(f"final {out['test'][a]['lifespan'][0]:.0f}")
        L.append(f"- {a}: " + " → ".join(pts))
    (HERE / "analysis.json").write_text(json.dumps(out, indent=1), encoding="utf-8")
    (HERE / "analysis.md").write_text("\n".join(L) + "\n", encoding="utf-8")
    print("\n".join(L))


if __name__ == "__main__":
    main()
