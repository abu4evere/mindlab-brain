# CX1 blind recompute

**Recomputed by:** a fresh Claude Code subagent session, 24 November 2026, on the creator's PC (Windows 10, Python + numpy).
**Blind:** I did not open `analyse_cx1.py`, `analysis.json`, `analysis.md`, any `findings*.md` or any other `recompute_*` file. I read only the five raw JSONL files in `CX1/output/` and the plan text I was given.

## Method (as given in the frozen plan)
- For each life, an achievement counts as unlocked if its count is above 0.
- s_i is the percent of lives (0 to 100) that unlocked achievement i, over all 22 Crafter achievements.
- Score S = exp(mean_i ln(1 + s_i)) - 1.
- 95% interval: percentile bootstrap (2.5th and 97.5th) over lives, 2,000 resamples, `numpy.random.default_rng(0)`.
- **Order of rng draws:**
  - Per-arm interval: a fresh `default_rng(0)` for each arm, then one call `rng.integers(0, n, size=(2000, n))`.
  - Difference A − B: a fresh `default_rng(0)` for each difference. First one call `(2000, n_A)` for arm A, then one call `(2000, n_B)` for arm B, from the same generator. Then resample k's score of A minus resample k's score of B.
- Reading: "above" if the whole interval is above 0, "below" if the whole interval is below 0, otherwise "no difference".

## Per arm

| arm | lives | total steps | mean steps/life (min to max) | S | 95% interval |
|---|---|---|---|---|---|
| brain | 5,275 | 1,000,128 | 189.60 (5 to 852) | 0.5603 | [0.5522, 0.5679] |
| random5 | 5,923 | 1,000,001 | 168.83 (15 to 452) | 0.5324 | [0.5243, 0.5403] |
| random | 5,944 | 1,000,154 | 168.26 (26 to 440) | 1.5370 | [1.5031, 1.5713] |
| sated | 5,321 | 1,000,032 | 187.94 (5 to 818) | 0.8103 | [0.8074, 0.8130] |
| random5s | 5,909 | 1,000,178 | 169.26 (15 to 450) | 0.5281 | [0.5193, 0.5361] |

Nonzero s_i (percent of lives):
- **brain:** collect_drink 93.498, eat_cow 22.294, wake_up 7.090
- **random5:** collect_drink 32.923, eat_cow 2.651, wake_up 95.678
- **random:**
  - collect_drink 9.690, collect_sapling 50.471, collect_stone 0.034, collect_wood 24.058
  - defeat_skeleton 0.034, defeat_zombie 0.118, eat_cow 0.387
  - make_wood_pickaxe 0.219, make_wood_sword 0.219
  - place_plant 45.188, place_stone 0.017, place_table 4.206, wake_up 93.674
- **sated:** collect_drink 90.133, eat_cow 75.117, wake_up 66.472
- **random5s:** collect_drink 32.797, eat_cow 2.437, wake_up 95.837

## Differences

| difference | point | 95% interval | reading |
|---|---|---|---|
| **brain − random5 (primary)** | **+0.0279** | **[+0.0167, +0.0386]** | **above** |
| brain − random | −0.9767 | [−1.0102, −0.9427] | below |
| sated − random5s | +0.2822 | [+0.2734, +0.2911] | above |
| sated − brain | +0.2500 | [+0.2418, +0.2584] | above |

## Checks and anything odd
- **Parsing:** every line parsed (0 bad lines). Every line has the same keys: steps, reward, achievements, actions, cells, death, seed, seconds. No achievement names outside the 22. No zero counts inside `achievements`.
- **Seeds:** each arm's seeds are exactly 1..n, in order, unique, with no gaps or duplicates.
  - So the arms share their low seeds (seeds 1..5,275 appear in every arm), but have different lengths.
  - The plan resamples each arm independently, so I treated them as independent, not paired.
- **Step budget:** each arm stops just past about 1,000,000 total steps (1,000,001 to 1,000,178). So the number of lives differs by arm: brain and sated live longer per life, so they have fewer lives.
- **Actions:** in every life, the action counts (move + do + sleep + other) add up exactly to `steps`.
- **Deaths:** every life in every arm ended with death "health". No life reached a time limit (longest life 852 steps).
- **The brain's achievements:** it unlocks only drink, cow and wake_up.
  - Its lead over random5 comes from drink (93.5% vs 32.9%) and cow (22.3% vs 2.7%).
  - It is far behind on wake_up (7.1% vs 95.7%).
  - The lead is small (+0.028 on a score near 0.53 to 0.56).
- **Unrestricted random** scores far higher (1.54), because it reaches sapling, wood, place_plant and table, which the 5-action arms evidently cannot.
- **random5 and random5s** are nearly identical (0.532 vs 0.528; same three achievements at similar rates).
- **File time:** `random.jsonl` has the same timestamp (24 Nov 11:51) as `analysis.json` in the output folder. That is only an observation (it may have been written last). I did not open `analysis.json`.

## Code

```python
import json, collections
import numpy as np

D = r"D:\mindlab\exam_crafter\CX1\output"
ACH = ["collect_coal","collect_diamond","collect_drink","collect_iron","collect_sapling","collect_stone",
       "collect_wood","defeat_skeleton","defeat_zombie","eat_cow","eat_plant","make_iron_pickaxe",
       "make_iron_sword","make_stone_pickaxe","make_stone_sword","make_wood_pickaxe","make_wood_sword",
       "place_furnace","place_plant","place_stone","place_table","wake_up"]
ARMS = ["brain","random5","random","sated","random5s"]
B = 2000

def load(arm):
    rows, bad = [], 0
    with open(D + "\\" + arm + ".jsonl", encoding="utf-8") as f:
        for line in f:
            if not line.strip(): continue
            try: rows.append(json.loads(line))
            except Exception: bad += 1
    return rows, bad

def score_from_pct(s):          # s: (..., 22) percents 0-100
    return np.exp(np.mean(np.log1p(s), axis=-1)) - 1

def presence(rows):
    return np.array([[1.0 if r["achievements"].get(a, 0) > 0 else 0.0 for a in ACH] for r in rows])

def boot_scores(X, rng):
    n = X.shape[0]
    idx = rng.integers(0, n, size=(B, n))           # one draw: B x n indices
    W = np.stack([np.bincount(row, minlength=n) for row in idx]).astype(float)
    return score_from_pct(100.0 * (W @ X) / n)

data = {}
for arm in ARMS:
    rows, bad = load(arm)
    X = presence(rows)
    seeds = [r.get("seed") for r in rows]
    c = collections.Counter(seeds)
    dups = {s: k for s, k in c.items() if k > 1}
    ss = sorted(set(s for s in seeds if s is not None))
    gaps = sorted(set(range(ss[0], ss[-1] + 1)) - set(ss)) if ss else []
    unknown = sorted({a for r in rows for a in r["achievements"] if a not in ACH})
    zero_cnt = sum(1 for r in rows for a, v in r["achievements"].items() if v <= 0)
    steps = np.array([r["steps"] for r in rows])
    deaths = collections.Counter(r.get("death") for r in rows)
    s = 100.0 * X.mean(0)
    rng = np.random.default_rng(0)
    bs = boot_scores(X, rng)
    data[arm] = dict(X=X, n=len(rows), bad=bad, steps=steps, s=s, S=float(score_from_pct(s)),
                     lo=float(np.percentile(bs, 2.5)), hi=float(np.percentile(bs, 97.5)),
                     dups=dups, nseeds=len(ss), smin=ss[0] if ss else None, smax=ss[-1] if ss else None,
                     gaps=gaps, unknown=unknown, zero_cnt=zero_cnt, deaths=deaths)

for arm in ARMS:
    d = data[arm]
    print(f"== {arm}: lives={d['n']} badlines={d['bad']} total_steps={int(d['steps'].sum())} "
          f"mean={d['steps'].mean():.2f} median={np.median(d['steps'])} min={d['steps'].min()} max={d['steps'].max()}")
    print(f"   S={d['S']:.4f} 95%CI [{d['lo']:.4f}, {d['hi']:.4f}]")
    print(f"   seeds: unique={d['nseeds']} range {d['smin']}..{d['smax']} dups={len(d['dups'])} {dict(list(d['dups'].items())[:10])} gaps={len(d['gaps'])} {d['gaps'][:20]}")
    print(f"   unknown ach={d['unknown']} zero-count entries={d['zero_cnt']} deaths={dict(d['deaths'])}")
    print("   nonzero s_i: " + ", ".join(f"{a}={v:.3f}" for a, v in zip(ACH, d['s']) if v > 0))

def diff(a, b):
    rng = np.random.default_rng(0)
    ba = boot_scores(data[a]["X"], rng)   # arm a drawn first
    bb = boot_scores(data[b]["X"], rng)   # then arm b, same generator
    dd = ba - bb
    lo, hi = np.percentile(dd, 2.5), np.percentile(dd, 97.5)
    read = "above" if lo > 0 else ("below" if hi < 0 else "no difference")
    return data[a]["S"] - data[b]["S"], lo, hi, read

print("== differences")
for a, b in [("brain","random5"),("brain","random"),("sated","random5s"),("sated","brain")]:
    pt, lo, hi, read = diff(a, b)
    print(f"   {a} - {b}: {pt:+.4f} [{lo:+.4f}, {hi:+.4f}] -> {read}")

# other keys present
keys = collections.Counter(k for arm in ARMS for r in load(arm)[0] for k in r)
print("keys:", dict(keys))
# overlap of seeds between arms
for a in ARMS:
    print(a, "seed set equal to brain's?", set(r["seed"] for r in load(a)[0]) == set(r["seed"] for r in load("brain")[0]))
```
