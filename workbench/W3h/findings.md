# W3h findings: pain (17 November 2026, about 02:10)

**Plan:** `questions.md` (W3h-frozen; council `../W3h_council_2026-11-16.md`; amendment 1 before any brain trained:
the careful parent's bar relative to the no-thorn Script).
- **The world:** 2 thorn patches, harm 6. Pain in the pain arms is 0.75 per thorn step.
- **Checks:** All: PASS (11).
- **Runs:** 32 cloud jobs, all finished (closed 01:57). The frozen `analyse_w3h.py` gives `analysis.md`.
- n = 8 seeds × 50 test lives per arm. Mind Lab: no blind recompute.

## The frozen readings
| arm | thorn steps / 1,000 | steps onto a thorn per chance | lifespan | survived |
|---|---|---|---|---|
| TH (no pain, thorn-blind parent) | 35.6 | 0.28 | 404 | 0.013 |
| THP (pain) | **22.2** | **0.17** | 513 | 0.033 |
| THw (careful parent) | 26.8 | 0.19 | 582 | 0.050 |
| THPw (pain + careful parent) | **14.3** | 0.14 | 582 | 0.070 |

1. **"Pain teaches avoidance": yes.** THP − TH −13.4 [−22.8, −4.3] thorn steps per 1,000 (about 40% fewer).
   Stepping onto a thorn when one is beside it falls from 0.28 to 0.17 [−0.15, −0.08].
2. **"Pain helps it live": not shown.** THP − TH lifespan +109 [−12, +217]; survival +0.020 [−0.003, +0.045].
3. **"Watching teaches avoidance": no, just.** THw − TH −8.8 [−19.2, +0.6].
   - Secondary: steps onto a thorn per chance −0.10 [−0.15, −0.04];
   - and survival +0.038 [+0.018, +0.057].
4. **"Pain adds to watching": yes.** THPw − THw −12.5 [−22.3, −2.8].

**The priors:**
- reading 1, about 75%: yes;
- reading 2, about 35%: not shown;
- reading 3, about 50%: no (the interval just touches 0);
- reading 4, about 50%: yes.

## What the training curves show (thorn steps per 1,000, per 100,000-step block; reported, frozen measure 6)
| block (×100,000 steps) | 1 | 4 | 8 | 12 | 16 | 20 |
|---|---|---|---|---|---|---|
| TH | 43 | 43 | 27 | 31 | 33 | 34 |
| THP | 44 | 38 | 18 | 18 | 19 | 17 |
| THw | 24 | **6** | 9 | 13 | 20 | **23** |
| THPw | 24 | 7 | 9 | 12 | 13 | 14 |

- **A careful parent teaches avoidance fast.** During childhood (the first 400,000 steps) THw's thorn steps fall from
  24 to 6.
- **Without pain, that lesson wears off once the parent is gone.** THw climbs back to 23 by the end. With pain
  (THPw), it climbs only to 14.
- **Pain alone teaches slowly but keeps it.** THP falls after childhood (44 → 18) and stays there.
- **No pain:** TH drifts back up (27 → 34). Hunger alone is too late a teacher.

## Fear? (secondary)
- **No over-avoidance.** In every arm, the share of meals eaten within 2 cells of a thorn (0.18) equals the share of
  the land's food that lies there (0.18).
- **The pain-taught brains avoid stepping on thorns, not the places beside them.** That is avoidance, not
  generalised fear.

## What it means (the assistant's reading)
1. **Pain works as a teacher.** An immediate, harm-sized pain cuts harm by about 40%, where the later hunger from the
   same injury barely does. This is the creator's "for beginning there should be pain", measured.
2. **Pain and a parent are better together.** The parent shows the way early, and pain keeps the lesson after the
   parent leaves. This matches W3f's finding that copying alone loses skill.
3. **Living longer needs more than avoiding thorns.** The brains still die mostly for the old reason (W3/WX: no food
   known). Thorns made every arm live shorter than W3d's thorn-free 806.
4. **For the starting brain:** keep pain during development, together with a parent's childhood.

## Limits
- 8 seeds.
- One harm level and one pain scale.
- Thorns are visible: this is avoidance of a seen danger, not of an unseen one.
- Pain is a reward signal. Nothing here says anything is felt.
