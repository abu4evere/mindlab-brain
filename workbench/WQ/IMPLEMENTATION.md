# WQ implementation notes (written before the run)

- **`Room`** subclasses W3's World:
  - the relocation schedule is emptied;
  - before each step energy is set to EMAX + 1, so after the step's cost it is EMAX and nothing is eaten (W3 eats
    only when energy < EMAX);
  - after the step, energy is set to 150 and fatigue to 0, so both needs are always 0, and death is cleared;
  - a stay ends at 10,000 steps.
- **Brains:** W3's `DriveVIN`, loaded from W3's (D2, D3, Dc) or W3c's (GYFR) saved weights.
  - GYFR was trained with the need gate. With both needs at 0 the gate is inert (g = 0), so the ungated class gives
    exactly its behaviour here.
- **Acting:** sampled from the policy, as in W3's tests, with a generator per (seed, room).
- **Living:** W3's A2C update every 64 steps, with W3's reward (only curiosity can be non-zero), through W3's own
  `reward` and `update`.
- **Activity** counts only steps that changed position (moving into a wall counts as staying).
- Run on GitHub's machines: 10 jobs. Checks: All: PASS (`checks.log`).
