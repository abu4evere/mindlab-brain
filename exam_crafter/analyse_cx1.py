"""CX1 analysis (written before the study data; frozen with the plan).

  python analyse_cx1.py OUTDIR   -> OUTDIR/analysis.json and a printed table
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
        "cows_per_life": round(float(np.mean([r["achievements"].get("eat_cow", 0) for r in recs])), 3)}


def main():
    out = Path(sys.argv[1])
    rng = np.random.default_rng(BOOT_SEED)
    res = {}
    boots = {}
    for kind in ("brain", "random"):
        recs = [json.loads(x) for x in open(out / f"{kind}.jsonl")]
        _, boots[kind], res[kind] = arm(recs, rng)
    d = boots["brain"] - boots["random"]
    res["difference"] = {"brain_minus_random": round(res["brain"]["score"] - res["random"]["score"], 3),
                         "ci95": [round(float(np.percentile(d, 2.5)), 3), round(float(np.percentile(d, 97.5)), 3)]}
    lo, hi = res["difference"]["ci95"]
    res["reading"] = ("above the floor" if lo > 0 else "below the floor" if hi < 0 else "not separable from the floor")
    (out / "analysis.json").write_text(json.dumps(res, indent=1))
    for kind in ("brain", "random"):
        r = res[kind]
        print(f"{kind:6s}: score {r['score']:.2f}% {r['score_ci95']} over {r['lives']} lives / {r['steps']} steps; "
              f"life mean {r['length_mean']} median {r['length_median']}; actions {r['action_share']}")
        print("        ", {k: v for k, v in r["rates"].items() if v > 0})
    print("difference", res["difference"], "->", res["reading"])


if __name__ == "__main__":
    main()
