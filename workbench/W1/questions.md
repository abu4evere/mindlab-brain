# W1: the detour. Can a brain step away from its goal to reach it? (frozen plan)

**Frozen** as git tag `W1-frozen` (Mind Lab's local repository), before any code or data.
**Sign-off:** the creator's standing go-ahead ("do not ask me go ahead bro"; "keep working on project", 11 November
2026).
**Draft and council:** `../W1_detour_draft.md`; `../W1_council_after_2026-11-11.md` (GPT, Gemini). All their changes
are taken.

## The world
- **An 11 × 11 open area inside a border wall.** One agent, one food.
- **Moves:** north, south, east, west, or stay. An episode ends at the food, or after 60 steps.
- **What the agent sees:**
  - a 5 × 5 window around itself, with two channels (wall, food);
  - **smell:** the food's offset (dx, dy) ÷ 10. It knows where the food is, but not what walls lie between.
- **Reward** (for the learning brains): +1 at the food, −0.01 per step.

## The layouts (generated from a fixed seed, 20261115, before any brain runs)
- **A layout is a "detour" layout** if no path from the start to the food keeps the Manhattan distance from ever
  growing (checked by search). Otherwise it is a "control" layout.
- **Every layout is solvable within 60 steps.** Its shortest path is at most 30 steps.
- **Wall families:**
  - **learning:** U-shapes (cups opening away from the agent), L-shapes, straight bars;
  - **a third of the detour layouts carry a dead-end pocket:** a short branch off the wall on the side facing the
    agent, where wall-following loses steps;
  - **test only (unseen topologies):** double walls with offset gaps; a C-shape with an inner pocket; a U inside a
    larger U.
- **The sets:**
  - learning: 400 layouts (200 detour, 200 control);
  - test: 240 layouts. 120 detour: 40 of the learning families in new places and sizes, 40 with pockets, 40 of the
    test-only topologies. 120 control: the same walls turned or placed so a direct path exists.

## The brains
| brain | what it is | role |
|---|---|---|
| **G** | greedy: step to the open neighbour nearest the food (stay if none is nearer) | negative control |
| **W** | wall-follower (the "bug" algorithm): greedy until blocked, then follow the wall with the left hand until it is nearer the food than where it was blocked | negative control for "looks ahead" |
| **B** | breadth-first search on the true map | positive control |
| **M** | remembers every cell it has seen (wall, open, unknown) and replans a shortest path each step by BFS on that map, treating unknown cells as open (optimistic) | **engineered planning on a map it builds itself** |
| **M−** | the same map, but no planning: it steps to the neighbour nearest the food that it has not visited, else any not visited, else any open | ablation of M's planner |
| **F** | a feed-forward network: 52 inputs → 32 tanh → 5 action scores and a value; actor-critic | the kind of brain ACL's people have |
| **R** | F with an Elman memory of 32 units (backprop through the episode, truncated at 16 steps) | adds memory |
| **F-imit** | F's network trained to imitate B's actions on B's paths (same inputs as F) | separates "actor-critic failed" from "this kind of brain cannot" |

- **Learning brains (F, R, F-imit):** 16 seeds each, 30,000 learning episodes on the 400 learning layouts (drawn at
  random), learning rate 0.01 (plain gradient steps, gradient norm clipped at 1.0), γ 0.97, entropy bonus 0.01.
  Nothing is tuned after a first look.
- **Scripted brains (G, W, B, M, M−):** run once each; they draw nothing at random.
- **The test:** every brain runs every test layout once; the learning brains greedily (the arg-max action), learning
  off.

## Measures
- **Detour success:** the share of the 120 detour layouts reached within 60 steps. Also by family (learning shapes,
  pockets, unseen topologies).
- **Control success:** the same on the 120 control layouts.
- **Path ratio:** steps taken ÷ shortest path, on solved detour layouts (median).

## Readings (frozen)
- **"Looks ahead"** needs all of:
  - detour success ≥ 0.80;
  - success on the pocket layouts ≥ 0.70;
  - median path ratio on solved detours ≤ 1.5;
  - detour success above G's (for learning brains, the lower bound of the difference over seeds is above 0).
- **"Reactive"** if control success ≥ 0.80 but detour success ≤ 0.50.
- **"Neither"** otherwise; reported with every measure.
- **Valid only if** B "looks ahead" and both G and W do not. If W passes, the test cannot tell wall-following from
  looking ahead, and nothing is concluded.
- **For the learning brains:** per-seed values; 95% bootstrap intervals over the 16 seeds (10,000 draws, NumPy seed
  20261115). A brain meets a threshold if its mean does.
- **F-imit:**
  - if it "looks ahead" while F does not, F's failure is in actor-critic learning;
  - if F-imit also fails, this kind of brain (no memory, a 5 × 5 view) cannot.
- **M** is labelled "engineered planning on a learned map". It does not show learned planning.

## The assistant's prior
- G reactive, W fails the pockets or the path bound, B passes: about 90% each.
- F reactive: about 70%. R looks ahead: about 25%. F-imit looks ahead: about 15%.
- M looks ahead: about 85%. M− looks ahead: about 20%.
- GPT: F reactive 70%, R 30%, M 65%. Gemini: F 70%, R 35%, M 65%.
