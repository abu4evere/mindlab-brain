"""CW2's frozen analysis (questions.md, Measures). Reads output/{ARM}_{SEED}.jsonl (50 lives per arm and seed).
Per seed: the mean over its 50 lives; differences paired by seed; 95% bootstrap over the 16 seeds (10,000 resamples,
generator seeded CW2_SEED).
  Primary: mean completed chains per life, GUIDE-REFLEX - NO-GUIDE (a real gain if the lower end is above 0).
  Key secondary (GPT's reading rule): GUIDE-MAP - NO-GUIDE.
  Named secondaries: GUIDE-REFLEX - SHAM-REFLEX, GUIDE-MAP - SHAM-MAP; each GUIDE - RANDOM-OPS; carrying time (steps
  from holding A and B to the next join); joins made on a station guide; returns to the station after the first join;
  hand acts per carrying step; survival and lifespan, each GUIDE - NO-GUIDE (a cost check only).
  python analyse_cw2.py  -> output/analysis.json, output/analysis.md
"""
from __future__ import annotations

import json
import math
from pathlib import Path

import numpy as np

HERE = Path(__file__).parent
OUT = HERE / "output"
ARMS = ("GUIDE-REFLEX", "GUIDE-MAP", "SHAM-REFLEX", "SHAM-MAP", "NO-GUIDE", "RANDOM-OPS")
SEEDS = range(1, 17)
CW2_SEED = 20261128


def load():
    d = {}
    for a in ARMS:
        for s in SEEDS:
            p = OUT / f"{a}_{s}.jsonl"
            L = [json.loads(x) for x in p.read_text().splitlines() if x.strip()]
            assert len(L) == 50 and len({x["land"] for x in L}) == 50, (p, len(L))
            d[a, s] = L
    return d


def per_seed(d, arm, f):
    return np.array([f(d[arm, s]) for s in SEEDS], float)


def boot(diff, B=10_000):
    diff = diff[~np.isnan(diff)]
    if len(diff) == 0:
        return {"mean": math.nan, "lo": math.nan, "hi": math.nan, "seeds": 0, "positive_seeds": 0, "negative_seeds": 0}
    rng = np.random.default_rng(CW2_SEED)
    idx = rng.integers(0, len(diff), (B, len(diff)))
    m = diff[idx].mean(1)
    return {"mean": float(diff.mean()), "lo": float(np.percentile(m, 2.5)), "hi": float(np.percentile(m, 97.5)),
            "seeds": int(len(diff)), "positive_seeds": int((diff > 0).sum()), "negative_seeds": int((diff < 0).sum())}


def mean(L, key):
    return float(np.mean([x[key] for x in L]))


def carry_time(L):
    tot = sum(x["carry_to_join_mean"] * x["carry_to_join_n"] for x in L if x["carry_to_join_n"])
    n = sum(x["carry_to_join_n"] for x in L)
    return tot / n if n else math.nan


def acts_per_carry(L):
    c = sum(x["carry_steps"] for x in L)
    return sum(x["acts_while_carrying"] for x in L) / c if c else math.nan


MEASURES = {
    "mean_chains": lambda L: mean(L, "chains"),
    "share_1plus": lambda L: float(np.mean([x["chains"] >= 1 for x in L])),
    "share_3plus": lambda L: float(np.mean([x["chains"] >= 3 for x in L])),
    "carry_time": carry_time,
    "joins_on_station_guide": lambda L: mean(L, "joins_on_guide"),
    "station_returns": lambda L: mean(L, "station_arrivals_after_first_join"),
    "station_guides": lambda L: mean(L, "station_guides"),
    "acts_per_carry_step": acts_per_carry,
    "lifespan": lambda L: mean(L, "lifespan"),
    "survival": lambda L: mean(L, "survived"),
    "acts": lambda L: mean(L, "acts"),
}


def main():
    d = load()
    am = {a: {k: float(np.nanmean(per_seed(d, a, f))) for k, f in MEASURES.items()} for a in ARMS}
    diff = lambda a, b, k: boot(per_seed(d, a, MEASURES[k]) - per_seed(d, b, MEASURES[k]))
    res = {"lives_per_arm": {a: sum(len(d[a, s]) for s in SEEDS) for a in ARMS}, "arm_means": am}
    res["primary"] = diff("GUIDE-REFLEX", "NO-GUIDE", "mean_chains")
    res["primary"]["real_gain"] = res["primary"]["lo"] > 0
    res["key_secondary_MAP"] = diff("GUIDE-MAP", "NO-GUIDE", "mean_chains")
    res["key_secondary_MAP"]["real_gain"] = res["key_secondary_MAP"]["lo"] > 0
    res["secondaries"] = {
        "REFLEX-SHAM_chains": diff("GUIDE-REFLEX", "SHAM-REFLEX", "mean_chains"),
        "MAP-SHAM_chains": diff("GUIDE-MAP", "SHAM-MAP", "mean_chains"),
        "REFLEX-RANDOM_chains": diff("GUIDE-REFLEX", "RANDOM-OPS", "mean_chains"),
        "MAP-RANDOM_chains": diff("GUIDE-MAP", "RANDOM-OPS", "mean_chains"),
        "REFLEX-NOGUIDE_share_1plus": diff("GUIDE-REFLEX", "NO-GUIDE", "share_1plus"),
        "REFLEX-NOGUIDE_carry_time": diff("GUIDE-REFLEX", "NO-GUIDE", "carry_time"),
        "MAP-NOGUIDE_carry_time": diff("GUIDE-MAP", "NO-GUIDE", "carry_time"),
        "REFLEX-NOGUIDE_station_returns": diff("GUIDE-REFLEX", "NO-GUIDE", "station_returns"),
        "MAP-NOGUIDE_station_returns": diff("GUIDE-MAP", "NO-GUIDE", "station_returns"),
        "REFLEX-NOGUIDE_survival": diff("GUIDE-REFLEX", "NO-GUIDE", "survival"),
        "MAP-NOGUIDE_survival": diff("GUIDE-MAP", "NO-GUIDE", "survival"),
        "REFLEX-NOGUIDE_lifespan": diff("GUIDE-REFLEX", "NO-GUIDE", "lifespan"),
        "MAP-NOGUIDE_lifespan": diff("GUIDE-MAP", "NO-GUIDE", "lifespan"),
    }
    res["machines"] = sorted({json.dumps(x["machine"], sort_keys=True) for L in d.values() for x in L})
    (OUT / "analysis.json").write_text(json.dumps(res, indent=1))
    f = lambda b: (f"{b['mean']:+.3f} [{b['lo']:+.3f}, {b['hi']:+.3f}] ({b['positive_seeds']}+/{b['negative_seeds']}- "
                   f"of {b['seeds']} seeds)")
    L = ["# CW2 analysis (frozen script)", "", f"Lives per arm: {res['lives_per_arm']}", "",
         f"**Primary: mean chains per life, GUIDE-REFLEX - NO-GUIDE = {f(res['primary'])}; real gain: "
         f"{res['primary']['real_gain']}**", "",
         f"**Key secondary (GPT's reading rule): GUIDE-MAP - NO-GUIDE = {f(res['key_secondary_MAP'])}; real gain: "
         f"{res['key_secondary_MAP']['real_gain']}**", "",
         "| measure | " + " | ".join(ARMS) + " |", "|---" * (len(ARMS) + 1) + "|"]
    for k in MEASURES:
        L.append(f"| {k} | " + " | ".join(f"{am[a][k]:.3f}" for a in ARMS) + " |")
    L += ["", "Secondaries:"] + [f"- {k}: {f(b)}" for k, b in res["secondaries"].items()]
    L += ["", f"Machines: {len(res['machines'])}"] + [f"- {m}" for m in res["machines"]]
    (OUT / "analysis.md").write_text("\n".join(L) + "\n")
    print("\n".join(L))


if __name__ == "__main__":
    main()
