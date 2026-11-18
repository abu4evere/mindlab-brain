# W3k analysis (the frozen analysis, analyse_w3k.py)

- Checks All: PASS: **yes**
- All runs present: **yes**

- **The determinism job** (R seed 1 three times): D1 {"exact": true, "max_abs_diff": 0.0}; D2 {"exact": true, "max_abs_diff": 0.0}
- Processors seen: Intel(R) Xeon(R) 6975P-C (53 run parts); AMD EPYC 7763 64-Core Processor (21 run parts); Intel(R) Xeon(R) 6973P-C (1 run parts); Intel(R) Xeon(R) Platinum 8370C CPU @ 2.80GHz (3 run parts); Intel64 Family 6 Model 186 Stepping 3, GenuineIntel (1 run parts)

| arm | lifespan | median | survived | to 1,000 | fresh lands: survived | drift | agrees with the parent |
|---|---|---|---|---|---|---|---|
| R2 | 1635.585 [1400.291, 1870.479] | 1634.4 | 0.409 [0.321, 0.500] | 0.548 [0.459, 0.633] | 0.391 [0.297, 0.490] | 0.522 [0.492, 0.553] | 0.303 [0.281, 0.323] |
| CS | 1834.950 [1622.328, 2024.612] | 1885.1 | 0.478 [0.393, 0.556] | 0.611 [0.531, 0.680] | 0.445 [0.364, 0.524] | 0.467 [0.436, 0.497] | 0.326 [0.307, 0.345] |
| CY | 1792.439 [1579.336, 1987.653] | 1840.6 | 0.450 [0.365, 0.532] | 0.604 [0.524, 0.672] | 0.448 [0.365, 0.530] | 0.459 [0.434, 0.482] | 0.327 [0.308, 0.346] |
| C3 | 1752.856 [1473.339, 1995.185] | 1868.5 | 0.429 [0.338, 0.515] | 0.600 [0.497, 0.688] | 0.460 [0.354, 0.561] | 0.482 [0.431, 0.550] | 0.308 [0.270, 0.337] |
| CR | 666.886 [550.621, 789.024] | 662.2 | 0.039 [0.020, 0.060] | 0.176 [0.122, 0.235] | 0.034 [0.019, 0.051] | 0.342 [0.310, 0.374] | 0.542 [0.514, 0.568] |

## Readings (lifespan, paired by seed)

**1. Two primary readings (97.5% intervals, Bonferroni):**
- **A longer childhood still helps (C3 − R2):** 117.271 [-193.443, 431.876] -> **no**; median 172.1; leave-one-seed-out means [30.8, 178.0]
- **Choosing its own best copy helps (CS − R2):** 199.365 [70.313, 346.782] -> **yes**; median 181.7; leave-one-seed-out means [154.9, 222.7]
**2. How to read CS (CS − CY, 95%):** 42.511 [-20.532, 108.695] -> **no** (no information shown beyond 'an earlier copy')
**3. Secondary (95%):**
- CR − R2: -968.699 [-1196.168, -752.836] -> no
- CY − R2: 156.854 [32.595, 285.004] -> yes
**4. Toward the bar:** the best arm by test lifespan is CS; fresh-land survival 0.445 [0.364, 0.524] (bar 0.80)

## The kept copies

- CS's step (millions): 3.21, 3.13, 3.35, 2.79, 3.18, 3.50, 3.49, 3.83, 3.25, 2.98, 2.95, 2.73, 3.67, 2.96, 3.10, 2.83
- CY's step (millions): 2.86, 3.14, 3.48, 2.93, 3.47, 3.90, 3.53, 2.73, 2.68, 2.62, 3.01, 3.48, 3.62, 2.79, 2.97, 2.82

## Exploratory (labelled): the learning curves and the oracle

- R: 2.4M 1208 → 2.8M 1821 → 3.2M 1868 → 3.6M 1718 → final 1636
- C3: 3.6M 1454 → 4.0M 1756 → 4.4M 1769 → 4.8M 1743 → final 1753
- CR: 2.4M 888 → 2.8M 511 → 3.2M 651 → 3.6M 683 → final 667
- The oracle (best tested snapshot of run R per seed, chosen by the test: an upper bound, not a result): 1931.389 [1696.410, 2135.146]
