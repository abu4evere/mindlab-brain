# W3: implementation notes (before any training data)

## The files
- **world3.py:** the land, the body, relocations, the 3 × 3 view, the map memory (the fixed writer), Script (reading
  only a `MapView` of the memory) and the per-life measures.
- **brains3.py:** `DriveVIN`, which is W2's MapVIN arithmetic on a 15 × 15, 5-channel map with the drive-weighted
  reward map. It includes the A2C update on 64-step segments (W1's actor-critic arithmetic).
- **run_w3.py:** calibration, training, tests and the reference brains.
- **checks_w3.py:** the frozen code checks (→ `checks.log`).
- **analyse_w3.py:** the frozen analysis.

## Choices where questions.md is silent (made before any data)
- **Test actions** are sampled from the learned policy (learning off). A fixed generator per test land is the same for
  every brain, as for Rand, so the brains face the same land, schedule and random draws.
  - Greedy actions were not chosen: a deterministic policy on a slowly changing map can loop forever.
- **Training lands** come from `1000·seed + life`, so seed numbers pair the brains' training lands.

## Pre-data corrections (no learned brain had been trained; calibration had not been run)
1. **Script, when hungry with no remembered food.**
   - **The fault:** as frozen, Script then waited until some cell reached u ≥ 0.5, and starved after relocations (a
     smoke test on scratch lands 700001+).
   - **The fix:** it now searches, going to the stalest reachable open cell.
   - It still reads only the map memory.
2. **Script's targets must be reachable.**
   - **The fault:** never-seen corner cells (border walls that can never come into view) stayed "never seen" with u = 1,
     and Script aimed at them forever.
   - **The fix:** every search target is now restricted to cells reachable on the map memory (unknown cells count as
     open).
   - With 1 and 2, Script survived 0.90–1.00 of 20 scratch lives at R = 200, 100 and 50. Scratch lands are neither
     calibration nor test lands.
3. **The step budget is cut from 2,000,000 to 800,000 per run, for every learned brain** (questions.md: "If the
   measured speed (before any data) means more than 14 hours, the step budget is cut to fit").
   - **The measured speed:** 7.4 ms per training step with 4 runs at once (6 cores; NumPy single-threaded).
   - 32 runs × 2,000,000 would take about 33 hours. 32 × 800,000 takes about 13 hours.
4. **Correction 3 is withdrawn: back to the frozen 2,000,000 steps.**
   - The creator, 13 November 2026 (about 15:03), in the Claude Code chat: "you can actually run full plan in needed 33
     hours in my pc thats fine".
   - The 800,000-step queue had run for about 5 minutes. It was stopped before any learned brain had finished or been
     tested. Only the reference brains (Rand and Script) had been tested, and their numbers are unaffected.
   - The queue was relaunched at 2,000,000 steps per run, the same for every brain.
