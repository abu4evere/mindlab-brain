# Bob Profile baseline: W3n's HRS (the living brain), 21 November 2026

Tests: `BP-frozen` (bp_tests.py, bp_score.py), run 00:05–03:50 on 21 Nov, on the creator's PC. Brains: W3n's HR kept
copies, seeds 1, 2, 3, 5, 6, 7, 8, 9 (seed 4 still training). The scorer's output is `battery_done.txt` and
`output/profile_HR.md`; the raw files are in `output/`.

| Learning | Reasoning | Memory | Generalization | Autonomy | measured total |
|---|---|---|---|---|---|
| 2 | 0 | 0 | 2 | 2 | **6 / 100** |

- **Learning 2, pass.** Normalised lifespan on the test lands is 0.95 (lower bound 0.93): far above random (174 steps)
  and close to Script (2,963).
- **Reasoning 2, fail.** Detours behind a wall succeed 0.27 (lower bound 0.22; Script 1.00, greedy 0.00); long
  detours 0.11. This is the clearest weakness: the learned planner does not go round walls reliably.
- **Memory 2, fail, narrowly.** Returning to food seen 100 steps ago succeeds 0.80 on average, but the lower bound is
  0.69 (one seed 0.36). With the memory erased: 0.47. The brain uses its memory; it is not reliable enough.
  Memory 5 fails by construction: the brain has no learned memory of its own.
- **Generalization 2, pass.** On lands with twice the walls it keeps 0.81 of its standard lifespan (lower bound 0.77;
  Script 0.97).
- **Autonomy 2, pass.** Its first move follows the larger need (tracks 0.79, lower bound 0.67; Script 1.00, random
  −0.07). Only 7 lands qualify (the first steps toward food and the shelter differ). Source: the drives are ours, the
  weights learned.
- **Autonomy 5, fail.** Bare (no reflexes) fresh-land survival is 0.40 (lower bound 0.31; Script 0.94).

**Reading.** The assistant's opinion before measuring was about 13/100. The measured profile is 6/100: two abilities are
at 0. The creator's goal is 60 or more, with at least 10 in each ability. The first targets, in order:
1. **Detours (reasoning).** A learned "blocked here" map (Ishida and Henriques 2022), or more planning iterations and
   wall-aware value passing. This is also likely to lift memory 2, since reaching remembered food often needs a detour.
2. **A learned memory of its own** (memory 5).
3. **Surviving without the reflexes** (autonomy 5).
