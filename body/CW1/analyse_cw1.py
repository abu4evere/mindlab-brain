"""CW1's frozen analysis (questions.md, Measures). Reads output/{ARM}_{SEED}.jsonl (50 lives per arm and seed).
Per seed: the mean over its 50 lives; differences paired by seed; 95% bootstrap over the 16 seeds (10,000 resamples,
generator seeded CW1_SEED).
  Primary: mean completed chains per life, LEARN - RANDOM-OPS (a real gain if the interval's lower end is above 0).
  Named secondaries (LEARN - RANDOM-OPS): share of lives with 3+ chains, with at least 1; chains per 1,000 steps alive;
    steps to the first join (lives with a join); partial progress (took A, took B, joined, ate C: shares of lives);
    reuse after discovery (chains after the first); the dead-action rate (dead acts / acts).
  Other: LEARN - NO-MAKE in lifespan and full-life survival; PAD - LEARN in mean chains and first-join latency.
  python analyse_cw1.py  -> output/analysis.json, output/analysis.md
"""
from __future__ import annotations

import json
import math
from pathlib import Path

import numpy as np

HERE = Path(__file__).parent
OUT = HERE / "output"
ARMS = ("LEARN", "RANDOM-OPS", "NO-MAKE", "PAD")
SEEDS = range(1, 17)
CW1_SEED = 20261127


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
    """f(lives) -> a number or nan; returns the 16 per-seed values."""
    return np.array([f(d[arm, s]) for s in SEEDS], float)


def boot(diff, B=10_000):
    diff = diff[~np.isnan(diff)]
    rng = np.random.default_rng(CW1_SEED)
    idx = rng.integers(0, len(diff), (B, len(diff)))
    m = diff[idx].mean(1)
    return {"mean": float(diff.mean()), "lo": float(np.percentile(m, 2.5)), "hi": float(np.percentile(m, 97.5)),
            "seeds": int(len(diff)), "positive_seeds": int((diff > 0).sum()), "negative_seeds": int((diff < 0).sum())}


def mean(L, key):
    return float(np.mean([x[key] for x in L]))


def share(L, cond):
    return float(np.mean([bool(cond(x)) for x in L]))


def latency(L):
    v = [x["first_join"] for x in L if x["first_join"] is not None]
    return float(np.mean(v)) if v else math.nan


def dead_rate(L):
    acts = sum(x["acts"] for x in L)
    return sum(x["dead_acts"] for x in L) / acts if acts else math.nan


MEASURES = {
    "mean_chains": lambda L: mean(L, "chains"),
    "share_3plus": lambda L: share(L, lambda x: x["chains"] >= 3),
    "share_1plus": lambda L: share(L, lambda x: x["chains"] >= 1),
    "chains_per_1000": lambda L: mean(L, "chains_per_1000"),
    "first_join_latency": latency,
    "took_A": lambda L: share(L, lambda x: x["took_A"] > 0),
    "took_B": lambda L: share(L, lambda x: x["took_B"] > 0),
    "joined": lambda L: share(L, lambda x: x["joins"] > 0),
    "ate_C": lambda L: share(L, lambda x: x["chains"] > 0),
    "reuse": lambda L: mean(L, "reuse"),
    "dead_action_rate": dead_rate,
    "lifespan": lambda L: mean(L, "lifespan"),
    "survival": lambda L: mean(L, "survived"),
    "acts": lambda L: mean(L, "acts"),
    "moments": lambda L: mean(L, "moments"),
}


def main():
    d = load()
    arm_means = {a: {k: float(np.nanmean(per_seed(d, a, f))) for k, f in MEASURES.items()} for a in ARMS}
    res = {"lives_per_arm": {a: sum(len(d[a, s]) for s in SEEDS) for a in ARMS}, "arm_means": arm_means}
    res["primary"] = boot(per_seed(d, "LEARN", MEASURES["mean_chains"]) - per_seed(d, "RANDOM-OPS", MEASURES["mean_chains"]))
    res["primary"]["real_gain"] = res["primary"]["lo"] > 0
    res["secondary_LEARN_minus_RANDOM"] = {
        k: boot(per_seed(d, "LEARN", MEASURES[k]) - per_seed(d, "RANDOM-OPS", MEASURES[k]))
        for k in ("share_3plus", "share_1plus", "chains_per_1000", "first_join_latency", "took_A", "took_B",
                  "joined", "ate_C", "reuse", "dead_action_rate")}
    res["LEARN_minus_NO-MAKE"] = {k: boot(per_seed(d, "LEARN", MEASURES[k]) - per_seed(d, "NO-MAKE", MEASURES[k]))
                                  for k in ("lifespan", "survival")}
    res["PAD_minus_LEARN"] = {k: boot(per_seed(d, "PAD", MEASURES[k]) - per_seed(d, "LEARN", MEASURES[k]))
                              for k in ("mean_chains", "first_join_latency")}
    res["machines"] = sorted({json.dumps(x["machine"], sort_keys=True) for L in d.values() for x in L})
    (OUT / "analysis.json").write_text(json.dumps(res, indent=1))
    f = lambda b: f"{b['mean']:+.3f} [{b['lo']:+.3f}, {b['hi']:+.3f}] ({b['positive_seeds']}+/{b['negative_seeds']}- of {b['seeds']} seeds)"
    L = ["# CW1 analysis (frozen script)", "",
         f"Lives per arm: {res['lives_per_arm']}", "",
         f"**Primary: mean chains per life, LEARN - RANDOM-OPS = {f(res['primary'])}; real gain: {res['primary']['real_gain']}**",
         "", "| measure | " + " | ".join(ARMS) + " |", "|---" * (len(ARMS) + 1) + "|"]
    for k in MEASURES:
        L.append(f"| {k} | " + " | ".join(f"{arm_means[a][k]:.3f}" for a in ARMS) + " |")
    L += ["", "LEARN - RANDOM-OPS (secondaries):"] + [f"- {k}: {f(b)}" for k, b in res["secondary_LEARN_minus_RANDOM"].items()]
    L += ["", "LEARN - NO-MAKE:"] + [f"- {k}: {f(b)}" for k, b in res["LEARN_minus_NO-MAKE"].items()]
    L += ["", "PAD - LEARN:"] + [f"- {k}: {f(b)}" for k, b in res["PAD_minus_LEARN"].items()]
    L += ["", f"Machines: {len(res['machines'])}"] + [f"- {m}" for m in res["machines"]]
    (OUT / "analysis.md").write_text("\n".join(L) + "\n")
    print("\n".join(L))


if __name__ == "__main__":
    main()
