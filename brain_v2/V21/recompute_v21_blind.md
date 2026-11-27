# V2-1 Revise: blind recompute

Done without seeing the study's analysis script (`analyse_v21.py`) or its outputs (`analysis.json`, `analysis.md`),
findings, roundtable files or worklogs; worked only from the frozen plan `questions.md` and the raw `output/*.jsonl`
(files starting with `pilot` ignored).

- Date: 2026-11-27 (EST)
- Script: `recompute_v21_blind.py`
- Method: per seed = mean over its 50 lives; differences paired by seed; 95% percentile bootstrap over the 16 seeds, 10,000 resamples; one shared resample index matrix from `numpy.random.default_rng(20261127)`.
- RNG seed: 20261127
- Python 3.12.10, numpy 2.5.3

Format: mean difference [95% CI]  seeds positive / negative / tied.

## 1. Primary: swap survival, SURPRISE - PLAIN
+0.625 [+0.581, +0.667]  seeds +16 / -0 / =0
Lower end above 0: YES

## 2. No-loss gate: stable survival, SURPRISE - PLAIN
-0.001 [-0.007, +0.005]  seeds +3 / -4 / =9
Lower end above -0.03: YES (pass)

## 3. Swap survival, SURPRISE - SHAM and SURPRISE - WINDOW
- SURPRISE - SHAM:   +0.600 [+0.551, +0.649]  seeds +16 / -0 / =0
- SURPRISE - WINDOW: +0.561 [+0.496, +0.621]  seeds +16 / -0 / =0
- (also, stable WINDOW - PLAIN: -0.004 [-0.011, +0.004]  seeds +3 / -6 / =7)

## 4. Per arm and condition (mean over 16 seed means)

| arm | cond | survival | resets per life |
|---|---|---|---|
| PLAIN | swap | 0.226 | 0.000 |
| SURPRISE | swap | 0.851 | 2.348 |
| WINDOW | swap | 0.290 | 0.000 |
| SHAM | swap | 0.251 | 18.552 |
| PLAIN | stable | 0.849 | 0.000 |
| SURPRISE | stable | 0.848 | 0.618 |
| WINDOW | stable | 0.845 | 0.000 |
| SHAM | stable | 0.838 | 0.694 |

Test B per arm:

| arm | chains_before | chains_after | resets per life |
|---|---|---|---|
| PLAIN | 2.732 | 0.816 | 0.000 |
| SURPRISE | 2.732 | 1.681 | 0.370 |
| WINDOW | 2.721 | 1.740 | 0.000 |
| SHAM | 2.732 | 0.626 | 0.841 |

## 5. Test B
- chains_after SURPRISE - PLAIN:  +0.865 [+0.647, +1.090]  seeds +15 / -1 / =0
- chains_after WINDOW - PLAIN:    +0.924 [+0.711, +1.143]  seeds +16 / -0 / =0
- chains_before SURPRISE - PLAIN: +0.000 [+0.000, +0.000]  seeds +0 / -0 / =16  (|mean| within 0.3: YES)
- (also, chains_after SURPRISE - SHAM: +1.055 [+0.834, +1.282]  seeds +16 / -0 / =0)
- (also, chains_after SURPRISE - WINDOW: -0.059 [-0.169, +0.057]  seeds +5 / -11 / =0)

## 6. Checks
- Test A files with 50 lives and 50 distinct lands 960001-960050: 128/128
- Test B files with 50 lives and 50 distinct lands 970001-970050: 64/64
- PLAIN total resets (all A and B lives): 0
