# W1: the detour. Can a brain step away from its goal to reach it? (DRAFT, not frozen)

**Why:**
- The scorecard's Part A #2 ("looking ahead") is one of the two tests to build first (scorecard council 1, Gemini).
- It is cheap. A short-term cost before a long-term payoff separates reactive agents from agents that look ahead.
- ACL's people starve with food in reach (NB3), and Cradle's child needed memory to keep up (C1). Both are about
  acting for what is not right in front of you.

## The task
- **A small grid world** (11 × 11). One agent, one piece of food. Walls are drawn from a family of shapes.
- **Detour layouts:** a U-shaped or L-shaped wall stands between the agent and the food, open on the far side. Every
  shortest path's first steps move *away* from the food (the straight-line distance grows), by 2 to 6 steps.
- **Control layouts:** the same walls, turned so that the shortest path never moves away from the food.
- **What the agent sees:** a 5 × 5 window around itself (walls, food) and the direction to the food (it can smell it,
  but not see past walls).
- **Moves:** 4 directions or stay. An episode ends at the food, or after 60 steps.
- **Layouts:**
  - 400 for learning;
  - 200 held out for the test (wall shapes and places never seen in learning);
  - each half detour, half control.

## The brains (each a "brain part" on the workbench)
| brain | what it is | role |
|---|---|---|
| **G** | greedy: step to whichever open cell is nearest the food | negative control (cannot detour by design) |
| **B** | breadth-first search on the true map | positive control (detours by design) |
| **F** | a feed-forward network on the window and direction, trained by actor-critic (as ACL's NB2) | the current ACL brain's kind |
| **R** | the same with an Elman memory (as Cradle C1's R) | adds memory |
| **M** | R plus a learned map: it marks cells it has seen as walls or open, and plans a path on its own map (BFS) when the path it has is blocked | "looks ahead" on a model it learned |

F, R and M learn on the 400 learning layouts for the same number of episodes, with 16 seeds per brain.

## Measures (on the 200 held-out layouts, learning off)
- **Success** on detour and on control layouts.
- **Detour cost:** extra steps over the shortest path.
- **The detour gap** (the primary measure): control success − detour success. A brain that looks ahead has a small
  gap. A reactive one has a large gap.

## Readings (to be frozen)
- **"Looks ahead"** if detour success ≥ 0.8, and the detour gap's upper bound < 0.1, and detour success is above G's.
- **"Reactive"** if control success ≥ 0.8 but the gap's lower bound > 0.2.
- **Valid only if** B passes "looks ahead" and G is "reactive" (the positive and negative controls work).

## Open questions for the council
1. Is the 5 × 5 window with smell a fair setup? Should M get the true map (no), or have to learn it (yes, as drafted)?
2. Is it fair that M's planner is hand-written (BFS) and only its map is learned?
3. What baseline would show that F's failure is about looking ahead, not about learning?

## The assistant's prior
- F reactive: about 75%.
- R looks ahead: about 20%.
- M looks ahead: about 80%.
