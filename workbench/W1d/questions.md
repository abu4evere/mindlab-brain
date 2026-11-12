# W1d: thinking ahead. Does an iterative planning layer let a network take the short way round? (frozen plan)

**Frozen** as git tag `W1d-frozen` (Mind Lab), before any training. The VIN code (`vin.py`) was written and
gradient-checked before the freeze.
**Sign-off:** the creator, 12 November 2026: "alr then keep working" (after agreeing that the brain is built in Mind
Lab).
**Draft:** `../W1d_draft.md`. **Council:** GPT (chat 6af5d2af) and Gemini (chat 74fdf4c2).

## The council, in short
- **Both:** a good next test, but success is "learned planning inside an engineered planning structure" (the max over
  channels is built in), not planning discovered from scratch.
- **Both asked:**
  - for a sweep of the number of iterations K;
  - for perturbation tests (move the food, change a wall);
  - for a check that value flows around walls, not through them.
- **Gemini also asked:**
  - for a control that iterates without the max, separating the planning-style update from a large receptive field;
  - for more seeds for the actor-critic check;
  - it also warned about learning through 30 unrolled steps.
- **GPT:** V looks ahead 60%, V − V1 85%, V-ac navigates at 30,000 30%. **Gemini:** 65%, 90%, 20%.
- **Not taken:**
  - a wall-masked VIN (it would build the walls in, which is more engineering);
  - a learning-rate search (W1b's settings are kept so all W tests compare).

## Kept from W1b and W1c (unchanged)
- W1b's world, its learning and test layouts, its scripted controls and their results, its measures, readings and
  validity;
- W1c's probe sets (empty rooms, held-out topologies);
- W1c's C-imit as the reference.

## The brains (16 seeds each unless stated; 30,000 episodes; W1b's settings)
| brain | what | learning |
|---|---|---|
| **V** | VIN on the 11 × 11 map: r = 3 × 3 conv of (walls, food) + bias; q = 3 × 3 conv of r (8 channels); then 29 times: v = max over channels of q, q = conv(r) + conv(v); the agent's cell's q → 5 action scores (+ value) | imitating B |
| **V1** | the same with K = 1 (no iteration) | imitating B |
| **Vm** | the same as V, but v = tanh(mean over channels of q) instead of the max (iterates, no planning-style max) | imitating B |
| **V-ac** | V | actor-critic |

- **The 100,000-episode check:** V-ac, 8 seeds (secondary).

## Probes and diagnostics (all pre-set; probes only, never learned from)
1. **W1c's empty rooms and held-out topologies.**
2. **The K sweep** (V only, at test time, no retraining): K = 1, 5, 10, 15, 20, 30 on the main test.
   - Reported against each layout's shortest path: does success rise once K reaches the path length?
3. **Moving food** (every brain): on the 120 detour test layouts, after the 3rd step the food moves to another open
   cell (at least 4 away; drawn from seed 20261119, the same for every brain).
   - **Success** = reaching the new food within 1.15 × the shortest path from where the agent was when it moved.
4. **The value map** (V, Vm, V1): on the test layouts, the Spearman correlation between the final v map and −(true BFS
   distance to the food) over reachable cells. High means value flows around walls, as a planner's should.

## Readings (frozen)
- **Per brain:** W1b's "looks ahead" / "reactive" / "mixed"; W1c's "navigates" (control ≥ 0.80 and empty room ≥
  0.90).
- **"Iteration matters"** if V − V1 on efficient detour has a lower bound above 0 (bootstrap over seeds, 10,000
  draws, NumPy seed 20261119).
- **"The max matters"** if V − Vm on efficient detour has a lower bound above 0.
- **Planning, not memory** (descriptive): the held-out topologies, the moving food, the K sweep and the value map, all
  reported beside the main readings.
- **Even a pass is learned planning in an engineered planning structure,** and behaviour, not proof of an inner
  look-ahead.

## The assistant's prior
- V looks ahead: about 55%.
- Iteration matters: about 80%.
- The max matters: about 60%.
- V-ac navigates at 30,000: about 20%; at 100,000: about 45%.
