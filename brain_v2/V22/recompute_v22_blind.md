# V2-2 Goals: blind recompute

Done on 2026-11-28 (EST) WITHOUT seeing the study's analysis script (`analyse_v22.py`) or any of its outputs (analysis.json/.md, findings, roundtable, WORKLOG). Worked only from `questions.md` and the raw files in `output/` and `bp_output/`.

- Method: per seed = mean over its 50 lives; differences paired by seed; 95% percentile bootstrap over 16 seeds, 10,000 resamples.
- RNG: `numpy.random.default_rng(20261128)`, one 10,000 x 16 index matrix reused for all comparisons (the no-pilot-seeds subset uses its own matrix from the same seed).
- Python 3.12.10, numpy 2.5.3 (Windows-10-10.0.19045-SP0).
- Bob Profile score: first present of success, survived, ratio, tracks; else lifespan/3000.

## 1. Primary: chains per life, GOAL - FT-NOGOAL
- All 16 seeds: mean -0.096, 95% CI [-0.225, +0.039], seeds +5 / -11 / =0  -> real gain (lower end > 0): NO
- Without pilot seeds 1-2 (14 seeds): mean -0.096, 95% CI [-0.244, +0.057], seeds +5 / -9 / =0
- Per-seed differences: s1 -0.140, s2 -0.060, s3 +0.060, s4 -0.320, s5 +0.120, s6 -0.080, s7 -0.040, s8 -0.580, s9 -0.400, s10 +0.300, s11 -0.260, s12 +0.180, s13 -0.080, s14 +0.440, s15 -0.520, s16 -0.160

## 2. GOAL - ref GUIDE-REFLEX
- Chains: mean -1.009, 95% CI [-1.397, -0.641], seeds +1 / -15 / =0  -> lower end above -0.2: NO
- Survival: mean +0.026, 95% CI [-0.035, +0.089], seeds +8 / -7 / =1  -> lower end above -0.03: NO

## 3. Chains GOAL - GOAL-ABLATE
- mean +0.004, 95% CI [-0.059, +0.069], seeds +7 / -8 / =1

## 4. Plain-land survival minus RMS
- GOAL - RMS: mean -0.006, 95% CI [-0.044, +0.036], seeds +6 / -8 / =2  -> lower end above -0.03: NO
- FT-NOGOAL - RMS: mean -0.016, 95% CI [-0.060, +0.029], seeds +5 / -8 / =3  -> lower end above -0.03: NO
- GOAL-NOFLOOR - RMS (extra): mean +0.020, 95% CI [-0.020, +0.064], seeds +7 / -6 / =3  -> lower end above -0.03: YES
- SHAM-GOAL - RMS (extra): mean +0.016, 95% CI [-0.016, +0.050], seeds +8 / -7 / =1  -> lower end above -0.03: YES
- Plain survival means: RMS 0.859, GOAL 0.853, GOAL-NOFLOOR 0.879, FT-NOGOAL 0.843, SHAM-GOAL 0.875

## 5. Bob Profile, paired difference vs RMS
### GOAL
| test | RMS mean | arm mean | diff mean | CI lower | CI upper |
|---|---|---|---|---|---|
| L2 | 0.896 | 0.880 | -0.016 | -0.041 | +0.010 |
| R2 | 0.260 | 0.188 | -0.073 | -0.109 | -0.042 |
| R5d | 0.125 | 0.094 | -0.031 | -0.070 | +0.008 |
| M2 | 0.818 | 0.755 | -0.063 | -0.129 | -0.006 |
| M2e | 0.502 | 0.504 | +0.001 | -0.048 | +0.052 |
| G2 | 0.820 | 0.806 | -0.015 | -0.063 | +0.031 |
| A2 | 0.804 | 0.817 | +0.013 | -0.054 | +0.080 |
| A5s | 0.274 | 0.170 | -0.104 | -0.165 | -0.041 |
- Tests with CI lower end below -0.05: R2, R5d, M2, G2, A2, A5s

### FT-NOGOAL
| test | RMS mean | arm mean | diff mean | CI lower | CI upper |
|---|---|---|---|---|---|
| L2 | 0.896 | 0.901 | +0.004 | -0.021 | +0.030 |
| R2 | 0.260 | 0.151 | -0.109 | -0.149 | -0.075 |
| R5d | 0.125 | 0.094 | -0.031 | -0.094 | +0.023 |
| M2 | 0.818 | 0.776 | -0.041 | -0.084 | -0.003 |
| M2e | 0.502 | 0.480 | -0.022 | -0.074 | +0.034 |
| G2 | 0.820 | 0.787 | -0.033 | -0.087 | +0.019 |
| A2 | 0.804 | 0.835 | +0.031 | -0.022 | +0.089 |
| A5s | 0.274 | 0.169 | -0.105 | -0.146 | -0.060 |
- Tests with CI lower end below -0.05: R2, R5d, M2, M2e, G2, A5s

## 6. Per-arm means (mean of 16 per-seed means)
| arm | chains per life | survival |
|---|---|---|
| GOAL | 0.740 | 0.844 |
| GOAL-NOFLOOR | 0.821 | 0.846 |
| FT-NOGOAL | 0.836 | 0.863 |
| SHAM-GOAL | 0.806 | 0.863 |
| GOAL-ABLATE | 0.736 | 0.840 |
| ref GUIDE-REFLEX | 1.749 | 0.818 |
| ref NO-GUIDE | 0.730 | 0.828 |

## 7. Checks
- jsonl files present: 256 in output/ (expected set of 192 test/ref/plain files; missing: 0).
- Every jsonl file has 50 lives with 50 distinct lands: PASS (also checked the unseen_* files present in output/).
  - plain_* land ranges (min-max): [(910001, 910050)]
  - ref_* land ranges (min-max): [(990001, 990050)]
  - test_* land ranges (min-max): [(990001, 990050)]
  - unseen_* land ranges (min-max): [(995001, 995050)]
- Bob Profile files (8 tests x 5 WHO x 16 seeds = 640): PASS, all present

