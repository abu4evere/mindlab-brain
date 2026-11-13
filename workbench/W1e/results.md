# W1e: a planner that cannot cut corners (results)

Frozen as `W1e-frozen`. run_w1e.py, analyse_w1e.py (written before any training).

## Validity

- Code checks (All: PASS): **yes**
- All 48 runs present: **yes**
- V's 30,000-episode results equal W1d's for every seed (replication): **yes**

## 30,000 episodes (16 seeds): mean [95% bootstrap]

| measure | V | V+ | V+ - V |
|---|---|---|---|
| efficient detour | 0.151 [0.111, 0.192] | 0.171 [0.126, 0.216] | +0.020 [-0.029, +0.067] |
| pocket | 0.043 [0.020, 0.070] | 0.062 [0.035, 0.094] | +0.020 [-0.023, +0.062] |
| control | 0.734 [0.636, 0.813] | 0.817 [0.768, 0.859] | +0.083 [+0.002, +0.184] |
| empty room | 0.837 [0.735, 0.921] | 0.924 [0.877, 0.966] | +0.086 [+0.001, +0.191] |
| held-out detour | 0.110 [0.074, 0.150] | 0.150 [0.116, 0.183] | +0.040 [-0.005, +0.084] |
| moving food | 0.470 [0.398, 0.534] | 0.542 [0.492, 0.591] | +0.071 [-0.003, +0.152] |
| map read-out: efficient detour | 0.160 [0.094, 0.228] | 0.229 [0.176, 0.279] | +0.069 [+0.009, +0.133] |
| map read-out: pocket | 0.059 [0.027, 0.094] | 0.102 [0.055, 0.156] | +0.043 [+0.000, +0.090] |
| value-map correlation | 0.706 [0.604, 0.790] | 0.781 [0.746, 0.813] | +0.075 [-0.017, +0.185] |
| step accuracy (detours) | 0.228 [0.200, 0.259] | 0.208 [0.184, 0.231] | -0.020 [-0.061, +0.017] |
| mean gap between the two best scores | 2.731 [2.148, 3.334] | 3.858 [3.318, 4.440] | +1.127 [+0.587, +1.684] |
| share of near-ties (gap < 0.05) | 0.033 [0.021, 0.048] | 0.016 [0.011, 0.022] | -0.017 [-0.031, -0.004] |
- V: **mixed**; map read-out above the head by +0.009
- V+: **reactive**; map read-out above the head by +0.058

**The plus matters** (V+ - V, efficient detour): +0.020 [-0.029, +0.067] -> **no**

## 150,000 episodes (8 seeds, secondary): mean [95% bootstrap]

| measure | V | V+ | V+ - V |
|---|---|---|---|
| efficient detour | 0.348 [0.259, 0.443] | 0.536 [0.442, 0.632] | +0.189 [+0.089, +0.296] |
| pocket | 0.195 [0.109, 0.281] | 0.281 [0.195, 0.391] | +0.086 [-0.031, +0.227] |
| control | 0.856 [0.811, 0.896] | 0.939 [0.910, 0.966] | +0.082 [+0.057, +0.108] |
| empty room | 0.925 [0.863, 0.977] | 0.992 [0.983, 0.998] | +0.067 [+0.021, +0.121] |
| held-out detour | 0.329 [0.233, 0.419] | 0.406 [0.327, 0.494] | +0.077 [-0.035, +0.185] |
| moving food | 0.623 [0.553, 0.689] | 0.780 [0.729, 0.825] | +0.157 [+0.105, +0.211] |
| map read-out: efficient detour | 0.299 [0.155, 0.443] | 0.568 [0.497, 0.651] | +0.269 [+0.130, +0.414] |
| map read-out: pocket | 0.188 [0.086, 0.297] | 0.312 [0.234, 0.414] | +0.125 [-0.008, +0.266] |
| value-map correlation | 0.731 [0.581, 0.847] | 0.876 [0.859, 0.900] | +0.145 [+0.033, +0.290] |
| step accuracy (detours) | 0.318 [0.286, 0.345] | 0.361 [0.297, 0.429] | +0.043 [-0.030, +0.115] |
| mean gap between the two best scores | 5.546 [4.094, 6.969] | 9.883 [8.349, 11.839] | +4.337 [+2.565, +6.230] |
| share of near-ties (gap < 0.05) | 0.012 [0.005, 0.021] | 0.003 [0.000, 0.007] | -0.009 [-0.019, -0.000] |
- V: **reactive**; map read-out above the head by -0.049
- V+: **reactive**; map read-out above the head by +0.031

Rules (frozen; W1b's). Even a pass is learned planning inside an engineered structure, and behaviour, not proof of an inner look-ahead.

