# W3l findings: the longer childhood with the kept copy, and longer still (19 November 2026)

**Plan:** `questions.md` (W3l-frozen; council `../W3l_council_2026-11-19.md`). Checks All: PASS before data, and in all
87 cloud check logs. 32 cloud jobs (16 seeds × C3, C5), all closed 17:17 on 19 November.
- The frozen `analyse_w3l.py` gives `analysis.md`. n = 16 seeds × 50 test lives (and 50 fresh lands).
- **Recompute:** the assistant recomputed the primary readings with a separate short script and a different bootstrap
  seed: the same means; interval ends within 8 steps.
- **The reproduction check is exact: 16 of 16 seeds.** C3 retrained here equals W3k's C3 bit for bit (every weight
  array), with the same kept-copy step. (The freeze commit's message said "checked" too early; it is checked here.)

## The frozen readings
| arm | what | lifespan | median | survived | to 1,000 | fresh lands: survived |
|---|---|---|---|---|---|---|
| CS (W3k, cited) | 2.4M fade of 4.0M, kept copy | 1,835 | 1,885 | 0.478 | 0.611 | 0.445 |
| C3 | 3.6M fade of 5.2M, the end | 1,753 | 1,869 | 0.429 | 0.600 | 0.460 |
| C3S | the same run, kept copy | 1,697 | 1,811 | 0.410 | 0.584 | 0.425 |
| C3Y | the same run, a copy at a step drawn in advance | 1,755 | 1,643 | 0.416 | 0.610 | 0.420 |
| **C5** | **4.8M fade of 6.4M**, the end | **2,031** | 1,950 | **0.552** | 0.688 | 0.546 |
| **C5S** | the same run, kept copy | **2,041** | 2,065 | **0.555** | 0.695 | **0.559** |
| C5Y | the same run, a copy at a step drawn in advance | 2,071 | 2,180 | 0.564 | 0.705 | 0.521 |

1. **Primary readings (97.5% intervals):**
   - **"The longer childhood (and 1.2M more steps) adds to the kept copy" (C3S − CS): −138 [−515, +246]. No.**
     6 of 16 seeds above 0.
   - **"An even longer childhood helps" (C5S − C3S): +344 [+102, +651]. Yes.** 12 of 16 seeds; every
     leave-one-seed-out mean +245 to +382.
2. **Secondary (95%):** C5 − C3 **+278 [+44, +564], yes** (the ends agree: the gain is in the brain, not the copy);
   C3S − C3 −56 [−215, +126], no; C3S − C3Y −58, no; C5S − C5Y −30, no.
3. **Toward the bar:** the best arm by lifespan is C5Y (2,071); **C5S's fresh-land survival 0.559 [0.478, 0.635] is
   the best yet** (W3k's CS 0.445). The bar is 0.80.

**The priors** (frozen): C3S − CS above 0, about 30%: no. C5S − C3S above 0, about 35%: yes. C3S − C3 above 0, about
25%: no. The reproduction exact, about 85%: yes. Any arm at 0.80, about 2%: no.

## Exploratory (labelled)
- The learning curves (tested snapshots, mean lifespan): C3 1,454 → 1,756 → 1,769 → 1,743 → end 1,753; C5 1,725 →
  2,062 → 2,067 → 1,993 → end 2,031. After a long childhood the curve stays flat, so a kept copy has nothing to rescue.

## What it means (the assistant's reading)
1. **A longer childhood is the strongest lever, a fourth time** (W3d, W3i, W3j, now W3l): 4.8M steps of fading
   parent within 6.4M steps gives the best brain yet, full lives 0.55, fresh lands 0.56.
2. **The kept copy only helps when the curve declines** (W3k's run R). After a long childhood it adds nothing.
3. **The best recipe so far is C5 (no copy needed).** The bar (0.80 on fresh lands) is still far; W3m (running) tests
   the body's sleep reflex on W3k's recipe, where tiredness near food is the main cause of death.
4. The council's advice stands: no fifth length for now; the next gains should come from the deaths (W3m), then the
   two combined (C5's childhood with the winning part of W3m).
