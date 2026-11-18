# W3j analysis (the frozen analysis, analyse_w3j.py)

- Checks All: PASS: **yes**
- All runs present: **yes**
- The reproduction job (W3i's C seed 1 with W3j's code): {"exact": false, "max_abs_diff": 0.26961166981767937}

| arm | lifespan | survived | to 1,000 | fresh lands: survived | drift from the end of childhood | agrees with the parent |
|---|---|---|---|---|---|---|
| C | 1248.105 [900.407, 1568.510] | 0.255 [0.148, 0.365] | 0.405 [0.273, 0.528] | 0.235 [0.130, 0.340] | – | – |
| CF | 855.590 [616.110, 1117.452] | 0.105 [0.040, 0.183] | 0.263 [0.155, 0.368] | – | – | – |
| CK | 1111.720 [777.927, 1467.608] | 0.208 [0.113, 0.312] | 0.363 [0.225, 0.512] | 0.170 [0.095, 0.255] | 0.503 [0.418, 0.589] | 0.298 [0.243, 0.355] |
| CV | 598.768 [363.425, 872.001] | 0.048 [0.003, 0.113] | 0.140 [0.045, 0.245] | 0.045 [0.013, 0.087] | 0.419 [0.343, 0.526] | 0.500 [0.399, 0.564] |
| C4 | 829.567 [493.312, 1163.407] | 0.145 [0.060, 0.228] | 0.242 [0.108, 0.375] | 0.165 [0.068, 0.263] | 0.651 [0.566, 0.754] | 0.228 [0.176, 0.269] |
| C2 | 1593.545 [1397.070, 1836.143] | 0.363 [0.280, 0.458] | 0.535 [0.465, 0.625] | 0.380 [0.275, 0.493] | 0.505 [0.469, 0.547] | 0.310 [0.290, 0.331] |

## Readings (lifespan, paired by seed)

- **1. Primary, settling down keeps it (CK − C):** -136.385 [-503.595, 191.025] -> **no**
- Secondary: adult learning hurts (CF − C): -392.515 [-687.553, -108.185] -> no
- Secondary: a quiet parent keeps it (CV − C): -649.337 [-981.594, -308.176] -> no
- Secondary: a longer childhood at equal steps (C2 − C4): 763.978 [375.598, 1153.530] -> yes
- Secondary: more steps, the same childhood (C4 − C): -418.538 [-813.315, -69.009]
- CK against CF: 256.130 [-209.195, 689.581] (not separated)
- **Toward the bar:** the best final arm by test lifespan is C2; fresh-land survival 0.380 [0.275, 0.493] (bar 0.80)

## The learning curves (exploratory; snapshot tests, mean lifespan over seeds)

- CK: 1.2M 856 → 1.6M 1255 → 2.0M 1127 → 2.4M 1079 → final 1112
- CV: 1.2M 499 → 1.6M 558 → 2.0M 345 → 2.4M 362 → final 599
- C4: 1.2M 792 → 1.6M 1255 → 2.0M 1315 → 2.4M 1283 → 2.8M 1068 → 3.2M 1074 → 3.6M 833 → final 830
- C2: 2.4M 1375 → 2.8M 1832 → 3.2M 1773 → 3.6M 1810 → final 1594
