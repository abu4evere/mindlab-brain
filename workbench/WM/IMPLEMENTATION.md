# WM implementation notes (written before the run)

- `wm.py` copies WS's `try_box` and `copy_step` with three additions: a sampling temperature, blocked pairs and extra
  senses. With T = 1, no blocking and no extra senses, Base reproduces WC's M128 and M32 children exactly (checked).
- **Blocking (TB):** in practice tries only.
  - At the first step, a first act is blocked when all four of its pairs are listed.
  - At the second step, a second act is blocked when (first act, it) is listed.
  - A lid's list clears when that lid opens.
  - Only lids actually tried are listed (a try ends at the first wrong lid).
- **Surprise (SU):** e and u are per kind, updated after each practice try from the lids opened / 2. The temperature
  and the learning-step factor use u from before the try. The copy step is not scaled.
- **LSi:** 10 more inputs (acts tried on this lid last time, and the result).
  - The new input columns are drawn from `[seed, 12]`; the base 29 columns are the base network's.
  - The showing steps get zeros for the new inputs.
  - The test sees the child's last practice try (part of its senses).
- **Tests:** greedy, with no blocking and no temperature.
- Run on GitHub's machines (`run.yml`): one job per arm and size (10 jobs), each running 48 children.
  Checks: All: PASS (`checks.log`).

## Correction 1 (14 November 2026, before any TB or SUTB data was seen)
- **What happened:** the first cloud run of TB and SUTB crashed. All 4 jobs failed with "Probabilities contain NaN".
  - A pair that failed under a lid's old code stays listed. After the change it can be exactly the new right pair.
  - Once every other pair failed too, all 16 were blocked.
- **The frozen plan did not say** what happens when every pair is listed.
- **Fix:** when all 16 pairs of a lid are listed, the list clears and the search starts again.
- **A new check** runs TB through 12 full lives without the problem.
- Base, SU and LSi are unchanged and their cloud results stand; they were downloaded but not looked at before this fix.
- The partial TB and SUTB files (12 children) were deleted unread, and those 4 jobs were run again.
