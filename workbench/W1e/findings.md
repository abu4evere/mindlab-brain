# W1e: a planner that cannot cut corners. Findings (12 November 2026)

**Status:** valid (code checks pass; all 48 runs present; V replicates W1d exactly, seed by seed).

## The frozen readings
- **The plus matters (30,000 episodes): no.** V+ − V on efficient detour +0.020 [−0.029, +0.067].
- **Looks ahead: no brain.** At 30,000: V mixed (0.15), V+ reactive (control 0.82, efficient detour 0.17).
  At 150,000: both reactive by W1b's rule (control ≥ 0.80, efficient detour ≤ 0.60).
- **The read-out is the bottleneck: no.** For V+ the map read-out beats the trained head by only +0.058 (30,000) and
  +0.031 (150,000), below the 0.10 line.

## The secondary run (150,000 episodes, 8 seeds; frozen as secondary)
| | V | V+ | V+ − V |
|---|---|---|---|
| efficient detour | 0.35 | **0.54** | **+0.19 [+0.09, +0.30]** |
| pocket | 0.20 | 0.28 | +0.09 [−0.03, +0.23] |
| control | 0.86 | 0.94 | +0.08 [+0.06, +0.11] |
| empty room | 0.93 | 0.99 | +0.07 |
| moving food | 0.62 | 0.78 | +0.16 [+0.11, +0.21] |
| value-map correlation | 0.73 | **0.88** | +0.15 [+0.03, +0.29] |

## What it means (the assistant's reading)
1. **The plus is right, but it pays only with training.** At 30,000 episodes the brains are too young for the
   difference to show. At 150,000, V+ has a much truer map (0.88 against 0.73) and takes the short way round
   0.54 of the time against 0.35. Diagonal leaks were part of W1d's gap.
2. **Training is the biggest lever.** V+ rose from 0.17 to 0.54 between 30,000 and 150,000 episodes, and still
   rising. "Reactive" by W1b's rule at 0.54 is the rule's band (≤ 0.60), not reflex behaviour: greedy scores 0 on
   these layouts.
3. **The read-out is fine.** Walking straight down the learned value map does no better than the head. What limits
   the brain is the map's precision at barrier ends, not how it reads it.
4. **For the starting brain:** the planner part is V+ (plus-shaped), trained at least 150,000 episodes. W2 uses it.

## Next
- **Exploratory (labelled, after the data):** V+ at 500,000 episodes, 4 seeds, to see where training levels off.
- **W2** (partial view plus remembered map) uses V+ as its planner; draft updated.
