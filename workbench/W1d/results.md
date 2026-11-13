# W1d: thinking ahead (results)

Frozen as `W1d-frozen`. run_w1d.py, analyse_w1d.py (written before any training).

## Validity

- Code checks (All: PASS): **yes**
- W1b's scripted controls (valid; G's efficient detour 0.000) are the reference.
- All 64 main runs present: **yes**

## The brains (30,000 episodes; 16 seeds; mean [95% bootstrap])

| brain | efficient detour | pocket | control | empty room | held-out detour | moving food | first 3 | navigates | reading |
|---|---|---|---|---|---|---|---|---|---|
| V | 0.151 [0.109, 0.193] | 0.043 [0.020, 0.070] | 0.734 [0.634, 0.812] | 0.837 [0.734, 0.921] | 0.110 [0.073, 0.151] | 0.470 [0.396, 0.534] | 0.413 | **no** | **mixed** |
| V1 | 0.030 [0.018, 0.043] | 0.020 [0.004, 0.039] | 0.194 [0.157, 0.237] | 0.252 [0.181, 0.347] | 0.022 [0.013, 0.033] | 0.077 [0.055, 0.101] | 0.224 | **no** | **mixed** |
| Vm | 0.097 [0.077, 0.120] | 0.020 [0.000, 0.047] | 0.495 [0.427, 0.559] | 0.656 [0.569, 0.744] | 0.086 [0.070, 0.103] | 0.296 [0.250, 0.340] | 0.352 | **no** | **mixed** |
| V-ac | 0.019 [0.009, 0.031] | 0.000 [0.000, 0.000] | 0.308 [0.210, 0.407] | 0.410 [0.276, 0.546] | 0.016 [0.004, 0.029] | 0.145 [0.092, 0.199] | 0.222 | **no** | **mixed** |

## Readings (frozen)

- **Iteration matters** (V - V1, efficient detour): +0.121 [+0.074, +0.167] -> **yes**
- **The max matters** (V - Vm): +0.054 [+0.001, +0.106] -> **yes**

## The value map (mean Spearman correlation with -(true distance), test layouts)

- V: 0.706
- V1: 0.306
- Vm: -0.045

## The K sweep (V, test time): efficient detour by K, and by the layout's shortest path

| K | all detours | shortest <= 10 | 11-15 | > 15 |
|---|---|---|---|---|
| 1 | 0.004 | 0.003 (n 672) | 0.006 (n 976) | 0.000 (n 272) |
| 5 | 0.043 | 0.068 (n 672) | 0.033 (n 976) | 0.015 (n 272) |
| 10 | 0.080 | 0.135 (n 672) | 0.059 (n 976) | 0.018 (n 272) |
| 15 | 0.106 | 0.171 (n 672) | 0.083 (n 976) | 0.026 (n 272) |
| 20 | 0.119 | 0.188 (n 672) | 0.093 (n 976) | 0.044 (n 272) |
| 30 | 0.151 | 0.211 (n 672) | 0.132 (n 976) | 0.070 (n 272) |

## The 100,000-episode check (V-ac, 8 seeds)

- eff 0.150, pocket 0.109, control 0.780, empty 0.931, moving 0.381

Rules (frozen, W1b's and W1c's). Even a pass is learned planning inside an engineered planning structure, and behaviour, not proof of an inner look-ahead.

