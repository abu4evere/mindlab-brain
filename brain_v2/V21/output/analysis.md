# V2-1 analysis (frozen script)

**Primary: swap survival SURPRISE - PLAIN = +0.625 [+0.580, +0.667] (16+/0- of 16); real gain: True**
**No-loss gate: stable survival SURPRISE - PLAIN = -0.001 [-0.007, +0.005] (3+/4- of 16); passed: True**

| arm, condition | survival | lifespan | table right at end | latency | resets | hunger-reflex share of post-swap meals |
|---|---|---|---|---|---|---|
| PLAIN_swap | 0.226 | 2080 | 0.203 | 359 | 0.00 | 0.383 |
| PLAIN_stable | 0.849 | 2696 | 0.987 | nan | 0.00 | 0.032 |
| SURPRISE_swap | 0.851 | 2702 | 0.095 | 70 | 2.35 | 0.047 |
| SURPRISE_stable | 0.848 | 2694 | 0.987 | nan | 0.62 | 0.032 |
| WINDOW_swap | 0.290 | 2156 | 0.196 | 103 | 0.00 | 0.283 |
| WINDOW_stable | 0.845 | 2692 | 0.987 | nan | 0.00 | 0.030 |
| SHAM_swap | 0.251 | 2128 | 0.095 | 302 | 18.55 | 0.228 |
| SHAM_stable | 0.838 | 2688 | 0.982 | nan | 0.69 | 0.032 |

Secondaries:
- SURPRISE-SHAM_swap: +0.600 [+0.551, +0.650] (16+/0- of 16)
- SURPRISE-WINDOW_swap: +0.561 [+0.495, +0.623] (16+/0- of 16)
- WINDOW-PLAIN_swap: +0.064 [+0.019, +0.106] (12+/4- of 16)
- WINDOW-PLAIN_stable: -0.004 [-0.010, +0.004] (3+/6- of 16)
- SURPRISE-PLAIN_acc_end_swap: -0.108 [-0.140, -0.078] (0+/15- of 16)
- SURPRISE-PLAIN_reflex_share_swap: -0.337 [-0.359, -0.315] (0+/16- of 16)

Test B (join changed at step 1,500):
- PLAIN: before 2.73, after 0.82
- SURPRISE: before 2.73, after 1.68
- WINDOW: before 2.72, after 1.74
- SHAM: before 2.73, after 0.63
- SURPRISE-PLAIN_after: +0.865 [+0.656, +1.081] (15+/1- of 16)
- WINDOW-PLAIN_after: +0.924 [+0.716, +1.139] (16+/0- of 16)
- SHAM-PLAIN_after: -0.190 [-0.280, -0.111] (2+/14- of 16)
- SURPRISE-SHAM_after: +1.055 [+0.833, +1.276] (16+/0- of 16)
- SURPRISE-WINDOW_after: -0.059 [-0.172, +0.059] (5+/11- of 16)
- SURPRISE-PLAIN_before: +0.000 [+0.000, +0.000] (0+/0- of 16)

Machines: 3
- {"node": "DESKTOP-B9PA260", "numpy": "2.5.3", "platform": "Windows-10-10.0.19045-SP0", "python": "3.12.10"}
- {"node": "mindlab-1.us-east4-a.c.aiiab-515203.internal", "numpy": "2.5.3", "platform": "Linux-7.0.0-1017-gcp-x86_64-with-glibc2.43", "python": "3.14.4"}
- {"node": "mindlab-2", "numpy": "2.5.3", "platform": "Linux-7.0.0-1013-oracle-x86_64-with-glibc2.39", "python": "3.14.10"}
