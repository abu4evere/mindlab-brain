# W3b findings: living by feelings, with "that worked!" and rest replay (15 November 2026)

- **Plan:** `questions.md` (W3b-frozen after a council of GPT, Gemini and DeepSeek; built and launched by the Fable
  session; pre-data correction 1).
- **Review:** the Opus session's independent review of the plan, code and checks was written before any result was
  opened (`review_opus.md`).
- **Run:** 35 cloud jobs, all finished (`manage.log`: "all chains closed" at 17:09; the manager script is kept as
  `manage_w3b.py`). The frozen `analyse_w3b.py` gives `analysis.md`, run at 18:0x by the Opus session.
- n = 8 seeds × 50 test lives per arm. Mind Lab: exploratory, no blind recompute.

## Validity
- Checks All: PASS before data (D3 with no part reproduces W3 bit for bit; a split run equals an unsplit one; and the
  rest in `checks.log`).
- All 32 training runs and both test-only parts finished. W3b is valid.

## Step 0: why did W3's D3i (given the right links) die?
| W3 brain | (a) learned head | (b) greedy walk on its value map | (c) one-step look-ahead | food cells' reward minus the rest |
|---|---|---|---|---|
| D3i | 0.000 | 0.000 | 0.000 | +0.623 [+0.328, +0.877] |
| D3 | 0.000 | 0.000 | 0.000 | +0.184 [−0.254, +0.588] |

- **Frozen reading: "neither alone".** Walking straight down the value map dies too, so the head is not the only
  broken part. But the food cells do get more reward than the rest in D3i.
- **The logged parts at hungry steps show why** (D3i, mean absolute part per open cell):
  - hunger × link: 0.009;
  - curiosity × link: 0.551;
  - the drive-free base map W₀: 0.875.
- **Reading (the Opus session's, from these logs; not a separate test):** the hunger signal was about 100 times
  weaker than the base map and the curiosity term, which drowned it.
  - W₀ starts random (N(0, 0.3)) and never learned to be quiet.
  - So even a correct hunger → food link barely changed where the brain went.

## The arms
| arm | survived to 3,000 | survived to 1,000 | lifespan | land known |
|---|---|---|---|---|
| D3 (W3) | 0.000 | 0.000 | 204 | 0.53 |
| D3+Y ("that worked!") | 0.000 | 0.003 | 220 | 0.65 |
| D3+FR (fast store replayed at rest) | 0.000 | 0.000 | 218 | 0.61 |
| **D3+Y+FR** | 0.000 | 0.010 | **248** | 0.63 |
| D3+RR (random replay, control) | 0.000 | 0.000 | 192 | 0.31 |
| D3+F (acting fast memory, engineered ceiling) | 0.000 | 0.000 | 205 | 0.50 |

**The frozen readings:**
1. **"A learned brain lives": NO.** Every survival share is 0.
2. **"The parts help":** read on lifespan, as frozen, since every survival is 0.
   - Y − D3 +16 [−4, +33]: no.
   - FR − D3 +14 [−12, +38]: no.
   - **Y+FR − D3 +44 [+14, +89]: yes.** The two together lengthen life by about a fifth.
3. **"Content, not compute": YES.** FR − RR on lifespan +25 [+9, +40].
   - But RR is itself worse than D3 (192 against 204; land known 0.31 against 0.53).
   - So part of this gap is random replay doing harm, not only successful replay helping.
4. **"The ceiling is reachable": NO.** D3+F survives 0.
5. **Survival to 1,000:** at most 0.010 (Y+FR − D3 +0.010 [+0.003, +0.020]).

**The priors:**
- step 0 "neither alone" (about 25%): yes;
- reading 1 (about 15%): no;
- reading 2, each part lifts life (about 55%): only the pair;
- reading 3 (about 45%): yes;
- reading 4 (about 60%): no.

## Why the engineered ceiling failed (a reading after the data, not a tested cause)
- **F walks to the cell where the need was last relieved,** that is, the food cell it last ate at. In W3's world an
  eaten cell is empty and regrows only after R = 200 steps.
- So F returns to an empty cell when hungry. Script, which survives 0.96, goes to the nearest food remembered as full.
- **The ceiling, as designed, pointed at the wrong place.** A "remembered full food" store is the fair ceiling. It is
  not tested here.

## What it means (the assistant's reading)
- **The box-test recipe helped a little:**
  - "that worked!" plus rest replay lived about 20% longer;
  - replaying one's successes beat replaying random moments.
  - But no brain learned to stay alive.
- **The deeper fault is in the starting brain, not in what it learns from:** the hunger signal is drowned by a random
  base map and by curiosity. A part that lets a strong need take over (when starving, food matters most) is missing.
  In animals, a strong need narrows attention.
- **Next candidates (need the creator):**
  - (1) a base map that starts at zero, or that a strong need turns down (drive-gated attention);
  - (2) a fair ceiling (a store of food remembered as full);
  - (3) W3b's recipe again on top of (1).

## Limits
- One world and body; 8 seeds; the parts' numbers fixed by the council.
- The hungry-step logs come from step 0 only (W3's weights), not from the W3b arms.
