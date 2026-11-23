# W3p-H: the detour result on lands never used before (plan, frozen as tag `W3p-heldout-frozen` before any run)

- **Why:** GPT (W3p council addendum, 22 Nov): the detour probe's 50 test lands shaped the design (pilot, diagnoses), so
  a win should be confirmed on new lands. The W3p preview (23 Nov): R2 detours MB 0.80, MBb 1.00, HR 0.27.
- **Labelled:** a confirmatory follow-up to W3p, not part of W3p's frozen readings.
- **Lands:** 200 lands, seeds 980001–980200, used by no study before (W3's test lands are 900001–050, fresh 910001–050,
  the Bob Profile's dense lands 940001+, W3q's probe 970001–200).
- **Tests:** the Bob Profile's own detour tests, unchanged (`scorecard/bp/bp_tests.py`, BP-frozen): R2 (food 5+ steps
  away behind a wall, a detour of 4+) and R5d (10+ and 10+); memory fully known, hungry, no reflex; the walk uses the
  brain's moves as in its life, up to 3 × the shortest path. Only the list of lands changes.
- **Brains:** the kept copies of W3p's MB and MBb and W3n's HR, seeds 1–8; controls: the Script, the greedy walker and
  random moves.
- **Readings (`heldout_w3p.py`, frozen):** success per arm; MB − HR and MBb − HR paired by seed, bootstrap over seeds
  (numpy seed 20261124, 10,000 resamples), 5th and 95th percentiles as in W3p. **Confirmed** if the lower bound of
  MB − HR (and, separately, MBb − HR) on R2 is above 0; MBb's R2 lower bound against the Bob Profile's 0.80 beside it.
- **Prior (the assistant):** MB − HR confirmed 90%; MBb − HR confirmed 95%; MBb's R2 lower bound at least 0.80: 85%.
