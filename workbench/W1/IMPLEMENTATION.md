# W1: implementation readings (written before any run)

- **Layouts** (`world.py`, seed 20261115):
  - start and food are drawn among open cells, at least 4 apart;
  - a draw is kept only if it is solvable within 30 steps and its detour/control label is the one wanted;
  - **"Pocket" cups** carry their dead-end pocket (two parallel walls, 3–4 deep) on the outside of the cup's base. The
    plan's "the side facing the agent" is not forced: the label (detour) is.
  - Test-only shapes: offset double walls, a cup with an inner bar, nested cups.
- **Window:** cells outside the 11 × 11 area count as walls.
- **W (wall-follower):**
  - greedy along the larger axis first;
  - when blocked, it turns right and follows the wall with the left hand;
  - it leaves the wall when nearer the food than where it was blocked and a step toward the food is open.
- **M:** marks walls seen in its window; BFS on its own map each step (unknown = open).
- **M−:** the same map; steps to the unvisited neighbour nearest the food, else any unvisited, else the nearest.
- **Actor-critic:**
  - Monte Carlo returns per episode, advantage = return − value, value loss ½(v − R)², entropy bonus 0.01;
  - one update per episode, the gradient norm clipped at 1.0, learning rate 0.01;
  - **R's backprop through time is cut every 16 steps** (chunked truncation).
- **F-imit:** one update per episode on B's path: cross-entropy toward B's action, on F's own inputs.
- **The test:** the arg-max action; learning off; each layout once.
