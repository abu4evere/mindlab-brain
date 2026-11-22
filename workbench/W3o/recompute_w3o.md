# W3o: independent blind recompute

Done 2026-11-22 11:22 EST on the creator's PC (User-PC, Windows), by a fresh assistant session acting as the blind recompute.

**What I did not open:** `analyse_w3o.py`, `analysis.md`, `analysis.json`, `analysis.out`, `probe.out`, and any `findings*` or `recompute*` file in W3o or W3n. I wrote my own script from the task description: `recompute_w3o_blind.py` (beside this file). It reads only the raw `test_*.json` / `test_fresh_*.json` lists and `probe.json`.

**Method.**
- For each seed: mean `lifespan` over the 50 test lives. For fresh lands: mean `survived` over the 50 fresh lives.
- Contrasts are paired by seed, over the 8 seeds (1 to 8).
- Percentile bootstrap resampling seeds: 50,000 resamples, numpy `default_rng(20261122)`.
- A t interval (df = 7) is given beside it.
- For the two primary contrasts I also checked two things:
  - the exact bootstrap, with all 8^8 resamples enumerated;
  - five other numpy seeds (1 to 5).
  
  Both agree with the main bootstrap to within about 2 steps.

## Files read (each label: 8 files, seeds 1 to 8, 50 lives each)

| Label | Folder | test files | test_fresh files |
|---|---|---|---|
| HRS | W3n/output | 8 | 8 |
| HRS-bare | W3n/output | 8 | (not used) |
| RES | W3o/output | 8 | 8 |
| RES-bare | W3o/output | 8 | (not used) |
| RES-swap | W3o/output | 8 | (not used) |
| RVS | W3o/output | 8 | 8 |
| RVS-bare | W3o/output | 8 | (not used) |

Plus `W3o/probe.json`. It holds 4 brains (HRS, RES, RVS, RES-swap), each with seeds 1 to 8 and both "hungry" and "tired".

## Data checks

- Every file has exactly 50 lives.
- No lifespan is outside 0 to 3000, and no value is missing or non-finite.
- `survived` is always 0 or 1, and `survived = 1` exactly when `lifespan = 3000` (no mismatches in any file).
- No two labels have byte-identical lists for the same seed.

## Per-seed means (lifespan, steps; 50 test lives each)

| Seed | HRS | HRS-bare | RES | RES-bare | RES-swap | RVS | RVS-bare |
|---|---|---|---|---|---|---|---|
| 1 | 2670.6 | 1658.8 | 2718.2 | 1152.0 | 341.9 | 1010.2 | 287.0 |
| 2 | 2890.7 | 1858.8 | 2648.2 | 1492.9 | 240.2 | 1700.7 | 324.8 |
| 3 | 2871.9 | 1797.7 | 2912.5 | 1873.4 | 226.0 | 1430.7 | 380.7 |
| 4 | 2667.8 | 1823.6 | 2567.9 | 1741.8 | 346.3 | 1127.6 | 361.9 |
| 5 | 2729.4 | 1656.5 | 2670.9 | 1561.1 | 284.0 | 1326.3 | 430.7 |
| 6 | 2822.7 | 1558.9 | 2853.4 | 1897.8 | 390.1 | 1249.4 | 404.3 |
| 7 | 2830.3 | 1113.9 | 2690.5 | 1287.3 | 269.2 | 982.6 | 432.4 |
| 8 | 2939.9 | 1391.9 | 2788.1 | 1438.8 | 483.5 | 1737.5 | 458.4 |
| **mean** | **2802.93** | **1607.53** | **2731.20** | **1555.64** | **322.64** | **1320.62** | **385.03** |

Arm means with 95% intervals (bootstrap; t):

| Arm | Mean | Bootstrap 95% | t 95% |
|---|---|---|---|
| HRS | 2802.93 | [2736.28, 2868.27] | [2717.23, 2888.62] |
| HRS-bare | 1607.53 | [1432.00, 1755.33] | [1397.09, 1817.96] |
| RES | 2731.20 | [2659.43, 2806.61] | [2636.39, 2826.02] |
| RES-bare | 1555.64 | [1381.19, 1728.28] | [1331.03, 1780.25] |
| RES-swap | 322.64 | [270.75, 381.06] | [250.70, 394.59] |
| RVS | 1320.62 | [1141.49, 1514.27] | [1079.29, 1561.95] |
| RVS-bare | 385.03 | [346.30, 421.52] | [336.21, 433.86] |

## 1. Primary (97.5% two-sided, paired by seed)

| Contrast | Mean diff | Bootstrap 97.5% | Exact bootstrap 97.5% | t 97.5% | Seeds > 0 | Verdict |
|---|---|---|---|---|---|---|
| (a) RES-bare minus HRS-bare | -51.89 | [-261.29, 142.61] | [-262.47, 142.61] | [-330.30, 226.53] | 4 / 8 | **unclear** (lower bound below -200, upper bound above 0) |
| (b) RES minus HRS | -71.72 | [-151.84, 3.68] | [-150.34, 3.93] | [-178.10, 34.66] | 3 / 8 | **small** (lower bound above -200; upper bound just above 0, so not "real") |

Per-seed differences:
- (a): -506.7, -365.9, +75.7, -81.8, -95.4, +338.9, +173.3, +46.8
- (b): +47.6, -242.5, +40.5, -99.9, -58.5, +30.7, -139.8, -151.9

The bootstrap bounds with numpy seeds 1 to 5:
- (a) lower bound: -260.7 to -262.6
- (b) upper bound: +3.4 to +4.3

So neither verdict depends on the bootstrap seed. The t interval gives the same verdicts.

## 2. Secondary (95%, paired by seed)

| Contrast | Mean diff | Bootstrap 95% | t 95% | Seeds > 0 |
|---|---|---|---|---|
| RVS minus HRS | -1482.30 | [-1628.67, -1341.20] | [-1668.87, -1295.74] | 0 / 8 |
| RVS-bare minus HRS-bare | -1222.49 | [-1395.32, -1020.25] | [-1466.27, -978.72] | 0 / 8 |
| RES-swap minus RES (manipulation check) | -2408.56 | [-2502.45, -2327.91] | [-2521.46, -2295.66] | 0 / 8 |

**Manipulation check passes:** the whole RES-swap minus RES interval is below 0, by both methods.

## 3. Fresh-land survival (mean of `survived`, 50 fresh lives per seed, 95%)

| Brain | Per seed (1 to 8) | Mean | Bootstrap 95% | t 95% | Lower bound at or above 0.80? |
|---|---|---|---|---|---|
| HRS | 0.88, 0.84, 0.92, 0.84, 0.86, 0.94, 0.86, 0.88 | 0.8775 | [0.8550, 0.9025] | [0.8473, 0.9077] | yes (both) |
| RES | 0.84, 0.88, 0.94, 0.82, 0.88, 0.94, 0.84, 0.88 | 0.8775 | [0.8500, 0.9050] | [0.8402, 0.9148] | yes (both) |
| RVS | 0.30, 0.52, 0.18, 0.22, 0.22, 0.30, 0.10, 0.32 | 0.2700 | [0.1950, 0.3575] | [0.1658, 0.3742] | no (both) |

## 4. Probe ("toward" share, 95%, paired by seed)

Each brain's mean "toward" share:

| Brain | Hungry: mean [boot 95%] {t 95%} | Tired: mean [boot 95%] {t 95%} |
|---|---|---|
| HRS | 0.8675 [0.8175, 0.9100] {0.8083, 0.9267} | 0.7525 [0.6025, 0.8550] {0.5804, 0.9246} |
| RES | 0.8425 [0.7875, 0.8875] {0.7772, 0.9078} | 0.7000 [0.6000, 0.7800] {0.5814, 0.8186} |
| RVS | 0.5550 [0.5050, 0.6100] {0.4859, 0.6241} | 0.6025 [0.5600, 0.6525] {0.5429, 0.6621} |
| RES-swap | 0.1475 [0.1125, 0.1900] {0.0970, 0.1980} | 0.8525 [0.7700, 0.9150] {0.7563, 0.9487} |
| chance (same for every brain and seed) | 0.292 | 0.348 |

Paired differences:

| Contrast | Mean diff | Bootstrap 95% | t 95% | Seeds > 0 |
|---|---|---|---|---|
| RES minus HRS, hungry | -0.0250 | [-0.0600, +0.0100] | [-0.0712, +0.0212] | 2 / 8 |
| RVS minus HRS, hungry | -0.3125 | [-0.3875, -0.2200] | [-0.4212, -0.2038] | 0 / 8 |
| RES minus HRS, tired | -0.0525 | [-0.1875, +0.1300] | [-0.2638, +0.1588] | 1 / 8 |
| RVS minus HRS, tired | -0.1500 | [-0.2825, +0.0150] | [-0.3442, +0.0442] | 2 / 8 |

Every brain is above chance on both needs (toward minus chance: interval above 0), except RES-swap on "hungry". RES-swap hungry is below chance: -0.1445, bootstrap [-0.1795, -0.1020].

## Things that look odd in the data (noted, not judged)

1. **W3n has 16 seeds** of HRS and HRS-bare; only seeds 1 to 8 were used here, as the task says. W3n also has `HRS-off`, and W3o has `RES-off`, `RVS-off`, `RVS-swap`, `REY` and `RVY` files. None of these were used.
2. **Primary (a) is driven by two seeds.** Seeds 1 and 2 lose about 507 and 366 steps; seeds 6 and 7 gain about 339 and 173. That spread is why the lower bound passes -200 and the verdict is "unclear".
3. **Primary (b) sits on the edge of "real".** The upper bound is only +3.7 (exact: +3.9) steps above 0. By the fixed rule the verdict is "small", not "real", but a loss of about 72 steps is likely.
4. **HRS seed 7, "tired", is an outlier.** Its toward share is 0.28, below chance (0.348); the other seeds are 0.68 to 0.88. It alone gives the only positive RES minus HRS "tired" seed (+0.52) and widens that interval.
5. **RES-swap fails on hunger only.** Its "hungry" toward share (0.15) is below chance, while "tired" (0.85) is as high as HRS. This fits a swap that touches the food cue only, but I did not check what the swap changes.
6. **RVS lives longer on fresh lands than on test lands** (fresh mean lifespan 1528.2 versus 1320.6 on test; fresh survival 0.270 versus 0.2075 on test). RVS-bare almost never survives on test lands (7 of 8 seeds at 0.00; seed 8 at 0.04).
7. **The probe's "chance" share is one constant per need** (0.292 hungry, 0.348 tired) across all brains and seeds.

## Summary of verdicts

- **(a) RES-bare minus HRS-bare:** -52 steps, 97.5% [-261, +143]. **Unclear** (4 of 8 seeds above 0).
- **(b) RES minus HRS:** -72 steps, 97.5% [-152, +4]. **Small** (3 of 8 seeds above 0); the upper bound is barely above 0.
- **RVS** is far worse than HRS: -1482 steps with reflexes, -1222 bare (95% intervals well below 0; 0 of 8 seeds above 0).
- **Manipulation check passes:** RES-swap minus RES is -2409 steps, 95% [-2502, -2328].
- **Fresh-land survival:** HRS 0.878 [0.855, 0.903] and RES 0.878 [0.850, 0.905] reach 0.80; RVS 0.270 [0.195, 0.358] does not.
- **Probe:**
  - RES is not clearly different from HRS on either need: hungry -0.025 [-0.060, +0.010]; tired -0.053 [-0.188, +0.130].
  - RVS is lower on hungry: -0.313 [-0.388, -0.220].
  - RVS on tired is unclear: -0.150 [-0.283, +0.015].
