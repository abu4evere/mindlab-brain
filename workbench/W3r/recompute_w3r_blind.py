"""Blind recompute for W3r: fresh-land survival and lifespan, paired seed bootstrap.

Reads only output/test_fresh_{ARM}_{SEED}.json for ARM in RVS, RMS, RMXS, RE5S, HRS, SEED 1..16.
Run: python -I recompute_w3r_blind.py
"""
import json
import math
import os
import platform
import sys
from collections import Counter

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "output")
ARMS = ["RVS", "RMS", "RMXS", "RE5S", "HRS"]
SEEDS = list(range(1, 17))
B = 10_000
RNG_SEED = 1

print("platform:", platform.platform())
print("python:", sys.version.replace("\n", " "))
print("numpy:", np.__version__)
print()

# ---------------- load + data checks ----------------
surv = {a: np.full(len(SEEDS), np.nan) for a in ARMS}
life = {a: np.full(len(SEEDS), np.nan) for a in ARMS}
checks = []
n_lives = Counter()
key_sets = Counter()
surv_values = Counter()
life_min, life_max = math.inf, -math.inf
life_when_survived = Counter()
life_max_when_dead = -math.inf
inconsistent = 0
missing_files = []
arm_keys = Counter()
sigs = {}
missing_fields = 0
nonnum = 0

for a in ARMS:
    for i, s in enumerate(SEEDS):
        fn = os.path.join(OUT, f"test_fresh_{a}_{s}.json")
        if not os.path.exists(fn):
            missing_files.append(fn)
            continue
        with open(fn, encoding="utf-8") as f:
            d = json.load(f)
        if not isinstance(d, list):
            checks.append(f"{a}_{s}: top level is {type(d).__name__}, not list")
            continue
        n_lives[len(d)] += 1
        if len(d) != 50:
            checks.append(f"{a}_{s}: {len(d)} lives (expected 50)")
        sv, lv = [], []
        for j, r in enumerate(d):
            key_sets[tuple(sorted(r.keys()))] += 1
            if "survived" not in r or "lifespan" not in r:
                missing_fields += 1
                checks.append(f"{a}_{s} life {j}: missing survived/lifespan")
                continue
            x, L = r["survived"], r["lifespan"]
            arm_keys[(a, "labels" in r, "fair_fed" in r)] += 1
            if not isinstance(x, (int, float)) or not isinstance(L, (int, float)):
                nonnum += 1
                checks.append(f"{a}_{s} life {j}: non-numeric survived={x!r} lifespan={L!r}")
                continue
            if (isinstance(x, float) and math.isnan(x)) or (isinstance(L, float) and math.isnan(L)):
                nonnum += 1
                checks.append(f"{a}_{s} life {j}: NaN")
                continue
            surv_values[repr(x)] += 1
            life_min, life_max = min(life_min, L), max(life_max, L)
            if x == 1:
                life_when_survived[L] += 1
            else:
                life_max_when_dead = max(life_max_when_dead, L)
            sv.append(float(x))
            lv.append(float(L))
        sigs.setdefault(tuple(zip(sv, lv)), []).append(f"{a}_{s}")
        surv[a][i] = np.mean(sv)
        life[a][i] = np.mean(lv)

print("DATA CHECKS")
print("  files expected:", len(ARMS) * len(SEEDS), " missing:", len(missing_files), missing_files)
print("  lives-per-file distribution:", dict(n_lives))
print("  distinct key sets (count of lives):")
for k, c in key_sets.items():
    print("    ", c, k)
print("  'survived' values seen:", dict(surv_values))
print("  lifespan min/max:", life_min, life_max)
print("  lifespan values among survived==1 lives:", dict(life_when_survived))
print("  max lifespan among survived!=1 lives:", life_max_when_dead)
print("  records missing survived/lifespan:", missing_fields, " non-numeric/NaN:", nonnum)
print("  lives by (arm, has 'labels', has 'fair_fed'):")
for k in sorted(arm_keys):
    print("    ", k, arm_keys[k])
dups = [v for v in sigs.values() if len(v) > 1]
print("  files with identical (survived, lifespan) sequences:", dups if dups else "none")
for c in checks[:50]:
    print("  !", c)
print()

# ---------------- per-arm table ----------------
np.set_printoptions(linewidth=200)
print("PER-SEED FRESH-LAND SURVIVAL (seeds 1..16)")
for a in ARMS:
    print(f"  {a:5s}", " ".join(f"{v:.2f}" for v in surv[a]))
print("PER-SEED LIFESPAN (seeds 1..16)")
for a in ARMS:
    print(f"  {a:5s}", " ".join(f"{v:.0f}" for v in life[a]))
print()
print("PER-ARM MEANS OVER 16 SEEDS")
print(f"  {'arm':5s} {'survival':>9s} {'sd_seeds':>9s} {'min':>6s} {'max':>6s} {'lifespan':>9s}")
for a in ARMS:
    print(f"  {a:5s} {surv[a].mean():9.4f} {surv[a].std(ddof=1):9.4f} "
          f"{surv[a].min():6.2f} {surv[a].max():6.2f} {life[a].mean():9.2f}")
print()

# ---------------- paired bootstrap ----------------
# One shared resample-index matrix drawn once from default_rng(1): B x 16 seed indices with
# replacement. Each contrast below is also redrawn with a fresh default_rng(1) so every contrast
# individually matches "random seed 1" -- both give identical indices since the draw is the same.
def boot(diff):
    rng = np.random.default_rng(RNG_SEED)
    idx = rng.integers(0, len(diff), size=(B, len(diff)))
    means = diff[idx].mean(axis=1)
    lo, hi = np.percentile(means, [2.5, 97.5])
    return diff.mean(), lo, hi

def report(name, a, b, metric):
    m = surv if metric == "survival" else life
    diff = m[a] - m[b]
    est, lo, hi = boot(diff)
    above = int((diff > 0).sum()); below = int((diff < 0).sum()); tie = int((diff == 0).sum())
    fmt = "{:+.4f}" if metric == "survival" else "{:+.2f}"
    print(f"  {name:30s} est {fmt.format(est)}  95% CI [{fmt.format(lo)}, {fmt.format(hi)}]  "
          f"seeds {a}>{b}: {above}/16 (ties {tie}, below {below})  "
          f"whole CI > 0: {lo > 0}")
    print(f"    per-seed diffs: " + " ".join(fmt.format(v) for v in diff))
    return est, lo, hi

print(f"BOOTSTRAP: B={B}, numpy default_rng({RNG_SEED}), integers(0,16,size=(B,16)), percentile 2.5/97.5 (numpy linear)")
print("PRIMARY")
report("RMS - RVS survival", "RMS", "RVS", "survival")
print("SECONDARY")
report("RMS - RMXS survival", "RMS", "RMXS", "survival")
report("RE5S - RVS survival", "RE5S", "RVS", "survival")
report("RMS - HRS survival", "RMS", "HRS", "survival")
report("RMS - RVS lifespan", "RMS", "RVS", "lifespan")

# sensitivity: legacy RandomState(1) with randint, to show the RNG choice matters little
print()
print("SENSITIVITY (not the frozen method): numpy RandomState(1).randint, primary only")
rs = np.random.RandomState(RNG_SEED)
d = surv["RMS"] - surv["RVS"]
mm = d[rs.randint(0, 16, size=(B, 16))].mean(axis=1)
print("  RMS - RVS survival CI [{:+.4f}, {:+.4f}]".format(*np.percentile(mm, [2.5, 97.5])))
