# W3p: independent blind recompute

- **Who:** a fresh assistant session (a subagent), 23 November 2026.
- **Not read:** `analyse_w3p.py`, `analysis.md`, `analysis.json`, `analysis.out`, and every `findings*` / `recompute*`
  file in W3p, W3n and scorecard.
- **Script:** `recompute_w3p_blind.py`, written fresh. It reads only the raw result files below.
- **How it was run:** `OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 python recompute_w3p_blind.py`.

## Method

- **Seeds:** 1 to 8 for every arm. Each arm is the kept copy, "S".
- **Value per seed:**
  - Probes: the `success` value from `scorecard/bp/output/<TEST>_<ARM>S_<seed>.json`. For PLAN it is `uphill`.
  - Lifespan: the mean `lifespan` over the 50 lives in `test_<ARM>S_<seed>.json` (reflexes on) or
    `test_<ARM>S-bare_<seed>.json` (reflexes off).
  - Fresh lands: the mean `survived` in `test_fresh_<ARM>S_<seed>.json`.
  - MB, MBb and MV come from `workbench/W3p/output/`. HR comes from `workbench/W3n/output/`.
- **Differences:** paired by seed (arm A seed k minus arm B seed k).
- **Bootstrap:**
  - Resamples seeds with replacement: 8 of 8, **50,000 resamples**.
  - numpy `default_rng(20261123)`. Every measure uses the same resample indices.
  - Reports the 5th and 95th percentiles of the resampled mean, read as a one-sided 95% bound.
- **t interval:** mean ± t(0.95, df 7) × sd/√8, with t = 1.8946. This gives the matching one-sided 95% bounds.

## Files read (per test and arm)

Every cell is **8 files** (seeds 1 to 8). No file was missing.

| measure | MB | MBb | MV | HR |
|---|---|---|---|---|
| R2 | 8 | 8 | 8 | 8 |
| R5d | 8 | 8 | 8 | 8 |
| M2 | 8 | 8 | 8 | 8 |
| PLAN | 8 | 8 | 8 | 8 |
| life (`<ARM>S`) | 8 | 8 | 8 | 8 |
| life bare (`<ARM>S-bare`) | 8 | 8 | 8 | 8 |
| fresh (`test_fresh_<ARM>S`) | 8 | 8 | 8 | 8 |

Cases per probe file:
- R2: 36 for all files.
- R5d: 8 for all files.
- M2: 50 for all files.
- PLAN: 36 for all files.

Each life file is a list of 50 lives.

## Results (mean over 8 seeds; bootstrap 5th to 95th percentile; t 5th to 95th)

### 1. Primary: R2 detours

| quantity | mean | boot 5th | boot 95th | t 5th | t 95th |
|---|---|---|---|---|---|
| **MB − HR** | **0.5312** | **0.4479** | 0.6250 | 0.4282 | 0.6343 |
| MB (own) | 0.7986 | **0.7396** | 0.8576 | 0.7264 | 0.8708 |

- **Primary, MB − HR > 0:** **YES.** The 5th percentile is 0.448, well above 0. MB beats HR on every seed; the paired
  per-seed differences range from 0.417 to 0.833.
- **MB's own R2 5th percentile ≥ 0.80:** **NO.** The 5th percentile is 0.740 (t: 0.726), and the mean itself is 0.799,
  just under 0.80.

### 2. R2 by arm and the other contrasts

| quantity | mean | boot 5th | boot 95th | t 5th | t 95th |
|---|---|---|---|---|---|
| R2 MB | 0.7986 | 0.7396 | 0.8576 | 0.7264 | 0.8708 |
| R2 MBb | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 |
| R2 MV | 0.2778 | 0.2049 | 0.3611 | 0.1819 | 0.3737 |
| R2 HR | 0.2674 | 0.2153 | 0.3194 | 0.2037 | 0.3310 |
| MBb − MB | 0.2014 | 0.1424 | 0.2604 | 0.1292 | 0.2736 |
| MB − MV | 0.5208 | 0.4236 | 0.6285 | 0.3943 | 0.6473 |
| MV − HR | 0.0104 | −0.0868 | 0.1111 | −0.1126 | 0.1334 |
| (extra) MBb − HR | 0.7326 | 0.6806 | 0.7847 | 0.6690 | 0.7963 |

- **MBb's R2 5th percentile ≥ 0.80:** **YES.** All 8 seeds score 1.000, so the interval collapses to 1.000.
- **MBb > MB:** yes. The 5th percentile is 0.142.
- **MB > MV:** yes. The 5th percentile is 0.424.
- **MV vs HR:** no difference. The interval spans 0, from −0.087 to 0.111.

### 3. R5d (long detours) and M2 (memory)

| quantity | mean | boot 5th | boot 95th | t 5th | t 95th |
|---|---|---|---|---|---|
| R5d MB | 0.0625 | 0.0000 | 0.1250 | −0.0150 | 0.1400 |
| R5d MBb | 0.8750 | 0.7969 | 0.9375 | 0.7855 | 0.9645 |
| R5d MV | 0.0469 | 0.0156 | 0.0781 | 0.0035 | 0.0902 |
| R5d HR | 0.1250 | 0.0625 | 0.1875 | 0.0475 | 0.2025 |
| **R5d MB − HR** | −0.0625 | −0.1562 | 0.0469 | −0.1891 | 0.0641 |
| M2 MB | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 |
| M2 MBb | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 |
| M2 MV | 0.9875 | 0.9800 | 0.9950 | 0.9775 | 0.9975 |
| M2 HR | 0.8250 | 0.6950 | 0.9000 | 0.6982 | 0.9518 |
| **M2 MB − HR** | 0.1750 | 0.1000 | 0.3050 | 0.0482 | 0.3018 |

- **R5d:** MB does not beat HR. The interval spans 0 and the mean is slightly negative. MB scores 0 on 6 of 8 seeds.
  Only MBb does well on long detours.
- **M2:** MB beats HR; the 5th percentile is above 0 (bootstrap 0.100, t 0.048). Part of the gap comes from one HR seed
  (seed 7, M2 = 0.36). Without that seed the gap is about 0.11 on every seed.

### 4. Lifespan (mean of 50 lives, capped at 3000)

| quantity | mean | boot 5th | boot 95th | t 5th | t 95th |
|---|---|---|---|---|---|
| reflexes on, MB | 2956.4 | 2935.1 | 2976.4 | 2930.8 | 2982.1 |
| reflexes on, MBb | 3000.0 | 3000.0 | 3000.0 | 3000.0 | 3000.0 |
| reflexes on, MV | 2901.1 | 2869.2 | 2931.2 | 2863.1 | 2939.0 |
| reflexes on, HR | 2802.9 | 2745.8 | 2858.0 | 2734.3 | 2871.6 |
| **on, MB − HR** | 153.5 | 91.5 | 212.5 | 79.1 | 227.9 |
| **on, MBb − HR** | 197.1 | 142.0 | 254.2 | 128.4 | 265.7 |
| bare, MB | 2843.3 | 2801.8 | 2881.9 | 2794.3 | 2892.3 |
| bare, MBb | 2983.3 | 2970.1 | 2995.2 | 2967.8 | 2998.9 |
| bare, MV | 2566.6 | 2502.7 | 2626.2 | 2490.5 | 2642.6 |
| bare, HR | 1607.5 | 1463.2 | 1735.9 | 1438.9 | 1776.1 |
| **bare, MB − HR** | 1235.8 | 1114.7 | 1373.4 | 1076.5 | 1395.1 |
| **bare, MBb − HR** | 1375.8 | 1245.2 | 1527.1 | 1202.5 | 1549.1 |

- MB and MBb both outlive HR, with reflexes on and bare; every 5th percentile is above 0.
- With reflexes on, MB − HR is negative on one seed (seed 8, −47).
- Bare, the gap is about 1,200 to 1,400 steps. HR depends heavily on the reflexes; the new brains hardly do.

### 5. Fresh-land survival (share of 50 lives)

| arm | mean | boot 5th | boot 95th | t 5th | t 95th |
|---|---|---|---|---|---|
| MB | 0.9900 | 0.9775 | 1.0000 | 0.9757 | 1.0043 |
| MBb | 0.9975 | 0.9925 | 1.0000 | 0.9928 | 1.0022 |
| MV | 0.9550 | 0.9375 | 0.9725 | 0.9326 | 0.9774 |
| HR | 0.8775 | 0.8575 | 0.8975 | 0.8533 | 0.9017 |

### 6. PLAN `uphill`

| arm | mean | boot 5th | boot 95th | t 5th | t 95th |
|---|---|---|---|---|---|
| MB | 0.8507 | 0.8056 | 0.8958 | 0.7954 | 0.9060 |
| MBb | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 |
| MV | 0.5382 | 0.4861 | 0.5938 | 0.4708 | 0.6056 |
| HR | 0.0764 | 0.0382 | 0.1146 | 0.0300 | 0.1228 |

## Per-seed values (seeds 1 to 8)

| measure | MB | MBb | MV | HR |
|---|---|---|---|---|
| R2 | .861 .917 .722 .833 .778 .667 .667 .944 | all 1.000 | .556 .111 .333 .306 .333 .167 .278 .139 | .194 .417 .306 .250 .361 .250 .250 .111 |
| R5d | 0 .25 0 0 0 0 0 .25 | .875 .625 .875 .75 1 1 1 .875 | .125 0 .125 .125 0 0 0 0 | .125 .125 .25 .25 0 .25 0 0 |
| M2 | all 1.00 | all 1.00 | .98 1 .98 1 1 .96 1 .98 | .86 .90 .88 .92 .92 .86 .36 .90 |
| PLAN | .889 .917 .750 .889 .861 .778 .750 .972 | all 1.000 | .694 .500 .500 .583 .667 .444 .500 .417 | 0 .083 .111 .194 .139 .056 0 .028 |
| fresh | 1 1 1 1 1 1 .98 .94 | 1 .98 1 1 1 1 1 1 | .96 .92 .90 .96 1 .94 .98 .98 | .88 .84 .92 .84 .86 .94 .86 .88 |

## Anything odd in the data

1. **Extra HR files.**
   - HR has a 9th probe file for R2, R5d and M2 (`*_HRS_9.json`), but no `PLAN_HRS_9`.
   - HR's life-test folder (W3n) has seeds 1 to 16.
   - As instructed, only seeds 1 to 8 were used. Including HR seed 9 or seeds 9 to 16 would change the HR numbers.
2. **MBb sits at the ceiling.**
   - R2 = 1.000, PLAN = 1.000, M2 = 1.000 and reflexes-on lifespan = 3000 on every one of the 8 seeds.
   - Its bootstrap and t intervals are therefore zero-width. The verdict "5th percentile ≥ 0.80" holds trivially.
   - A perfect score on every seed is worth a sanity check: is the probe easier for this arm, or does it overlap with
     training? Nothing in the raw files shows a fault.
3. **R5d is coarse.** It has only 8 cases per seed, so each seed's value moves in steps of 0.125.
4. **One HR M2 outlier.** HR seed 7 scores M2 = 0.36; the other seven seeds score 0.86 to 0.92. This widens HR's M2
   interval and lifts the MB − HR gap.
5. **Data integrity.** No integrity problems were found:
   - every `agent` and `test` field matches its file name;
   - every probe value is in 0..1;
   - every life file has exactly 50 lives, with lifespan ≤ 3000;
   - `survived` = 1 exactly when lifespan = 3000.

## Verdicts

| check | result | verdict |
|---|---|---|
| Primary: R2 MB − HR, 5th percentile > 0 | 0.531 [boot 5th 0.448; t 0.428] | **YES** |
| MB R2 5th percentile ≥ 0.80 | 0.799 [boot 5th 0.740; t 0.726] | **NO** |
| MBb R2 5th percentile ≥ 0.80 | 1.000 [1.000] | **YES** (at ceiling) |
| R2 MBb − MB > 0 | 0.201 [0.142] | yes |
| R2 MB − MV > 0 | 0.521 [0.424] | yes |
| R2 MV − HR > 0 | 0.010 [−0.087] | no (no difference) |
| R5d MB − HR > 0 | −0.063 [−0.156] | no |
| M2 MB − HR > 0 | 0.175 [0.100; t 0.048] | yes (helped by HR seed 7) |
| Lifespan on, MB − HR | +153.5 [91.5] | yes |
| Lifespan on, MBb − HR | +197.1 [142.0] | yes |
| Lifespan bare, MB − HR | +1235.8 [1114.7] | yes |
| Lifespan bare, MBb − HR | +1375.8 [1245.2] | yes |
