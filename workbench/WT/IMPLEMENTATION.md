# WT implementation notes (written before the run)

- `wt.py` is WE's `run_child` with one change: on days 1–30, the teacher's presence on each try comes from the world
  (`[seed, 5, day]`, 18 draws, present if below p).
  - When the teacher is absent: no showing prefix and no copy step.
  - With p = 1 it reproduces WE's child exactly (checked).
- Evolution and the final test reuse WE's genes, schedule, clamping, mutation and selection. The evolution seed is
  `[run, 77, P]`.
- Run: one process at Idle (W3 already uses 4). Order: p50 runs 1 and 2, p20 runs 1 and 2, the final tests, then
  the analysis. Checks: All: PASS (`checks.log`).
