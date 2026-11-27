# V2-2 analysis (frozen script)

**Primary: chains per life GOAL - FT-NOGOAL = -0.096 [-0.230, +0.038] (5+/11- of 16); real gain: False**
Without the pilot seeds 1-2: -0.096 [-0.244, +0.057] (5+/9- of 14)

**Retirement test: passed = False** (chains vs the carry reflex -1.009 [-1.388, -0.636] (1+/15- of 16); survival +0.026 [-0.033, +0.089] (8+/7- of 16); Bob Profile worse beyond margin: ['R2', 'R5d', 'M2', 'G2', 'A5s'])

| arm | chains | survival |
|---|---|---|
| GOAL | 0.740 | 0.844 |
| GOAL-NOFLOOR | 0.821 | 0.846 |
| FT-NOGOAL | 0.836 | 0.863 |
| SHAM-GOAL | 0.806 | 0.863 |
| GOAL-ABLATE | 0.736 | 0.840 |
| GUIDE-REFLEX | 1.749 | 0.818 |
| NO-GUIDE | 0.730 | 0.828 |

Plain-land gate (survival vs RMS):
- GOAL: -0.006 [-0.044, +0.036] (6+/8- of 16) passed False
- GOAL-NOFLOOR: +0.020 [-0.020, +0.063] (7+/6- of 16) passed True
- FT-NOGOAL: -0.016 [-0.060, +0.029] (5+/8- of 16) passed False
- SHAM-GOAL: +0.016 [-0.018, +0.050] (8+/7- of 16) passed True

Bob Profile gate:
- GOAL: passed False, worse: ['R2', 'R5d', 'M2', 'G2', 'A5s']
- GOAL-NOFLOOR: passed False, worse: ['R2', 'R5d', 'M2', 'M2e', 'G2', 'A5s']
- FT-NOGOAL: passed False, worse: ['R2', 'R5d', 'M2', 'M2e', 'G2', 'A5s']
- SHAM-GOAL: passed False, worse: ['R2', 'M2', 'M2e', 'G2', 'A2', 'A5s']

Unseen world:
- GOAL: chains 0.566, survival 0.794
- GOAL-NOFLOOR: chains 0.570, survival 0.835
- FT-NOGOAL: chains 0.496, survival 0.820
- SHAM-GOAL: chains 0.535, survival 0.831
- GOAL - FT-NOGOAL chains +0.070 [-0.079, +0.220] (8+/8- of 16); survival -0.026 [-0.060, +0.012] (5+/9- of 16)

Secondaries:
- GOAL-SHAM-GOAL_chains: -0.066 [-0.217, +0.086] (5+/10- of 16)
- GOAL-GOAL-ABLATE_chains: +0.004 [-0.059, +0.070] (7+/8- of 16)
- GOAL-NOFLOOR-GOAL_chains: +0.081 [-0.131, +0.295] (9+/7- of 16)
- GOAL-NOFLOOR-GOAL_survival: +0.003 [-0.046, +0.054] (7+/9- of 16)
- GOAL-NO-GUIDE_chains: +0.010 [-0.166, +0.193] (8+/7- of 16)
- FT-NOGOAL-NO-GUIDE_chains: +0.106 [-0.040, +0.243] (11+/5- of 16)

Goal pursuit (share of goal steps moving closer):
- GOAL: hungry 0.409, fed 0.428
- GOAL-NOFLOOR: hungry 0.402, fed 0.430
- SHAM-GOAL: hungry 0.416, fed 0.429
