# W3c findings: when a need is strong, it takes over (15 November 2026)

**Plan:** `questions.md` (W3c-frozen; exploratory, no council, the creator's "go ahead").
- Checks All: PASS before data (12 checks).
- 35 cloud jobs, all finished; the manager logged "all chains closed" at 22:38.
- The frozen `analyse_w3c.py` gives `analysis.md`. It and these findings were run and written at the 22:47
  sleep-mode heartbeat.
- n = 8 seeds × 50 test lives per arm. Mind Lab: no blind recompute.

## The frozen readings
1. **"The gate un-drowns hunger" (step 0c): NO.**
   - W3's D3i with the gate added at test: survival 0 on every walk.
   - Lifespan: learned head 199, greedy value walk 162, one-step look-ahead 170.
2. **"The fair ceiling is reachable": NO.**
   - F2 (hungry → walk to food remembered as full; tired → the shelter; otherwise W3's D3) survives 0.055
     [0.033, 0.080], against Script's 0.96.
   - But it lives **679 steps** [563, 786] against D3's 204, and 0.21 of its lives reach 1,000 steps.
3. **"A learned brain lives": NO.** G 0.000, GYFR 0.013 [0.000, 0.038], Gi 0.000.
4. **"The gate helps":** GYFR's survival is not 0, so the frozen rule reads survival.
   - G − D3 0.000; Gi − D3i 0.000; GYFR − W3b's Y+FR +0.013 [0.000, +0.038]. All **NO**.
5. **Gate or quiet start:** G − Z0 on survival 0.000 [0.000, 0.000].

**The priors:**
- reading 1 (about 40%): no;
- reading 2 (about 70%): **no**, my largest miss;
- reading 3 (about 15%): no;
- reading 4 (about 55%): no.

## Exploratory (after the data, labelled; `explore_lifespan.py`, the same bootstrap)
**Paired lifespan differences**, which the frozen rule did not use:

| difference | lifespan, mean [95% interval] |
|---|---|
| G − D3 | +4.5 [−5.8, +13.9] (no gain) |
| **Gi − D3i** | **−21.6 [−35.6, −8.8]** (the gate made the given-link brain worse) |
| G − Z0 | +15.0 [+2.8, +27.4] |
| **GYFR − G** | **+104 [+18, +254]** |
| GYFR − W3b's Y+FR | +64 [−62, +247] |

- **One GYFR seed (5) lived 835 steps on average, and 5 of its 50 test lives survived the full 3,000 steps.**
  - This is the first time in W3–W3c that a brain that learned everything itself lived a whole life.
  - It is one seed of eight, so it is not a finding about the arm; it shows the recipe can sometimes get there.

## What it means (the assistant's reading)
- **The gate, as built (damping the base map and curiosity when a need is strong), did not help.**
  - Alone it changed nothing. With the designer's links it made things worse.
  - Damping everything else also damps what the planner uses to find its way, so a strong need may make the brain
    blinder, not more focused.
  - The biology (incentive salience; `D:\acl\docs\research\incentive_salience_2026-11-15.md`) describes a narrower,
    need-specific gain on the relevant cue, not a damping of the rest.
- **What helps is the box-test recipe:** "that worked!" plus rest replay (GYFR beats G by about 100 steps), as in W3b.
- **The fair ceiling shows the other half of the problem:**
  - remembering where full food is lets an animal live about 3.3× longer;
  - but with W3's poor exploring it still rarely survives. Script survives because it explores systematically
    (always to the nearest unseen place).
  - **Finding food is now the bottleneck, as much as remembering it.**
- **Next candidates (need the creator):**
  - (1) a need-specific gain (hunger raises the food channel more steeply) instead of the damping gate;
  - (2) a better exploring drive (curiosity that heads for the nearest unknown, as Script does), tested first in the
    fair ceiling;
  - (3) the recipe (Y+FR) kept in every arm.

## Limits
- W3's one world and body; 8 seeds; one gate form; no council.
- The ceiling's non-hungry behaviour is W3's D3 (poor exploring), which caps it.
