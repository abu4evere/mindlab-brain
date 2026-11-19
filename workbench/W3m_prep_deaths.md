# What still kills the best brains (a read of W3k's saved tests; 19 November 2026)

**Exploratory, read-only.** W3i's test (used by W3k) records WX's death labels for every test life, so no new runs were
needed: this reads `W3k/output/test_*.json` (16 seeds × 50 lives per arm). Labels can overlap (WX's definitions).

## Death labels (share of deaths, mean of seeds)
| brain | deaths per 50 | no food known | food known within 30 steps, not reached | exhaustion |
|---|---|---|---|---|
| W3d's PYFR (WX, cited) | 30–50 | **0.80** | 0.27 | 0.63 |
| W3k R2 | 29.6 | 0.50 | 0.67 | 0.68 |
| W3k **CS** (best) | 26.1 | 0.47 | **0.66** | **0.66** |
| W3k C3 | 28.6 | 0.47 | 0.65 | 0.68 |
(Fresh lands: the same picture, within 0.05.)

## CS: lives that die against lives that survive (all 800 test lives)
| | dying lives | surviving lives |
|---|---|---|
| share of steps exhausted (moving costs double) | **0.28** | **0.03** |
| share of steps hungry | 0.12 | 0.004 |
| steps since the last meal at the end | 144 | 34 |
| land known at the end | 0.90 | 1.00 |
- **47% of CS's deaths are both "exhausted" and "food known within 30 steps".** Median lifespan of a death: 504.

## The assistant's reading (for the next study's design)
- The longer childhood fixed most of the "no food known" problem (0.80 → 0.47). The brains now mostly **know where food
  is but arrive too tired to reach it**: tiredness doubles the cost of each move, and a tired brain starves near food.
- Surviving lives almost never get exhausted (3% of steps), as the Script (2%, WX). So **managing tiredness, resting
  before exhaustion**, is the main gap left toward the 0.80 bar.
- Candidates for W3m (to be drafted when W3l ends, then council): a parent that also shows resting (if the Script's rest
  is not already copied), a body signal of tiredness during development (as pain for harm), or tiredness in the drives.
