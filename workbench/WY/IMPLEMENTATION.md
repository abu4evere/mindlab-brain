# WY implementation notes (written before the run)

- `wy.py` uses WM's `try_box` (with TB's blocking for TBYS, including WM's correction 1) and WS's copy and learning.
  Base reproduces WC's M128 and M32 children exactly (checked).
- **YS:**
  - after each practice try, the lids that opened are copied from the child's own acts, through the try's memory
    steps, at LR × 1.0, each lid weighted by 1 − e (its expectation from before the try);
  - e is per kind and lid and is updated for every lid tried.
- **Seen in the checks (a property of WS's learning rule, kept as frozen):** every learning step is clipped to a
  gradient length of 1 (WS's CLIP).
  - So the surprise weight shrinks a step only when the step would be small anyway. Weights 0.3 and 1.0 moved one
    test act by +0.0169 and +0.0171.
  - In practice YS gives a near full-size step on most surprising successes, about twice a showing's copy step
    (rate 0.5).
- **TBYS − TB** uses WM's TB children (the same seeds; TB's parts are the same code).
- Run on GitHub's machines (`run.yml`): 6 jobs of 48 children. Checks: All: PASS (`checks.log`).
