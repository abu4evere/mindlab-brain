"""Blind independent recompute of W3p key numbers, from raw result files only.

Written fresh, without reading analyse_w3p.py or any analysis/findings/recompute file.
Run with OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1.
"""
import json
import os
import sys

import numpy as np

ROOT = r"D:\mindlab"
BP = os.path.join(ROOT, "scorecard", "bp", "output")
W3P = os.path.join(ROOT, "workbench", "W3p", "output")
W3N = os.path.join(ROOT, "workbench", "W3n", "output")

ARMS = ["MB", "MBb", "MV", "HR"]
SEEDS = list(range(1, 9))
BOOT_SEED = 20261123
NBOOT = 50000
T95_7 = 1.894578605  # one-sided 95% t quantile, df = 7

notes = []      # odd things found in the data
counts = {}     # (measure, arm) -> files read


def life_dir(arm):
    return W3N if arm == "HR" else W3P


def load_probe(test, arm, seed, key):
    p = os.path.join(BP, f"{test}_{arm}S_{seed}.json")
    with open(p) as f:
        d = json.load(f)
    if d.get("agent") != f"{arm}S_{seed}":
        notes.append(f"{os.path.basename(p)}: agent field is {d.get('agent')!r}")
    if d.get("test") != test:
        notes.append(f"{os.path.basename(p)}: test field is {d.get('test')!r}")
    v = d[key]
    if not (0.0 <= v <= 1.0):
        notes.append(f"{os.path.basename(p)}: {key}={v} outside 0..1")
    return float(v), d.get("cases")


def load_lives(name):
    with open(name) as f:
        d = json.load(f)
    if not isinstance(d, list):
        notes.append(f"{os.path.basename(name)}: not a list")
    if len(d) != 50:
        notes.append(f"{os.path.basename(name)}: {len(d)} lives, not 50")
    ls = np.array([x["lifespan"] for x in d], dtype=float)
    sv = np.array([x["survived"] for x in d], dtype=float)
    if ls.max() > 3000 or ls.min() < 0:
        notes.append(f"{os.path.basename(name)}: lifespan range {ls.min()}..{ls.max()}")
    if not set(np.unique(sv)).issubset({0.0, 1.0}):
        notes.append(f"{os.path.basename(name)}: survived not 0/1")
    # consistency: survived lives should have lifespan 3000
    bad = int(np.sum((sv == 1) & (ls < 3000)) + np.sum((sv == 0) & (ls >= 3000)))
    if bad:
        notes.append(f"{os.path.basename(name)}: {bad} lives where survived and lifespan==3000 disagree")
    return ls, sv


def collect():
    data = {}
    cases = {}
    for test, key in [("R2", "success"), ("R5d", "success"), ("M2", "success"), ("PLAN", "uphill")]:
        for arm in ARMS:
            vals, cs = [], []
            for s in SEEDS:
                v, c = load_probe(test, arm, s, key)
                vals.append(v)
                cs.append(c)
            data[(test, arm)] = np.array(vals)
            cases[(test, arm)] = cs
            counts[(test, arm)] = len(vals)
    for arm in ARMS:
        for lab, meas in [(f"{arm}S", "life"), (f"{arm}S-bare", "life_bare")]:
            vals = []
            for s in SEEDS:
                ls, _ = load_lives(os.path.join(life_dir(arm), f"test_{lab}_{s}.json"))
                vals.append(ls.mean())
            data[(meas, arm)] = np.array(vals)
            counts[(meas, arm)] = len(vals)
        vals = []
        for s in SEEDS:
            _, sv = load_lives(os.path.join(life_dir(arm), f"test_fresh_{arm}S_{s}.json"))
            vals.append(sv.mean())
        data[("fresh", arm)] = np.array(vals)
        counts[("fresh", arm)] = len(vals)
    return data, cases


rng = np.random.default_rng(BOOT_SEED)
IDX = rng.integers(0, len(SEEDS), size=(NBOOT, len(SEEDS)))  # same resamples for every measure


def summarise(x):
    x = np.asarray(x, dtype=float)
    n = len(x)
    m = x.mean()
    bm = x[IDX].mean(axis=1)
    p5, p95 = np.percentile(bm, [5, 95])
    sd = x.std(ddof=1)
    half = T95_7 * sd / np.sqrt(n)
    return dict(mean=m, p5=p5, p95=p95, t5=m - half, t95=m + half, sd=sd, n=n,
                per_seed=[round(float(v), 4) for v in x])


def main():
    data, cases = collect()
    res = {}
    for k, v in data.items():
        res[k] = summarise(v)

    def diff(meas, a, b):
        return summarise(data[(meas, a)] - data[(meas, b)])

    diffs = {}
    for a, b in [("MB", "HR"), ("MBb", "MB"), ("MB", "MV"), ("MV", "HR"), ("MBb", "HR")]:
        diffs[("R2", a, b)] = diff("R2", a, b)
    for meas in ["R5d", "M2"]:
        diffs[(meas, "MB", "HR")] = diff(meas, "MB", "HR")
    for meas in ["life", "life_bare"]:
        for a in ["MB", "MBb"]:
            diffs[(meas, a, "HR")] = diff(meas, a, "HR")

    # case counts per test
    case_info = {}
    for (t, arm), cs in cases.items():
        case_info.setdefault(t, set()).update(cs)

    out = dict(res={f"{k[0]}|{k[1]}": v for k, v in res.items()},
               diffs={f"{k[0]}|{k[1]}-{k[2]}": v for k, v in diffs.items()},
               counts={f"{k[0]}|{k[1]}": v for k, v in counts.items()},
               cases={t: sorted(c) for t, c in case_info.items()},
               notes=notes, boot_seed=BOOT_SEED, nboot=NBOOT)
    json.dump(out, sys.stdout, indent=1, default=float)


if __name__ == "__main__":
    main()
