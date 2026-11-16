# W3d analysis (the frozen analysis, analyse_w3d.py)

Per run: the mean over its 50 test lives (tested alone); intervals: bootstrap over the 8 seeds (seed 20261130).

| arm | runs | survived to 3,000 | to 1,000 | lifespan | known@end | hungry | exhausted |
|---|---|---|---|---|---|---|---|
| D3 (W3) | 8 | 0.000 [0.000, 0.000] | 0.000 [0.000, 0.000] | 204 [191, 217] | 0.53 | 0.20 | 0.45 |
| YFR (W3b) | 8 | 0.000 [0.000, 0.000] | 0.010 [0.002, 0.020] | 248 [216, 296] | 0.63 | 0.19 | 0.33 |
| P | 8 | 0.033 [0.000, 0.098] | 0.065 [0.000, 0.190] | 388 [223, 694] | 0.78 | 0.15 | 0.44 |
| PYFR | 8 | 0.128 [0.050, 0.225] | 0.243 [0.130, 0.355] | 806 [512, 1104] | 0.83 | 0.14 | 0.25 |
| PA | 8 | 0.003 [0.000, 0.007] | 0.013 [0.003, 0.028] | 272 [242, 308] | 0.78 | 0.16 | 0.41 |

## Readings

1. **A child taught by a parent lives** (P or PYFR: mean >= 0.50, lower >= 0.30): **NO**
2. **The parent helps** (P − D3 on survived): 0.033 [0.000, 0.098] -> **NO**
3. **The recipe adds** (PYFR − P on survived): 0.095 [-0.010, 0.210]
4. **A parent who never leaves** (PA − P): survival -0.030 [-0.098, 0.007]; lifespan -116.075 [-434.438, 65.179]

Secondary (survival to 1,000, paired):
- P − D3 (W3): 0.065 [0.000, 0.190]
- PYFR − P: 0.177 [0.040, 0.315]
- PA − P: -0.052 [-0.185, 0.025]
- PYFR − YFR (W3b): 0.233 [0.115, 0.347]
