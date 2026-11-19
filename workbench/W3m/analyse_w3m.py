"""W3m's frozen analysis (questions.md), written before any data.

  python analyse_w3m.py        -> analysis.json, analysis.md
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
IDX = np.random.default_rng(20261200).integers(0, N, (10_000, N))
LABELS = ("no_food_known", "food_known_not_reached", "exhaustion")


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
    dead = [l for l in L if l.get("labels")]
    out = {"lifespan": mean([l["lifespan"] for l in L]), "survived": mean([l["survived"] for l in L]),
           "to1000": mean([float(l["lifespan"] >= 1000) for l in L]),
           "exhausted": mean([l["exhausted"] for l in L]), "hungry": mean([l["hungry"] for l in L]),
           "deaths": len(dead)}
    for k in LABELS:
        out[k] = mean([float(d["labels"][k]) for d in dead]) if dead else float("nan")
    return out


# arm -> (folder, test label); R2, CS and CY are W3k's (the same code with both parts off, bit for bit)
ARMS = {"R2": (W3K, "R2"), "CS": (W3K, "CS"), "CY": (W3K, "CY"),
        "SL": (OUT, "SL"), "SLS": (OUT, "SLS"), "SLY": (OUT, "SLY"), "SLS-off": (OUT, "SLS-off"),
        "SR": (OUT, "SR"), "SRS": (OUT, "SRS"), "SRY": (OUT, "SRY"), "SRS-off": (OUT, "SRS-off"),
        "UR": (OUT, "UR"), "URS": (OUT, "URS"), "URY": (OUT, "URY")}


def main():
    checks = (HERE / "checks.log").read_text() if (HERE / "checks.log").exists() else ""
    files = {a: [d / f"test_{lab}_{s}.json" for s in SEEDS] for a, (d, lab) in ARMS.items()}
    missing = [p.name for ps in files.values() for p in ps if not p.exists()]
    L = ["# W3m analysis (the frozen analysis, analyse_w3m.py)", "",
         f"- Checks All: PASS: **{'yes' if 'All: PASS' in checks else 'NO'}**",
         f"- All runs present: **{'yes' if not missing else 'NO, missing ' + ', '.join(missing[:12])}**"]
    cpus = {}
    for p in sorted(OUT.glob("machine_*.json")):
        for rec in json.loads(p.read_text()):
            cpus.setdefault(rec["cpu"], []).append(p.stem.replace("machine_", ""))
    L += ["- Processors seen: " + "; ".join(f"{c} ({len(v)} run parts)" for c, v in cpus.items()), ""]
    res = {}
    if missing:
        (HERE / "analysis.md").write_text("\n".join(L) + "\n", encoding="utf-8")
        print("\n".join(L))
        return

    S = {a: [summ(p) for p in ps] for a, ps in files.items()}
    F = {a: [summ(d / f"test_fresh_{lab}_{s}.json") for s in SEEDS] for a, (d, lab) in ARMS.items()}
    life = {a: np.array([x["lifespan"] for x in S[a]]) for a in ARMS}
    tired = {a: np.array([x["exhausted"] for x in S[a]]) for a in ARMS}

    L += ["| arm | lifespan | median | survived | to 1,000 | fresh lands: survived | steps exhausted | steps hungry |",
          "|---|---|---|---|---|---|---|---|"]
    table = {}
    for a in ARMS:
        row = {"lifespan": ci(life[a]), "median": round(float(np.median(life[a])), 1),
               "survived": ci([x["survived"] for x in S[a]]), "to1000": ci([x["to1000"] for x in S[a]]),
               "fresh": ci([x["survived"] for x in F[a]]), "exhausted": ci(tired[a]),
               "hungry": ci([x["hungry"] for x in S[a]])}
        table[a] = row
        L.append(f"| {a}{' (W3k)' if ARMS[a][0] == W3K else ''} | {f3(row['lifespan'])} | {row['median']} | "
                 f"{f3(row['survived'])} | {f3(row['to1000'])} | {f3(row['fresh'])} | {f3(row['exhausted'])} | "
                 f"{f3(row['hungry'])} |")
    res["table"] = table

    def diff(a, b, level):
        return ci(life[a] - life[b], level)

    def loo(a, b):
        d = life[a] - life[b]
        means = [float(np.delete(d, i).mean()) for i in range(N)]
        return [round(min(means), 1), round(max(means), 1)]

    prim = {"SLS − CS": diff("SLS", "CS", 97.5), "URS − CS": diff("URS", "CS", 97.5)}
    sec = {k: diff(*k.split(" − "), 95) for k in ("SL − R2", "UR − R2", "SLS-off − CS", "SRS − CS",
                                                       "SLS − SRS", "SR − R2", "SRS-off − CS")}
    sec_tired = ci(tired["SLS"] - tired["CS"])
    res.update(primary=prim, secondary=sec, tired_SLS_minus_CS=sec_tired,
               loo={k: loo(*k.split(" − ")) for k in prim},
               medians={k: float(np.median(life[k.split(" − ")[0]] - life[k.split(" − ")[1]])) for k in prim},
               seeds_positive={k: int((life[k.split(" − ")[0]] - life[k.split(" − ")[1]] > 0).sum()) for k in prim})
    yes = lambda t: "yes" if t[1] > 0 else "no"  # noqa: E731
    names = {"SLS − CS": "The sleep reflex helps", "URS − CS": "The tiredness urge helps"}
    L += ["", "## Readings (lifespan, paired by seed)", "", "**1. Two primary readings (97.5% intervals, Bonferroni):**"]
    for k, v in prim.items():
        L.append(f"- **{names[k]} ({k}):** {f3(v)} -> **{yes(v)}**; median {res['medians'][k]:.1f}; "
                 f"{res['seeds_positive'][k]} of {N} seeds above 0; leave-one-seed-out means {res['loo'][k]}")
    L.append("**2. Secondary (95%):**")
    for k, v in sec.items():
        L.append(f"- {k}: {f3(v)} -> {yes(v)}")
    L.append(f"- The share of steps exhausted, SLS − CS: {f3(sec_tired)} -> "
             f"{'lower' if sec_tired[2] < 0 else 'not shown lower'}")
    best = max(ARMS, key=lambda a: table[a]["lifespan"][0])
    res["best_arm"] = best
    L += [f"**3. Toward the bar:** the best arm by test lifespan is {best}; fresh-land survival "
          f"{f3(table[best]['fresh'])} (bar 0.80)", ""]

    # the deaths, and how much the reflex took over
    L += ["## The deaths (share of deaths with each label, mean of seeds; labels overlap)", "",
          "| arm | deaths per 50 | no food known | food known, not reached | exhaustion |", "|---|---|---|---|---|"]
    res["deaths"] = {}
    for a in ARMS:
        d = {k: mean([x[k] for x in S[a]]) for k in ("deaths",) + LABELS}
        res["deaths"][a] = d
        L.append(f"| {a} | {d['deaths']:.1f} | {d['no_food_known']:.2f} | {d['food_known_not_reached']:.2f} | "
                 f"{d['exhaustion']:.2f} |")
    rx = {lab: mean([json.loads((OUT / f"reflex_{lab}_{s}.json").read_text())["forced"]
                     / max(1, json.loads((OUT / f"reflex_{lab}_{s}.json").read_text())["steps"]) for s in SEEDS])
          for lab in ("SL", "SLS", "SLY", "SR", "SRS", "SRY")}
    res["reflex_share"] = rx
    L += ["", "- The share of test steps the reflex took over: " + ", ".join(f"{k} {v:.3f}" for k, v in rx.items()), ""]

    # exploratory: the learning curves
    L += ["## Exploratory (labelled): the learning curves", ""]
    for run in ("SL", "SR", "UR"):
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
