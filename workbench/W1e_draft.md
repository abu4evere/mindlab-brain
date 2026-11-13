# W1e: a planner that cannot cut corners. Does it take the short way round? (DRAFT)

**Why:**
- In W1d the value iteration network (V) learned a planner-like value map (0.71 correlation with true distance; 0.83
  for one seed trained 150,000 episodes), but took the efficient detour only 0.15 (0.25 at 150,000).
- **A likely structural cause:** V's propagation filter is 3 × 3, so value spreads diagonally and can cut across a
  wall's corner. The agent moves only in 4 directions. The map is therefore wrong exactly at a barrier's ends, where
  the short-way choice is made.
- **The fix is one line:** the propagation filter (the one applied to v) is plus-shaped: the cell itself and its 4
  neighbours, with the diagonals fixed at 0. Everything else is W1d's.

## Kept from W1b, W1c, W1d (unchanged)
The world, the layouts, the controls, the probes (empty rooms, held-out shapes, moving food), the measures and the
readings. W1d's V (16 seeds, 30,000 episodes) is the paired reference: the same seeds, unchanged.

## The new brain
- **V+:** W1d's V with the v-propagation filter masked to a plus (5 of 9 weights learned; the 4 diagonals always
  0). Imitating B. 16 seeds, 30,000 episodes.
- **Secondary:** V+ at 150,000 episodes, 8 seeds; and V at 150,000, 8 seeds (W1d had only one exploratory seed).

## Readings (to be frozen)
- **"The plus matters"** if V+ − V on efficient detour has a lower bound above 0 (paired by seed).
- **"Looks ahead"** by W1b's rule, for V+.
- The value-map correlation, the K sweep and the moving food, as W1d's.

## Open questions for the council
1. Is masking the diagonals fair, or is it "telling" the brain how it moves (engineering)?
2. Should the reward-map filter be plus-shaped too?
3. Anything else that could explain W1d's gap (the read-out, ties, the greedy action)?

## The assistant's prior
- The plus matters: about 65%.
- V+ looks ahead at 30,000: about 25%; at 150,000: about 45%.
