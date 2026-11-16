# W3e implementation notes (written before the run)

- **`w3e.py` builds `train_net_gen` from W3b's `train_net` source,** with one anchored insertion (checked once) plus the
  name. While the parent is present (W3d's fading childhood), on every 4th step the parent's argmax act on the
  child's (map, levels, cell) is copied with W3b's `imitate`. The recipe parts are on (Y + FR).
- **The parent's act is computed only on copy steps;** a fixed net needs no per-step state.
- **The parents:**
  - G2: W3d's `PYFR_<seed>.npz`;
  - G3: W3e's `G2_<seed>.npz`, so G2's outputs are committed before stage 2 is dispatched.
  - The parent net is the ungated D3 class, as W3d's children were trained.
- **Fidelity:** the parent (sampled, learning off) lives on test lands 900001–900010, and every 10th step's state is
  recorded. The child's argmax is compared with the parent's argmax on those states; W3's D3 of the same seed is the
  baseline.
- **The thread count is set to 1 before numpy is imported** (WG2's lesson).
- Cloud: 8 jobs per stage; `manage_w3e.py` (W3b's manager with W3e paths) resumes paused runs. Checks: All: PASS (8).
