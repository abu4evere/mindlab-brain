"""V2-1's frozen analysis (questions.md). Per seed: the mean over its 50 lives; paired by seed; 95% bootstrap over the
16 seeds (10,000 resamples, generator seeded V21_SEED).
  Primary: survival under the swap, SURPRISE - PLAIN (real gain if the lower end > 0).
  No-loss gate: stable survival SURPRISE - PLAIN, lower end > -0.03.
  Secondaries: SURPRISE - SHAM, SURPRISE - WINDOW (swap); WINDOW - PLAIN (stable); table accuracy at the end (food and
  wall ranked right, swap); recovery latency (lives that recovered); resets per life on stable lands; the hunger
  reflex's share of post-swap meals. Test B: chains after 1,500 SURPRISE - PLAIN, - SHAM, - WINDOW; chains before 1,500
  SURPRISE - PLAIN (no-loss within 0.3).
  python analyse_v21.py  -> output/analysis.json, output/analysis.md
"""
from __future__ import annotations

import json
import math
from pathlib import Path

import numpy as np

HERE = Path(__file__).parent
OUT = HERE / "output"
ARMS = ("PLAIN", "SURPRISE", "WINDOW", "SHAM")
SEEDS = range(1, 17)
V21_SEED = 20261129


def load(name):
    p = OUT / name
    L = [json.loads(x) for x in p.read_text().splitlines() if x.strip()]
    assert len(L) == 50 and len({x["land"] for x in L}) == 50, (p, len(L))
    return L


def boot(diff, B=10_000):
    diff = np.asarray(diff, float)
    diff = diff[~np.isnan(diff)]
    if not len(diff):
        return {"mean": math.nan, "lo": math.nan, "hi": math.nan, "seeds": 0, "positive_seeds": 0, "negative_seeds": 0}
    idx = np.random.default_rng(V21_SEED).integers(0, len(diff), (B, len(diff)))
    m = diff[idx].mean(1)
    return {"mean": float(diff.mean()), "lo": float(np.percentile(m, 2.5)), "hi": float(np.percentile(m, 97.5)),
            "seeds": int(len(diff)), "positive_seeds": int((diff > 0).sum()), "negative_seeds": int((diff < 0).sum())}


def per_seed(f, files):
    return np.array([f(files[s]) for s in SEEDS], float)


def mean_of(key):
    return lambda L: float(np.mean([float(x[key]) for x in L]))


def acc(L):
    return float(np.mean([bool(x["acc_food"]) and bool(x["acc_wall"]) for x in L]))


def latency(L):
    v = [x["latency"] for x in L if x["latency"] is not None]
    return float(np.mean(v)) if v else math.nan


def reflex_share(L):
    m = sum(x["meals_post"] for x in L)
    return sum(x["meals_post_reflex"] for x in L) / m if m else math.nan


def main():
    A = {(a, c): {s: load(f"A_{a}_{c}_{s}.jsonl") for s in SEEDS} for a in ARMS for c in ("swap", "stable")}
    Bf = {a: {s: load(f"B_{a}_{s}.jsonl") for s in SEEDS} for a in ARMS}
    surv = mean_of("survived")
    d = lambda a, b, c, f=surv: boot(per_seed(f, A[a, c]) - per_seed(f, A[b, c]))
    res = {"lives": {f"A_{a}_{c}": 800 for a in ARMS for c in ("swap", "stable")} | {f"B_{a}": 800 for a in ARMS}}
    res["arm_means"] = {f"{a}_{c}": {"survival": float(np.mean(per_seed(surv, A[a, c]))),
                                     "lifespan": float(np.mean(per_seed(mean_of("lifespan"), A[a, c]))),
                                     "acc_end": float(np.mean(per_seed(acc, A[a, c]))),
                                     "latency": float(np.nanmean(per_seed(latency, A[a, c]))),
                                     "resets": float(np.mean(per_seed(mean_of("resets"), A[a, c]))),
                                     "reflex_share_post_meals": float(np.nanmean(per_seed(reflex_share, A[a, c])))}
                        for a in ARMS for c in ("swap", "stable")}
    res["primary"] = d("SURPRISE", "PLAIN", "swap")
    res["primary"]["real_gain"] = res["primary"]["lo"] > 0
    res["no_loss"] = d("SURPRISE", "PLAIN", "stable")
    res["no_loss"]["passed"] = res["no_loss"]["lo"] > -0.03
    res["secondaries"] = {
        "SURPRISE-SHAM_swap": d("SURPRISE", "SHAM", "swap"),
        "SURPRISE-WINDOW_swap": d("SURPRISE", "WINDOW", "swap"),
        "WINDOW-PLAIN_swap": d("WINDOW", "PLAIN", "swap"),
        "WINDOW-PLAIN_stable": d("WINDOW", "PLAIN", "stable"),
        "SURPRISE-PLAIN_acc_end_swap": d("SURPRISE", "PLAIN", "swap", acc),
        "SURPRISE-PLAIN_reflex_share_swap": d("SURPRISE", "PLAIN", "swap", reflex_share),
    }
    ca, cb = mean_of("chains_after"), mean_of("chains_before")
    res["B_means"] = {a: {"chains_before": float(np.mean(per_seed(cb, Bf[a]))),
                          "chains_after": float(np.mean(per_seed(ca, Bf[a]))),
                          "resets": float(np.mean(per_seed(mean_of("resets"), Bf[a])))}
                      for a in ARMS}
    res["B"] = {f"{a}-PLAIN_after": boot(per_seed(ca, Bf[a]) - per_seed(ca, Bf["PLAIN"])) for a in ("SURPRISE", "WINDOW", "SHAM")}
    res["B"]["SURPRISE-SHAM_after"] = boot(per_seed(ca, Bf["SURPRISE"]) - per_seed(ca, Bf["SHAM"]))
    res["B"]["SURPRISE-WINDOW_after"] = boot(per_seed(ca, Bf["SURPRISE"]) - per_seed(ca, Bf["WINDOW"]))
    nb = boot(per_seed(cb, Bf["SURPRISE"]) - per_seed(cb, Bf["PLAIN"]))
    nb["no_loss_within_0.3"] = abs(nb["mean"]) <= 0.3
    res["B"]["SURPRISE-PLAIN_before"] = nb
    res["machines"] = sorted({json.dumps(x["machine"], sort_keys=True) for v in list(A.values()) + list(Bf.values())
                              for L in v.values() for x in L})
    (OUT / "analysis.json").write_text(json.dumps(res, indent=1))
    f = lambda b: (f"{b['mean']:+.3f} [{b['lo']:+.3f}, {b['hi']:+.3f}] ({b['positive_seeds']}+/{b['negative_seeds']}- "
                   f"of {b['seeds']})")
    L = ["# V2-1 analysis (frozen script)", "",
         f"**Primary: swap survival SURPRISE - PLAIN = {f(res['primary'])}; real gain: {res['primary']['real_gain']}**",
         f"**No-loss gate: stable survival SURPRISE - PLAIN = {f(res['no_loss'])}; passed: {res['no_loss']['passed']}**",
         "", "| arm, condition | survival | lifespan | table right at end | latency | resets | hunger-reflex share of post-swap meals |",
         "|---|---|---|---|---|---|---|"]
    for k, v in res["arm_means"].items():
        L.append(f"| {k} | {v['survival']:.3f} | {v['lifespan']:.0f} | {v['acc_end']:.3f} | {v['latency']:.0f} | "
                 f"{v['resets']:.2f} | {v['reflex_share_post_meals']:.3f} |")
    L += ["", "Secondaries:"] + [f"- {k}: {f(b)}" for k, b in res["secondaries"].items()]
    L += ["", "Test B (join changed at step 1,500):"] + [f"- {a}: before {v['chains_before']:.2f}, after "
                                                          f"{v['chains_after']:.2f}" for a, v in res["B_means"].items()]
    L += [f"- {k}: {f(b)}" for k, b in res["B"].items()]
    L += ["", f"Machines: {len(res['machines'])}"] + [f"- {m}" for m in res["machines"]]
    (OUT / "analysis.md").write_text("\n".join(L) + "\n")
    print("\n".join(L))


if __name__ == "__main__":
    main()
