# W3r analysis (the frozen analysis, analyse_w3r.py)

- Checks All: PASS on every study machine: **yes**
- All runs present: **yes**

Each cell: the mean over 16 seeds [95% bootstrap]; fresh lands: 50 lives per seed.

| arm | fresh-land survival | test-land survival | lifespan |
|---|---|---|---|
| RVS | 0.211 [0.164, 0.268] | 0.166 [0.119, 0.221] | 1246 [1122, 1382] |
| RMS | 0.859 [0.819, 0.894] | 0.846 [0.811, 0.877] | 2688 [2624, 2750] |
| RMXS | 0.482 [0.400, 0.555] | 0.460 [0.375, 0.534] | 1735 [1502, 1929] |
| RE5S | 0.774 [0.741, 0.807] | 0.795 [0.754, 0.835] | 2570 [2482, 2653] |
| HRS | 0.885 [0.860, 0.907] | 0.879 [0.845, 0.909] | 2766 [2698, 2826] |
| RVS-bare | 0.003 [0.000, 0.007] | 0.003 [0.000, 0.007] | 395 [360, 433] |
| RMS-bare | 0.274 [0.221, 0.328] | 0.271 [0.215, 0.326] | 1260 [1127, 1396] |
| RMXS-bare | 0.028 [0.014, 0.043] | 0.033 [0.021, 0.044] | 385 [340, 429] |
| RE5S-bare | 0.138 [0.104, 0.175] | 0.154 [0.114, 0.193] | 933 [816, 1051] |
| HRS-bare | 0.396 [0.335, 0.456] | 0.359 [0.311, 0.410] | 1646 [1527, 1764] |
| RVS-midswap | 0.214 [0.166, 0.270] | 0.165 [0.124, 0.212] | 1250 [1132, 1380] |
| RMS-midswap | 0.250 [0.201, 0.302] | 0.217 [0.184, 0.253] | 2071 [2001, 2139] |
| RMXS-midswap | 0.347 [0.287, 0.403] | 0.310 [0.251, 0.362] | 1546 [1336, 1717] |
| RE5S-midswap | 0.280 [0.204, 0.359] | 0.261 [0.179, 0.349] | 2063 [1944, 2185] |
| HRS-soft | 0.671 [0.535, 0.789] | 0.659 [0.545, 0.762] | 2310 [2060, 2537] |
| RV | 0.201 [0.140, 0.271] | 0.144 [0.094, 0.204] | 1141 [973, 1326] |
| RM | 0.861 [0.810, 0.905] | 0.836 [0.789, 0.877] | 2667 [2559, 2759] |
| RMX | 0.496 [0.412, 0.573] | 0.517 [0.444, 0.593] | 1879 [1671, 2069] |
| RE5 | 0.766 [0.729, 0.800] | 0.759 [0.699, 0.811] | 2495 [2387, 2595] |
| HR | 0.805 [0.728, 0.869] | 0.810 [0.749, 0.864] | 2544 [2371, 2688] |

## Readings

**1. Primary, RMS − RVS (fresh-land survival):** 0.647 [0.578, 0.714] -> **a real gain**; 16 of 16 seeds above 0

**2. Secondary, fresh-land survival (95%):**
- RMS − RMXS: 0.376 [0.291, 0.469]
- RE5S − RVS: 0.562 [0.500, 0.620]
- RMS − HRS: -0.026 [-0.068, 0.010]
- RMS-bare − RVS-bare: 0.271 [0.217, 0.326]
- RMS-midswap − RMS: -0.609 [-0.642, -0.575]
- RVS-midswap − RVS: 0.003 [-0.015, 0.021]
- HRS-soft − HRS: -0.214 [-0.350, -0.095]
**3. Secondary, test-land lifespan (95%):**
- RMS − RVS: 1443 [1282, 1597]
- RMS − RMXS: 953 [735, 1213]
- RE5S − RVS: 1325 [1150, 1488]
- RMS − HRS: -78 [-177, 21]
**4. The module on fresh lands** (share of lives where 'fed' came to rank the food colour first after a meal; mean step and fair trials when it did):
- RMS: 0.996 of lives; step 25; trials 25
- RMXS: 0.886 of lives; step 95; trials 95
- RE5S: 0.985 of lives; step 31; trials 31
**5. The learning curve** (probe_w3r.py): see probe.json
