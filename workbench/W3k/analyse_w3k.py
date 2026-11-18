"""W3k's frozen analysis (questions.md), written before any data.

  python analyse_w3k.py        -> analysis.json, analysis.md
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
IDX = np.random.default_rng(20261180).integers(0, N, (10_000, N))


def ci(v, level=95.0):
    """Mean and a percentile bootstrap interval over the seeds (paired: v is already a per-seed difference)."""
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
    if not path.exists():
        return None
    L = json.loads(path.read_text())
    return {"lifespan": mean([l["lifespan"] for l in L]), "survived": mean([l["survived"] for l in L]),
            "to1000": mean([float(l["lifespan"] >= 1000) for l in L])}


def main():
    checks = (HERE / "checks.log").read_text() if (HERE / "checks.log").exists() else ""
    arms = {"R2": "R2", "CS": "CS", "CY": "CY", "C3": "C3", "CR": "CR"}
    files = {a: [OUT / f"test_{lab}_{s}.json" for s in SEEDS] for a, lab in arms.items()}
    missing = [p.name for ps in files.values() for p in ps if not p.exists()]
    L = ["# W3k analysis (the frozen analysis, analyse_w3k.py)", "",
         f"- Checks All: PASS: **{'yes' if 'All: PASS' in checks else 'NO'}**",
         f"- All runs present: **{'yes' if not missing else 'NO, missing ' + ', '.join(missing[:12])}**", ""]
    res = {}

    # the determinism job: R seed 1 trained three times (R, D1, D2), and the machines each part ran on
    det = {}
    base = OUT / "R_1.npz"
    for name in ("D1", "D2"):
        p = OUT / f"{name}_1.npz"
        if base.exists() and p.exists():
            with np.load(base) as x, np.load(p) as y:
                det[name] = {"exact": all(np.array_equal(x[k], y[k]) for k in x.files),
                             "max_abs_diff": max(float(np.abs(x[k] - y[k]).max()) for k in x.files)}
        else:
            det[name] = "NOT PRESENT"
    cpus = {}
    for p in sorted(OUT.glob("machine_*.json")):
        for rec in json.loads(p.read_text()):
            cpus.setdefault(rec["cpu"], []).append(p.stem.replace("machine_", ""))
    res["determinism"] = det
    L += [f"- **The determinism job** (R seed 1 three times): D1 {json.dumps(det['D1'])}; D2 {json.dumps(det['D2'])}",
          "- Processors seen: " + "; ".join(f"{c} ({len(v)} run parts)" for c, v in cpus.items()), ""]
    if missing:
        (HERE / "analysis.md").write_text("\n".join(L) + "\n", encoding="utf-8")
        print("\n".join(L))
        return

    S = {a: [summ(p) for p in ps] for a, ps in files.items()}
    F = {a: [summ(OUT / f"test_fresh_{arms[a]}_{s}.json") for s in SEEDS] for a in arms}
    D = {a: [json.loads((OUT / f"drift_{arms[a]}_{s}.json").read_text()) for s in SEEDS] for a in arms}
    life = {a: np.array([x["lifespan"] for x in S[a]]) for a in arms}

    L += ["| arm | lifespan | median | survived | to 1,000 | fresh lands: survived | drift | agrees with the parent |",
          "|---|---|---|---|---|---|---|---|"]
    table = {}
    for a in arms:
        row = {"lifespan": ci(life[a]), "median": round(float(np.median(life[a])), 1),
               "survived": ci([x["survived"] for x in S[a]]), "to1000": ci([x["to1000"] for x in S[a]]),
               "fresh": ci([x["survived"] for x in F[a]]),
               "drift": ci([mean([d["drift"] for d in dd]) for dd in D[a]]),
               "parent": ci([mean([d["parent_agree"] for d in dd]) for dd in D[a]])}
        table[a] = row
        L.append(f"| {a} | {f3(row['lifespan'])} | {row['median']} | {f3(row['survived'])} | {f3(row['to1000'])} | "
                 f"{f3(row['fresh'])} | {f3(row['drift'])} | {f3(row['parent'])} |")
    res["table"] = table

    def diff(a, b, level):
        return ci(life[a] - life[b], level)

    def loo(a, b):
        d = life[a] - life[b]
        means = [float(np.delete(d, i).mean()) for i in range(N)]
        return [round(min(means), 1), round(max(means), 1)]

    p1, p2 = diff("C3", "R2", 97.5), diff("CS", "R2", 97.5)
    interp = diff("CS", "CY", 95)
    sec = {"CR − R2": diff("CR", "R2", 95), "CY − R2": diff("CY", "R2", 95)}
    res.update(primary={"C3 − R2": p1, "CS − R2": p2}, cs_vs_cy=interp, secondary=sec,
               loo={"C3 − R2": loo("C3", "R2"), "CS − R2": loo("CS", "R2")},
               medians={"C3 − R2": float(np.median(life["C3"] - life["R2"])), "CS − R2": float(np.median(life["CS"] - life["R2"]))})
    yes = lambda t: "yes" if t[1] > 0 else "no"  # noqa: E731
    L += ["", "## Readings (lifespan, paired by seed)", "",
          "**1. Two primary readings (97.5% intervals, Bonferroni):**",
          f"- **A longer childhood still helps (C3 − R2):** {f3(p1)} -> **{yes(p1)}**; median {res['medians']['C3 − R2']:.1f}; "
          f"leave-one-seed-out means {res['loo']['C3 − R2']}",
          f"- **Choosing its own best copy helps (CS − R2):** {f3(p2)} -> **{yes(p2)}**; median {res['medians']['CS − R2']:.1f}; "
          f"leave-one-seed-out means {res['loo']['CS − R2']}",
          f"**2. How to read CS (CS − CY, 95%):** {f3(interp)} -> **{yes(interp)}**"
          + (" (the brain's own lives carry information about when it was better)" if interp[1] > 0
             else " (no information shown beyond 'an earlier copy')"),
          "**3. Secondary (95%):**"]
    for k, v in sec.items():
        L.append(f"- {k}: {f3(v)} -> {yes(v)}")
    best = max(arms, key=lambda a: table[a]["lifespan"][0])
    res["best_arm"] = best
    L += [f"**4. Toward the bar:** the best arm by test lifespan is {best}; fresh-land survival {f3(table[best]['fresh'])} (bar 0.80)", ""]

    # CS's and CY's chosen steps
    meta = [json.loads((OUT / f"R_{s}_meta.json").read_text()) for s in SEEDS]
    L += ["## The kept copies", "",
          "- CS's step (millions): " + ", ".join(f"{(m['cs_step'] or 0) / 1e6:.2f}" for m in meta),
          "- CY's step (millions): " + ", ".join(f"{(m['cy_at'] or 0) / 1e6:.2f}" for m in meta), ""]
    res["kept"] = [{"cs_step": m["cs_step"], "cy_at": m["cy_at"]} for m in meta]

    # exploratory: the learning curves, and the oracle (the best tested snapshot of run R, per seed)
    L += ["## Exploratory (labelled): the learning curves and the oracle", ""]
    for run, label in (("R", "R"), ("C3", "C3"), ("CR", "CR")):
        steps = sorted({int(p.stem.split("_")[-1][:-1]) for p in OUT.glob(f"test_{label}_*_*k.json")})
        parts = []
        for k in steps:
            v = [summ(OUT / f"test_{label}_{s}_{k}k.json") for s in SEEDS]
            if all(v):
                parts.append(f"{k / 1000:.1f}M {np.mean([x['lifespan'] for x in v]):.0f}")
        L.append(f"- {run}: " + " → ".join(parts) + f" → final {life['R2' if run == 'R' else run].mean():.0f}")
    oracle = []
    for s in SEEDS:
        snaps = [summ(p) for p in OUT.glob(f"test_R_{s}_*k.json")] + [S["R2"][s - 1]]
        oracle.append(max(x["lifespan"] for x in snaps if x))
    res["oracle"] = ci(oracle)
    L.append(f"- The oracle (best tested snapshot of run R per seed, chosen by the test: an upper bound, not a result): "
             f"{f3(res['oracle'])}")
    (HERE / "analysis.json").write_text(json.dumps(res, indent=1), encoding="utf-8")
    (HERE / "analysis.md").write_text("\n".join(L) + "\n", encoding="utf-8")
    print("\n".join(L))


if __name__ == "__main__":
    main()
