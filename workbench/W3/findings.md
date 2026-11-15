# W3 findings: drives only (survival, comfort, curiosity) — the brain did not learn to live (15 November 2026)

Plan: `questions.md` (W3-frozen, council of 13 November). Pre-data corrections 1–4 in `IMPLEMENTATION.md`. Checks
All: PASS before data.
- **Run:** on the creator's PC at Idle, 13 November (about 15:00) to 15 November 06:26: 32 training runs of 2,000,000
  steps; `jobs.log`: "all done; failures 0".
- **Analysis:** the frozen `analyse_w3.py`, giving `results.md`. n = 8 runs × 50 test lives per learned brain.
- Mind Lab: exploratory, no blind recompute.

## Validity
- Calibration rule met: Script survived 0.96 of the test lives (2,963 steps on average); Rand none.
- Code checks All: PASS. All 32 runs finished with return code 0.
- W3 is valid; the readings below are its results.

## The frozen readings
| brain | survived to 3,000 | lifespan (steps) | land known at the end | hungry | exhausted |
|---|---|---|---|---|---|
| D3 (all three drives) | 0.000 [0.000, 0.000] | 204 [191, 217] | 0.527 [0.444, 0.610] | 0.201 | 0.451 |
| D2 (no curiosity) | 0.000 | 195 [187, 203] | 0.424 [0.399, 0.453] | 0.217 | 0.425 |
| Dc (curiosity only) | 0.000 | 246 [243, 249] | 0.863 [0.844, 0.882] | 0.165 | 0.542 |
| D3i (the designer's links given) | 0.000 | 215 [203, 229] | 0.560 [0.474, 0.651] | 0.210 | 0.486 |
| D3− (D3 with curiosity off) | 0.000 | 172 [163, 183] | 0.295 [0.244, 0.343] | 0.248 | 0.365 |
| Rand (50 lives) | 0.000 | 174 | 0.428 | 0.201 | 0.364 |
| Script (50 lives) | 0.960 | 2963 | 1.000 | 0.002 | 0.020 |

- **Reading 1, "drives are enough to live": NO.** D3 survival 0.000 [0.000, 0.000]. The prior was about 35%.
- **Reading 2, "curiosity pays": NO.**
  - The finding share is undefined (no learned brain was alive at any relocation, which needs about 300 steps), and
    survival is 0 against 0.
  - D3's curiosity row did not collapse (0 of 8).
  - The prior was about 40%.
- **Reading 3, "curiosity alone is not enough": NO** by the frozen rule (Dc − D3 survival 0.000, upper bound not
  below 0). Every brain is at the floor, so this "no" carries no information. The prior was about 90%.
- **D3i at least as good as D3:** formally yes (both 0). Not informative.

## Secondary (intervals, no gate)
- **D3 − D2, land known: +0.103 [+0.033, +0.178].**
- D3 − D2: hungry −0.016 [−0.035, +0.006]; exhausted +0.025 [−0.004, +0.058].
- **Curiosity drives exploring:**
  - Dc knows 0.86 of its land;
  - taking curiosity out of the trained D3 (D3−) drops what it knows from 0.53 to 0.30 and its lifespan from 204 to
    172.
- **The learned links are not consistent:** D3's food-channel weight in W_s is positive in 6 seeds and negative in 2;
  D2's in 6 and 2 (`results.md`).

## An exploratory check after the data (labelled): did learning happen at all?
From the training logs (lives logged every 20), the mean lifespan of training lives:

| brain | first 200,000 steps | last 200,000 steps |
|---|---|---|
| D3 | 171 (n = 461) | 204 (n = 391) |
| D2 | 167 (n = 474) | 196 (n = 414) |
| Dc | 203 (n = 393) | 243 (n = 330) |
| D3i | 169 (n = 470) | 210 (n = 377) |

- Learning happened, but very little in 2,000,000 steps (about 10,000 lives per run).
- This is a real "too slow", not a frozen-code fault: the checks passed, and training moved in the right direction.

## What it means (the assistant's reading)
- **The weak point is learning to act from sparse, delayed reward alone,** not the hunger-to-food link.
  - Even D3i, given the right link, died as fast as the others. A starting brain that must learn every step of a
    3,000-step life from its feelings alone, with a slow actor-critic, does not get there in 10,000 lives.
- **This is the same weakness Mind Lab met in the box world on 14–15 November** (WC, WM). Slow learning from reward
  could not undo or build habits in time.
- **The parts that helped there are the natural next candidates here:**
  - learning strongly from a surprising success, such as eating when hungry (WY's "that worked!");
  - a fast memory of where food and the shelter were, used at once and replayed to the slow network (WF);
  - the map memory already exists, and Script shows it is enough when it is used.
- **Curiosity does its job** (exploring), but exploring without a way to turn found food into a lasting habit does
  not keep a body alive.

## Next (needs the creator's OK; not started)
- **W3b:** the same world and drives, with WY's and WF's parts added (a surprising-success copy and a fast store with
  nightly replay), compared with W3's D3, on the cloud.
