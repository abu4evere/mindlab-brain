# W1b: the detour, seen. Does a brain take the short way round a barrier it can see? (frozen plan)

**Frozen** as git tag `W1b-frozen` (Mind Lab), before any code or data.
**Sign-off:** the creator, 11 November 2026: "alr bro go ahead".
**History:**
- W1 was not valid: a wall-follower passed (`../W1/findings.md`);
- draft: `../W1b_detour_draft.md`;
- council: GPT (chat 6af52a25) and Gemini (chat 461e0f74), below. All the changes they asked for are taken.

## The council, in short
- **Both:** a full view is right (it separates planning from exploration). But a rule that uses the visible geometry
  without any search could still pass: "walk toward the food until blocked, then head for the nearer end of the wall"
  (Gemini), or "go to the wall end that looks closer to the food" (GPT). So both are added as negative controls, with
  layouts where the nearer end is a trap.
- **GPT:** report first-decision accuracy, report the families separately, and require every heuristic to fail. GPT
  probabilities: F reactive 65%, F looks ahead 25%, R 30%, F-imit 55%.
- **Gemini:**
  - tighten the bound to 1.15 × the shortest path, with pockets at least 3 deep;
  - put every wall family in learning (new configurations in the test), so a failure is not just novelty;
  - label the band between "reactive" and "looks ahead" as "mixed";
  - M− must fail too.
  - Gemini's probabilities: F reactive 55%, F looks ahead 10%, R 15%, F-imit 30%.
  - Its concern that a flat network lacks spatial structure is noted. F stays a plain network: it is the kind of brain
    ACL's people have, and F-imit shows whether that kind can hold the plan at all.

## The world
- **11 × 11 area, border wall, moves N/S/E/W/stay, 60 steps,** as W1.
- **The brain sees everything:** three 11 × 11 channels (walls, itself, the food) = 363 numbers.
- **Reward:** +1 at the food, −0.01 per step.

## The layouts (fixed seed 20261116, made before any brain runs)
- **Families** (all of them appear in learning, in other sizes and places):
  - straight barriers with one near end and one far end;
  - L-shapes;
  - cups;
  - cups with a dead-end pocket at least 3 deep on the agent's side;
  - double walls with offset gaps;
  - nested cups;
  - a barrier with two gaps.
- **Detour:** no path keeps the Manhattan distance from growing (as W1). **Control:** such a path exists.
- **An "efficient" solve** is one within 1.15 × the shortest path.
- **The test set** (240 layouts: 120 detour, 120 control; none in the learning set):
  - **60 ordinary detours:** drawn from the families at random;
  - **60 adversarial detours:** drawn from the families, kept only if at least one of the reactive controls (W, W2, H1,
    H2, below) fails to solve it efficiently;
  - **120 controls:** the same families, placed so a direct path exists.
- **Learning set:** 400 layouts, half detour and half control, drawn from all families with no adversarial filter.

## The brains
| brain | what | role |
|---|---|---|
| **G** | greedy | negative control |
| **W** | wall-follower, left hand (W1's) | negative control |
| **W2** | wall-follower that keeps the wall on the side away from the food's lateral offset (turns toward the food's side) | negative control |
| **H1** | walk toward the food until blocked; then go around the end of the touched wall segment nearer to itself (the cells of that segment are visible) | negative control (Gemini's rule) |
| **H2** | the same, but it picks the end that minimises (its distance to the end + the end's distance to the food), straight-line | negative control (GPT's rule) |
| **M−** | remembers where it has been, no planning (W1's) | negative control |
| **B** | BFS on the map it sees | positive control |
| **F** | network: 363 → 64 tanh → 5 action scores + value; actor-critic | ACL's kind of brain |
| **R** | F with an Elman memory (64 units, truncated BPTT 16) | adds memory |
| **F-imit** | F's network, trained to imitate B's actions on B's paths | can this kind of network hold the plan? |

- **H1 and H2** follow their chosen end by walking along the wall (keeping the touched segment on one side) until a step
  toward the food is open, then go greedy again.
- **Learning:** 16 seeds per learning brain, 30,000 episodes, learning rate 0.01, gradient-norm clip 1.0, γ 0.97,
  entropy 0.01 (W1's settings).

## Measures (test set, learning off, arg-max actions)
1. **Efficient detour success:** the share of the 120 detour layouts solved within 1.15 × the shortest path. Also
   reported for ordinary vs adversarial, and per family.
2. **Pocket success:** efficient success on the pocket-family detours.
3. **Control success:** solved, on the 120 control layouts.
4. **First-decision accuracy:** on detour layouts, the share where each of the first 3 moves shortens the true BFS
   distance to the food.

## Readings (frozen)
- **"Looks ahead":** efficient detour success ≥ 0.80, pocket success ≥ 0.70, and above G's (for learning brains,
  the lower bound of the difference over seeds above 0).
- **"Reactive":** control success ≥ 0.80 and efficient detour success ≤ 0.60.
- **"Mixed":** anything else.
- **Valid only if** B looks ahead and none of G, W, W2, H1, H2, M− does. If any of them passes, nothing is concluded.
- **Learning brains:** 95% bootstrap intervals over the 16 seeds (10,000 draws, NumPy seed 20261116). A threshold is
  met if the mean meets it.
- **Even a pass is behaviour, not proof of an internal look-ahead** (GPT). A mechanistic probe would be a later study.

## The assistant's prior
- Valid (all six controls fail, B passes): about 75%.
- F reactive: about 55%. F looks ahead: about 10%. R looks ahead: about 15%. F-imit looks ahead: about 35%.
