# BV1 gate result

Seeds run: [1, 2, 3, 4, 5, 6, 7, 8]; machine: {'platform': 'Windows-10-10.0.19045-SP0', 'python': '3.12.10', 'numpy': '2.5.3', 'processor': 'AMD64 Family 25 Model 33 Stepping 2, AuthenticAMD'}

| seed | lifespan (NATIVE) | BODY vs NATIVE | BODY-SHUF vs NATIVE | wall hits | meals <cap | meals at cap | rests | edge steps |
|---|---|---|---|---|---|---|---|---|
| 1 | 3000 | identical | identical | 50 | 113 | 7 | 372 | 262 |
| 2 | 3000 | identical | identical | 59 | 115 | 21 | 371 | 256 |
| 3 | 3000 | identical | identical | 15 | 116 | 16 | 349 | 213 |
| 4 | 1628 | identical | identical | 93 | 58 | 10 | 203 | 544 |
| 5 | 3000 | identical | identical | 1 | 121 | 10 | 326 | 93 |
| 6 | 3000 | identical | identical | 105 | 112 | 9 | 701 | 535 |
| 7 | 3000 | identical | identical | 150 | 121 | 23 | 348 | 235 |
| 8 | 3000 | identical | identical | 106 | 109 | 9 | 420 | 480 |

Coverage met: True ({'wall_hits': 579, 'meals_below_cap': 865, 'meals_at_cap': 105, 'rests_at_shelter': 3090, 'edge_steps': 2618}); determinism (BODY seed 1 twice): identical

**Gate: PASS**
