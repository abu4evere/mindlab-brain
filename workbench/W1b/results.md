# W1b: the detour, seen (results)

Frozen as `W1b-frozen`. run_w1b.py, analyse_w1b.py (written before any run).

## Validity

- Code checks (All: PASS): **yes**
- All runs present: **yes**
- B looks ahead: **yes**; none of the six negative controls does: **yes**
- **Valid.**

## Scripted brains (one run each)

| brain | efficient detour | ordinary | adversarial | pocket | first 3 moves | detours solved at all | control | reading |
|---|---|---|---|---|---|---|---|---|
| G | 0.000 | 0.000 | 0.000 | 0.000 | 0.333 | 0.000 | 0.925 | reactive |
| W | 0.283 | 0.300 | 0.267 | 0.250 | 0.542 | 1.000 | 1.000 | reactive |
| W2 | 0.233 | 0.300 | 0.167 | 0.062 | 0.525 | 1.000 | 1.000 | reactive |
| H1 | 0.542 | 0.533 | 0.550 | 0.188 | 0.625 | 1.000 | 1.000 | reactive |
| H2 | 0.525 | 0.550 | 0.500 | 0.125 | 0.625 | 1.000 | 1.000 | reactive |
| M- | 0.225 | 0.117 | 0.333 | 0.312 | 0.433 | 0.833 | 0.967 | reactive |
| B | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | looks ahead |

## Learning brains (16 seeds; mean [95% bootstrap])

| brain | efficient detour | ordinary | adversarial | pocket | first 3 moves | control | eff - G | reading |
|---|---|---|---|---|---|---|---|---|
| F | 0.000 [0.000, 0.000] | 0.000 [0.000, 0.000] | 0.000 [0.000, 0.000] | 0.000 [0.000, 0.000] | 0.118 [0.101, 0.134] | 0.014 [0.009, 0.020] | +0.000 [+0.000, +0.000] | **mixed** |
| R | 0.001 [0.000, 0.002] | 0.000 [0.000, 0.000] | 0.001 [0.000, 0.003] | 0.000 [0.000, 0.000] | 0.070 [0.058, 0.083] | 0.037 [0.028, 0.045] | +0.001 [+0.000, +0.002] | **mixed** |
| F-imit | 0.000 [0.000, 0.000] | 0.000 [0.000, 0.000] | 0.000 [0.000, 0.000] | 0.000 [0.000, 0.000] | 0.242 [0.232, 0.252] | 0.084 [0.076, 0.094] | +0.000 [+0.000, +0.000] | **mixed** |

Rules (frozen): 'looks ahead' = efficient detour success (within 1.15 x the shortest) >= 0.80, pocket >= 0.70, above G's; 'reactive' = control >= 0.80 and efficient detour <= 0.60; else 'mixed'. Valid only if B looks ahead and none of G, W, W2, H1, H2, M- does. Even a pass is behaviour, not proof of an internal look-ahead.

