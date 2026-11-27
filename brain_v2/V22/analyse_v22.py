"""V2-2's frozen analysis (questions.md, Measures), written before any test life was run.
Per seed: the mean over its 50 lives; paired by seed; 95% bootstrap over the 16 seeds (10,000 resamples, generator seeded
V22_SEED). Also the primary without seeds 1-2 (the pilot seeds; GPT).
  Primary: chains per life, GOAL - FT-NOGOAL (test lands 990001-050); real gain if the lower end > 0.
  Retirement test (all must hold): chains GOAL - GUIDE-REFLEX lower end > -0.2; survival GOAL - GUIDE-REFLEX lower end
    > -0.03; the Bob Profile of GOAL vs RMS with no test worse beyond its margin.
  The Bob Profile margin (questions.md says "its margin" without a number; defined here, before data): for each of the
    8 tests, the test's main 0-1 score (the first of success, survived, ratio, tracks present in its result; else
    lifespan / 3000), paired by seed, arm - RMS; "worse beyond its margin" = the lower end of the 95% bootstrap below
    -0.05.
  No-loss gates (every fine-tuned arm): plain W3r lands survival arm - RMS lower end > -0.03; the Bob Profile as above;
    the unseen world (chains and survival reported, GOAL - FT-NOGOAL).
  Secondaries: GOAL - SHAM-GOAL; GOAL - GOAL-ABLATE; GOAL-NOFLOOR - GOAL (chains, survival); goal pursuit by energy band
    (share of goal steps that moved closer, energy < 150 vs >= 150); references GUIDE-REFLEX and NO-GUIDE.
  python analyse_v22.py  -> output/analysis.json, output/analysis.md
"""
from __future__ import annotations

import json
import math
from pathlib import Path

import numpy as np

HERE = Path(__file__).parent
OUT, BP = HERE / "output", HERE / "bp_output"
SEEDS = list(range(1, 17))
FT = ("GOAL", "GOAL-NOFLOOR", "FT-NOGOAL", "SHAM-GOAL")
V22_SEED = 20261130
BP_TESTS = ("L2", "R2", "R5d", "M2", "M2e", "G2", "A2", "A5s")


def lives(name):
    L = [json.loads(x) for x in (OUT / name).read_text().splitlines() if x.strip()]
    assert len(L) == 50 and len({x["land"] for x in L}) == 50, (name, len(L))
    return L


def boot(d, seeds=SEEDS):
    d = np.array([d[s] for s in seeds], float)
    d = d[~np.isnan(d)]
    if not len(d):
        return {"mean": math.nan, "lo": math.nan, "hi": math.nan, "n": 0, "pos": 0, "neg": 0}
    idx = np.random.default_rng(V22_SEED).integers(0, len(d), (10_000, len(d)))
    m = d[idx].mean(1)
    return {"mean": float(d.mean()), "lo": float(np.percentile(m, 2.5)), "hi": float(np.percentile(m, 97.5)),
            "n": int(len(d)), "pos": int((d > 0).sum()), "neg": int((d < 0).sum())}


def per_seed(prefix, arm, key):
    return {s: float(np.mean([float(x[key]) for x in lives(f"{prefix}_{arm}_{s}.jsonl")])) for s in SEEDS}


def diff(a, b):
    return {s: a[s] - b[s] for s in SEEDS}


def pursuit(prefix, arm, band):
    out = {}
    for s in SEEDS:
        L = lives(f"{prefix}_{arm}_{s}.jsonl")
        steps = sum(x[f"goal_steps_{band}"] for x in L)
        out[s] = sum(x[f"toward_{band}"] for x in L) / steps if steps else math.nan
    return out


def bp_score(who):
    res = {}
    for t in BP_TESTS:
        vals = {}
        for s in SEEDS:
            d = json.loads((BP / f"{t}_{who}_{s}.json").read_text())
            key = next((k for k in ("success", "survived", "ratio", "tracks") if k in d), None)
            vals[s] = float(d[key]) if key else float(d["lifespan"]) / 3000.0
        res[t] = vals
    return res


def main():
    ch = {a: per_seed("test", a, "chains") for a in FT + ("GOAL-ABLATE",)}
    sv = {a: per_seed("test", a, "survived") for a in FT + ("GOAL-ABLATE",)}
    for r in ("GUIDE-REFLEX", "NO-GUIDE"):
        ch[r], sv[r] = per_seed("ref", r, "chains"), per_seed("ref", r, "survived")
    res = {"means": {a: {"chains": float(np.mean(list(ch[a].values()))), "survival": float(np.mean(list(sv[a].values())))}
                     for a in ch}}
    res["primary"] = boot(diff(ch["GOAL"], ch["FT-NOGOAL"]))
    res["primary"]["real_gain"] = res["primary"]["lo"] > 0
    res["primary_without_pilot_seeds"] = boot(diff(ch["GOAL"], ch["FT-NOGOAL"]), SEEDS[2:])
    bpr = {w: bp_score(w) for w in ("RMS",) + FT}
    bp_gate = {}
    for w in FT:
        tests = {t: boot(diff(bpr[w][t], bpr["RMS"][t])) for t in BP_TESTS}
        worse = [t for t, b in tests.items() if b["lo"] < -0.05]
        bp_gate[w] = {"tests": tests, "worse_beyond_margin": worse, "passed": not worse}
    res["bob_profile"] = bp_gate
    plain = {w: per_seed("plain", w, "survived") for w in ("RMS",) + FT}
    res["plain_gate"] = {w: boot(diff(plain[w], plain["RMS"])) for w in FT}
    for w in FT:
        res["plain_gate"][w]["passed"] = res["plain_gate"][w]["lo"] > -0.03
    rc = boot(diff(ch["GOAL"], ch["GUIDE-REFLEX"]))
    rs = boot(diff(sv["GOAL"], sv["GUIDE-REFLEX"]))
    res["retirement"] = {"chains_vs_reflex": rc, "survival_vs_reflex": rs,
                         "passed": rc["lo"] > -0.2 and rs["lo"] > -0.03 and bp_gate["GOAL"]["passed"]}
    uc = {a: per_seed("unseen", a, "chains") for a in FT}
    us = {a: per_seed("unseen", a, "survived") for a in FT}
    res["unseen"] = {"means": {a: {"chains": float(np.mean(list(uc[a].values()))), "survival": float(np.mean(list(us[a].values())))} for a in FT},
                     "GOAL-FT-NOGOAL_chains": boot(diff(uc["GOAL"], uc["FT-NOGOAL"])),
                     "GOAL-FT-NOGOAL_survival": boot(diff(us["GOAL"], us["FT-NOGOAL"]))}
    res["secondaries"] = {
        "GOAL-SHAM-GOAL_chains": boot(diff(ch["GOAL"], ch["SHAM-GOAL"])),
        "GOAL-GOAL-ABLATE_chains": boot(diff(ch["GOAL"], ch["GOAL-ABLATE"])),
        "GOAL-NOFLOOR-GOAL_chains": boot(diff(ch["GOAL-NOFLOOR"], ch["GOAL"])),
        "GOAL-NOFLOOR-GOAL_survival": boot(diff(sv["GOAL-NOFLOOR"], sv["GOAL"])),
        "GOAL-NO-GUIDE_chains": boot(diff(ch["GOAL"], ch["NO-GUIDE"])),
        "FT-NOGOAL-NO-GUIDE_chains": boot(diff(ch["FT-NOGOAL"], ch["NO-GUIDE"])),
    }
    res["pursuit"] = {a: {b: float(np.nanmean(list(pursuit("test", a, b).values()))) for b in ("hungry", "fed")}
                      for a in ("GOAL", "GOAL-NOFLOOR", "SHAM-GOAL")}
    (OUT / "analysis.json").write_text(json.dumps(res, indent=1))
    f = lambda b: f"{b['mean']:+.3f} [{b['lo']:+.3f}, {b['hi']:+.3f}] ({b['pos']}+/{b['neg']}- of {b['n']})"
    L = ["# V2-2 analysis (frozen script)", "",
         f"**Primary: chains per life GOAL - FT-NOGOAL = {f(res['primary'])}; real gain: {res['primary']['real_gain']}**",
         f"Without the pilot seeds 1-2: {f(res['primary_without_pilot_seeds'])}", "",
         f"**Retirement test: passed = {res['retirement']['passed']}** (chains vs the carry reflex {f(rc)}; survival {f(rs)}; "
         f"Bob Profile worse beyond margin: {bp_gate['GOAL']['worse_beyond_margin']})", "",
         "| arm | chains | survival |", "|---|---|---|"]
    L += [f"| {a} | {v['chains']:.3f} | {v['survival']:.3f} |" for a, v in res["means"].items()]
    L += ["", "Plain-land gate (survival vs RMS):"] + [f"- {w}: {f(b)} passed {b['passed']}" for w, b in res["plain_gate"].items()]
    L += ["", "Bob Profile gate:"] + [f"- {w}: passed {g['passed']}, worse: {g['worse_beyond_margin']}" for w, g in bp_gate.items()]
    L += ["", "Unseen world:"] + [f"- {a}: chains {v['chains']:.3f}, survival {v['survival']:.3f}" for a, v in res["unseen"]["means"].items()]
    L += [f"- GOAL - FT-NOGOAL chains {f(res['unseen']['GOAL-FT-NOGOAL_chains'])}; survival {f(res['unseen']['GOAL-FT-NOGOAL_survival'])}"]
    L += ["", "Secondaries:"] + [f"- {k}: {f(b)}" for k, b in res["secondaries"].items()]
    L += ["", "Goal pursuit (share of goal steps moving closer):"] + [f"- {a}: hungry {v['hungry']:.3f}, fed {v['fed']:.3f}" for a, v in res["pursuit"].items()]
    (OUT / "analysis.md").write_text("\n".join(L) + "\n")
    print("\n".join(L))


if __name__ == "__main__":
    main()
