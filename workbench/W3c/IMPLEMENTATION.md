# W3c implementation notes (written before the run)

- `w3c.py` reuses W3b's training loop, test, ceiling walker and step 0 (`../W3b/w3b.py`) unchanged. It swaps in a
  brain class (`GatedVIN`, a subclass of W3's DriveVIN) by setting `brains3.DriveVIN`, and points W3b's output folder
  at `W3c/output`.
- **The gate:** the reward map's level vector becomes (1 − g, s, f, c·(1 − g)), with g = max(s, f) per step. W3's
  backprop already scales each part by that vector, so gradients stay exact (checked by finite differences, worst
  relative error 3.1e-08).
- **Z0** sets W0 to zero at birth. **Gi** uses D3i's fixed links (`fixed_map=True`) with the gate.
- **Step 0c** runs W3b's `step0("D3i", seed)` with the gated class loading W3's saved D3i weights. Its hungry-step
  "contributions" log is computed by W3b's code without the gate, so it is not a reading here.
- **F2** extends W3b's FPolicy:
  - hungry (s ≥ 0.2): the shortest path to the nearest cell remembered as full;
  - tired (f ≥ 0.4): to the shelter;
  - otherwise W3's D3.
- **Cloud:** run.yml jobs (W3b's practice). Training runs pause near 4.5 hours, and `manage_w3c.py` (W3b's manager
  with W3c's paths) resumes them. Checks: All: PASS (`checks.log`).
