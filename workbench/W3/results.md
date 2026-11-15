# W3 results (the frozen analysis, analyse_w3.py)

Per run: the mean over its 50 test lives; intervals: bootstrap over the training seeds (10,000 draws, seed 20261113). n = runs x 50 lives.

| brain | runs | survived to 3,000 | lifespan | known@500 | known@end | found share | hungry | exhausted |
|---|---|---|---|---|---|---|---|---|
| D3 | 8 | 0.000 [0.000, 0.000] | 203.855 [190.779, 217.030] | 0.527 [0.444, 0.610] | 0.527 [0.444, 0.610] | nan [nan, nan] | 0.201 [0.180, 0.224] | 0.451 [0.416, 0.483] |
| D2 | 8 | 0.000 [0.000, 0.000] | 195.045 [186.955, 203.018] | 0.424 [0.399, 0.453] | 0.424 [0.399, 0.453] | nan [nan, nan] | 0.217 [0.203, 0.228] | 0.425 [0.399, 0.452] |
| Dc | 8 | 0.000 [0.000, 0.000] | 246.113 [243.280, 248.775] | 0.863 [0.844, 0.882] | 0.863 [0.844, 0.882] | nan [nan, nan] | 0.165 [0.162, 0.169] | 0.542 [0.528, 0.554] |
| D3i | 8 | 0.000 [0.000, 0.000] | 215.248 [203.090, 228.810] | 0.560 [0.474, 0.651] | 0.560 [0.474, 0.651] | nan [nan, nan] | 0.210 [0.192, 0.228] | 0.486 [0.458, 0.517] |
| D3- | 8 | 0.000 [0.000, 0.000] | 172.312 [162.815, 182.858] | 0.295 [0.244, 0.343] | 0.295 [0.244, 0.343] | nan [nan, nan] | 0.248 [0.227, 0.270] | 0.365 [0.340, 0.392] |
| Rand | 1 (50 lives) | 0.000 | 173.940 | 0.428 | 0.428 | nan | 0.201 | 0.364 |
| Script | 1 (50 lives) | 0.960 | 2963.120 | 1.000 | 1.000 | 1.000 | 0.002 | 0.020 |

**Reading 1, 'drives are enough to live':** D3 survival share 0.000 [0.000, 0.000] (n = 8 runs) -> NO (needs mean >= 0.80 and lower bound >= 0.70).
**Reading 2, 'curiosity pays':** D3 - D2 found share nan [nan, nan]; survival 0.000 [0.000, 0.000] (n = 8 seed pairs); D3 curiosity-row collapses: 0 of 8 -> NO (needs found lower bound > 0, survival lower bound > -0.10, at most 2 collapses).
**Reading 3, 'curiosity alone is not enough':** Dc - D3 survival 0.000 [0.000, 0.000] (n = 8 seed pairs) -> NO (needs upper bound < 0).

## Secondary (intervals, no gate)
- D3i - D3, survived: 0.000 [0.000, 0.000] (n = 8 seed pairs)
- D3i - D3, found_share: nan [nan, nan] (n = 8 seed pairs)
- D3- - D3, found_share: nan [nan, nan] (n = 8 seed pairs)
- D3- - D3, survived: 0.000 [0.000, 0.000] (n = 8 seed pairs)
- D3 - D2, known_end: 0.103 [0.033, 0.178] (n = 8 seed pairs)
- D3 - D2, hungry: -0.016 [-0.035, 0.006] (n = 8 seed pairs)
- D3 - D2, exhausted: 0.025 [-0.004, 0.058] (n = 8 seed pairs)

## Learned links (final row norms per run; D3, D2, Dc learn them; D3i's are fixed)
- D3 seed 1: Ws 0.888, Wf 0.900, Wc 0.795
- D3 seed 2: Ws 0.504, Wf 1.015, Wc 1.079
- D3 seed 3: Ws 0.788, Wf 0.869, Wc 0.783
- D3 seed 4: Ws 0.562, Wf 0.840, Wc 0.753
- D3 seed 5: Ws 0.912, Wf 0.906, Wc 1.146
- D3 seed 6: Ws 0.635, Wf 0.986, Wc 0.844
- D3 seed 7: Ws 0.632, Wf 1.027, Wc 1.227
- D3 seed 8: Ws 0.689, Wf 0.866, Wc 1.181
- D2 seed 1: Ws 0.974, Wf 0.808, Wc 0.000
- D2 seed 2: Ws 0.824, Wf 0.983, Wc 0.000
- D2 seed 3: Ws 0.982, Wf 0.860, Wc 0.000
- D2 seed 4: Ws 0.667, Wf 0.664, Wc 0.000
- D2 seed 5: Ws 0.843, Wf 0.852, Wc 0.000
- D2 seed 6: Ws 0.940, Wf 0.778, Wc 0.000
- D2 seed 7: Ws 0.963, Wf 0.947, Wc 0.000
- D2 seed 8: Ws 0.832, Wf 0.762, Wc 0.000
- Dc seed 1: Ws 0.000, Wf 0.000, Wc 0.628
- Dc seed 2: Ws 0.000, Wf 0.000, Wc 0.943
- Dc seed 3: Ws 0.000, Wf 0.000, Wc 1.071
- Dc seed 4: Ws 0.000, Wf 0.000, Wc 0.777
- Dc seed 5: Ws 0.000, Wf 0.000, Wc 0.762
- Dc seed 6: Ws 0.000, Wf 0.000, Wc 1.092
- Dc seed 7: Ws 0.000, Wf 0.000, Wc 1.662
- Dc seed 8: Ws 0.000, Wf 0.000, Wc 1.802

Which map channel each learned link weights most (the centre tap and its plus neighbours):
- D3 seed 1 (sum per channel: wall, unseen, food, shelter, uncertainty): Ws: +0.03, +0.02, -0.00, -0.01, -0.20; Wf: +0.41, +0.43, +0.14, -0.03, +0.28; Wc: -0.77, +0.05, +0.04, -0.24, +0.10
- D3 seed 2 (sum per channel: wall, unseen, food, shelter, uncertainty): Ws: +0.81, +0.12, -0.88, +0.26, -0.32; Wf: +2.40, +1.00, -0.05, -0.01, +1.32; Wc: -1.37, -1.30, -1.16, -0.26, -0.47
- D3 seed 3 (sum per channel: wall, unseen, food, shelter, uncertainty): Ws: -1.67, -0.22, +0.17, -0.24, -0.12; Wf: -1.47, -0.42, -0.21, +0.02, -0.45; Wc: +1.44, +0.75, +0.29, +0.17, +0.67
- D3 seed 4 (sum per channel: wall, unseen, food, shelter, uncertainty): Ws: +1.46, +0.50, -0.34, +0.17, +0.42; Wf: +2.11, +0.62, +0.06, -0.00, +1.11; Wc: -0.40, -1.31, -0.35, -0.13, -0.20
- D3 seed 5 (sum per channel: wall, unseen, food, shelter, uncertainty): Ws: -1.33, -0.78, +0.94, -0.09, +0.41; Wf: -1.50, -1.19, -0.02, +0.21, -0.34; Wc: +1.13, +1.21, +0.94, +0.85, +1.19
- D3 seed 6 (sum per channel: wall, unseen, food, shelter, uncertainty): Ws: -0.98, -0.94, +0.79, -0.24, +0.29; Wf: -1.94, -1.79, -0.07, +0.02, -0.92; Wc: +0.43, +0.86, +1.12, +0.13, +1.05
- D3 seed 7 (sum per channel: wall, unseen, food, shelter, uncertainty): Ws: -0.35, +0.54, +1.34, -0.13, +1.03; Wf: -2.40, -0.92, +0.20, +0.20, -1.29; Wc: +1.58, +1.44, +1.83, +0.92, +1.19
- D3 seed 8 (sum per channel: wall, unseen, food, shelter, uncertainty): Ws: -1.70, -0.57, +0.60, -0.14, -0.09; Wf: -1.72, -1.24, -0.13, +0.06, -0.95; Wc: +1.44, +0.82, +1.23, +0.60, +0.88
- D2 seed 1 (sum per channel: wall, unseen, food, shelter, uncertainty): Ws: -0.94, -0.50, +0.46, -0.05, -0.38; Wf: -0.37, -0.83, +0.37, +0.07, -0.86; Wc: +0.00, +0.00, +0.00, +0.00, +0.00
- D2 seed 2 (sum per channel: wall, unseen, food, shelter, uncertainty): Ws: +2.09, +0.36, -0.95, +0.24, +0.28; Wf: +2.30, +0.76, +0.14, -0.01, +1.50; Wc: +0.00, +0.00, +0.00, +0.00, +0.00
- D2 seed 3 (sum per channel: wall, unseen, food, shelter, uncertainty): Ws: -2.37, -0.68, +0.43, -0.13, -0.51; Wf: -1.91, -0.90, +0.08, +0.07, -1.03; Wc: +0.00, +0.00, +0.00, +0.00, +0.00
- D2 seed 4 (sum per channel: wall, unseen, food, shelter, uncertainty): Ws: +1.54, +0.91, -0.27, +0.18, +0.58; Wf: +1.45, +0.68, +0.21, +0.01, +1.06; Wc: +0.00, +0.00, +0.00, +0.00, +0.00
- D2 seed 5 (sum per channel: wall, unseen, food, shelter, uncertainty): Ws: -2.16, -0.72, +0.26, -0.07, -0.61; Wf: -2.04, -0.79, +0.16, +0.05, -1.07; Wc: +0.00, +0.00, +0.00, +0.00, +0.00
- D2 seed 6 (sum per channel: wall, unseen, food, shelter, uncertainty): Ws: -1.73, -0.46, +0.76, -0.22, -0.15; Wf: -1.13, -1.02, +0.18, +0.07, -0.89; Wc: +0.00, +0.00, +0.00, +0.00, +0.00
- D2 seed 7 (sum per channel: wall, unseen, food, shelter, uncertainty): Ws: -2.39, -0.48, +0.69, -0.05, -0.58; Wf: -2.07, -0.77, +0.59, +0.11, -1.36; Wc: +0.00, +0.00, +0.00, +0.00, +0.00
- D2 seed 8 (sum per channel: wall, unseen, food, shelter, uncertainty): Ws: -1.67, -0.96, +0.51, -0.06, -0.61; Wf: -1.25, -1.14, +0.17, +0.07, -0.81; Wc: +0.00, +0.00, +0.00, +0.00, +0.00
- Dc seed 1 (sum per channel: wall, unseen, food, shelter, uncertainty): Ws: +0.00, +0.00, +0.00, +0.00, +0.00; Wf: +0.00, +0.00, +0.00, +0.00, +0.00; Wc: +0.72, -0.55, -0.27, -0.09, -1.34
- Dc seed 2 (sum per channel: wall, unseen, food, shelter, uncertainty): Ws: +0.00, +0.00, +0.00, +0.00, +0.00; Wf: +0.00, +0.00, +0.00, +0.00, +0.00; Wc: +1.64, -0.52, -0.88, +0.07, -1.67
- Dc seed 3 (sum per channel: wall, unseen, food, shelter, uncertainty): Ws: +0.00, +0.00, +0.00, +0.00, +0.00; Wf: +0.00, +0.00, +0.00, +0.00, +0.00; Wc: +2.04, -1.03, -0.81, -0.04, -1.50
- Dc seed 4 (sum per channel: wall, unseen, food, shelter, uncertainty): Ws: +0.00, +0.00, +0.00, +0.00, +0.00; Wf: +0.00, +0.00, +0.00, +0.00, +0.00; Wc: -0.90, +0.19, +0.85, +0.08, +1.64
- Dc seed 5 (sum per channel: wall, unseen, food, shelter, uncertainty): Ws: +0.00, +0.00, +0.00, +0.00, +0.00; Wf: +0.00, +0.00, +0.00, +0.00, +0.00; Wc: +1.14, -0.74, -0.37, +0.07, -1.63
- Dc seed 6 (sum per channel: wall, unseen, food, shelter, uncertainty): Ws: +0.00, +0.00, +0.00, +0.00, +0.00; Wf: +0.00, +0.00, +0.00, +0.00, +0.00; Wc: -1.93, +0.76, +0.62, -0.03, +1.63
- Dc seed 7 (sum per channel: wall, unseen, food, shelter, uncertainty): Ws: +0.00, +0.00, +0.00, +0.00, +0.00; Wf: +0.00, +0.00, +0.00, +0.00, +0.00; Wc: +0.27, +0.42, +0.72, +0.30, +0.57
- Dc seed 8 (sum per channel: wall, unseen, food, shelter, uncertainty): Ws: +0.00, +0.00, +0.00, +0.00, +0.00; Wf: +0.00, +0.00, +0.00, +0.00, +0.00; Wc: -0.40, +1.69, +1.27, +0.08, +4.03
