# W3i implementation notes (written before the run)

- **`w3i.py`:**
  - `StaleWorld` (W3's World plus two read-only counters: stale-food arrivals and the last meal) and its
    `life_measures`;
  - `configure(arm)` sets W3d's PYFR with the arm's fade;
  - `train_staged` runs W3d's `train_net_parent` and pauses at the first life boundary after each snapshot (L and
    LC: 2M, 4M), tests the snapshot, then continues. It is resumable through the checkpoint, as W3b's `train`;
  - `test_all` is W3's test with WX's death recorder (labels from the last 100 steps, as WX);
  - the fresh-land test uses seeds 910001–910050;
  - `repro` trains W3d's PYFR seed 1 with W3b's own `train` and compares the weights with `W3d/output/PYFR_1.npz`.
- **Checks: All: PASS** (8, `checks.log`):
  - the counters do not change the world;
  - the stale counter;
  - the fade per arm;
  - no step-scheduled learning rate or entropy;
  - split = unsplit;
  - the same seed twice;
  - a snapshot does not change the run;
  - the staged run equals W3d's plain loop.
- **The analysis:**
  - PYFR's reference numbers come from W3d's test files, and its death labels from WX's recorder (`WX/output`);
  - PYFR's stale arrivals were never measured, so the L and LC 2M snapshots stand in, labelled.
- **Cloud:** 25 jobs (L, LC, C × 8, and R). The 6M jobs need about 6.5 hours of training, so they pause and resume
  through `manage_w3i.py`.
