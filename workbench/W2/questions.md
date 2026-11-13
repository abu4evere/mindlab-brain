# W2: planning on what one remembers. A partial view plus a remembered map (frozen plan)

**Frozen** as git tag `W2-frozen` (Mind Lab), before any code or data.
**Sign-off:** the creator, 12 November 2026: "alr bet keep working" (standing: "do not ask me go ahead bro"; "we gotta
build good basic starting brain to put into acl").
**Draft:** `../W2_draft.md`. **Council:** GPT (chat 6af69320) and Gemini (chat b4cb16b0). **Planner:** V+ from W1e.

## The council, in short (all changes taken unless said)
- **Both:**
  - the fixed map writer is fair if it is labelled: "engineered memory plus a learned planner", not "the brain learned
    to remember";
  - keep the food's cell sensed (searching belongs to W3);
  - keep the tour scripted (the same for every brain).
- **Gemini:**
  - A full tour leaves nothing unknown, so in familiar rooms M would simply be P. **The tour is made partial and
    random per layout.**
  - A memoryless local planner could pass. **B0 is added,** and M0 imitates B0 (not Bp), so M0 is a fair
    memoryless brain, not a student copying a teacher who sees what it cannot.
  - **The view shrinks to 3 × 3.** 5 × 5 shows about a third of the room.
  - The "replanning" measure is ill-defined; it is replaced by regret.
  - Gemini's probabilities (for the draft): 95%, 80%, 85% (55% with a partial tour).
- **GPT:**
  - **The memory probes:** M with its map erased after the tour, and M with the map from another layout. Both must
    fall.
  - **The decisive test, look-alike pairs:** two rooms identical near the start (same start, same food, same local
    view), whose gap lies on opposite sides, out of view. After different tours, a brain using memory turns the right
    way; a memoryless one is at chance.
  - **A bootstrap over layouts** as well as over seeds; report the gap to Bp in absolute terms.
  - M − R is an architecture comparison (a given map against a learned memory), not proof that maps are better in
    themselves. Said so.
  - GPT's probabilities: 90%, 75%, 55%.

## The world (W1b's, with a partial view)
- **The area and the rules:** 11 × 11; W1b's layout families, moves, 60 steps; "efficient" means within 1.15 × the
  shortest path.
- **The view:** 3 × 3 around the brain (radius 1).
- **What every brain is given:** its own cell and the food's cell (position sense and smell).
- **New room:** nothing seen before the start.
- **Familiar room:** before the start, a scripted tour.
  - It begins in a random open cell and walks shortest paths between random open waypoints until 60% of the open
    cells have been in view. It does not pass through the start cell's 3 × 3.
  - No food, no learning, no choices: every brain receives the same observations (the same tour per layout).
  - Then the brain is placed at the start and the episode begins.

### The test sets (seed 20261122, made before any brain runs)
- **Detours (120):** from W1b's families.
  - Kept only if B0, H2 and W2 all fail to solve them efficiently in a new room, and Bp solves them efficiently in a
    familiar room.
  - Each has its own fixed tour.
- **Look-alike pairs (40 pairs):** a straight barrier across the room with one gap.
  - The start is below the barrier and the food above it, in the same column. The gap is k = 3–4 cells to the left
    (room A) or to the right (room B), so both rooms look the same from the start.
  - Each tour reveals the gap.
  - **Measure:** the share of first moves toward the gap's side (west or east) among the brain's first sideways move.
    Chance is 0.5.
- **Controls (120):** a direct path exists.
- **Learning set:** 400 W1b-style layouts (no filter), each episode new or familiar with equal chance, with a fresh
  random tour.

## The brains
| brain | what | taught by | role |
|---|---|---|---|
| **Bp** | BFS on the remembered map (unknown = open), replanning each step | – | positive control; the ceiling with what is known |
| **B0** | BFS on the current 3 × 3 view only (unknown = open), replanning each step | – | memoryless control; must fail the detours |
| **G, W, W2, H2, M−** | W1b's reactive controls, on the 3 × 3 view | – | must fail |
| **M** | V+ (W1e) on the remembered map: a fixed writer stores wall / open / unknown for every cell seen | Bp | engineered memory, learned planner |
| **M0** | V+ on the current view only (every other cell unknown) | B0 | the same planner without memory |
| **R** | W1c's convolution on the 3 × 3 view plus its cell and the food's, an Elman state of 64 (truncated BPTT 16); it steps through the tour too | Bp | learned memory, no map |

- **Learning:** 16 seeds, 150,000 episodes, imitation (W1e's settings and checks).
- **The planner inputs** (M, M0): the map channels (wall, open, unknown), the brain, the food; V+ unchanged
  otherwise.

## Measures (test, learning off, arg-max)
1. Efficient detour success, new and familiar rooms; controls; empty rooms.
2. **The tour's use:** familiar minus new, per brain.
3. **The look-alike pairs:** the correct-side share.
4. **The memory probes for M:**
   - **M-erase:** familiar rooms, the map cleared after the tour;
   - **M-shuffle:** the map from another layout's tour, with similar wall counts.
5. **Regret:** in solved episodes, steps taken minus Bp's steps.
6. The value-map correlation on the true map (as W1d).

## Readings (frozen; paired by seed; 10,000 draws; NumPy seed 20261122)
- **"Memory matters":** M − M0 on efficient detour, familiar rooms, lower bound above 0.
- **"Decisions follow memory":**
  - M's look-alike correct-side share has a lower bound above 0.5 (the bootstrap over seeds);
  - and M − M-erase on familiar efficient detour has a lower bound above 0.
- **"The given map beats a learned memory"** (an architecture comparison): M − R, familiar rooms, lower bound above
  0.
- **"Uses what it knows":** M's familiar efficient detour is at least 0.80 × Bp's. The absolute gap is reported too.
- **Validity:**
  - Bp passes (familiar efficient detour at least 0.90, by construction of the test set);
  - B0 and the reactive controls fail the detours (efficient at most 0.20 in new rooms);
  - otherwise W2 is invalid and is reported as such.
- **Secondary:** the same comparisons with a bootstrap over layouts (2,000 draws), for robustness.

## The assistant's prior (updated after the council)
- Memory matters: about 80%.
- Decisions follow memory: about 65%.
- The given map beats a learned memory: about 80%.
- Uses what it knows (≥ 0.80 of Bp): about 35%. V+ reached only 0.54 even with a full view.
