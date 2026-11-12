# W1d: thinking ahead. Does an iterative planning layer let a network take the short way round? (DRAFT)

**Why:**
- W1c: a convolutional network learns to navigate (0.73 on control layouts by imitation; 0.95 in empty rooms from
  reward at 100,000 episodes), but takes the short way round a barrier only about a third of the time, and almost
  never escapes a pocket.
- Perception is not planning. Planning means propagating "how far is the food from here" across the whole map,
  several steps, before acting.
- A **value iteration network** (VIN; Tamar et al. 2016) does this inside the network. A learned reward map, then a
  small convolution applied K times, with a max over action channels each time, spreads value outward from the goal.
  Everything is learned.

## Kept from W1b and W1c (unchanged)
- W1b's world, its 400 learning and 240 test layouts, its scripted controls and their results, its measures and
  readings.
- W1c's probe sets (empty rooms; held-out topologies).
- W1c's C-imit as the reference (convolution, no iteration).

## The new brains
| brain | what | learning |
|---|---|---|
| **V** | VIN on the 11 × 11 map (channels: walls, food): reward map r = 3 × 3 conv of the input; then K = 30 times: q = 3 × 3 conv of r + 3 × 3 conv of v (8 channels), v = max over channels; the agent's cell's q (8 numbers) → 5 action scores (+ value) | imitating B |
| **V1** | V with K = 1 (no iteration) | imitating B (the ablation: does iterating matter?) |
| **V-ac** | V | actor-critic |

- **Settings:** 16 seeds, 30,000 episodes, learning rate 0.01, clip 1.0, as before.
- **100,000-episode check:** V-ac, 4 seeds.

## Questions (readings as W1b's)
1. Does V "look ahead" (efficient detour ≥ 0.80, pocket ≥ 0.70, above G)?
2. Does iterating matter (V − V1 on efficient detour)?
3. Does V-ac learn it from reward alone?
4. Does it carry over to the held-out topologies?

## Open questions for the council
1. Is K = 30 fair (the longest shortest path is 30)?
2. Is the VIN's planning "engineered" (the max over channels is built in) or learned?
3. What would show it plans rather than memorises?

## The assistant's prior
- V looks ahead: about 55%.
- V − V1 above 0: about 80%.
- V-ac navigates at 30,000: about 25%.
