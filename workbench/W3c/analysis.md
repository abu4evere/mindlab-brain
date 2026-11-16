# W3c analysis (the frozen analysis, analyse_w3c.py)

Per run: the mean over its 50 test lives; intervals: bootstrap over the 8 seeds (10,000 draws, seed 20261129).

## Step 0c: W3's D3i with the gate (test only)

| walk | survived to 3,000 | lifespan |
|---|---|---|
| (a) learned head (n = 8) | 0.000 [0.000, 0.000] | 199 [191, 209] |
| (b) greedy value walk (n = 8) | 0.000 [0.000, 0.000] | 162 [154, 173] |
| (c) one-step look-ahead (n = 8) | 0.000 [0.000, 0.000] | 170 [157, 186] |

## Arms

| arm | runs | survived to 3,000 | to 1,000 | lifespan | known@end | hungry | exhausted |
|---|---|---|---|---|---|---|---|
| D3 (W3) | 8 | 0.000 [0.000, 0.000] | 0.000 [0.000, 0.000] | 204 [191, 217] | 0.53 | 0.20 | 0.45 |
| D3i (W3) | 8 | 0.000 [0.000, 0.000] | 0.000 [0.000, 0.000] | 215 [203, 229] | 0.56 | 0.21 | 0.49 |
| YFR (W3b) | 8 | 0.000 [0.000, 0.000] | 0.010 [0.003, 0.020] | 248 [216, 297] | 0.63 | 0.19 | 0.33 |
| F2 | 8 | 0.055 [0.033, 0.080] | 0.210 [0.158, 0.258] | 679 [563, 786] | 0.64 | 0.15 | 0.28 |
| G | 8 | 0.000 [0.000, 0.000] | 0.000 [0.000, 0.000] | 208 [193, 225] | 0.55 | 0.20 | 0.46 |
| GYFR | 8 | 0.013 [0.000, 0.038] | 0.045 [0.005, 0.115] | 312 [214, 471] | 0.59 | 0.19 | 0.38 |
| Gi | 8 | 0.000 [0.000, 0.000] | 0.000 [0.000, 0.000] | 194 [182, 206] | 0.41 | 0.24 | 0.42 |
| Z0 | 8 | 0.000 [0.000, 0.000] | 0.000 [0.000, 0.000] | 193 [185, 201] | 0.43 | 0.22 | 0.42 |

## Readings

1. **The gate un-drowns hunger** (D3i + gate, walk (b) or (c) survives >= 0.50): best 0.000 -> **NO**
2. **The fair ceiling is reachable** (F2 >= 0.50): 0.055 -> **NO**
3. **A learned brain lives** (G, GYFR or Gi: mean >= 0.50, lower >= 0.30): **NO**
4. **The gate helps** (on survived):
   - G − D3 (W3): 0.000 [0.000, 0.000] -> NO
   - Gi − D3i (W3): 0.000 [0.000, 0.000] -> NO
   - GYFR − YFR (W3b): 0.013 [0.000, 0.038] -> NO
5. **Gate or quiet start** (G − Z0 on survived): 0.000 [0.000, 0.000]

Secondary (survival to 1,000, paired):
- G − D3 (W3): 0.000 [0.000, 0.000]
- Gi − D3i (W3): 0.000 [0.000, 0.000]
- GYFR − YFR (W3b): 0.035 [-0.013, 0.110]
- G − Z0: 0.000 [0.000, 0.000]
