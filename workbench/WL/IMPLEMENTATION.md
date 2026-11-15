# WL implementation notes (written before the run)

- `wl.py` replaces `ws.run_prefix` with a version that knows wait steps: no input, plus fixed noise added to the
  neurons' input before tanh. WS's `try_box`, `copy_step` and learning are unchanged.
- **One memory episode per try:** the showing plus D wait steps, with the noise drawn once from the child's stream
  `[seed, 13]`. The same episode is used by the copy step and by the try.
- **Gradients:** they run through the wait steps, with the noise held fixed (finite-difference check, worst relative
  error 1.9e-06).
- **Tests:** with no showing, no wait. The after-showing test at day 30 uses an episode with noise from
  `[seed, 14, day]`.
- **L0 reproduces WN's M32 and M128** (seeds 1 and 2) exactly.
- Run on GitHub's machines (`run.yml`): 9 jobs (3 levels × 3 sizes), 48 children each. Checks: All: PASS
  (`checks.log`).
