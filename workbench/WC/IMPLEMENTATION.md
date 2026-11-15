# WC implementation notes (written before the run)

- `wc.py` builds on WT's world (`../WT/wt.py`, p = 0.5) and WE's evolution. With no change it reproduces WT's child
  (p = 0.5) and WE's child (p = 1) exactly (checked).
- **The change:** the codes in `home.pairs` are replaced at the start of day 31 (kinds 0–2) and day 46 (kinds 3–5),
  before that day's tries. New codes are drawn once per world from `[seed, 8]` by rejection: each lid differs from its
  old pair, and a kind's two lids differ.
- **Tests:** after the day's practice and before any growth step, one try per kind with WS's test look draws
  `[seed, 6, day, 0]` and no showing.
  - Success = both lids.
  - Stale = the first lid's chosen pair equals the old first-lid pair, on changed kinds only.
- **T1 and T2:** WT's p = 0.5 evolved schedules, read from `../WT/evolved_p50.json` (day keys turned into integers).
- Run: one process at Idle (W3 uses 4): evolution runs 1 and 2, then the final test, then the analysis.
  Checks: All: PASS (`checks.log`).
