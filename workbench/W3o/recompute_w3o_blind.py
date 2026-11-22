"""Blind recompute of W3o key numbers, from raw output files only.

Written fresh for the independent recompute (22 Nov 2026). It does not import or read
analyse_w3o.py, analysis.*, probe.out, or any findings/recompute file.

Run with OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1.
"""
import json
import os
import sys

import numpy as np
from scipy import stats

HERE = os.path.dirname(os.path.abspath(__file__))
W3O_OUT = os.path.join(HERE, "output")
W3N_OUT = os.path.join(os.path.dirname(HERE), "W3n", "output")
SEEDS = list(range(1, 9))
CAP = 3000
N_BOOT = 50000
RNG_SEED = 20261122

DIRS = {"HRS": W3N_OUT, "HRS-bare": W3N_OUT,
        "RES": W3O_OUT, "RES-bare": W3O_OUT, "RES-swap": W3O_OUT,
        "RVS": W3O_OUT, "RVS-bare": W3O_OUT}

notes = []
files_read = {}


def load(label, seed, fresh=False):
    name = ("test_fresh_%s_%d.json" if fresh else "test_%s_%d.json") % (label, seed)
    path = os.path.join(DIRS[label], name)
    with open(path, "r", encoding="utf-8") as f:
        lives = json.load(f)
    key = ("fresh:" if fresh else "test:") + label
    files_read.setdefault(key, []).append(name)
    # data checks
    if len(lives) != 50:
        notes.append("%s has %d lives (expected 50)" % (name, len(lives)))
    ls = np.array([float(x["lifespan"]) for x in lives])
    sv = np.array([float(x["survived"]) for x in lives])
    if np.any(~np.isfinite(ls)) or np.any(~np.isfinite(sv)):
        notes.append("%s has non-finite values" % name)
    if ls.max() > CAP or ls.min() < 0:
        notes.append("%s lifespan outside [0, %d]: min %g max %g" % (name, CAP, ls.min(), ls.max()))
    if not set(np.unique(sv)).issubset({0.0, 1.0}):
        notes.append("%s survived not 0/1: %s" % (name, sorted(set(np.unique(sv)))))
    mism = int(np.sum((sv == 1) != (ls >= CAP)))
    if mism:
        notes.append("%s: %d lives where survived=1 does not match lifespan=cap" % (name, mism))
    return ls, sv


def per_seed(label, fresh=False):
    m_life, m_surv = [], []
    raw = []
    for s in SEEDS:
        ls, sv = load(label, s, fresh)
        m_life.append(ls.mean())
        m_surv.append(sv.mean())
        raw.append((ls.tobytes(), sv.tobytes()))
    return np.array(m_life), np.array(m_surv), raw


def boot_ci(x, level, rng):
    x = np.asarray(x, float)
    n = len(x)
    idx = rng.integers(0, n, size=(N_BOOT, n))
    means = x[idx].mean(axis=1)
    a = (1 - level) / 2
    return float(np.percentile(means, 100 * a)), float(np.percentile(means, 100 * (1 - a)))


def t_ci(x, level):
    x = np.asarray(x, float)
    n = len(x)
    m = x.mean()
    se = x.std(ddof=1) / np.sqrt(n)
    q = stats.t.ppf(1 - (1 - level) / 2, n - 1)
    return float(m - q * se), float(m + q * se)


def summarise(x, level, rng):
    x = np.asarray(x, float)
    return {"mean": float(x.mean()), "boot": boot_ci(x, level, rng), "t": t_ci(x, level),
            "n_pos": int(np.sum(x > 0)), "n": len(x), "per_seed": [float(v) for v in x]}


def exact_boot(x, level):
    """Exact percentile bootstrap: every one of the n**n equally likely resamples,
    enumerated as multisets with multinomial weights. Returns (lower, upper)."""
    from itertools import combinations_with_replacement
    from math import factorial
    x = np.asarray(x, float)
    n = len(x)
    vals, wts = [], []
    for combo in combinations_with_replacement(range(n), n):
        counts = np.bincount(combo, minlength=n)
        w = factorial(n)
        for c in counts:
            w //= factorial(int(c))
        vals.append(float(np.dot(counts, x)) / n)
        wts.append(w)
    vals = np.array(vals)
    wts = np.array(wts, float) / float(n ** n)
    order = np.argsort(vals)
    vals, cdf = vals[order], np.cumsum(wts[order])
    a = (1 - level) / 2
    lo = vals[np.searchsorted(cdf, a - 1e-15)]
    hi = vals[np.searchsorted(cdf, 1 - a - 1e-15)]
    return float(lo), float(hi)


def seed_spread(x, level, seeds=(1, 2, 3, 4, 5)):
    out = []
    for s in seeds:
        out.append(boot_ci(x, level, np.random.default_rng(s)))
    return out


def verdict_primary(r):
    lo, hi = r["boot"]
    tlo, thi = r["t"]
    def v(lo, hi):
        if hi < 0:
            return "real loss"
        if lo > -200:
            return "small (lower bound above -200)"
        return "unclear"
    return v(lo, hi), v(tlo, thi)


def main():
    rng = np.random.default_rng(RNG_SEED)
    life, surv, raw = {}, {}, {}
    for lab in ["HRS", "HRS-bare", "RES", "RES-bare", "RES-swap", "RVS", "RVS-bare"]:
        life[lab], surv[lab], raw[lab] = per_seed(lab)
    fsurv, flife, fraw = {}, {}, {}
    for lab in ["HRS", "RES", "RVS"]:
        flife[lab], fsurv[lab], fraw[lab] = per_seed(lab, fresh=True)

    # identical-file check between labels (same seed)
    labs = list(raw)
    for i in range(len(labs)):
        for j in range(i + 1, len(labs)):
            same = sum(raw[labs[i]][k] == raw[labs[j]][k] for k in range(8))
            if same:
                notes.append("%s and %s: %d seeds with byte-identical lifespan+survived lists" % (labs[i], labs[j], same))

    out = {"n_boot": N_BOOT, "rng_seed": RNG_SEED,
           "per_seed_lifespan": {k: [float(v) for v in life[k]] for k in life},
           "per_seed_survived_test": {k: [float(v) for v in surv[k]] for k in surv},
           "per_seed_fresh_survived": {k: [float(v) for v in fsurv[k]] for k in fsurv},
           "per_seed_fresh_lifespan": {k: [float(v) for v in flife[k]] for k in flife}}

    # 1. primary, 97.5%
    prim = {}
    for name, a, b in [("RES-bare minus HRS-bare", "RES-bare", "HRS-bare"),
                       ("RES minus HRS", "RES", "HRS")]:
        r = summarise(life[a] - life[b], 0.975, rng)
        r["verdict_boot"], r["verdict_t"] = verdict_primary(r)
        r["exact_boot"] = exact_boot(life[a] - life[b], 0.975)
        r["boot_other_numpy_seeds_1to5"] = seed_spread(life[a] - life[b], 0.975)
        prim[name] = r
    out["primary_97.5"] = prim

    # 2. secondary, 95%
    sec = {}
    for name, a, b in [("RVS minus HRS", "RVS", "HRS"),
                       ("RVS-bare minus HRS-bare", "RVS-bare", "HRS-bare"),
                       ("RES-swap minus RES", "RES-swap", "RES")]:
        sec[name] = summarise(life[a] - life[b], 0.95, rng)
    m = sec["RES-swap minus RES"]
    m["check_passes_boot"] = m["boot"][1] < 0
    m["check_passes_t"] = m["t"][1] < 0
    out["secondary_95"] = sec

    # arm means (lifespan), 95%
    out["arm_lifespan_95"] = {k: summarise(life[k], 0.95, rng) for k in life}

    # 3. fresh-land survival, 95%
    fr = {}
    for lab in ["HRS", "RES", "RVS"]:
        r = summarise(fsurv[lab], 0.95, rng)
        r["lower_reaches_0.80_boot"] = r["boot"][0] >= 0.80
        r["lower_reaches_0.80_t"] = r["t"][0] >= 0.80
        fr[lab] = r
    out["fresh_survival_95"] = fr

    # 4. probe
    with open(os.path.join(HERE, "probe.json"), "r", encoding="utf-8") as f:
        probe = json.load(f)
    pr = {"brains": sorted(probe.keys()), "seeds_per_brain": {b: sorted(probe[b].keys(), key=int) for b in probe}}
    tow = {}
    for b in ["HRS", "RES", "RVS", "RES-swap"]:
        for need in ["hungry", "tired"]:
            tow[(b, need)] = np.array([float(probe[b][str(s)][need]["toward"]) for s in SEEDS])
            ch = np.array([float(probe[b][str(s)][need]["chance"]) for s in SEEDS])
            pr["%s %s toward" % (b, need)] = summarise(tow[(b, need)], 0.95, rng)
            pr["%s %s chance" % (b, need)] = {"mean": float(ch.mean()), "per_seed": [float(v) for v in ch]}
            pr["%s %s toward minus chance" % (b, need)] = summarise(tow[(b, need)] - ch, 0.95, rng)
    for need in ["hungry", "tired"]:
        for b in ["RES", "RVS"]:
            pr["%s minus HRS, %s" % (b, need)] = summarise(tow[(b, need)] - tow[("HRS", need)], 0.95, rng)
    out["probe_95"] = pr

    out["files_read"] = {k: len(v) for k, v in files_read.items()}
    out["notes"] = notes
    json.dump(out, sys.stdout, indent=1)


if __name__ == "__main__":
    main()
