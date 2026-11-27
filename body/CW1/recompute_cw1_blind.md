# CW1 blind recompute

Done on 2026-11-26 (EST) by a fresh session **without seeing the study's analysis script** (`analyse_cw1.py`), `output/analysis.*`, any findings or roundtable file, or the WORKLOG. Sources: the frozen plan `questions.md` (Measures) and the raw files `output/{ARM}_{SEED}.jsonl` (pilot files ignored).

- Script: `recompute_cw1_blind.py`. Python 3.12.10, numpy 2.5.3.
- Bootstrap: 10,000 resamples of the 16 seeds with replacement, 95% percentile interval (numpy `percentile`, linear), `numpy.random.default_rng(20261126)`; one index matrix shared by all contrasts, so every contrast is paired by seed.
- Unit: per seed, the mean over its 50 lives; differences are paired by seed; "mean" = mean over 16 seeds.
- Populations: 16 seeds x 50 lives = 800 lives per arm.

## 1. Primary: mean completed chains per life, LEARN - RANDOM-OPS

| seed | LEARN | RANDOM-OPS | diff | NO-MAKE | PAD |
|---|---|---|---|---|---|
| 1 | 6.340 | 0.620 | 5.720 | 0.000 | 5.460 |
| 2 | 4.820 | 0.800 | 4.020 | 0.000 | 4.080 |
| 3 | 6.960 | 0.860 | 6.100 | 0.000 | 6.260 |
| 4 | 6.060 | 0.480 | 5.580 | 0.000 | 5.700 |
| 5 | 5.940 | 0.640 | 5.300 | 0.000 | 4.780 |
| 6 | 4.320 | 0.420 | 3.900 | 0.000 | 4.260 |
| 7 | 5.140 | 0.360 | 4.780 | 0.000 | 6.780 |
| 8 | 5.060 | 0.620 | 4.440 | 0.000 | 4.040 |
| 9 | 5.500 | 0.860 | 4.640 | 0.000 | 5.020 |
| 10 | 6.560 | 0.660 | 5.900 | 0.000 | 6.480 |
| 11 | 6.240 | 0.780 | 5.460 | 0.000 | 6.660 |
| 12 | 6.140 | 0.720 | 5.420 | 0.000 | 5.020 |
| 13 | 5.860 | 0.720 | 5.140 | 0.000 | 7.900 |
| 14 | 5.340 | 0.720 | 4.620 | 0.000 | 3.860 |
| 15 | 6.600 | 0.680 | 5.920 | 0.000 | 7.040 |
| 16 | 4.800 | 0.460 | 4.340 | 0.000 | 3.380 |
| **mean** | 5.730 | 0.650 | **5.080** | 0.000 | 5.420 |

- LEARN - RANDOM-OPS: **5.080** chains per life, 95% CI **[4.739, 5.405]** (16 seeds, 800 lives per arm).
- Seeds with a positive difference: **16 of 16** (negative 0, zero 0).
- Lower end above 0: **yes**.

## 2. Share of lives with 3+ chains

| arm | pooled (800 lives) | mean of per-seed shares |
|---|---|---|
| LEARN | 0.446 | 0.446 |
| RANDOM-OPS | 0.030 | 0.030 |
| NO-MAKE | 0.000 | 0.000 |
| PAD | 0.396 | 0.396 |

- LEARN - RANDOM-OPS in per-seed share: **0.416**, 95% CI **[0.388, 0.444]**; seeds positive 16 of 16.

## 3. Share of lives with 1+ chains

| arm | pooled (800 lives) | mean of per-seed shares |
|---|---|---|
| LEARN | 0.930 | 0.930 |
| RANDOM-OPS | 0.453 | 0.453 |
| NO-MAKE | 0.000 | 0.000 |
| PAD | 0.879 | 0.879 |

- (Extra) LEARN - RANDOM-OPS in per-seed share: 0.478, 95% CI [0.440, 0.518].

## 4. LEARN - NO-MAKE: lifespan and full-life survival

| arm | mean lifespan (steps) | survival share |
|---|---|---|
| LEARN | 2679.454 | 0.847 |
| RANDOM-OPS | 2554.710 | 0.763 |
| NO-MAKE | 2669.735 | 0.846 |
| PAD | 2554.684 | 0.804 |

- Lifespan: LEARN - NO-MAKE **9.719** steps, 95% CI **[-64.076, 79.771]**.
- Survival: LEARN - NO-MAKE **0.001**, 95% CI **[-0.024, 0.029]**.

## 5. PAD - LEARN: mean chains per life

- PAD 5.420 vs LEARN 5.730: difference **-0.310**, 95% CI **[-0.764, 0.200]**; seeds where PAD > LEARN 4 of 16.

## 6. Manipulation and integrity checks

- NO-MAKE lives with chains != 0: **0** of 800; with joins != 0: **0** of 800.
- Every file has exactly 50 lives with 50 distinct `land` values (and matching arm/seed fields): **yes** (64 files).
- Every file uses the same set of lands: **yes** (lands 920001-920050).

