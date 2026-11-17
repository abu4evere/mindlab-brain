# W3h implementation notes (written before the run)

- **`w3h.py` installs patches into W3's modules before training** (as W3g did):
  - `World` becomes `ThornWorld`: thorn patches from `[seed, 77]`, harm on thorn steps, a sixth `obs_map` channel
    (thorns seen), and the per-life counters;
  - `DriveVIN` becomes `ThornVIN`: its 6th channel starts at zero, and `row_norms` adds "thorn";
  - `MapView` becomes `ThornMapView`: the careful parent sees seen thorns as walls;
  - `life_measures` gains the thorn measures;
  - `run_w3.reward` subtracts pain (harm / 8) in the pain arms.
- **Training is W3d's `train_net_parent`** (fading childhood + Y + FR), with each arm named as itself. The training
  curve (thorn steps per 1,000 per 100,000-step block) is counted in the world. It is kept across cloud pauses in
  `output/<arm>_<seed>_curve_state.json`.
- **Calibration:** amendment 1 (questions.md), 2 patches, harm 6.
- **Checks:** All: PASS (11, `checks.log`).
  - The harm check first used a random walk that never reached a thorn (0 thorn steps, so it failed). It was fixed to
    walk toward thorns half the time, then passed with 53 thorn steps.
  - "No thorns reproduces W3d's PYFR" is allclose (1e-10), not bit-exact, as W3g's.
- **A smoke run** (3,000 steps, childhood 2,000, THPw, a temporary folder on D:) wrote the test, curve and norm files.
  It was deleted.
- **Cloud:** 32 jobs (4 arms × 8 seeds); `manage_w3h.py` (retries) resumes paused runs.
