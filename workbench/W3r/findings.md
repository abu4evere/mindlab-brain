# W3r findings: learning what colours DO within one life — a real gain (final; recomputed blind)

Frozen plan: `questions.md` (tag W3r-frozen; the creator's sign-off 24 Nov 2026). Runs: 80 (5 arms x 16 seeds): seeds
1-11 on the Oracle VM, 12-16 on the Google VM (each machine's runs paired on that machine), 0 failures; finished
26 Nov 2026 (Google's last run, HR 16, confirmed from run_HR_16.out: the queue log never records the last run). Finish
(`finish_w3r.sh`: download, merge, probe, frozen analysis) run on the second computer (Windows, Python 3.12.10, numpy
2.5.3). Every number below is from `analysis.md` / `analysis.json` (the frozen `analyse_w3r.py`) or `probe.json`.

## The primary reading
**RMS − RVS, fresh-land survival of the kept copy: +0.647 [+0.578, +0.714] -> a real gain; 16 of 16 seeds above 0.**
RVS 0.211 [0.164, 0.268]; **RMS 0.859 [0.819, 0.894]**; HRS (the ceiling, true kinds) 0.885 [0.860, 0.907].
When the colours of wall, food and shelter are dealt anew on each land, the brain that learns within its life what
each colour does (from blocked, fed, rested) survives full lives about as often as the brain told the true kinds.

## Secondary readings (95% bootstrap over seeds)
- **The sham:** RMS − RMXS +0.376 [+0.291, +0.469] (RMXS 0.482): the gain comes from crediting the right cell, not from
  having an extra learned layer (an extra layer alone helps somewhat: RMXS − RVS is about +0.27).
- **The borrowed learner:** RE5S − RVS +0.562 [+0.500, +0.620] (RE5S 0.774): Plan2Explore's ensemble works too, a
  little below the table.
- **The gap left:** RMS − HRS −0.026 [−0.068, +0.010]: not separable from the ceiling.
- **Lifespan (test lands):** RMS − RVS +1443 [+1282, +1597] steps.
- **Bare (both reflexes off):** RMS-bare − RVS-bare +0.271 [+0.217, +0.326] (RMS-bare 0.274, HRS-bare 0.396): without
  the body's reflexes the gain remains.
- **The module itself:** "fed" ranks the food colour first after the first meal in 0.996 of RMS's fresh lives (mean
  step 25); RMXS 0.886 (step 95); RE5S 0.985 (step 31).
- **The learning curve** (`probe.json`, mean over 16 seeds; toward food alone, chance 0.29): RM 0.41 before any meal,
  **0.85 after one meal** and after 3 and 5 (HR 0.86): one meal is enough. (RMX's probe, 0.81 after one meal, does not
  separate it from RM: the probe writes a fixed history straight into the table, bypassing the sham's random credit.)

## A failure, stated plainly: meanings are not revised
**The mid-life swap** (from step 1,500 the wall and food colours are exchanged, test only): RMS-midswap − RMS
−0.609 [−0.642, −0.575] (RMS-midswap 0.250, about RV's level; RVS is unaffected: +0.003). The plan expected RM to
recover after a few meals; it does not. The table only adds counts (positives / (positives + fair negatives) over the
whole life), so a meaning learned in the first half outweighs the new evidence for the rest of the life. Learning
a meaning works; **revising** one does not yet. This is exactly the third criterion GPT set for G1 ("can still revise
a meaning when the world changes").

## The blind recompute (`recompute_w3r_blind.md`)
A fresh subagent that saw only the 80 raw files test_fresh_{RVS,RMS,RMXS,RE5S,HRS}_{1..16}.json and the plan's
definitions: **primary +0.6475 [+0.5775, +0.7137], 16/16 seeds** — the same as the frozen analysis (rounded); every
survival secondary the same (RMS − RMXS +0.376 [+0.291, +0.469]; RE5S − RVS +0.562 [+0.500, +0.620]; RMS − HRS
−0.026 [−0.068, +0.010]). Its lifespan difference (+1342 [+1150, +1525]) is on the fresh lands, as the prompt asked;
the frozen analysis reports lifespan on the test lands (+1443): the same quantity on a different set of lands, not a
disagreement. It noted RMXS seed 15 (0.10) and that RMS − HRS comes mostly from seeds 6 and 16.

## Still to do
- **The Bob Profile on the kept copies** (amendments 5-6: does learning meanings cost any earlier ability?): Oracle's
  352 tests are done, Google's 160 are finishing; read as a secondary when complete.
- A preliminary look at Oracle's seeds 1-11 was taken on 26 Nov at the creator's request and logged (it did not
  change any file or the frozen analysis).

## What it means for Bob
Bob can now learn, within one life and from his own body, what the things around him mean, and it is enough to live
almost as well as if he had been told: the first rung of grounding meaning in experience. The next limit is shown
just as clearly: what he has learned, he cannot unlearn when the world changes. That points straight at G1 (grow and
protect, and still revise) and at the consequence models of Body v1's step 2 (CW1), which should forget or weigh
recent evidence.

## Addendum (26 Nov 2026, 20:00 EST): the Bob Profile on the kept copies (amendments 5-6), all 16 seeds
All 512 tests ran (Oracle 352, Google 160; 0 errors); scored with scorecard/bp/bp_score.py unchanged (its controls from scorecard/bp/output), results in bp_output/.

| arm | Learning | Reasoning | Memory | Generalization | Autonomy | total |
|---|---|---|---|---|---|---|
| RMS | 2 | 0 | 0 | 2 | 2 | **6** |
| HRrS (W3r's rerun of HR, the comparison) | 2 | 0 | 0 | 2 | 2 | **6** |
| RE5S | 2 | 0 | 0 | 2 | 0 | 4 |
| RMXS | 0 | 0 | 0 | 2 | 2 | 4 |

**No regression: learning meanings costs no earlier ability.** RMS vs HRrS, test by test (means): Learning 2 0.90 vs 0.93; Reasoning 2 (detours) 0.26 vs 0.27; Memory 2 0.82 vs 0.82 (fails its 0.80 lower-bound rule in both); Generalization 2 0.82 vs 0.83; Autonomy 2 0.80 vs 0.80; Autonomy 5 (bare survival) 0.27 vs 0.40 (both fail the 0.50 bar). The sham loses Learning 2 (0.56) and RE5 loses Autonomy 2 (tracks 0.25). Note: W3r's brains score 6, below W3p's MBb (10), which solved detours with its bump lessons; W3r did not use them.
