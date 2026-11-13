# W1e: a planner that cannot cut corners, and a check of its read-out (frozen plan)

**Frozen** as git tag `W1e-frozen` (Mind Lab), before any training.
**Sign-off:** the creator, 12 November 2026: "alr good keep working we gotta build good basic starting brain to put into
acl".
**Draft:** `../W1e_draft.md`. **Council:** GPT (chat 6af67561) and Gemini (chat bdf93b50).

## The council, in short
- **Both:** a fair inductive bias (the movement graph, not a hard-coded policy). Keep the reward filter 3 × 3, so only
  the propagation changes.
- **Both raised the read-out:** a good value map does not guarantee good moves. The action head may ignore small
  differences at a fork, or ties may pick the long way.
- **GPT:** an oracle check, local decision accuracy, ties and margins, and paired longer training. Probabilities: the
  plus matters 65%; V+ looks ahead at 30,000 30%; at 150,000 50%.
- **Gemini:** a parameter-free read-out (step to the neighbour with the best learned value), the margin at the fork,
  and horizon attenuation. Its probabilities were truncated in the page.

## The brains (W1d's code and settings; imitating B)
| brain | | seeds | episodes |
|---|---|---|---|
| **V** | W1d's VIN (3 × 3 propagation filter), retrained (it also checks that W1d replicates exactly) | 1–16 | 30,000 |
| **V+** | the same, with the propagation filter masked to a plus: the cell and its 4 neighbours learned, the 4 diagonals fixed at 0 | 1–16 | 30,000 |
| **V, V+ (long)** | as above | 1–8 | 150,000 |

## Measures (W1b's test set and W1c/W1d's probes, unchanged), plus three read-out diagnostics
1. **The map read-out:** the brain's own trained network decides the map, but each move goes to the open neighbour
   with the highest learned value v (no action head). The main measures are reported for it too.
2. **Step accuracy:** on detour layouts, the share of the brain's steps that shorten the true BFS distance by one.
3. **Near-ties:** on detour layouts, the gap between the two best action scores at each step. Reported are its mean
   and the share of steps where it is below 0.05.

## Readings (frozen; W1b's rules)
- **"The plus matters"** if V+ − V on efficient detour (30,000 episodes) has a lower bound above 0 (paired by seed;
  10,000 draws; NumPy seed 20261121).
- **"Looks ahead"** for V+ (and V) by W1b's rule, at 30,000 (16 seeds) and at 150,000 (8 seeds, secondary).
- **"The read-out is the bottleneck"** (descriptive) if the map read-out's efficient detour is above the trained head's
  by more than 0.10 for V+.
- **Replication:** V's 30,000-episode results must equal W1d's for every seed. If they do not, the reason is stated
  before anything is read.

## The assistant's prior
- The plus matters: about 60%.
- V+ looks ahead at 30,000: about 20%; at 150,000: about 40%.
- The read-out is the bottleneck: about 45%.
