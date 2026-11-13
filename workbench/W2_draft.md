# W2: planning on what one remembers. A partial view plus a remembered map (DRAFT)

**Why:** ACL's people cannot see the whole land; they know it from having walked it. W1b–W1e gave the brain the whole
11 × 11 area to see. W2 asks whether the planner still finds the short way round when it sees only a small window,
and whether a remembered map is what makes the difference.

**Depends on W1e:** the planner used here is whichever of V and V+ W1e shows is better (named before this plan is
frozen). If neither takes the efficient detour well, W2 still measures what memory adds, relative to the full-view
planner as the ceiling.

## The world (W1b's, with a partial view)
- The same 11 × 11 area, layouts, moves, 60 steps, and "efficient" (within 1.15 × the shortest path).
- **The view:** a 5 × 5 window centred on the brain (radius 2). Walls and the food are seen only inside it.
- **The food's direction is always sensed** (a smell: the food's cell is given), so the task is not a search for
  the food but a route around walls that are only partly seen.
- **Two kinds of episode:**
  1. **New room:** the brain starts with nothing seen.
  2. **Familiar room:** first a fixed, scripted walk through the room (the same tour for every brain; it covers the
     whole area at radius 2), with no food and no learning; then the food appears and the episode starts. The brain
     keeps whatever it remembers from the tour.

## The brains
| brain | what | role |
|---|---|---|
| **P** | the full-view planner from W1e (sees all) | ceiling |
| **M** | the same planner on a remembered map: a grid that writes what the window shows (wall / open / unknown) and keeps it | memory as a map |
| **M0** | the same planner on the current window only (everything else unknown) | no memory |
| **R** | W1c's convolution brain on the window, with a recurrent state (no map) | learned memory, no map |
| **Bp** | scripted: BFS on the remembered map, unknown cells treated as open, replanning each step | positive control (the best one can do with what is known) |
| **G, W, M−** | W1b's reactive controls, on the window | negative controls |

- The map writer in M is fixed (it stores what is seen; it does not decide anything). Everything that chooses moves
  is learned, imitating Bp as W1b–W1e imitated B.
- Same seeds (16), budget (30,000 episodes), learning settings and checks as W1e.

## Measures
1. Efficient detour success, new rooms and familiar rooms separately (control layouts, empty rooms, held-out shapes
   as before).
2. **How much of the tour is used:** familiar minus new, per brain.
3. The value-map correlation on the remembered map (as W1d).
4. **Replanning:** in new rooms, the share of episodes where the brain turns back within 3 steps of seeing a wall
   that blocks its route (Bp does).

## Readings (to be frozen)
- **"Memory matters"** if M − M0 on efficient detour, familiar rooms, has a lower bound above 0 (paired by seed).
- **"The map helps beyond a learned memory"** if M − R, familiar rooms, has a lower bound above 0.
- **"Uses what it knows"** for a brain if its familiar-room efficient detour is at least 0.80 of P's.
- The reactive controls must fail (as W1b); Bp must pass.

## Open questions for the council
1. Is a fixed map writer fair, or is it engineering (the hippocampus does build maps, but we hand-built ours)?
2. Should the food also be hidden (search plus memory), or is that a separate task (W3, curiosity)?
3. Is a 5 × 5 window right for an 11 × 11 area?
4. Is the tour fair (scripted, the same for every brain), or should the brain explore on its own?

## The assistant's prior
- Memory matters: about 85% (M0 is nearly blind past 2 cells).
- The map helps beyond a learned memory: about 70%.
- M uses what it knows (≥ 0.80 of P): about 60%, if the W1e planner is good; lower if not.
