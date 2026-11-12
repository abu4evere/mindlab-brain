# W1b: the detour, seen. Findings (11 November 2026)

**Status:** valid. All six negative controls fail "looks ahead" and the planner B passes, so the test separates
looking ahead from rule-based shortcuts. (W1 could not.)

## The controls
- **The rule-based shortcuts take the efficient route on at most about half the detours:**
  - "walk to the wall, then head for the nearer end" (H1) 0.54;
  - the endpoint-distance rule (H2) 0.53;
  - the wall-followers 0.23–0.28;
  - memory without planning (M−) 0.23.
- **On pocket detours, none manages more than 0.31.**
- **B (BFS on the map it sees):** 1.00 everywhere.

## The learning brains: none learned to navigate at all
| brain | efficient detour | control layouts solved | first 3 moves right | reading |
|---|---|---|---|---|
| F (actor-critic) | 0.000 | 0.014 | 0.118 | mixed |
| R (actor-critic, memory) | 0.001 | 0.037 | 0.070 | mixed |
| F-imit (imitating B) | 0.000 | 0.084 | 0.242 | mixed |

- **"Mixed" here means they failed even the easy (control) layouts.** So W1b says nothing about whether they look
  ahead. They did not learn to walk to visible food in 30,000 episodes.
- **Actor-critic did not learn at all:** F's training success stayed at about 8%, the level of random moves.
- **A diagnostic after the data** (exploratory, labelled; one F-imit seed retrained with its accuracy logged) showed
  it is not a bug. Matching the planner's moves rose from 0.25 (chance) to 0.61 on learning layouts and 0.43 on new
  ones by episode 30,000, still rising. The flat network learns, but far too slowly to plan routes in this budget.

## What it means (the assistant's reading)
1. **The kind of brain ACL's people have** (a flat feed-forward network learning from one reward) **cannot even learn
   to walk to food it can see** in an 11 × 11 room, in 30,000 tries. It has no sense of space: every cell is a
   separate input, and nothing tells it that "food to my right" means the same anywhere.
2. **This matches ACL:**
   - NB2's network alone died within a year;
   - NB3's garden (the network alone) died within a year;
   - NB3's people starve. The old hand-written instincts carry all the navigation and foraging.
3. **The missing part is spatial structure**, as Gemini warned in the council. The candidates are:
   - an egocentric view (the world as seen from the agent, so "toward the food" is the same input everywhere);
   - a convolutional front-end (the same small filter applied everywhere);
   - or a learned map with a planner (M in W1, which worked).
4. **Next on the workbench:** W1c, the same frozen test with an egocentric and a convolutional brain, and with the
   learned-map planner. It asks which brain part lets a network learn to navigate and then to detour.
