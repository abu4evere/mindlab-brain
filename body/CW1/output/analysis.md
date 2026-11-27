# CW1 analysis (frozen script)

Lives per arm: {'LEARN': 800, 'RANDOM-OPS': 800, 'NO-MAKE': 800, 'PAD': 800}

**Primary: mean chains per life, LEARN - RANDOM-OPS = +5.080 [+4.745, +5.411] (16+/0- of 16 seeds); real gain: True**

| measure | LEARN | RANDOM-OPS | NO-MAKE | PAD |
|---|---|---|---|---|
| mean_chains | 5.730 | 0.650 | 0.000 | 5.420 |
| share_3plus | 0.446 | 0.030 | 0.000 | 0.396 |
| share_1plus | 0.930 | 0.453 | 0.000 | 0.879 |
| chains_per_1000 | 2.033 | 0.221 | 0.000 | 1.890 |
| first_join_latency | 295.877 | 1640.504 | nan | 354.454 |
| took_A | 0.976 | 0.941 | 0.965 | 0.965 |
| took_B | 0.965 | 0.935 | 0.970 | 0.945 |
| joined | 0.931 | 0.514 | 0.000 | 0.884 |
| ate_C | 0.930 | 0.453 | 0.000 | 0.879 |
| reuse | 4.800 | 0.198 | 0.000 | 4.541 |
| dead_action_rate | 0.460 | 0.848 | 0.513 | 0.665 |
| lifespan | 2679.454 | 2554.710 | 2669.735 | 2554.684 |
| survival | 0.847 | 0.763 | 0.846 | 0.804 |
| acts | 64.356 | 932.962 | 38.727 | 98.218 |
| moments | 1074.150 | 1066.139 | 2397.092 | 1010.759 |

LEARN - RANDOM-OPS (secondaries):
- share_3plus: +0.416 [+0.388, +0.444] (16+/0- of 16 seeds)
- share_1plus: +0.478 [+0.441, +0.516] (16+/0- of 16 seeds)
- chains_per_1000: +1.812 [+1.707, +1.916] (16+/0- of 16 seeds)
- first_join_latency: -1344.627 [-1429.395, -1257.489] (0+/16- of 16 seeds)
- took_A: +0.035 [+0.021, +0.049] (13+/1- of 16 seeds)
- took_B: +0.030 [+0.018, +0.042] (13+/1- of 16 seeds)
- joined: +0.417 [+0.386, +0.450] (16+/0- of 16 seeds)
- ate_C: +0.478 [+0.441, +0.516] (16+/0- of 16 seeds)
- reuse: +4.603 [+4.270, +4.935] (16+/0- of 16 seeds)
- dead_action_rate: -0.388 [-0.398, -0.378] (0+/16- of 16 seeds)

LEARN - NO-MAKE:
- lifespan: +9.719 [-62.464, +78.956] (7+/9- of 16 seeds)
- survival: +0.001 [-0.024, +0.028] (5+/5- of 16 seeds)

PAD - LEARN:
- mean_chains: -0.310 [-0.771, +0.213] (4+/12- of 16 seeds)
- first_join_latency: +58.577 [+27.228, +94.180] (13+/3- of 16 seeds)

Machines: 3
- {"node": "DESKTOP-B9PA260", "numpy": "2.5.3", "platform": "Windows-10-10.0.19045-SP0", "python": "3.12.10"}
- {"node": "mindlab-1.us-east4-a.c.aiiab-515203.internal", "numpy": "2.5.3", "platform": "Linux-7.0.0-1017-gcp-x86_64-with-glibc2.43", "python": "3.14.4"}
- {"node": "mindlab-2", "numpy": "2.5.3", "platform": "Linux-7.0.0-1013-oracle-x86_64-with-glibc2.39", "python": "3.14.10"}
