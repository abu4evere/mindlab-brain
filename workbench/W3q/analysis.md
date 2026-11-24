# W3q analysis (the frozen analysis, analyse_w3q.py)

- Checks All: PASS: **yes**
- All inputs present: **yes**

## Manipulation check (did the child learn the lie?)

- BF − HR at the end of childhood (2.4M), toward the lie: +0.052 [-0.004, +0.109] -> **FAILED: the study reads manipulation failed**

## Primary

- **A, recovery after the parent leaves (BF − HR, final):** +0.013 [-0.008, +0.033] -> **rejected** (at +0.05: rejected); seeds [0.025, -0.025, 0.05, -0.02, 0.05, -0.02, 0.03, 0.01]
- **B, resistance while the parent keeps teaching (BP − RP, final):** +0.125 [+0.111, +0.138] -> **kept** (at +0.05: kept); seeds [0.12, 0.15, 0.125, 0.15, 0.125, 0.085, 0.115, 0.13]

(The manipulation check failed: A and B say little about rejecting a lie.)

## The probe over time (mean share; random policy toward the lie about 0.246)

| copy | BF lie | BP lie | RP lie | HR lie | BF − HR | BP − RP | BF truth | BP truth | RP truth | HR truth |
|---|---|---|---|---|---|---|---|---|---|---|
| 2400k | 0.127 | 0.205 | 0.104 | 0.074 | +0.052 [-0.004, +0.109] | +0.101 [+0.041, +0.153] | 0.792 | 0.695 | 0.751 | 0.823 |
| 2800k | 0.091 | 0.214 | 0.113 | 0.079 | +0.011 [-0.004, +0.027] | +0.101 [+0.032, +0.170] | 0.846 | 0.704 | 0.764 | 0.843 |
| 3200k | 0.096 | 0.221 | 0.099 | 0.072 | +0.024 [+0.007, +0.043] | +0.122 [+0.058, +0.174] | 0.842 | 0.677 | 0.759 | 0.858 |
| 3600k | 0.075 | 0.224 | 0.092 | 0.074 | +0.001 [-0.016, +0.019] | +0.133 [+0.034, +0.206] | 0.854 | 0.689 | 0.786 | 0.857 |
| final | 0.081 | 0.218 | 0.093 | 0.069 | +0.013 [-0.008, +0.033] | +0.125 [+0.111, +0.138] | 0.859 | 0.679 | 0.789 | 0.872 |
| S | 0.092 | 0.214 | 0.085 | 0.082 | +0.010 [-0.027, +0.046] | +0.129 [+0.074, +0.184] | 0.852 | 0.706 | 0.807 | 0.849 |

## Secondary (final brains unless named)

- Toward the truth: BF − HR -0.013 [-0.036, +0.013]; BP − RP -0.109 [-0.160, -0.066]
- The walk, a corner entered before food: BF − HR +0.016 [-0.002, +0.035]; BP − RP +0.121 [+0.107, +0.133]
- The walk, steps to food: BF − HR +0.2 [-0.2, +0.7]; BP − RP +0.8 [-0.7, +2.3]

| measure | BF | BP | RP | HR | BF − HR | BP − RP | RP − HR |
|---|---|---|---|---|---|---|---|
| final, reflexes (lifespan) | 2658.1 | 1238.3 | 1515.6 | 2578.8 | +79.3 [-129.8, +261.5] | -277.3 [-676.4, +141.0] | -1063.3 [-1488.4, -672.7] |
| kept, reflexes (lifespan) | 2532.2 | 1066.9 | 1627.5 | 2802.9 | -270.7 [-548.0, -98.2] | -560.7 [-994.5, -153.9] | -1175.4 [-1673.5, -697.4] |
| kept, bare (lifespan) | 1611.5 | 383.4 | 731.7 | 1607.5 | +4.0 [-289.6, +264.4] | -348.3 [-602.6, -98.0] | -875.8 [-1154.6, -587.4] |
| final, fresh (survived) | 0.815 | 0.167 | 0.273 | 0.815 | +0.000 [-0.145, +0.145] | -0.105 [-0.253, +0.033] | -0.542 [-0.725, -0.328] |
| kept, fresh (survived) | 0.805 | 0.103 | 0.323 | 0.877 | -0.072 [-0.215, +0.028] | -0.220 [-0.430, -0.030] | -0.555 [-0.735, -0.350] |

- Lifespan loss small (lower bound above -200): BF − HR **True**; BP − RP **False**

## The dose (the lying parent's choices that differ from the right parent's)

- BF: 8 seeds; lies per run [740230, 648364, 680785, 668489, 637633, 640760, 660899, 657966]; share of the parent's choices [0.308, 0.27, 0.284, 0.279, 0.266, 0.267, 0.275, 0.274] (a copy lesson every 4th step)
- BP: 8 seeds; lies per run [1149942, 1041847, 1069954, 1043021, 1026905, 1025854, 1015756, 1044073]; share of the parent's choices [0.287, 0.26, 0.267, 0.261, 0.257, 0.256, 0.254, 0.261] (a copy lesson every 4th step)
