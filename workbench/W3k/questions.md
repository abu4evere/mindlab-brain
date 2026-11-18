# W3k: a longer childhood still, and keeping the adult's best (plan, frozen before any code was run or data)

**Frozen** as git tag `W3k-frozen`.
- **Sign-off:** the creator's standing "do not ask me go ahead bro", and, 18 November 2026: "alr bet keep it pushing".
- **Council:** `../W3k_council_2026-11-18.md` (GPT, Gemini). Draft: `../W3k_draft.md`.
- **Exploratory,** in the W3 series.

## Why
W3j's C2 (a 2.4M-step fading childhood within 4.0M steps) is the best brain yet: lifespan 1,594, fresh-land survival
0.380. A longer childhood is the strongest lever (W3d, W3i, W3j). But every brain peaks 0.4 to 0.8M steps after its
childhood and then declines while it keeps learning alone; a slower learning rate and a lingering live parent did not
stop it. And cloud runs were not bit-identical, which made seed noise huge.

## Arms (W3j's C2 settings unless stated: W3d's PYFR, no pain; 16 seeds, 1–16; GitHub's machines)
| arm | what | trained in |
|---|---|---|
| **R2** | C2 again with W3k's code: 4.0M steps, 2.4M fade; the brain at the end | run "R" |
| **CS** | the same run as R2; the brain is the copy kept by its own lives (below) | run "R" |
| **CY** | the same run as R2; the brain is the copy at a step drawn at random in advance (below) | run "R" |
| **C3** | 5.2M steps, **3.6M fade** (the same 1.6M alone as R2) | run "C3" |
| **CR** | R2's settings; after the fade, every 4th step, one copy step (weight 0.05) toward a stored parent example | run "CR" |

- **CS, "keep the best self":** from 200,000 steps after the fade, at the end of each training life, the brain computes
  the mean length of its training lives that ended in the last 200,000 steps. Whenever that mean is the highest so far,
  it keeps a copy of its weights. CS is the last copy kept (or the end-of-training brain if none was kept). Only the
  brain's own training lives are used, never a test.
- **CY, the control (GPT):** one step is drawn in advance, uniformly between 200,000 steps after the fade and the end of
  training, from numpy seed 20261181 + the run seed. CY is the brain at the first life boundary after that step.
- **CR, "remember the parent":** during the second half of the fade (1.2M to 2.4M steps), every parent copy step's
  example (the map, levels, cell and the parent's move) is kept by reservoir sampling, up to 20,000. After the fade,
  every 4th step, one stored example is drawn and the brain takes one copy step toward it at weight 0.05. The live
  parent is gone after the fade.
- **Numerical determinism:** before numpy loads, every run sets `OPENBLAS_CORETYPE=Haswell` and
  `NPY_DISABLE_CPU_FEATURES=X86_V4` (threads are already 1), so the maths take the same path on Intel and AMD runners.
  Every run logs its processor model and numpy's configuration.
- **The determinism job:** run "R" seed 1 trained twice more, as separate jobs (D1, D2). Reported whatever it shows:
  bit-identical weights to R seed 1, or not, with the processors logged.
- **Snapshots** at the first life boundary after the fade, then every 400,000 steps (tested), as W3j.

## Measures (W3's 50 test lands, alone, learning off; the parent never present)
1. Lifespan; survival to 3,000 and to 1,000; survival on the 50 fresh lands (910001–910050).
2. Policy drift from the end-of-fade brain; agreement with the parent (as W3j).
3. For CS and CY: the step their copy comes from.
4. Medians beside the means, and leave-one-seed-out ranges for the two primary readings (GPT).

## Readings (bootstrap over the 16 seeds, paired by seed; numpy seed 20261180)
1. **Two primary readings (Bonferroni: each read with a 97.5% interval, lower bound above 0):**
   - **"A longer childhood still helps":** C3 − R2 on lifespan.
   - **"Choosing its own best copy helps":** CS − R2 on lifespan.
2. **How to read a CS win (GPT), 95% interval:** CS − CY on lifespan.
   - If CS − CY is above 0: the brain's own lives carry information about when it was better.
   - If not: an earlier copy simply beats the worn-down end; the brain's own signal adds nothing shown.
3. **Secondary, 95% intervals:** CR − R2 on lifespan; CY − R2 (whether any earlier copy beats the end).
4. **Toward the bar:** the best arm's fresh-land survival against 0.80.
5. **Upper bound, exploratory (GPT):** per seed, the best tested snapshot of run "R" (chosen after the fact, by the
   test itself). Reported as how much choosing a copy could recover at most; never as a result.

## Validity (hard stops)
- **Checks All: PASS before data:**
  - R2, CS and CY come from one run; CS's copy follows its rule on a hand-made run; CY's step is drawn as stated;
  - C3 fades over 3.6M and trains 5.2M;
  - CR stores only second-half-of-fade examples, at most 20,000; replays only after the fade, every 4th step, at 0.05;
  - the determinism settings are set before numpy loads, in every entry point;
  - a split run equals an unsplit run (CS's and CR's state survives a pause);
  - the same seed twice is the same, locally.
- The determinism job is reported whatever it shows.

## The assistant's prior
- C3 − R2 above 0: about 50%.
- CS − R2 above 0: about 55%.
- CS − CY above 0: about 40%.
- CR − R2 above 0: about 25%.
- Any arm reaches 0.80 on fresh lands: about 3%.
- The determinism job is bit-identical: about 60%.

## Amendment 1 (18 November 2026, before any data; the first 50 jobs all stopped at the checks)
- **What happened:** on GitHub's Linux machines the determinism check failed, so no job trained. The check looked for
  "X86_V4" in numpy's list of *compiled* code paths, which on Linux always contains it (and two further AVX-512
  groups, AVX512_ICL and AVX512_SPR), whatever the processor. A diagnostic job confirmed this.
- **The change:** numpy is told to switch off all three AVX-512 groups (`NPY_DISABLE_CPU_FEATURES="AVX512_SPR
  AVX512_ICL X86_V4"`), and the check now reads the code paths numpy actually *uses*, requiring none of them to be
  AVX-512. Every run also records those paths. Nothing else changes.
