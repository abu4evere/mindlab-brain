# WE implementation notes (written before the run)

- `we.py` builds on WG (`../WG/wg.py`, "awake in" growth) and WN's network. The checks show that WG's GA schedule
  and M32 reproduce WG's saved seed-1 children exactly.
- **Rounding:** born size = round(2^a); final size = min(256, round(2^(a+g))); growth days round(s)..round(e).
  - At the end of each growth day the brain grows to n0 + round((final − n0) × days so far / days in the window),
    and only when that is larger.
  - A one-day window jumps straight to the final size.
- **Food** = the lids opened in the 18 practice tries a day (0–2 each), summed over 60 days (0–2160). The tests are not
  run during evolution, and they do not change learning.
- **Selection:** parents are drawn with replacement, in proportion to food + 1. The mutation draws come from the
  same stream as selection, `[run, 77]`.
- **The final test** (`final_we.py`) takes the median of each gene over the last generation, then the schedule.
- Run: one process at Idle (W3 already uses 4), evolution runs 1 then 2, then the final test. Checks: All: PASS
  (`checks.log`).
