# CW2 blind recompute

Done without seeing the study's analysis script (analyse_cw2.py) or its analysis outputs, findings, round-table files or worklog; written only from the frozen plan (questions.md, Measures) and the raw output/{ARM}_{SEED}.jsonl files (pilot files ignored).

- Date: 2026-11-27 EST
- Script: recompute_cw2_blind.py
- RNG: numpy.random.default_rng(20261127); one shared 10000 x 16 resample-index matrix
- Python 3.12.10, numpy 2.5.3
- Method: per seed = mean over its 50 lives; differences paired by seed; 95% percentile bootstrap of the mean difference over the 16 seeds, 10,000 resamples.

## Contrasts (mean over 16 seeds, 95% CI, seeds positive / negative / tied)

| item | contrast | measure | mean diff | 95% CI | +/-/0 seeds |
|---|---|---|---|---|---|
| 1 Primary | GUIDE-REFLEX − NO-GUIDE | chains | 0.627 | [0.432, 0.843] | 16/0/0 |
| 2 Key secondary | GUIDE-MAP − NO-GUIDE | chains | 0.108 | [0.060, 0.161] | 12/2/2 |
| 3a | GUIDE-REFLEX − SHAM-REFLEX | chains | 0.804 | [0.573, 1.054] | 16/0/0 |
| 3b | GUIDE-MAP − SHAM-MAP | chains | 0.091 | [0.046, 0.145] | 12/1/3 |
| 4a | GUIDE-REFLEX − NO-GUIDE | survival | -0.015 | [-0.026, -0.005] | 1/7/8 |
| 4b | GUIDE-MAP − NO-GUIDE | survival | -0.003 | [-0.007, 0.002] | 1/3/12 |

Per-seed differences (seeds 1..16):

- 1 Primary GUIDE-REFLEX − NO-GUIDE (chains): 0.740, 0.520, 1.360, 0.060, 0.540, 0.540, 1.320, 0.240, 0.600, 0.220, 0.420, 1.440, 0.580, 0.060, 0.400, 1.000
- 2 Key secondary GUIDE-MAP − NO-GUIDE (chains): 0.100, 0.080, 0.360, 0.100, 0.240, 0.100, 0.160, 0.060, 0.160, 0.060, -0.020, 0.240, 0.000, 0.000, 0.100, -0.020
- 3a GUIDE-REFLEX − SHAM-REFLEX (chains): 0.720, 0.540, 1.700, 0.140, 0.640, 0.960, 1.380, 0.460, 0.840, 0.380, 0.500, 1.800, 0.840, 0.060, 0.660, 1.240
- 3b GUIDE-MAP − SHAM-MAP (chains): 0.040, -0.020, 0.380, 0.060, 0.200, 0.080, 0.060, 0.100, 0.160, 0.000, 0.020, 0.160, 0.040, 0.000, 0.180, 0.000
- 4a GUIDE-REFLEX − NO-GUIDE (survival): -0.020, -0.020, -0.020, 0.000, 0.000, 0.000, 0.020, -0.060, 0.000, 0.000, 0.000, -0.040, -0.040, 0.000, -0.060, 0.000
- 4b GUIDE-MAP − NO-GUIDE (survival): 0.020, 0.000, 0.000, -0.020, 0.000, -0.020, 0.000, 0.000, -0.020, 0.000, 0.000, 0.000, 0.000, 0.000, 0.000, 0.000

## 5. Per-arm means over seeds

| arm | chains per life | survival | share of lives with chains >= 1 |
|---|---|---|---|
| GUIDE-REFLEX | 1.110 | 0.806 | 0.255 |
| GUIDE-MAP | 0.590 | 0.819 | 0.255 |
| SHAM-REFLEX | 0.306 | 0.812 | 0.255 |
| SHAM-MAP | 0.499 | 0.821 | 0.255 |
| NO-GUIDE | 0.483 | 0.821 | 0.255 |
| RANDOM-OPS | 0.000 | 0.782 | 0.000 |

## 6. Manipulation / data checks

- RANDOM-OPS has 0 chains in every life: YES (800 lives, max chains 0)
- Every file (96 files) has 50 lives with 50 distinct land values = 940001-940050, arm/seed fields matching the filename: YES
Note (extra check, run separately): the share of lives with chains >= 1 is identical (0.255) in the five
non-random arms because it is the same 204 of 800 lives (seed, land) in each arm. This fits the plan's rule that
guidance can start only after a join at the station has been experienced: whether a life gets any chain is set
before any guidance, and the arms differ only in how many chains follow the first one.
