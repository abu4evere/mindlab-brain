# CW2 analysis (frozen script)

Lives per arm: {'GUIDE-REFLEX': 800, 'GUIDE-MAP': 800, 'SHAM-REFLEX': 800, 'SHAM-MAP': 800, 'NO-GUIDE': 800, 'RANDOM-OPS': 800}

**Primary: mean chains per life, GUIDE-REFLEX - NO-GUIDE = +0.627 [+0.430, +0.843] (16+/0- of 16 seeds); real gain: True**

**Key secondary (GPT's reading rule): GUIDE-MAP - NO-GUIDE = +0.108 [+0.060, +0.160] (12+/2- of 16 seeds); real gain: True**

| measure | GUIDE-REFLEX | GUIDE-MAP | SHAM-REFLEX | SHAM-MAP | NO-GUIDE | RANDOM-OPS |
|---|---|---|---|---|---|---|
| mean_chains | 1.110 | 0.590 | 0.306 | 0.499 | 0.483 | 0.000 |
| share_1plus | 0.255 | 0.255 | 0.255 | 0.255 | 0.255 | 0.000 |
| share_3plus | 0.076 | 0.062 | 0.007 | 0.060 | 0.049 | 0.000 |
| carry_time | 113.806 | 241.704 | 347.417 | 282.844 | 291.562 | nan |
| joins_on_station_guide | 0.000 | 0.000 | 0.034 | 0.223 | 0.000 | 0.000 |
| station_returns | 50.157 | 8.726 | 1.131 | 2.509 | 2.671 | 0.000 |
| station_guides | 5.168 | 1.433 | 9.110 | 1.138 | 0.000 | 0.000 |
| acts_per_carry_step | 0.067 | 0.060 | 0.050 | 0.056 | 0.053 | 0.703 |
| lifespan | 2624.903 | 2639.976 | 2634.934 | 2639.841 | 2641.177 | 2566.319 |
| survival | 0.806 | 0.819 | 0.812 | 0.821 | 0.821 | 0.782 |
| acts | 92.214 | 91.683 | 87.184 | 90.125 | 89.765 | 973.290 |

Secondaries:
- REFLEX-SHAM_chains: +0.804 [+0.574, +1.051] (16+/0- of 16 seeds)
- MAP-SHAM_chains: +0.091 [+0.046, +0.145] (12+/1- of 16 seeds)
- REFLEX-RANDOM_chains: +1.110 [+0.853, +1.380] (16+/0- of 16 seeds)
- MAP-RANDOM_chains: +0.590 [+0.470, +0.715] (16+/0- of 16 seeds)
- REFLEX-NOGUIDE_share_1plus: +0.000 [+0.000, +0.000] (0+/0- of 16 seeds)
- REFLEX-NOGUIDE_carry_time: -177.757 [-214.263, -145.967] (0+/16- of 16 seeds)
- MAP-NOGUIDE_carry_time: -49.858 [-77.680, -23.044] (1+/14- of 16 seeds)
- REFLEX-NOGUIDE_station_returns: +47.486 [+39.962, +55.420] (16+/0- of 16 seeds)
- MAP-NOGUIDE_station_returns: +6.055 [+4.706, +7.356] (16+/0- of 16 seeds)
- REFLEX-NOGUIDE_survival: -0.015 [-0.026, -0.005] (1+/7- of 16 seeds)
- MAP-NOGUIDE_survival: -0.003 [-0.007, +0.002] (1+/3- of 16 seeds)
- REFLEX-NOGUIDE_lifespan: -16.275 [-28.705, -3.909] (1+/10- of 16 seeds)
- MAP-NOGUIDE_lifespan: -1.201 [-4.339, +1.779] (2+/5- of 16 seeds)

Machines: 3
- {"node": "DESKTOP-B9PA260", "numpy": "2.5.3", "platform": "Windows-10-10.0.19045-SP0", "python": "3.12.10"}
- {"node": "mindlab-1.us-east4-a.c.aiiab-515203.internal", "numpy": "2.5.3", "platform": "Linux-7.0.0-1017-gcp-x86_64-with-glibc2.43", "python": "3.14.4"}
- {"node": "mindlab-2", "numpy": "2.5.3", "platform": "Linux-7.0.0-1013-oracle-x86_64-with-glibc2.39", "python": "3.14.10"}
