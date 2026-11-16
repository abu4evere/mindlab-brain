# W3e analysis (the frozen analysis, analyse_w3e.py)

| arm | runs | survived to 3,000 | to 1,000 | lifespan | known@end |
|---|---|---|---|---|---|
| YFR (W3b, recipe only) | 8 | 0.000 [0.000, 0.000] | 0.010 [0.003, 0.020] | 248 [216, 296] | 0.63 |
| PYFR (W3d, script parent) = G2's parent | 8 | 0.128 [0.045, 0.225] | 0.243 [0.125, 0.353] | 806 [508, 1104] | 0.83 |
| G2 | 8 | 0.070 [0.028, 0.118] | 0.133 [0.068, 0.205] | 549 [367, 762] | 0.74 |
| G3 | 8 | 0.050 [0.022, 0.080] | 0.113 [0.062, 0.165] | 473 [357, 594] | 0.69 |

## Readings

- **1. Skill passes on (G2 − its parent):** lifespan -257.477 [-445.288, -66.430]; survival -0.058 [-0.122, 0.002]
- **2. A learned parent beats no parent (G2 − recipe only):** lifespan 300.630 [92.039, 529.968]; survival 0.070 [0.028, 0.118]
- **3. Ratchet or decay (G3 − G2):** lifespan -75.835 [-228.202, 71.171]; survival -0.020 [-0.058, 0.018]
- **4. Fidelity (G2 copies its parent):** child 0.660 [0.565, 0.746]; D3 baseline 0.281 [0.242, 0.318]; child − D3 0.379 [0.276, 0.468]
- **4. Fidelity (G3 copies its parent):** child 0.679 [0.582, 0.760]; D3 baseline 0.236 [0.212, 0.268]; child − D3 0.443 [0.343, 0.526]
