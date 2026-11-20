"""W3n's frozen analysis (questions.md), written before any data.

  python analyse_w3n.py        -> analysis.json, analysis.md
"""
import json
import math
import sys
from pathlib import Path

import numpy as np

sys.stdout.reconfigure(encoding="utf-8")
HERE = Path(__file__).parent
OUT = HERE / "output"
W3M = HERE.parent / "W3m" / "output"
SEEDS = list(range(1, 17))
N = len(SEEDS)
IDX = np.random.default_rng(20261210).integers(0, N, (10_000, N))
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


# arm -> (folder, test label); SL, SLS, SLY are W3m's (the same code with both new parts off, bit for bit)
ARMS = {"SL": (W3M, "SL"), "SLS": (W3M, "SLS"), "SLY": (W3M, "SLY"), "SLS-off": (W3M, "SLS-off"),
        "CR": (OUT, "CR"), "CRS": (OUT, "CRS"), "CRY": (OUT, "CRY"),
        "HR": (OUT, "HR"), "HRS": (OUT, "HRS"), "HRY": (OUT, "HRY"), "HRS-off": (OUT, "HRS-off"),
        "HC": (OUT, "HC"), "HCS": (OUT, "HCS"), "HCY": (OUT, "HCY"), "HCS-off": (OUT, "HCS-off"),
        # GPT (council): the old body (rest at full price), and bare (both reflexes off, the old body)
        "CRS-old": (OUT, "CRS-old"), "HCS-old": (OUT, "HCS-old"),
        "CRS-bare": (OUT, "CRS-bare"), "HRS-bare": (OUT, "HRS-bare"), "HCS-bare": (OUT, "HCS-bare")}


def main():
    checks = (HERE / "checks.log").read_text() if (HERE / "checks.log").exists() else ""
    files = {a: [d / f"test_{lab}_{s}.json" for s in SEEDS] for a, (d, lab) in ARMS.items()}
    missing = [p.name for ps in files.values() for p in ps if not p.exists()]
    L = ["# W3n analysis (the frozen analysis, analyse_w3n.py)", "",
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
        L.append(f"| {a}{' (W3m)' if ARMS[a][0] == W3M else ''} | {f3(row['lifespan'])} | {row['median']} | "
                 f"{f3(row['survived'])} | {f3(row['to1000'])} | {f3(row['fresh'])} | {f3(row['exhausted'])} | "
                 f"{f3(row['hungry'])} |")
    res["table"] = table

    def diff(a, b, level):
        return ci(life[a] - life[b], level)

    def loo(a, b):
        d = life[a] - life[b]
        means = [float(np.delete(d, i).mean()) for i in range(N)]
        return [round(min(means), 1), round(max(means), 1)]

    prim = {"HRS − SLS": diff("HRS", "SLS", 97.5), "CRS − SLS": diff("CRS", "SLS", 97.5)}
    sec = {k: diff(*k.split(" − "), 95) for k in ("HR − SL", "CR − SL", "HCS − HRS", "HCS − CRS", "HRS-off − SLS",
                                                       "HCS-off − SLS", "CRS-old − SLS", "HRS-bare − SLS-off",
                                                       "CRS-bare − SLS-off", "HCS-bare − SLS-off")}
    hungry = {a: np.array([x["hungry"] for x in S[a]]) for a in ARMS}
    sec_tired = ci(hungry["HRS"] - hungry["SLS"])
    res.update(primary=prim, secondary=sec, hungry_HRS_minus_SLS=sec_tired,
               loo={k: loo(*k.split(" − ")) for k in prim},
               medians={k: float(np.median(life[k.split(" − ")[0]] - life[k.split(" − ")[1]])) for k in prim},
               seeds_positive={k: int((life[k.split(" − ")[0]] - life[k.split(" − ")[1]] > 0).sum()) for k in prim})
    yes = lambda t: "yes" if t[1] > 0 else "no"  # noqa: E731
    names = {"HRS − SLS": "The hunger reflex helps", "CRS − SLS": "Cheaper rest helps"}
    L += ["", "## Readings (lifespan, paired by seed)", "", "**1. Two primary readings (97.5% intervals, Bonferroni):**"]
    for k, v in prim.items():
        L.append(f"- **{names[k]} ({k}):** {f3(v)} -> **{yes(v)}**; median {res['medians'][k]:.1f}; "
                 f"{res['seeds_positive'][k]} of {N} seeds above 0; leave-one-seed-out means {res['loo'][k]}")
    L.append("**2. Secondary (95%):**")
    for k, v in sec.items():
        L.append(f"- {k}: {f3(v)} -> {yes(v)}")
    L.append(f"- The share of steps hungry, HRS − SLS: {f3(sec_tired)} -> "
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
    def share(kind, lab):
        vals = []
        for sd in SEEDS:
            p = OUT / f"{kind}_{lab}_{sd}.json"
            if p.exists():
                c = json.loads(p.read_text())
                vals.append((c["forced"] if kind == "reflex" else c["hunger"]) / max(1, c["steps"]))
        return mean(vals)
    res["reflex_share"] = {lab: {"sleep": share("reflex", lab), "hunger": share("hunger", lab)}
                           for lab in ("CRS", "HRS", "HCS")}
    res["sleep_interrupted"] = {lab: mean([json.loads((OUT / f"hunger_{lab}_{sd}.json").read_text()).get("interrupts", 0)
                                           for sd in SEEDS]) for lab in ("HRS", "HCS")}
    res["stale_per_1000"] = {a: mean([mean([l["stale_per_1000"] for l in json.loads(
        (ARMS[a][0] / f"test_{ARMS[a][1]}_{sd}.json").read_text())]) for sd in SEEDS]) for a in ("SLS", "HRS", "HCS")}
    L += ["", "- The share of test steps each reflex took over: " + "; ".join(
          f"{k} sleep {v['sleep']:.3f}, hunger {v['hunger']:.3f}" for k, v in res["reflex_share"].items()),
          "- Arrivals at remembered food that had gone, per 1,000 steps: " + ", ".join(
          f"{k} {v:.2f}" for k, v in res["stale_per_1000"].items()), ""]

    # exploratory: the learning curves
    L += ["## Exploratory (labelled): the learning curves", ""]
    for run in ("CR", "HR", "HC"):
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
