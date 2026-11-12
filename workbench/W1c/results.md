# W1c: spatial structure (results)

Frozen as `W1c-frozen`. run_w1c.py, analyse_w1c.py (written before any training).

## Validity

- Code checks (All: PASS): **yes**
- W1b's scripted controls (valid; G's efficient detour 0.000) are the reference.
- All 80 main runs present: **yes**

## The brains at 30,000 episodes (16 seeds; mean [95% bootstrap])

| brain | efficient detour | pocket | control | empty room | held-out detour | held-out control | first 3 | imitation acc. (learn / test) | navigates | reading |
|---|---|---|---|---|---|---|---|---|---|---|
| E | 0.001 [0.000, 0.003] | 0.000 [0.000, 0.000] | 0.014 [0.005, 0.025] | 0.023 [0.011, 0.036] | 0.000 [0.000, 0.000] | 0.009 [0.004, 0.015] | 0.100 | 0.212 / 0.215 | **no** | **mixed** |
| E-imit | 0.013 [0.008, 0.018] | 0.012 [0.000, 0.023] | 0.217 [0.203, 0.231] | 0.270 [0.240, 0.302] | 0.014 [0.006, 0.022] | 0.211 [0.194, 0.230] | 0.243 | 0.588 / 0.523 | **no** | **mixed** |
| C | 0.000 [0.000, 0.000] | 0.000 [0.000, 0.000] | 0.019 [0.012, 0.027] | 0.031 [0.020, 0.042] | 0.000 [0.000, 0.000] | 0.027 [0.017, 0.039] | 0.135 | 0.227 / 0.224 | **no** | **mixed** |
| C-imit | 0.151 [0.122, 0.177] | 0.016 [0.000, 0.039] | 0.727 [0.653, 0.784] | 0.782 [0.720, 0.833] | 0.121 [0.097, 0.145] | 0.633 [0.560, 0.692] | 0.402 | 0.795 / 0.741 | **no** | **mixed** |
| C-dag | 0.134 [0.103, 0.163] | 0.016 [0.004, 0.031] | 0.683 [0.599, 0.752] | 0.766 [0.690, 0.829] | 0.113 [0.086, 0.140] | 0.611 [0.545, 0.668] | 0.388 | 0.763 / 0.723 | **no** | **mixed** |

## The 100,000-episode check (secondary; 4 seeds)

| brain | efficient detour | control | empty room | imitation acc. (test) |
|---|---|---|---|---|
| E | 0.000 | 0.021 | 0.046 | 0.243 |
| C | 0.029 | 0.758 | 0.946 | 0.550 |
| C-imit | 0.344 | 0.852 | 0.863 | 0.841 |

Rules (frozen, W1b's): 'looks ahead' = efficient detour >= 0.80, pocket >= 0.70, above G's (lower bound over seeds above 0); 'reactive' = control >= 0.80 and efficient detour <= 0.60; else 'mixed'. 'Navigates' = control >= 0.80 and empty-room success >= 0.90. Even a pass is behaviour, not proof of an internal look-ahead.

