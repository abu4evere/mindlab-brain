# W1b: implementation readings (written before any run)

- **Layouts** (`world_b.py`, seed 20261116):
  - the family is drawn first (each equally likely), then layouts of that family are drawn until one fits. An earlier
    build drew a layout from any family and retried the whole draw, which left pocket detours rare (3 in learning). It
    was rebuilt this way before any brain ran;
  - a pocket detour is kept only if the greedy walk ends in a dead end (3 or more walled sides), so the pocket is on
    the agent's side;
  - adversarial detours are kept only if at least one of W, W2, H1, H2 fails to solve them within 1.15 × the shortest
    path (checked in checks.log).
- **H1 and H2:**
  - the touched wall segment is the set of wall cells 8-connected to the blocking cell;
  - its two "ends" are the cells just past its extreme coordinates along the wall, in line with the blocking step;
  - H1 picks the end nearer to itself, H2 the end with the least (own distance + distance to the food), both
    straight-line;
  - then each follows the wall that way (W1's following and leaving rules).
- **W2:** after blocking, it turns toward the food's lateral side and follows the wall.
- **Learning:** W1's code (brains.py) with 363 inputs and 64 hidden units; settings as W1.
- **First-decision accuracy:** each of the first 3 moves shortens the true BFS distance by one.
