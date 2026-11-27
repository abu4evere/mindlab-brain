# W3r blind recompute

## Who did this, and how it was kept blind
- Done by a Claude Code subagent (model claude-opus-5-5), working from the raw data and the definitions in the task prompt only.
- **What I opened:** the directory listing of `C:\mindlab\workbench\W3r\output\` filtered to `test_fresh_*.json`, and the 80 files `test_fresh_{RVS,RMS,RMXS,RE5S,HRS}_{1..16}.json`. One record of `test_fresh_RMS_1.json` was printed to see the field names. I also wrote and ran my own script.
- **What I did not open:** `analyse_w3r.py`, `analysis.json`, `analysis.md`, `probe.json`, `probe_w3r.py`, any `findings*.md`, any `recompute_*.md` (other than writing this one), `finish_run.log`, gate files, anything under `C:\acl` or `C:\mindlab\body`, and the other `test_fresh_*` arm variants (such as `-bare`, `-off`, `-midswap`). I did not list the W3r folder itself, and I did not search the disk for other analyses. I also did not run `graphify`. A hook suggested it, but that would have broken blindness, and the inputs are raw data, not code.

## Time and machine
- Time (Git Bash, `TZ='EST5EDT,M3.2.0,M11.1.0' date`): run at Thu Nov 26 19:23:57 EST 2026. Final rerun at Thu Nov 26 19:24:42 EST 2026.
- Platform: Windows-10-10.0.19045-SP0
- Python: 3.12.10 (tags/v3.12.10:0cc8128, Apr 8 2025) MSC v.1943 64 bit (AMD64), run with `-I`
- numpy: 2.5.4

## Inputs
- `C:\mindlab\workbench\W3r\output\test_fresh_{ARM}_{SEED}.json`, with ARM in RVS, RMS, RMXS, RE5S, HRS and SEED 1..16 (80 files).
- Script: `C:\mindlab\workbench\W3r\recompute_w3r_blind.py` (run as `python -I recompute_w3r_blind.py`). Every number below is copied from its output.

## Definitions used (from the frozen plan, as given)
- Per arm and seed: fresh-land survival = mean of `survived` over the file's lives. Lifespan = mean of `lifespan`.
- Each contrast is a paired difference per seed (arm A − arm B on the same seed). The point estimate is the mean of those 16 differences.
- PRIMARY: RMS − RVS in survival. "A real gain" if the whole 95% interval is above 0. I also count the seeds where RMS > RVS.
- SECONDARY: RMS − RMXS, RE5S − RVS and RMS − HRS in survival, plus RMS − RVS in lifespan.

## How the bootstrap was drawn
- 10,000 resamples of the 16 per-seed differences, with replacement.
- RNG: `numpy.random.default_rng(1)`. Indices come from `rng.integers(0, 16, size=(10000, 16))`, then each row of resampled differences is averaged.
- The interval is the 2.5th and 97.5th percentiles of the 10,000 resampled means (`numpy.percentile`, default linear method).
- A fresh `default_rng(1)` is made for each contrast, so all five contrasts use the same resample indices.
- Sensitivity check, not the frozen method: drawing the primary contrast with legacy `RandomState(1).randint` instead gives [+0.5750, +0.7150].

## Per-arm table (means over 16 seeds)

| arm  | fresh-land survival | SD over seeds | min seed | max seed | lifespan |
|------|--------------------:|--------------:|---------:|---------:|---------:|
| RVS  | 0.2112 | 0.1103 | 0.08 | 0.52 | 1382.54 |
| RMS  | 0.8588 | 0.0805 | 0.70 | 0.96 | 2724.67 |
| RMXS | 0.4825 | 0.1662 | 0.10 | 0.70 | 1783.60 |
| RE5S | 0.7737 | 0.0696 | 0.66 | 0.90 | 2516.02 |
| HRS  | 0.8850 | 0.0487 | 0.76 | 0.94 | 2756.37 |

Per-seed survival, seeds 1..16:

```
RVS   0.28 0.52 0.18 0.22 0.22 0.30 0.10 0.32 0.20 0.08 0.08 0.12 0.16 0.16 0.24 0.20
RMS   0.84 0.88 0.94 0.74 0.92 0.72 0.84 0.86 0.90 0.80 0.96 0.90 0.90 0.90 0.94 0.70
RMXS  0.50 0.36 0.46 0.48 0.66 0.60 0.56 0.32 0.70 0.20 0.50 0.50 0.60 0.66 0.10 0.52
RE5S  0.72 0.80 0.78 0.74 0.84 0.90 0.76 0.74 0.88 0.74 0.88 0.72 0.70 0.78 0.74 0.66
HRS   0.88 0.84 0.92 0.76 0.86 0.94 0.86 0.88 0.90 0.84 0.90 0.94 0.94 0.94 0.86 0.90
```

Per-seed lifespan, seeds 1..16:

```
RVS   1418 2130 1243 1399 1380 1785  981 1780 1502  843  860 1382 1223 1319 1622 1254
RMS   2717 2759 2939 2576 2830 2389 2633 2723 2786 2703 2893 2831 2815 2757 2859 2385
RMXS  1871 1482 1877 1735 2160 2175 1850 1625 2333 1304 1739 1649 2031 2101  658 1949
RE5S  2521 2570 2453 2448 2632 2729 2486 2427 2746 2459 2696 2380 2291 2615 2471 2333
HRS   2687 2703 2945 2509 2687 2841 2642 2703 2782 2683 2804 2849 2917 2852 2671 2828
```

## Primary result
**RMS − RVS, fresh-land survival: +0.6475, 95% bootstrap interval [+0.5775, +0.7137].** The whole interval is above 0, so this meets the plan's "a real gain" reading. RMS is above RVS on **16 of 16** seeds (0 ties).

Per-seed differences: +0.56 +0.36 +0.76 +0.52 +0.70 +0.42 +0.74 +0.54 +0.70 +0.72 +0.88 +0.78 +0.74 +0.74 +0.70 +0.50

## Secondary results

| contrast | estimate | 95% interval | seeds A > B | whole interval > 0 |
|---|---:|---|---|---|
| RMS − RMXS, survival | +0.3762 | [+0.2913, +0.4688] | 16/16 (0 ties) | yes |
| RE5S − RVS, survival | +0.5625 | [+0.5000, +0.6200] | 16/16 (0 ties) | yes |
| RMS − HRS, survival | −0.0262 | [−0.0675, +0.0100] | 5/16 (1 tie, 10 below) | no (the interval includes 0) |
| RMS − RVS, lifespan | +1342.13 | [+1150.03, +1525.41] | 16/16 (0 ties) | yes |

The exact means are RMS − RMXS = 0.37625 and RMS − HRS = −0.02625. The script prints them at 4 decimals.

## Data checks
- All 80 expected files are present. None are missing.
- Lives per file: 50 in every file (80 of 80 files), 4,000 lives in total.
- `survived` and `lifespan` are present and numeric in all 4,000 records. There are no NaNs.
- The only `survived` values are 1.0 (2,569 lives) and 0.0 (1,431 lives).
- `lifespan` ranges from 126 to 3000. Every life with survived = 1 has lifespan 3000 exactly. The longest life with survived = 0 is 2988. So `survived` and the full length (3000) agree.
- No two of the 80 files have the same (survived, lifespan) sequence.

## Other things noticed (not interpreted)
- **The arms have different fields.** RMS, RMXS and RE5S lives have the extra fields `fair_fed`, `food_first` and `food_first_trials`. RVS and HRS lives do not.
- **The `labels` field is only on some lives.** Lives with `labels`, by arm: RVS 631/800, RMXS 414/800, RE5S 181/800, RMS 113/800, HRS 92/800. I did not use this field.
- **The output folder holds more arm variants than these five.** Besides the five arms here, it has 25 more variants with 16 files each, for 480 `test_fresh_*` files in total: RV, RM, RMX, RE5, HR, the `*Y` arms, and the `*-bare`, `*-off`, `*-midswap` and `HRS-soft` versions. I did not open them.
- RMXS has the widest spread over seeds (SD 0.1662). It includes seed 15 at 0.10 survival and 658 lifespan, which is the lowest RMXS seed by far.
- In RMS − HRS, two seeds account for most of the negative mean: seed 6 (−0.22) and seed 16 (−0.20). On those seeds RMS survival is 0.72 and 0.70.
