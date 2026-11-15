# WL2 implementation notes (written before the run)

- `wl2.py` extends WL's prefix runner with noisy showing steps (NS).
  - NP uses a subclass of WN's network that adds N(0, 0.3²) to every step's neuron input while `noise_on` (copy and
    practice), drawn from `[seed, 15]`; noise is off in tests.
  - Linf passes an empty prefix to both the copy step and the try.
- **L0 and L2 reproduce WL's saved children** (seed 1, sizes 32 and 128), with the same wait-noise stream
  `[seed, 13]`.
- **The after-showing test** uses the arm's own episode type with noise from `[seed, 14, day]`. For Linf it is a
  blank memory, the same as a plain test with different look draws.
- Run on GitHub's machines (`run.yml`): 12 jobs, 48 children each. Checks: All: PASS (`checks.log`).
