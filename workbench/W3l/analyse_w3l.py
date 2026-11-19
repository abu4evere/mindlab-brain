"""W3l's frozen analysis (questions.md), written before any data.

  python analyse_w3l.py        -> analysis.json, analysis.md
"""
import json
import math
import sys
from pathlib import Path

import numpy as np

sys.stdout.reconfigure(encoding="utf-8")
HERE = Path(__file__).parent
OUT = HERE / "output"
W3K = HERE.parent / "W3k" / "output"
SEEDS = list(range(1, 17))
N = len(SEEDS)
IDX = np.random.default_rng(20261190).integers(0, N, (10_000, N))


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


# arm -> (folder, test label); CS is W3k's, cited (tested there on the same lands)
ARMS = {"CS": (W3K, "CS"), "C3": (OUT, "C3"), "C3S": (OUT, "C3S"), "C3Y": (OUT, "C3Y"),
        "C5": (OUT, "C5"), "C5S": (OUT, "C5S"), "C5Y": (OUT, "C5Y")}


def main():
    checks = (HERE / "checks.log").read_text() if (HERE / "checks.log").exists() else ""
    files = {a: [d / f"test_{lab}_{s}.json" for s in SEEDS] for a, (d, lab) in ARMS.items()}
    missing = [p.name for ps in files.values() for p in ps if not p.exists()]
    L = ["# W3l analysis (the frozen analysis, analyse_w3l.py)", "",
         f"- Checks All: PASS: **{'yes' if 'All: PASS' in checks else 'NO'}**",
         f"- All runs present: **{'yes' if not missing else 'NO, missing ' + ', '.join(missing[:12])}**", ""]
    res = {}

    # the reproduction check: C3's end weights against W3k's C3, every named array; and the CS step W3k recorded
    rep = {}
    for s in SEEDS:
        a, b = OUT / f"C3_{s}.npz", W3K / f"C3_{s}.npz"
        if not (a.exists() and b.exists()):
            rep[s] = "NOT PRESENT"
            continue
        with np.load(a) as x, np.load(b) as y:
            same_keys = sorted(x.files) == sorted(y.files)
            exact = same_keys and all(np.array_equal(x[k], y[k]) for k in x.files)
            mad = max(float(np.abs(x[k] - y[k]).max()) for k in x.files) if same_keys else None
        m_new = json.loads((OUT / f"C3_{s}_meta.json").read_text())
        m_old = json.loads((W3K / f"C3_{s}_meta.json").read_text())
        rep[s] = {"exact": exact, "max_abs_diff": mad, "cs_step_same": m_new["cs_step"] == m_old["cs_step"]}
    n_exact = sum(1 for v in rep.values() if isinstance(v, dict) and v["exact"] and v["cs_step_same"])
    res["reproduction"] = rep
    cpus = {}
    for p in sorted(OUT.glob("machine_*.json")):
        for rec in json.loads(p.read_text()):
            cpus.setdefault(rec["cpu"], []).append(p.stem.replace("machine_", ""))
    L += [f"- **The reproduction check** (C3's end weights equal W3k's, every array, and the same CS step): "
          f"**{n_exact} of {N} seeds exact**",
          "- Processors seen: " + "; ".join(f"{c} ({len(v)} run parts)" for c, v in cpus.items()), ""]
    if missing:
        (HERE / "analysis.md").write_text("\n".join(L) + "\n", encoding="utf-8")
        print("\n".join(L))
        return

    S = {a: [summ(p) for p in ps] for a, ps in files.items()}
    F = {a: [summ(d / f"test_fresh_{lab}_{s}.json") for s in SEEDS] for a, (d, lab) in ARMS.items()}
    D = {a: [json.loads((d / f"drift_{lab}_{s}.json").read_text()) for s in SEEDS] for a, (d, lab) in ARMS.items()}
    life = {a: np.array([x["lifespan"] for x in S[a]]) for a in ARMS}

    L += ["| arm | lifespan | median | survived | to 1,000 | fresh lands: survived | drift | agrees with the parent |",
          "|---|---|---|---|---|---|---|---|"]
    table = {}
    for a in ARMS:
        row = {"lifespan": ci(life[a]), "median": round(float(np.median(life[a])), 1),
               "survived": ci([x["survived"] for x in S[a]]), "to1000": ci([x["to1000"] for x in S[a]]),
               "fresh": ci([x["survived"] for x in F[a]]),
               "drift": ci([mean([d["drift"] for d in dd]) for dd in D[a]]),
               "parent": ci([mean([d["parent_agree"] for d in dd]) for dd in D[a]])}
        table[a] = row
        L.append(f"| {a}{' (W3k, cited)' if a == 'CS' else ''} | {f3(row['lifespan'])} | {row['median']} | "
                 f"{f3(row['survived'])} | {f3(row['to1000'])} | {f3(row['fresh'])} | {f3(row['drift'])} | "
                 f"{f3(row['parent'])} |")
    res["table"] = table

    def diff(a, b, level):
        return ci(life[a] - life[b], level)

    def loo(a, b):
        d = life[a] - life[b]
        means = [float(np.delete(d, i).mean()) for i in range(N)]
        return [round(min(means), 1), round(max(means), 1)]

    prim = {"C3S − CS": diff("C3S", "CS", 97.5), "C5S − C3S": diff("C5S", "C3S", 97.5)}
    sec = {k: diff(*k.split(" − "), 95) for k in ("C3S − C3", "C5 − C3", "C3S − C3Y", "C5S − C5Y")}
    res.update(primary=prim, secondary=sec,
               loo={k: loo(*k.split(" − ")) for k in prim},
               medians={k: float(np.median(life[k.split(" − ")[0]] - life[k.split(" − ")[1]])) for k in prim},
               seeds_positive={k: int((life[k.split(" − ")[0]] - life[k.split(" − ")[1]] > 0).sum()) for k in prim})
    yes = lambda t: "yes" if t[1] > 0 else "no"  # noqa: E731
    names = {"C3S − CS": "The longer childhood (and 1.2M more steps) adds to the kept copy",
             "C5S − C3S": "An even longer childhood helps"}
    L += ["", "## Readings (lifespan, paired by seed)", "", "**1. Two primary readings (97.5% intervals, Bonferroni):**"]
    for k, v in prim.items():
        L.append(f"- **{names[k]} ({k}):** {f3(v)} -> **{yes(v)}**; median {res['medians'][k]:.1f}; "
                 f"{res['seeds_positive'][k]} of {N} seeds above 0; leave-one-seed-out means {res['loo'][k]}")
    L.append("**2. Secondary (95%):**")
    for k, v in sec.items():
        L.append(f"- {k}: {f3(v)} -> {yes(v)}")
    best = max(ARMS, key=lambda a: table[a]["lifespan"][0])
    res["best_arm"] = best
    L += [f"**3. Toward the bar:** the best arm by test lifespan is {best}; fresh-land survival "
          f"{f3(table[best]['fresh'])} (bar 0.80)", ""]

    # the kept copies' steps
    L += ["## The kept copies (step, millions)", ""]
    res["kept"] = {}
    for run in ("C3", "C5"):
        meta = [json.loads((OUT / f"{run}_{s}_meta.json").read_text()) for s in SEEDS]
        res["kept"][run] = [{"cs_step": m["cs_step"], "cy_at": m["cy_at"]} for m in meta]
        L += [f"- {run}S: " + ", ".join(f"{(m['cs_step'] or 0) / 1e6:.2f}" for m in meta),
              f"- {run}Y: " + ", ".join(f"{(m['cy_at'] or 0) / 1e6:.2f}" for m in meta)]

    # exploratory: the learning curves
    L += ["", "## Exploratory (labelled): the learning curves", ""]
    for run in ("C3", "C5"):
        steps = sorted({int(p.stem.split("_")[-1][:-1]) for p in OUT.glob(f"test_{run}_*_*k.json")})
        parts = []
        for k in steps:
            v = [summ(OUT / f"test_{run}_{s}_{k}k.json") for s in SEEDS]
            if all(v):
                parts.append(f"{k / 1000:.1f}M {np.mean([x['lifespan'] for x in v]):.0f}")
        L.append(f"- {run}: " + " → ".join(parts) + f" → end {life[run].mean():.0f}")
    (HERE / "analysis.json").write_text(json.dumps(res, indent=1), encoding="utf-8")
    (HERE / "analysis.md").write_text("\n".join(L) + "\n", encoding="utf-8")
    print("\n".join(L))


if __name__ == "__main__":
    main()
