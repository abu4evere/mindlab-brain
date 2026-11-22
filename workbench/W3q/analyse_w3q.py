"""W3q's frozen analysis (questions.md), written before any data (after the tag W3q-frozen, before any W3q run).
Paired by seed (1-8); bootstrap over seeds, numpy seed 20261123, 10,000 resamples, 95% (2.5th and 97.5th percentiles);
every seed's difference listed.

Inputs: output/probe_<ARM>_<SEED>.json for BF, BP, RP and HR (probe_w3q.py); test files in output/ (BF, BP, RP) and in
W3n/output (HR); output/dose_<ARM>_<SEED>.json.

  python analyse_w3q.py        -> analysis.json, analysis.md
"""
import json
import sys
from pathlib import Path

import numpy as np

sys.stdout.reconfigure(encoding="utf-8")
HERE = Path(__file__).parent
OUT = HERE / "output"
W3N = HERE.parent / "W3n" / "output"
SEEDS = list(range(1, 9))
IDX = np.random.default_rng(20261123).integers(0, len(SEEDS), (10_000, len(SEEDS)))
TIMES = ("2400k", "2800k", "3200k", "3600k", "final", "S")
MARGIN, MARGIN2, LIFE_MARGIN = 0.10, 0.05, -200.0


def ci(v):
    v = np.asarray(v, float)
    m = v[IDX].mean(axis=1)
    return [round(float(v.mean()), 4), round(float(np.percentile(m, 2.5)), 4), round(float(np.percentile(m, 97.5)), 4)]


def f(t, d=3):
    return f"{t[0]:+.{d}f} [{t[1]:+.{d}f}, {t[2]:+.{d}f}]"


def probe(arm, seed, time, key):
    p = OUT / f"probe_{arm}_{seed}.json"
    if not p.exists():
        return None
    v = json.loads(p.read_text()).get(time)
    return None if v is None else v[key]


def test(arm, label, seed, key):
    p = (W3N if arm == "HR" else OUT) / f"test_{label}_{seed}.json"
    if not p.exists():
        return None
    return float(np.mean([l[key] for l in json.loads(p.read_text())]))


def verdict(t, margin):
    return "rejected" if t[2] < margin else "kept" if t[1] > margin else "unclear"


def main():
    L = ["# W3q analysis (the frozen analysis, analyse_w3q.py)", ""]
    checks = (HERE / "checks.log").read_text() if (HERE / "checks.log").exists() else ""
    vals = {}
    for arm in ("BF", "BP", "RP", "HR"):
        for t in TIMES:
            for k in ("lie", "truth", "corner_first", "steps", "rand_lie"):
                vals[(arm, t, k)] = [probe(arm, s, t, k) for s in SEEDS]
    tests = {}
    for arm in ("BF", "BP", "RP", "HR"):
        for lab, key, what in ((f"{arm}", "lifespan", "final, reflexes"), (f"{arm}S", "lifespan", "kept, reflexes"),
                               (f"{arm}S-bare", "lifespan", "kept, bare"), (f"fresh_{arm}", "survived", "final, fresh"),
                               (f"fresh_{arm}S", "survived", "kept, fresh")):
            tests[(arm, what)] = [test(arm, lab, s, key) for s in SEEDS]
    missing = [f"{k}" for k, v in {**vals, **tests}.items() if any(x is None for x in v)
               and not (k[1] == "S" and k[0] == "HR" and False)]
    L += [f"- Checks All: PASS: **{'yes' if 'All: PASS' in checks else 'NO'}**",
          f"- All inputs present: **{'yes' if not missing else 'NO: ' + '; '.join(missing[:8])}**", ""]
    if missing:
        (HERE / "analysis.md").write_text("\n".join(L) + "\n", encoding="utf-8")
        print("\n".join(L))
        return
    a = lambda arm, t, k: np.array(vals[(arm, t, k)], float)
    res = {"probe": {}, "diff": {}, "tests": {}, "dose": {}}
    # 1. the manipulation check
    man = ci(a("BF", "2400k", "lie") - a("HR", "2400k", "lie"))
    res["manipulation"] = {"BF-HR 2.4M lie": man, "passed": bool(man[1] > 0)}
    # 2-3. the primaries
    pa = ci(a("BF", "final", "lie") - a("HR", "final", "lie"))
    pb = ci(a("BP", "final", "lie") - a("RP", "final", "lie"))
    res["primary"] = {"A BF-HR final lie": pa, "A verdict": verdict(pa, MARGIN), "A verdict at +0.05": verdict(pa, MARGIN2),
                      "B BP-RP final lie": pb, "B verdict": verdict(pb, MARGIN), "B verdict at +0.05": verdict(pb, MARGIN2)}
    seeds_a = [round(float(x), 3) for x in a("BF", "final", "lie") - a("HR", "final", "lie")]
    seeds_b = [round(float(x), 3) for x in a("BP", "final", "lie") - a("RP", "final", "lie")]
    L += ["## Manipulation check (did the child learn the lie?)", "",
          f"- BF − HR at the end of childhood (2.4M), toward the lie: {f(man)} -> **{'passed' if man[1] > 0 else 'FAILED: the study reads manipulation failed'}**", "",
          "## Primary", "",
          f"- **A, recovery after the parent leaves (BF − HR, final):** {f(pa)} -> **{verdict(pa, MARGIN)}** (at +0.05: {verdict(pa, MARGIN2)}); seeds {seeds_a}",
          f"- **B, resistance while the parent keeps teaching (BP − RP, final):** {f(pb)} -> **{verdict(pb, MARGIN)}** (at +0.05: {verdict(pb, MARGIN2)}); seeds {seeds_b}", ""]
    if not man[1] > 0:
        L += ["(The manipulation check failed: A and B say little about rejecting a lie.)", ""]
    # the time course and the other probe readings
    L += ["## The probe over time (mean share; random policy toward the lie about "
          f"{float(np.mean(a('HR', 'final', 'rand_lie'))):.3f})", "",
          "| copy | " + " | ".join(f"{x} lie" for x in ("BF", "BP", "RP", "HR")) + " | BF − HR | BP − RP | " +
          " | ".join(f"{x} truth" for x in ("BF", "BP", "RP", "HR")) + " |", "|---" * 11 + "|"]
    for t in TIMES:
        d1, d2 = ci(a("BF", t, "lie") - a("HR", t, "lie")), ci(a("BP", t, "lie") - a("RP", t, "lie"))
        res["probe"][t] = {x: {k: ci(a(x, t, k)) for k in ("lie", "truth", "corner_first", "steps")} for x in ("BF", "BP", "RP", "HR")}
        res["diff"][t] = {"BF-HR lie": d1, "BP-RP lie": d2,
                          "BF-HR truth": ci(a("BF", t, "truth") - a("HR", t, "truth")),
                          "BP-RP truth": ci(a("BP", t, "truth") - a("RP", t, "truth")),
                          "BF-HR corner_first": ci(a("BF", t, "corner_first") - a("HR", t, "corner_first")),
                          "BP-RP corner_first": ci(a("BP", t, "corner_first") - a("RP", t, "corner_first")),
                          "BF-HR steps": ci(a("BF", t, "steps") - a("HR", t, "steps")),
                          "BP-RP steps": ci(a("BP", t, "steps") - a("RP", t, "steps"))}
        L.append(f"| {t} | " + " | ".join(f"{np.mean(a(x, t, 'lie')):.3f}" for x in ("BF", "BP", "RP", "HR")) +
                 f" | {f(d1)} | {f(d2)} | " + " | ".join(f"{np.mean(a(x, t, 'truth')):.3f}" for x in ("BF", "BP", "RP", "HR")) + " |")
    df = res["diff"]["final"]
    L += ["", "## Secondary (final brains unless named)", "",
          f"- Toward the truth: BF − HR {f(df['BF-HR truth'])}; BP − RP {f(df['BP-RP truth'])}",
          f"- The walk, a corner entered before food: BF − HR {f(df['BF-HR corner_first'])}; BP − RP {f(df['BP-RP corner_first'])}",
          f"- The walk, steps to food: BF − HR {f(df['BF-HR steps'], 1)}; BP − RP {f(df['BP-RP steps'], 1)}", ""]
    L += ["| measure | BF | BP | RP | HR | BF − HR | BP − RP | RP − HR |", "|---|---|---|---|---|---|---|---|"]
    for what in ("final, reflexes", "kept, reflexes", "kept, bare", "final, fresh", "kept, fresh"):
        t = {x: np.array(tests[(x, what)], float) for x in ("BF", "BP", "RP", "HR")}
        d = {"BF-HR": ci(t["BF"] - t["HR"]), "BP-RP": ci(t["BP"] - t["RP"]), "RP-HR": ci(t["RP"] - t["HR"])}
        res["tests"][what] = {"means": {x: ci(t[x]) for x in t}, "diff": d}
        dd = 1 if "fresh" not in what else 3
        L.append(f"| {what} ({'survived' if 'fresh' in what else 'lifespan'}) | " + " | ".join(f"{t[x].mean():.{dd}f}" for x in t)
                 + f" | {f(d['BF-HR'], dd)} | {f(d['BP-RP'], dd)} | {f(d['RP-HR'], dd)} |")
    life = res["tests"]["final, reflexes"]["diff"]
    L += ["", f"- Lifespan loss small (lower bound above {LIFE_MARGIN:.0f}): BF − HR **{life['BF-HR'][1] > LIFE_MARGIN}**; "
              f"BP − RP **{life['BP-RP'][1] > LIFE_MARGIN}**", ""]
    # the dose
    L += ["## The dose (the lying parent's choices that differ from the right parent's)", ""]
    for arm in ("BF", "BP"):
        ds = [json.loads((OUT / f"dose_{arm}_{s}.json").read_text()) if (OUT / f"dose_{arm}_{s}.json").exists() else None for s in SEEDS]
        ok = [d for d in ds if d]
        share = [d["lies"] / max(1, d["acts"]) for d in ok]
        res["dose"][arm] = {"seeds": len(ok), "lies": [d["lies"] for d in ok], "share": [round(x, 3) for x in share]}
        L.append(f"- {arm}: {len(ok)} seeds; lies per run {[d['lies'] for d in ok]}; share of the parent's choices "
                 f"{[round(x, 3) for x in share]} (a copy lesson every 4th step)")
    (HERE / "analysis.json").write_text(json.dumps(res, indent=1), encoding="utf-8")
    (HERE / "analysis.md").write_text("\n".join(L) + "\n", encoding="utf-8")
    print("\n".join(L))


if __name__ == "__main__":
    main()
