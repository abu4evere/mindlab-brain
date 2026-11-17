"""W3i's frozen analysis (questions.md), written before any data.

  python analyse_w3i.py        -> analysis.json, analysis.md
"""
import json
import math
import sys
from pathlib import Path

import numpy as np

sys.stdout.reconfigure(encoding="utf-8")
HERE = Path(__file__).parent
OUT = HERE / "output"
W3D = HERE.parent / "W3d" / "output"
WXO = HERE.parent / "WX" / "output"
SEEDS = range(1, 9)
IDX = np.random.default_rng(20261138).integers(0, 8, (10_000, 8))
LABELS = ("no_food_known", "food_known_not_reached", "exhaustion")


def ci(v):
    v = np.asarray(v, float)
    m = v[IDX].mean(axis=1)
    return [round(float(v.mean()), 3), round(float(np.percentile(m, 2.5)), 3), round(float(np.percentile(m, 97.5)), 3)]


def f3(t):
    return f"{t[0]:.3f} [{t[1]:.3f}, {t[2]:.3f}]"


def nanmean(xs):
    xs = [x for x in xs if x is not None and not (isinstance(x, float) and math.isnan(x))]
    return float(np.mean(xs)) if xs else float("nan")


def summary(lives, label_lives=None):
    dead = [l for l in (label_lives or lives) if l.get("labels")]
    out = {"lifespan": nanmean([l["lifespan"] for l in lives]), "survived": nanmean([l["survived"] for l in lives]),
           "to1000": nanmean([float(l["lifespan"] >= 1000) for l in lives]),
           "stale_per_1000": nanmean([l.get("stale_per_1000") for l in lives]),
           "since_meal_dead": nanmean([l.get("since_meal_end", l.get("since_meal")) for l in (label_lives or lives)
                                       if not l["survived"]])}
    for k in LABELS:
        out[k] = nanmean([float(l["labels"][k]) for l in dead])
    return out


def load(tag):
    p = OUT / f"test_{tag}.json"
    return json.loads(p.read_text()) if p.exists() else None


def main():
    checks = (HERE / "checks.log").read_text() if (HERE / "checks.log").exists() else ""
    need = [f"{a}_{s}" for a in ("L", "LC", "C") for s in SEEDS] + [f"fresh_{a}_{s}" for a in ("L", "LC", "C")
                                                                      for s in SEEDS]
    missing = [n for n in need if load(n) is None]
    L = ["# W3i analysis (the frozen analysis, analyse_w3i.py)", "",
         f"- Checks All: PASS: **{'yes' if 'All: PASS' in checks else 'NO'}**",
         f"- All 24 runs present, with fresh-land tests: **{'yes' if not missing else 'NO, missing ' + ', '.join(missing)}**"]
    rp = OUT / "repro_1.json"
    L.append(f"- The reproduction job (W3d PYFR seed 1 again): {rp.read_text() if rp.exists() else 'NOT PRESENT'}")
    L.append("")
    if missing:
        (HERE / "analysis.md").write_text("\n".join(L) + "\n", encoding="utf-8")
        print("\n".join(L))
        return
    S = {a: [summary(load(f"{a}_{s}")) for s in SEEDS] for a in ("L", "LC", "C")}
    S["PYFR"] = [summary(json.loads((W3D / f"test_PYFR_{s}.json").read_text()),
                         json.loads((WXO / f"PYFR_{s}.json").read_text())) for s in SEEDS]
    F = {a: [summary(load(f"fresh_{a}_{s}")) for s in SEEDS] for a in ("L", "LC", "C")}
    keys = ("lifespan", "survived", "to1000", "stale_per_1000", "since_meal_dead") + LABELS
    out = {"test": {a: {k: ci([r[k] for r in S[a]]) if not any(math.isnan(r[k]) for r in S[a]) else None
                        for k in keys} for a in S},
           "fresh": {a: {k: ci([r[k] for r in F[a]]) for k in ("lifespan", "survived")} for a in F}}
    L += ["| arm | lifespan | survived to 3,000 | to 1,000 | stale arrivals / 1,000 | no food known (of deaths) | "
          "steps since the last meal at death |", "|---|---|---|---|---|---|---|"]
    for a in ("PYFR", "L", "LC", "C"):
        o = out["test"][a]
        g = lambda k: f3(o[k]) if o[k] else "–"  # noqa: E731
        L.append(f"| {a} | {g('lifespan')} | {g('survived')} | {g('to1000')} | {g('stale_per_1000')} | "
                 f"{g('no_food_known')} | {g('since_meal_dead')} |")

    def d(a, b, k):
        return ci([x[k] - y[k] for x, y in zip(S[a], S[b])])
    r1, r2, r3 = d("L", "PYFR", "lifespan"), d("LC", "L", "lifespan"), d("C", "PYFR", "lifespan")
    best = max(("L", "LC", "C"), key=lambda a: out["test"][a]["lifespan"][0])
    out["readings"] = {"1": r1, "2": r2, "3": r3, "best": best, "best_fresh_survival": out["fresh"][best]["survived"]}
    L += ["", "## Readings", "",
          f"- **1. More practice helps (L(6M) − PYFR, lifespan):** {f3(r1)} -> **{'yes' if r1[1] > 0 else 'no'}**",
          f"- **2. A longer childhood helps, with equal practice (LC − L at 6M, lifespan):** {f3(r2)} -> "
          f"**{'yes' if r2[1] > 0 else 'no'}**",
          f"- **3. Secondary, C − PYFR (lifespan):** {f3(r3)}",
          f"- **4. Toward the bar:** the best arm by test lifespan is {best}; its survival on 50 fresh lands "
          f"{f3(out['fresh'][best]['survived'])} (bar 0.80)",
          f"- **5. Does the failure change?** \"No food known\" deaths: PYFR {f3(out['test']['PYFR']['no_food_known'])}, "
          f"L {f3(out['test']['L']['no_food_known'])}, LC {f3(out['test']['LC']['no_food_known'])}. Stale arrivals: "
          f"see the table (PYFR's were not measured by W3d; the 2M snapshots below stand in)."]
    # exploratory: the snapshots
    L += ["", "## Exploratory: the learning curve (snapshots at the first life boundary after 2M and 4M)", ""]
    for a in ("L", "LC"):
        row = []
        for tag in ("2M", "4M", ""):
            lives = [load(f"{a}_{s}_{tag}" if tag else f"{a}_{s}") for s in SEEDS]
            if all(x is not None for x in lives):
                sm = [summary(x) for x in lives]
                row.append(f"{tag or '6M'}: lifespan {np.mean([r['lifespan'] for r in sm]):.0f}, survived "
                           f"{np.mean([r['survived'] for r in sm]):.3f}, stale {np.mean([r['stale_per_1000'] for r in sm]):.2f}")
        L.append(f"- {a}: " + "; ".join(row))
    L += ["", "Per seed (lifespan): " + "; ".join(f"{a} " + ", ".join(f"{r['lifespan']:.0f}" for r in S[a])
                                                   for a in ("PYFR", "L", "LC", "C"))]
    (HERE / "analysis.json").write_text(json.dumps(out, indent=1), encoding="utf-8")
    (HERE / "analysis.md").write_text("\n".join(L) + "\n", encoding="utf-8")
    print("\n".join(L))


if __name__ == "__main__":
    main()
