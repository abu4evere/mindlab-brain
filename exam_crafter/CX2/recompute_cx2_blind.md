# CX2 blind recompute (independent)

- Who: a fresh Claude Code subagent session, blind: it did not open analyse_cx2.py, analyse_cx1.py, analysis.json / analysis.md, findings*, other recompute_* files, lane.log or run_*.out.
- Inputs read: only `output/{learn,named,blind,learn_np,random5p}.jsonl` and the frozen plan text given in the task.
- When: 2026-11-25 06:02 EST (from `date`). Machine: the creator's Windows PC (Windows-10-10.0.19045), Python 3.14.7, numpy 2.5.3.
- Score: S = exp(mean_i ln(1 + s_i)) - 1 over all 22 achievements, s_i = percent of lives with achievement i at least once (count > 0).
- Bootstrap: 2,000 resamples, percentile 95% interval (2.5th and 97.5th), full score recomputed in each resample.

## RNG order (main result)
One generator, `numpy.random.default_rng(0)`. For resample b = 1..2000, in this fixed order: learn, named, blind, learn_np, random5p; each arm draws `rng.integers(0, n_arm, n_arm)` (lives resampled with replacement, independently per arm). All per-arm intervals and all differences come from these same 2,000 resamples (difference in resample b = S_x,b - S_y,b).
A sensitivity check with a different order (a fresh `default_rng(0)` per comparison, x-arm drawn before y-arm in each resample; and a fresh `default_rng(0)` per single arm) is reported below; every reading is the same.

## Per arm

| arm | lives | total steps | score S | 95% interval | first_drink share (mean step) | first_food share (mean step) | mean cells |
|---|---|---|---|---|---|---|---|
| learn | 5,320 | 1,000,086 | 1.5066 | [1.4904, 1.5238] | 0.5639 (3000/5320), 51.67 | 0.1008 (536/5320), 73.56 | 65.770 |
| named | 5,284 | 1,000,125 | 0.6033 | [0.5891, 0.6177] | 0.5859 (3096/5284), 49.01 | 0.1554 (821/5284), 89.40 | 35.665 |
| blind | 5,852 | 1,000,074 | 1.0485 | [1.0292, 1.0673] | 0.3141 (1838/5852), 86.13 | 0.0200 (117/5852), 89.33 | 17.081 |
| learn_np | 5,734 | 1,000,032 | 0.2135 | [0.2126, 0.2144] | 0.0000 (0/5734), n/a | 0.0000 (0/5734), n/a | 112.870 |
| random5p | 5,501 | 1,000,026 | 1.4796 | [1.4622, 1.4962] | 0.3801 (2091/5501), 93.25 | 0.1654 (910/5501), 102.95 | 42.481 |

Nonzero s_i (percent of lives); every other achievement of the 22 is 0 in every arm:

| achievement | learn | named | blind | learn_np | random5p |
|---|---|---|---|---|---|
| collect_drink | 91.541 | 93.357 | 57.194 | 0 | 39.138 |
| collect_wood | 86.823 | 0.397 | 45.523 | 0 | 72.823 |
| defeat_skeleton | 6.297 | 0.076 | 1.675 | 0 | 0.745 |
| defeat_zombie | 18.759 | 0.151 | 5.297 | 0 | 45.392 |
| eat_cow | 15.545 | 22.937 | 6.152 | 0 | 19.069 |
| wake_up | 30.075 | 7.286 | 20.796 | 69.655 | 97.564 |

Note: collect_drink share (achievement) and first_drink share (field) differ in learn, named, blind and random5p (for example learn 91.5% vs 56.4%). Both are reported exactly as read; the recompute does not interpret the fields.

## Comparisons (main RNG order)

| # | difference | point | 95% interval | reading |
|---|---|---|---|---|
| 1 PRIMARY | learn - random5p | +0.0270 | [+0.0027, +0.0508] | above |
| 2 | learn - blind | +0.4581 | [+0.4330, +0.4826] | above |
| 3 | learn - named | +0.9033 | [+0.8815, +0.9259] | above |
| 3 (rule) | named - random5p | -0.8763 | [-0.8995, -0.8532] | below |
| 4 | learn - learn_np | +1.2931 | [+1.2769, +1.3104] | above |

Comparison 3 "close" rule: named - random5p is below 0 (not above), so the condition for "close" is not met; "close" does not apply. learn - named reads "above".

Sensitivity (fresh default_rng(0) per comparison): learn-random5p [0.0036, 0.0499] above; learn-blind [0.4321, 0.4827] above; learn-named [0.8818, 0.9258] above; learn-learn_np [1.2773, 1.3096] above; named-random5p [-0.8981, -0.8529] below. Per single arm: learn [1.4898, 1.5234], named [0.5883, 0.6187], blind [1.0304, 1.0669], learn_np [0.2126, 0.2144], random5p [1.4626, 1.4964]. The primary lower bound is close to 0 (0.0027 / 0.0036) under both orders, so its exact value depends on RNG order; the reading does not.

## Checks and odd things
- Seeds: every arm has seeds 1..n with no duplicates and no gaps. Seeds 1..5284 are shared by all five arms (overlap = the smaller arm's count).
- Total steps: every arm is just over 1,000,000 (by 26 to 125 steps), consistent with the last life finishing past the budget.
- No achievement names outside the 22; every line has first_drink / first_food keys.
- All lives in all arms end with death = "health".
- Steps per life: min 5 in learn, named, blind, learn_np; min 20 in random5p. Max: learn 662, named 750, blind 606, learn_np 403, random5p 577.
- learn_np: only wake_up is ever unlocked (69.655%); first_drink and first_food are null in all 5,734 lives; its interval is very narrow because only one achievement varies.
- collect_drink share vs first_drink share disagree in four arms (see above).

## Code

```python
import json, numpy as np
from collections import Counter
D = "D:/mindlab/exam_crafter/CX2/output/"
ARMS = ["learn", "named", "blind", "learn_np", "random5p"]
ACH = ["collect_coal","collect_diamond","collect_drink","collect_iron","collect_sapling","collect_stone",
       "collect_wood","defeat_skeleton","defeat_zombie","eat_cow","eat_plant","make_iron_pickaxe",
       "make_iron_sword","make_stone_pickaxe","make_stone_sword","make_wood_pickaxe","make_wood_sword",
       "place_furnace","place_plant","place_stone","place_table","wake_up"]
B = 2000

def score_from_pct(p):  # p: (..., 22) percents
    return np.exp(np.mean(np.log1p(p), axis=-1)) - 1

data = {}
for a in ARMS:
    rows = [json.loads(l) for l in open(D + a + ".jsonl", encoding="utf-8") if l.strip()]
    data[a] = rows

pres = {}
for a in ARMS:
    rows = data[a]
    M = np.array([[1 if r["achievements"].get(k, 0) > 0 else 0 for k in ACH] for r in rows], dtype=np.int8)
    pres[a] = M
    unknown = set(k for r in rows for k in r["achievements"]) - set(ACH)
    seeds = [r["seed"] for r in rows]
    c = Counter(seeds); dup = {s: n for s, n in c.items() if n > 1}
    ss = sorted(set(seeds))
    gaps = sorted(set(range(ss[0], ss[-1] + 1)) - set(ss))
    steps = np.array([r["steps"] for r in rows])
    pct = M.mean(0) * 100
    fd = [r["first_drink"] for r in rows if r.get("first_drink") is not None]
    ff = [r["first_food"] for r in rows if r.get("first_food") is not None]
    print(f"== {a}: lives={len(rows)} total_steps={steps.sum()} min/max steps={steps.min()}/{steps.max()} "
          f"seeds {ss[0]}..{ss[-1]} unique={len(ss)} dups={len(dup)} {list(dup.items())[:5]} gaps={len(gaps)} {gaps[:10]} "
          f"unknown_ach={unknown} keys_missing_fd={sum('first_drink' not in r for r in rows)}")
    print("   score=%.4f" % score_from_pct(pct))
    print("   nonzero:", {k: round(float(v), 3) for k, v in zip(ACH, pct) if v > 0})
    print("   first_drink share=%.4f (%d/%d) mean=%.2f" % (len(fd)/len(rows), len(fd), len(rows), np.mean(fd) if fd else float('nan')))
    print("   first_food  share=%.4f (%d/%d) mean=%.2f" % (len(ff)/len(rows), len(ff), len(rows), np.mean(ff) if ff else float('nan')))
    print("   mean cells=%.3f" % np.mean([r["cells"] for r in rows]))
    print("   death:", dict(Counter(r.get("death") for r in rows)))

# Seeds overlap across arms
for i, a in enumerate(ARMS):
    for b in ARMS[i+1:]:
        sa = set(r["seed"] for r in data[a]); sb = set(r["seed"] for r in data[b])
        print(f"seed overlap {a}-{b}: {len(sa & sb)}")

# Main bootstrap: ONE rng = default_rng(0); for each of 2000 resamples, draw indices
# for every arm in the fixed order learn, named, blind, learn_np, random5p.
def boot(rng):
    S = {a: np.empty(B) for a in ARMS}
    for b in range(B):
        for a in ARMS:
            M = pres[a]; n = len(M)
            idx = rng.integers(0, n, n)
            S[a][b] = score_from_pct(M[idx].mean(0) * 100)
    return S

def ci(x): return np.percentile(x, [2.5, 97.5])
def reading(lo, hi): return "above" if lo > 0 else ("below" if hi < 0 else "not separable")

point = {a: score_from_pct(pres[a].mean(0) * 100) for a in ARMS}
S = boot(np.random.default_rng(0))
print("\nMAIN (shared rng, order per resample: " + ", ".join(ARMS) + ")")
for a in ARMS:
    lo, hi = ci(S[a]); print(f"  {a}: {point[a]:.4f} [{lo:.4f}, {hi:.4f}]")
comps = [("learn","random5p"),("learn","blind"),("learn","named"),("learn","learn_np"),("named","random5p")]
for x, y in comps:
    d = S[x] - S[y]; lo, hi = ci(d)
    print(f"  {x}-{y}: {point[x]-point[y]:.4f} [{lo:.4f}, {hi:.4f}] {reading(lo,hi)}")

# Sensitivity: fresh default_rng(0) per comparison, x-arm indices drawn before y-arm in each resample
print("\nSENSITIVITY (fresh default_rng(0) per comparison)")
for x, y in comps:
    rng = np.random.default_rng(0); d = np.empty(B)
    for b in range(B):
        ix = rng.integers(0, len(pres[x]), len(pres[x])); iy = rng.integers(0, len(pres[y]), len(pres[y]))
        d[b] = score_from_pct(pres[x][ix].mean(0)*100) - score_from_pct(pres[y][iy].mean(0)*100)
    lo, hi = ci(d); print(f"  {x}-{y}: [{lo:.4f}, {hi:.4f}] {reading(lo,hi)}")
print("\nSENSITIVITY (fresh default_rng(0) per single arm)")
for a in ARMS:
    rng = np.random.default_rng(0); s = np.empty(B)
    for b in range(B):
        i = rng.integers(0, len(pres[a]), len(pres[a])); s[b] = score_from_pct(pres[a][i].mean(0)*100)
    lo, hi = ci(s); print(f"  {a}: [{lo:.4f}, {hi:.4f}]")
```
