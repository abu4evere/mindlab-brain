# W1b: the detour, seen. Does a brain take the short way round a barrier it can see? (DRAFT, not frozen)

**Why a W1b:**
- W1 was not valid (`W1/findings.md`). With a 5 × 5 view, a wall-follower passed "looks ahead": no brain could see
  which way round was shorter, so planning and wall-following behaved alike.
- Animal detour tests show the goal and the barrier (food seen through a fence). Looking ahead then means choosing
  the right way round *before* bumping into the barrier.

## The task
- **The same 11 × 11 area and moves as W1, but the brain sees all of it:** three 11 × 11 channels (walls, itself, the
  food). No smell is needed.
- **Asymmetric barriers:** a wall between the agent and the food whose one end is near (the short way) and whose other
  end is far (the long way). The long way is at least twice the short way's length.
  - Which end is short is drawn at random, independent of where the food lies to the side. So no fixed rule ("turn
    left", "turn toward the food's side") wins more than about half the time.
- **Pockets:** a third of the detour layouts have a dead-end cup on the agent's side, on the straight line to the food.
- **Unseen shapes** in the test: double walls, nested cups, a barrier with two gaps of different lengths.
- **Control layouts:** the same walls placed so a direct path exists.
- **Sets:** 400 learning layouts and 240 test layouts (120 detour, 120 control), from a fixed seed. The test shapes and
  places are never seen in learning.

## The brains
| brain | what | role |
|---|---|---|
| G | greedy | negative control |
| W | wall-follower, left hand | negative control |
| W2 | wall-follower that turns toward the food's side | negative control (a smarter reactive rule) |
| B | BFS on the map it sees | positive control |
| M− | remembers where it has been, no planning | ablation |
| F | feed-forward network on the full view (363 → 64 → 5 + value), actor-critic | ACL's kind of brain |
| R | F with an Elman memory | adds memory |
| F-imit | F's network imitating B | can this kind of network represent the plan at all? |

Learning brains: 16 seeds, 30,000 episodes, as W1.

## The main measure
**Efficient detour success:** the share of detour layouts solved within 1.25 × the shortest path. A wall-follower
should get about half: it takes the long way about half the time. A planner gets nearly all.

## Readings (to be frozen)
- **"Looks ahead"** = efficient detour success ≥ 0.80, success on pocket layouts ≥ 0.70, and above G's.
- **"Reactive"** = control success ≥ 0.80 and efficient detour success ≤ 0.60.
- **Valid only if** B looks ahead and G, W and W2 do not.

## Open questions for the council
1. Is a full view the right fix, or should the view stay partial with the barrier seen from afar?
2. Is "within 1.25 × the shortest" a fair bound?
3. Anything else that would let a reactive rule pass?

## The assistant's prior
- F reactive: about 60%. F looks ahead: about 20%. R looks ahead: about 25%. F-imit looks ahead: about 45%.
