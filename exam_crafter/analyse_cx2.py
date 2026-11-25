"""CX2 analysis (written before the study data; CX2/questions.md). CX1's score and bootstrap (2,000 resamples over
lives, seed 0, the full score recomputed in every resample); CX2's arms and comparisons; the tables' discovery
measures (share of lives where water / cow was ever ranked first, and the mean step when it was).

  python analyse_cx2.py OUTDIR   -> OUTDIR/analysis.json and a printed table
"""
import json
import sys
from pathlib import Path

import numpy as np

ACH = ['collect_coal', 'collect_diamond', 'collect_drink', 'collect_iron', 'collect_sapling', 'collect_stone',
       'collect_wood', 'defeat_skeleton', 'defeat_zombie', 'eat_cow', 'eat_plant', 'make_iron_pickaxe',
       'make_iron_sword', 'make_stone_pickaxe', 'make_stone_sword', 'make_wood_pickaxe', 'make_wood_sword',
       'place_furnace', 'place_plant', 'place_stone', 'place_table', 'wake_up']
B, BOOT_SEED = 2000, 0
ARMS = ("learn", "named", "blind", "learn_np", "random5p")
# the achievements the bridge's hand can reach on purpose (questions.md): drink, eat, sleep and wake
REACHABLE = ["collect_drink", "eat_cow", "eat_plant", "wake_up"]
COMPARE = [("learn", "random5p", "PRIMARY: learned meanings vs random choices (same hand, same tables)"),
           ("learn", "blind", "do the learned meanings matter for the same brain and hand?"),
           ("learn", "named", "learned vs told meanings ('close' only if named - random5p > 0 and lower bound > -0.10)"),
           ("named", "random5p", "told meanings vs random (the condition for reading 'close')"),
           ("learn", "learn_np", "what the poke adds")]


def got(recs):
    return np.array([[a in r["achievements"] for a in ACH] for r in recs], float)   # lives x 22


def score_of(g):
    rates = 100.0 * g.mean(0)
    return float(np.exp(np.mean(np.log(1.0 + rates))) - 1.0)


def arm(recs, rng):
    g = got(recs)
    boot = np.array([score_of(g[rng.integers(len(g), size=len(g))]) for _ in range(B)])
    steps = np.array([r["steps"] for r in recs])
    acts = {k: int(sum(r["actions"][k] for r in recs)) for k in ("move", "do", "sleep", "other")}
    n_act = max(1, sum(acts.values()))
    return g, boot, {
        "lives": len(recs), "steps": int(steps.sum()), "score": round(score_of(g), 3),
        "score_ci95": [round(float(np.percentile(boot, 2.5)), 3), round(float(np.percentile(boot, 97.5)), 3)],
        "rates": dict(zip(ACH, (100.0 * g.mean(0)).round(2).tolist())),
        "length_mean": round(float(steps.mean()), 1), "length_median": float(np.median(steps)),
        "ended_by_time": int(sum(r["death"] == "time" for r in recs)),
        "action_share": {k: round(v / n_act, 4) for k, v in acts.items()},
        "drinks_per_life": round(float(np.mean([r["achievements"].get("collect_drink", 0) for r in recs])), 2),
        "cows_per_life": round(float(np.mean([r["achievements"].get("eat_cow", 0) for r in recs])), 3),
        "cells_mean": round(float(np.mean([r["cells"] for r in recs])), 1),
        "reachable_rates": {a: round(100.0 * float(np.mean([a in r["achievements"] for r in recs])), 2)
                            for a in REACHABLE},
        "water_ranked_first_share": round(float(np.mean([r["first_drink"] is not None for r in recs])), 4),
        "water_ranked_first_step": round(float(np.mean([r["first_drink"] for r in recs if r["first_drink"] is not None]
                                                       or [np.nan])), 1),
        "cow_ranked_first_share": round(float(np.mean([r["first_food"] is not None for r in recs])), 4),
        "cow_ranked_first_step": round(float(np.mean([r["first_food"] for r in recs if r["first_food"] is not None]
                                                     or [np.nan])), 1),
        "bouts_per_life": round(float(np.mean([r["bouts"] for r in recs])), 2),
        "bout_hurt_per_life": round(float(np.mean([r["bout_hurt"] for r in recs])), 3)}


def main():
    out = Path(sys.argv[1])
    rng = np.random.default_rng(BOOT_SEED)
    res, boots = {}, {}
    for kind in ARMS:
        recs = [json.loads(x) for x in open(out / f"{kind}.jsonl")]
        _, boots[kind], res[kind] = arm(recs, rng)
    res["comparisons"] = []
    for a, b, what in COMPARE:
        d = boots[a] - boots[b]
        lo, hi = float(np.percentile(d, 2.5)), float(np.percentile(d, 97.5))
        res["comparisons"].append({"a": a, "b": b, "what": what,
                                   "difference": round(res[a]["score"] - res[b]["score"], 3),
                                   "ci95": [round(lo, 3), round(hi, 3)],
                                   "reading": "a above b" if lo > 0 else "a below b" if hi < 0 else "not separable"})
    (out / "analysis.json").write_text(json.dumps(res, indent=1))
    for kind in ARMS:
        r = res[kind]
        print(f"{kind:8s}: score {r['score']:.2f}% {r['score_ci95']} over {r['lives']} lives / {r['steps']} steps; "
              f"life mean {r['length_mean']} median {r['length_median']}; cells {r['cells_mean']}; "
              f"actions {r['action_share']}")
        print("          ", {k: v for k, v in r["rates"].items() if v > 0})
    c3 = res["comparisons"][2]
    c3["close"] = bool(res["comparisons"][3]["ci95"][0] > 0 and c3["ci95"][0] > -0.10)
    (out / "analysis.json").write_text(json.dumps(res, indent=1))
    for kind in ARMS:
        r = res[kind]
        print(f"   {kind}: water ranked first in {r['water_ranked_first_share']:.3f} of lives (step "
              f"{r['water_ranked_first_step']}), cow {r['cow_ranked_first_share']:.3f} (step {r['cow_ranked_first_step']})")
    print("LEARN close to NAMED:", c3["close"])
    for c in res["comparisons"]:
        print(f"{c['a']} - {c['b']}: {c['difference']:+.3f} {c['ci95']} -> {c['reading']}  ({c['what']})")


if __name__ == "__main__":
    main()
