# W3d findings: learning to live from a parent (16 November 2026)

**Plan:** `questions.md` (W3d-frozen after a council of Gemini, ChatGPT and DeepSeek; sleep-mode sign-off). Checks All:
PASS before data (10).
- 24 cloud jobs, all finished; the manager logged "all chains closed" at 02:35.
- The frozen `analyse_w3d.py` gives `analysis.md`. Children are tested alone, with no parent, on W3's 50 test lands.
- n = 8 seeds × 50 lives. Mind Lab: no blind recompute.

## The frozen readings
1. **"A child taught by a parent lives" (≥ 0.50): NO.**
   - **PYFR** (parent childhood + "that worked!" + rest replay): survival to 3,000 = **0.128 [0.050, 0.225]**;
   - P: 0.033 [0.000, 0.098].
2. **"The parent helps" (P − D3 on survival): NO by the frozen rule.** +0.033 [0.000, +0.098]; the lower bound
   touches 0.
3. **"The recipe adds" (PYFR − P on survival):** +0.095 [−0.010, +0.210]. To 1,000 steps: **+0.177 [+0.040, +0.315]**.
4. **"A parent who never leaves" (PA − P):** survival −0.030 [−0.098, +0.007]; lifespan −116 [−434, +65].
   - PA's children live 272 steps against P's 388 and PYFR's 806.

| arm | survived to 3,000 | to 1,000 | lifespan | land known |
|---|---|---|---|---|
| D3 (W3, feelings only) | 0.000 | 0.000 | 204 | 0.53 |
| Y+FR (W3b, the recipe, no parent) | 0.000 | 0.010 | 248 | 0.63 |
| P (parent childhood, fading) | 0.033 | 0.065 | 388 | 0.78 |
| **PYFR (parent childhood + the recipe)** | **0.128** | **0.243** | **806** | **0.83** |
| PA (the parent all life) | 0.003 | 0.013 | 272 | 0.78 |

**The priors:**
- reading 1 (about 40%; council 65 / 35 / 15–20%): no;
- reading 2 (about 80%): formally no, though see below;
- reading 3 (PYFR above P, about 40%): not clear on survival, yes to 1,000;
- PA worse than P (about 35%): in the mean, yes, but the interval is wide.

## Exploratory (after the data, labelled; `explore_lifespan.py`, the same bootstrap)
| difference | lifespan | land known |
|---|---|---|
| P − D3 | +184 [+13, +500] | +0.25 [+0.09, +0.39] |
| **PYFR − D3** | **+602 [+309, +902]** | +0.30 [+0.20, +0.41] |
| PYFR − P | +418 [+51, +796] | +0.05 [−0.07, +0.18] |
| PYFR − Y+FR (W3b) | +558 [+232, +874] | +0.20 [+0.07, +0.28] |
| PA − P | −116 [−434, +65] | 0.00 [−0.15, +0.13] |

- **PYFR, per seed:** 5 of 8 children lived full 3,000-step lives at least sometimes (20, 10, 10, 6 and 5 of 50). The
  best seed averaged 1,528 steps. Three seeds stayed short (201–415).

## What it means (the assistant's reading)
- **This is the first rung where brains that learn mostly live long:** four times the lifespan of W3's brains, with
  real full lives.
- **The two ingredients work together, and neither is enough alone:**
  - the parent (the copying ingredient from every box test) teaches the child to explore its land (land known 0.53 →
    0.78–0.83);
  - "that worked!" plus rest replay (the box tests' learning-from-success part) keeps what was found. Without the
    parent it barely helped (W3b); without it, the parent's teaching mostly faded (P).
- **A parent who never leaves left children no better than a parent who left** (PA 272 against P 388; interval wide).
  Never weaned, the child depends on the teaching. This echoes WN, WE and WP's "teacher who never leaves", though not
  significantly here.
- **The council's caution holds (ChatGPT):** survival here shows that a parent's teaching can bootstrap a policy, not
  that feelings alone teach it.
- **Next (chosen by the assistant under the creator's "just go ahead"):**
  - a longer or stronger childhood (DeepSeek's dose and Gemini's longer fade), with the recipe kept;
  - or, more in line with ACL, the child learning from a learned parent (a W3d child as the next generation's parent):
    culture across generations.

## Limits
- One world and body; 8 seeds; Script as parent (engineered, fair in senses); the parent's teaching numbers fixed by
  the council.
