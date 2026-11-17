# W3i analysis (the frozen analysis, analyse_w3i.py)

- Checks All: PASS: **yes**
- All 24 runs present, with fresh-land tests: **yes**
- The reproduction job (W3d PYFR seed 1 again): {"exact": true, "allclose_1e-9": true, "max_abs_diff": 0.0}

| arm | lifespan | survived to 3,000 | to 1,000 | stale arrivals / 1,000 | no food known (of deaths) | steps since the last meal at death |
|---|---|---|---|---|---|---|
| PYFR | 806.322 [509.897, 1110.483] | 0.128 [0.045, 0.225] | 0.243 [0.127, 0.357] | – | 0.802 [0.762, 0.841] | 154.538 [148.541, 160.950] |
| L | 603.470 [336.347, 910.317] | 0.098 [0.025, 0.190] | 0.155 [0.060, 0.260] | 0.000 [0.000, 0.000] | 0.729 [0.604, 0.828] | 157.513 [147.544, 166.287] |
| LC | 980.097 [684.838, 1306.091] | 0.188 [0.095, 0.292] | 0.315 [0.208, 0.435] | 0.000 [0.000, 0.000] | 0.636 [0.492, 0.757] | 152.360 [138.013, 166.372] |
| C | 1248.105 [888.815, 1568.528] | 0.255 [0.145, 0.365] | 0.405 [0.268, 0.528] | 0.000 [0.000, 0.000] | 0.614 [0.461, 0.743] | 151.391 [144.253, 157.263] |

## Readings

- **1. More practice helps (L(6M) − PYFR, lifespan):** -202.852 [-613.870, 146.291] -> **no**
- **2. A longer childhood helps, with equal practice (LC − L at 6M, lifespan):** 376.627 [37.040, 707.431] -> **yes**
- **3. Secondary, C − PYFR (lifespan):** 441.782 [43.450, 888.740]
- **4. Toward the bar:** the best arm by test lifespan is C; its survival on 50 fresh lands 0.235 [0.128, 0.340] (bar 0.80)
- **5. Does the failure change?** "No food known" deaths: PYFR 0.802 [0.762, 0.841], L 0.729 [0.604, 0.828], LC 0.636 [0.492, 0.757]. Stale arrivals: see the table (PYFR's were not measured by W3d; the 2M snapshots below stand in).

## Exploratory: the learning curve (snapshots at the first life boundary after 2M and 4M)

- L: 2M: lifespan 840, survived 0.143, stale 0.00; 4M: lifespan 598, survived 0.090, stale 0.00; 6M: lifespan 603, survived 0.098, stale 0.00
- LC: 2M: lifespan 1340, survived 0.260, stale 0.00; 4M: lifespan 915, survived 0.153, stale 0.00; 6M: lifespan 980, survived 0.188, stale 0.00

Per seed (lifespan): PYFR 415, 1528, 883, 1005, 992, 307, 1119, 201; L 877, 217, 227, 1412, 606, 312, 953, 224; LC 381, 1001, 893, 1821, 519, 1472, 1070, 683; C 1547, 1261, 785, 1671, 1057, 1971, 1371, 322
