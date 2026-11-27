"""V2-3's frozen analysis (questions.md, Measures), written before any main-run test life was run.
Per seed: the mean over its 50 lives; paired by seed; 95% bootstrap over the 16 seeds (10,000 resamples, generator seeded
V23_SEED). FROZEN = the RMS walker unchanged.
  Primary, per arm (FREE, SLOW, ANCHOR, REHEARSE, REPLAY), both parts needed:
    (a) gain in B: survival on the B test lands (997001-050), arm - FROZEN, lower end > 0;
    (b) no home loss: the Bob Profile vs RMS with no test's lower end below -0.05 (V2-2's rule: each test's main 0-1
        score = the first of success, survived, ratio, tracks in its result, else lifespan / 3000), AND home survival
        (W3r's fresh lands 910001-050) arm - FROZEN lower end > -0.03.
  Judged against FREE (reported): retention arm - FREE (home survival; the Bob Profile mean over its 8 tests).
  "Must beat SLOW on retention at equal or better B gain" (questions.md), defined here before data: a protection P
    beats SLOW if it dominates SLOW, paired by seed: retention = home survival and the Bob Profile mean;
    EITHER B survival P - SLOW lower end > 0 AND both retention differences P - SLOW lower end > -0.03,
    OR some retention difference P - SLOW lower end > 0 AND B survival P - SLOW lower end > -0.03.
  The question is answered YES if at least one protection (ANCHOR, REHEARSE, REPLAY) passes (a) and (b) and beats SLOW.
  Secondaries (never the primary): B and home survival at the 250k and 500k snapshots (arm - FROZEN); mean lifespan in B
    (arm - FROZEN; reported because survival in B may sit at the floor); weight drift from RMS at 1M; REHEARSE's home
    steps; part (a) without the pilot seeds 1-2.
  python analyse_v23.py  -> output/analysis.json, output/analysis.md
"""
from __future__ import annotations

import json
import math
from pathlib import Path

import numpy as np

HERE = Path(__file__).parent
OUT, BP = HERE / "output", HERE / "bp_output"
SEEDS = list(range(1, 17))
ARMS = ("FREE", "SLOW", "ANCHOR", "REHEARSE", "REPLAY")
PROT = ("ANCHOR", "REHEARSE", "REPLAY")
V23_SEED = 20261201
BP_TESTS = ("L2", "R2", "R5d", "M2", "M2e", "G2", "A2", "A5s")


def lives(name):
    L = [json.loads(x) for x in (OUT / name).read_text().splitlines() if x.strip()]
    assert len(L) == 50 and len({x["land"] for x in L}) == 50, (name, len(L))
    return L


def boot(d, seeds=SEEDS):
    d = np.array([d[s] for s in seeds], float)
    idx = np.random.default_rng(V23_SEED).integers(0, len(d), (10_000, len(d)))
    m = d[idx].mean(1)
    return {"mean": float(d.mean()), "lo": float(np.percentile(m, 2.5)), "hi": float(np.percentile(m, 97.5)),
            "n": int(len(d)), "pos": int((d > 0).sum()), "neg": int((d < 0).sum())}


def per_seed(kind, arm, key, tag=""):
    a = "FROZEN" if arm == "FROZEN" else arm
    t = "" if arm == "FROZEN" else tag
    return {s: float(np.mean([float(x[key]) for x in lives(f"{kind}_{a}_{s}{t}.jsonl")])) for s in SEEDS}


def diff(a, b):
    return {s: a[s] - b[s] for s in SEEDS}


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


def bp_mean(sc):
    return {s: float(np.mean([sc[t][s] for t in BP_TESTS])) for s in SEEDS}


def main():
    bs = {a: per_seed("B", a, "survived") for a in ("FROZEN",) + ARMS}
    bl = {a: per_seed("B", a, "lifespan") for a in ("FROZEN",) + ARMS}
    hs = {a: per_seed("H", a, "survived") for a in ("FROZEN",) + ARMS}
    bpr = {w: bp_score(w) for w in ("RMS",) + ARMS}
    bpm = {w: bp_mean(bpr[w]) for w in bpr}
    res = {"means": {a: {"B_survival": float(np.mean(list(bs[a].values()))),
                         "B_lifespan": float(np.mean(list(bl[a].values()))),
                         "home_survival": float(np.mean(list(hs[a].values()))),
                         "bob_profile_mean": float(np.mean(list(bpm["RMS" if a == "FROZEN" else a].values())))}
                     for a in ("FROZEN",) + ARMS}}
    prim = {}
    for a in ARMS:
        ga = boot(diff(bs[a], bs["FROZEN"]))
        tests = {t: boot(diff(bpr[a][t], bpr["RMS"][t])) for t in BP_TESTS}
        worse = [t for t, b in tests.items() if b["lo"] < -0.05]
        home = boot(diff(hs[a], hs["FROZEN"]))
        pa, pb = ga["lo"] > 0, (not worse) and home["lo"] > -0.03
        prim[a] = {"a_B_gain": ga, "a_passed": pa, "b_bob_profile": tests, "b_worse_beyond_margin": worse,
                   "b_home_survival": home, "b_passed": pb, "passed_both": pa and pb,
                   "a_without_pilot_seeds": boot(diff(bs[a], bs["FROZEN"]), SEEDS[2:])}
    res["primary"] = prim
    vs_free, vs_slow = {}, {}
    for p in PROT:
        vs_free[p] = {"home_survival": boot(diff(hs[p], hs["FREE"])), "bob_profile_mean": boot(diff(bpm[p], bpm["FREE"])),
                      "B_survival": boot(diff(bs[p], bs["FREE"]))}
        bB = boot(diff(bs[p], bs["SLOW"]))
        rh, rp = boot(diff(hs[p], hs["SLOW"])), boot(diff(bpm[p], bpm["SLOW"]))
        dom = ((bB["lo"] > 0 and rh["lo"] > -0.03 and rp["lo"] > -0.03) or
               ((rh["lo"] > 0 or rp["lo"] > 0) and bB["lo"] > -0.03))
        vs_slow[p] = {"B_survival": bB, "home_survival": rh, "bob_profile_mean": rp, "beats_slow": bool(dom)}
    res["vs_free"], res["vs_slow"] = vs_free, vs_slow
    res["answer_yes"] = any(prim[p]["passed_both"] and vs_slow[p]["beats_slow"] for p in PROT)
    res["B_lifespan_gain"] = {a: boot(diff(bl[a], bl["FROZEN"])) for a in ARMS}
    snaps = {}
    for k in ("snap250k", "snap500k"):
        snaps[k] = {}
        for a in ARMS:
            try:
                sb = per_seed("B", a, "survived", "_" + k)
                sh = per_seed("H", a, "survived", "_" + k)
            except (FileNotFoundError, AssertionError) as e:
                snaps[k][a] = {"missing": str(e)}
                continue
            snaps[k][a] = {"B_gain": boot(diff(sb, bs["FROZEN"])), "home": boot(diff(sh, hs["FROZEN"]))}
    res["snapshots"] = snaps
    drift, home_steps = {}, {}
    for a in ARMS:
        rows = [json.loads((OUT / f"trainlog_{a}_{s}.json").read_text())["log"][-1] for s in SEEDS]
        drift[a] = float(np.mean([r["drift"] for r in rows]))
        home_steps[a] = float(np.mean([r["home_steps"] for r in rows]))
    res["drift_at_1M"], res["home_steps"] = drift, home_steps
    (OUT / "analysis.json").write_text(json.dumps(res, indent=1))

    f = lambda b: f"{b['mean']:+.3f} [{b['lo']:+.3f}, {b['hi']:+.3f}] ({b['pos']}+/{b['neg']}- of {b['n']})"
    L = ["# V2-3 analysis (frozen script)", "", f"**Answer (a protection passes both parts and beats SLOW): "
         f"{'YES' if res['answer_yes'] else 'NO'}**", "",
         "| arm | B survival | B lifespan | home survival | Bob Profile mean |", "|---|---|---|---|---|"]
    L += [f"| {a} | {v['B_survival']:.3f} | {v['B_lifespan']:.0f} | {v['home_survival']:.3f} | {v['bob_profile_mean']:.3f} |"
          for a, v in res["means"].items()]
    L += ["", "## Primary, per arm"]
    for a, p in prim.items():
        L += [f"- **{a}: both parts {p['passed_both']}** — (a) B gain {f(p['a_B_gain'])} passed {p['a_passed']}; "
              f"(b) home survival {f(p['b_home_survival'])}, Bob Profile worse beyond margin {p['b_worse_beyond_margin']}, "
              f"passed {p['b_passed']}; (a) without seeds 1-2 {f(p['a_without_pilot_seeds'])}"]
    L += ["", "## Protections vs SLOW (dominance rule)"]
    L += [f"- {p}: beats SLOW {v['beats_slow']} — B {f(v['B_survival'])}; home {f(v['home_survival'])}; "
          f"Bob Profile mean {f(v['bob_profile_mean'])}" for p, v in vs_slow.items()]
    L += ["", "## Protections vs FREE"]
    L += [f"- {p}: B {f(v['B_survival'])}; home {f(v['home_survival'])}; Bob Profile mean {f(v['bob_profile_mean'])}"
          for p, v in vs_free.items()]
    L += ["", "## Secondaries", "B lifespan, arm - FROZEN:"] + [f"- {a}: {f(b)}" for a, b in res["B_lifespan_gain"].items()]
    for k, d in snaps.items():
        L += [f"Snapshot {k}:"] + [f"- {a}: " + (v["missing"] if "missing" in v else f"B {f(v['B_gain'])}; home {f(v['home'])}")
                                   for a, v in d.items()]
    L += ["Weight drift from RMS at 1M: " + ", ".join(f"{a} {v:.3f}" for a, v in drift.items()),
          f"REHEARSE home steps (mean): {home_steps['REHEARSE']:.0f}"]
    (OUT / "analysis.md").write_text("\n".join(L) + "\n")
    print("\n".join(L))


if __name__ == "__main__":
    main()
