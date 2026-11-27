"""V2-2 Goals: independent blind recompute.

Written only from questions.md (frozen plan) and the raw files in output/ and bp_output/.
The study's own analysis script and its outputs were NOT opened.

Method: per seed = mean over its 50 lives; differences paired by seed; 95% percentile
bootstrap over the 16 seeds, 10,000 resamples. One resample-index matrix is drawn once
with numpy.random.default_rng(20261128) and reused for every comparison.
"""
import json
import os
import platform
import sys

import numpy as np

BASE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(BASE, "output")
BP = os.path.join(BASE, "bp_output")
SEEDS = list(range(1, 17))
RNG_SEED = 20261128
NBOOT = 10_000
TEST_ARMS = ["GOAL", "GOAL-NOFLOOR", "FT-NOGOAL", "SHAM-GOAL", "GOAL-ABLATE"]
REFS = ["GUIDE-REFLEX", "NO-GUIDE"]
PLAIN = ["RMS", "GOAL", "GOAL-NOFLOOR", "FT-NOGOAL", "SHAM-GOAL"]
BP_TESTS = ["L2", "R2", "R5d", "M2", "M2e", "G2", "A2", "A5s"]
BP_WHO = ["RMS", "GOAL", "GOAL-NOFLOOR", "FT-NOGOAL", "SHAM-GOAL"]
BP_KEYS = ["success", "survived", "ratio", "tracks"]

rng = np.random.default_rng(RNG_SEED)
IDX = rng.integers(0, len(SEEDS), size=(NBOOT, len(SEEDS)))

checks = []


def load_lives(path):
    with open(path, encoding="utf-8") as f:
        return [json.loads(line) for line in f if line.strip()]


def per_seed(prefix, who, field):
    vals = []
    for s in SEEDS:
        p = os.path.join(OUT, f"{prefix}_{who}_{s}.jsonl")
        lives = load_lives(p)
        vals.append(np.mean([float(l[field]) for l in lives]))
    return np.array(vals)


def check_jsonl():
    names = sorted(n for n in os.listdir(OUT) if n.endswith(".jsonl"))
    wanted = ([f"test_{a}_{s}.jsonl" for a in TEST_ARMS for s in SEEDS]
              + [f"ref_{r}_{s}.jsonl" for r in REFS for s in SEEDS]
              + [f"plain_{w}_{s}.jsonl" for w in PLAIN for s in SEEDS])
    missing = [w for w in wanted if w not in names]
    bad = []
    lands_by_prefix = {}
    for n in names:
        lives = load_lives(os.path.join(OUT, n))
        lands = [l["land"] for l in lives]
        if len(lives) != 50 or len(set(lands)) != 50:
            bad.append(f"{n}: {len(lives)} lives, {len(set(lands))} distinct lands")
        pre = n.split("_")[0]
        lands_by_prefix.setdefault(pre, set()).add((min(lands), max(lands)))
    return len(names), len(wanted), missing, bad, lands_by_prefix


def bp_score(d):
    for k in BP_KEYS:
        if k in d:
            return float(d[k])
    return float(d["lifespan"]) / 3000.0


def bp_per_seed(test, who):
    return np.array([bp_score(json.load(open(os.path.join(BP, f"{test}_{who}_{s}.json"),
                                             encoding="utf-8"))) for s in SEEDS])


def boot(diff):
    diff = np.asarray(diff, dtype=float)
    means = diff[IDX].mean(axis=1)
    lo, hi = np.percentile(means, [2.5, 97.5])
    return dict(mean=float(diff.mean()), lo=float(lo), hi=float(hi),
                pos=int((diff > 0).sum()), neg=int((diff < 0).sum()), zero=int((diff == 0).sum()))


def boot_sub(diff, keep):
    """Bootstrap over a subset of seeds (own index matrix, same RNG seed)."""
    d = np.asarray(diff, dtype=float)[keep]
    r = np.random.default_rng(RNG_SEED)
    idx = r.integers(0, len(d), size=(NBOOT, len(d)))
    lo, hi = np.percentile(d[idx].mean(axis=1), [2.5, 97.5])
    return dict(mean=float(d.mean()), lo=float(lo), hi=float(hi),
                pos=int((d > 0).sum()), neg=int((d < 0).sum()), zero=int((d == 0).sum()))


def fmt(r):
    return (f"mean {r['mean']:+.3f}, 95% CI [{r['lo']:+.3f}, {r['hi']:+.3f}], "
            f"seeds +{r['pos']} / -{r['neg']} / ={r['zero']}")


def main():
    L = []
    L.append("# V2-2 Goals: blind recompute")
    L.append("")
    L.append("Done on 2026-11-28 (EST) WITHOUT seeing the study's analysis script (`analyse_v22.py`) "
             "or any of its outputs (analysis.json/.md, findings, roundtable, WORKLOG). Worked only from "
             "`questions.md` and the raw files in `output/` and `bp_output/`.")
    L.append("")
    L.append(f"- Method: per seed = mean over its 50 lives; differences paired by seed; 95% percentile "
             f"bootstrap over 16 seeds, {NBOOT:,} resamples.")
    L.append(f"- RNG: `numpy.random.default_rng({RNG_SEED})`, one 10,000 x 16 index matrix reused for all "
             f"comparisons (the no-pilot-seeds subset uses its own matrix from the same seed).")
    L.append(f"- Python {platform.python_version()}, numpy {np.__version__} ({platform.platform()}).")
    L.append("- Bob Profile score: first present of success, survived, ratio, tracks; else lifespan/3000.")
    L.append("")

    # 7. checks first (so failures are visible)
    nfiles, nwanted, missing, bad, landr = check_jsonl()
    bp_missing = [f"{t}_{w}_{s}.json" for t in BP_TESTS for w in BP_WHO for s in SEEDS
                  if not os.path.exists(os.path.join(BP, f"{t}_{w}_{s}.json"))]

    chains = {a: per_seed("test", a, "chains") for a in TEST_ARMS}
    surv = {a: per_seed("test", a, "survived") for a in TEST_ARMS}
    for r in REFS:
        chains["ref " + r] = per_seed("ref", r, "chains")
        surv["ref " + r] = per_seed("ref", r, "survived")
    plain = {w: per_seed("plain", w, "survived") for w in PLAIN}

    # 1. primary
    L.append("## 1. Primary: chains per life, GOAL - FT-NOGOAL")
    d = chains["GOAL"] - chains["FT-NOGOAL"]
    r1 = boot(d)
    L.append(f"- All 16 seeds: {fmt(r1)}  -> real gain (lower end > 0): {'YES' if r1['lo'] > 0 else 'NO'}")
    keep = np.array([s not in (1, 2) for s in SEEDS])
    r1b = boot_sub(d, keep)
    L.append(f"- Without pilot seeds 1-2 (14 seeds): {fmt(r1b)}")
    L.append("- Per-seed differences: " + ", ".join(f"s{s} {v:+.3f}" for s, v in zip(SEEDS, d)))
    L.append("")

    # 2. retirement vs GUIDE-REFLEX
    L.append("## 2. GOAL - ref GUIDE-REFLEX")
    r2c = boot(chains["GOAL"] - chains["ref GUIDE-REFLEX"])
    r2s = boot(surv["GOAL"] - surv["ref GUIDE-REFLEX"])
    L.append(f"- Chains: {fmt(r2c)}  -> lower end above -0.2: {'YES' if r2c['lo'] > -0.2 else 'NO'}")
    L.append(f"- Survival: {fmt(r2s)}  -> lower end above -0.03: {'YES' if r2s['lo'] > -0.03 else 'NO'}")
    L.append("")

    # 3. ablation
    L.append("## 3. Chains GOAL - GOAL-ABLATE")
    L.append(f"- {fmt(boot(chains['GOAL'] - chains['GOAL-ABLATE']))}")
    L.append("")

    # 4. plain lands
    L.append("## 4. Plain-land survival minus RMS")
    for w in ["GOAL", "FT-NOGOAL", "GOAL-NOFLOOR", "SHAM-GOAL"]:
        r = boot(plain[w] - plain["RMS"])
        tag = "" if w in ("GOAL", "FT-NOGOAL") else " (extra)"
        L.append(f"- {w} - RMS{tag}: {fmt(r)}  -> lower end above -0.03: {'YES' if r['lo'] > -0.03 else 'NO'}")
    L.append("- Plain survival means: " + ", ".join(f"{w} {plain[w].mean():.3f}" for w in PLAIN))
    L.append("")

    # 5. Bob Profile
    L.append("## 5. Bob Profile, paired difference vs RMS")
    bp_flags = {}
    if not bp_missing:
        rms = {t: bp_per_seed(t, "RMS") for t in BP_TESTS}
        for who in ["GOAL", "FT-NOGOAL"]:
            L.append(f"### {who}")
            L.append("| test | RMS mean | arm mean | diff mean | CI lower | CI upper |")
            L.append("|---|---|---|---|---|---|")
            flags = []
            for t in BP_TESTS:
                a = bp_per_seed(t, who)
                r = boot(a - rms[t])
                L.append(f"| {t} | {rms[t].mean():.3f} | {a.mean():.3f} | {r['mean']:+.3f} | "
                         f"{r['lo']:+.3f} | {r['hi']:+.3f} |")
                if r["lo"] < -0.05:
                    flags.append(t)
            bp_flags[who] = flags
            L.append(f"- Tests with CI lower end below -0.05: {', '.join(flags) if flags else 'none'}")
            L.append("")
    else:
        L.append("- Skipped: Bob Profile files missing.")
        L.append("")

    # 6. per-arm means
    L.append("## 6. Per-arm means (mean of 16 per-seed means)")
    L.append("| arm | chains per life | survival |")
    L.append("|---|---|---|")
    for k in list(TEST_ARMS) + ["ref " + r for r in REFS]:
        L.append(f"| {k} | {chains[k].mean():.3f} | {surv[k].mean():.3f} |")
    L.append("")

    # 7. checks
    L.append("## 7. Checks")
    L.append(f"- jsonl files present: {nfiles} in output/ (expected set of {nwanted} test/ref/plain files; "
             f"missing: {len(missing)}{' -> ' + ', '.join(missing) if missing else ''}).")
    L.append(f"- Every jsonl file has 50 lives with 50 distinct lands: "
             f"{'PASS' if not bad else 'FAIL'}{' -> ' + '; '.join(bad) if bad else ''} "
             f"(also checked the unseen_* files present in output/).")
    for pre, rngs in sorted(landr.items()):
        L.append(f"  - {pre}_* land ranges (min-max): {sorted(rngs)}")
    L.append(f"- Bob Profile files (8 tests x 5 WHO x 16 seeds = 640): "
             f"{'PASS, all present' if not bp_missing else 'FAIL, missing ' + str(len(bp_missing)) + ': ' + ', '.join(bp_missing)}")
    L.append("")

    text = "\n".join(L)
    with open(os.path.join(BASE, "recompute_v22_blind.md"), "w", encoding="utf-8") as f:
        f.write(text + "\n")
    print(text)


if __name__ == "__main__":
    sys.exit(main())
