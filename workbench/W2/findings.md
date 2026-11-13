# W2: planning on what one remembers. Findings (13 November 2026)

**Status:** valid. Code checks pass; all 48 runs are present; Bp solves every familiar detour efficiently; B0 and the
reactive controls score at most 0.08.

## The frozen readings
- **Memory matters: yes.** M − M0, familiar efficient detour: +0.38 [+0.30, +0.46].
  - M 0.46; M0 (no memory) 0.09.
  - M with its map erased 0.11; with another room's map 0.18.
- **The given map beats a learned memory: yes** (an architecture comparison). M − R +0.31 [+0.22, +0.39]. R barely
  uses the tour: 0.16 familiar against 0.13 new.
- **Decisions follow memory: no.**
  - M − M-erase passes: +0.35 [+0.27, +0.43].
  - But the look-alike correct side is 0.26 [0.21, 0.32], below chance.
- **Uses what it knows: no.** M 0.46 against the 0.80 × Bp line (0.80); the absolute gap to Bp is −0.54.

## Why the look-alike pairs fell below chance (exploratory, after the data, labelled)
Three M seeds were retrained with the same code and seeds. They reproduce the frozen scores exactly (0.525, 0.15,
0.10). Each room was then classified (`explore/`). Two causes, neither of them "M ignores its memory":

1. **The unknown looks open.** When M turns away from the gap, the tour had shown only about 20–28% of the barrier on
   the other side, against about 90% on the gap's side. M remembers that the gap's side is walled and gambles on the
   side it has not seen. Bp does the same: it turns away 27 times in 80, and in those rooms the other side was 13%
   known. Bp's own score on this test is only 0.66. The test was confounded: with "unknown = open" (the frozen
   design), turning away is often what the map says.
2. **Stuck at the barrier.** In two seeds, M never moves sideways in about 60% of the rooms (a full-width barrier
   with one gap is not among the learning families). Those count as 0.
3. **When both sides were known** (the other side at least 80% seen), M turned toward the gap 0.90, 0.85 and 0.58 of
   the time (seeds 1, 4, 6). When it can see in memory that the other side is closed, it mostly follows its memory.

## What it means (the assistant's reading)
1. **A remembered map works as a brain part.** With the same planner, memory lifts familiar-room detours from 0.09
   to 0.46, and wrong or erased memories take it away. A learned recurrent memory (R) did not learn to use the tour
   at this budget.
2. **The planner is still the limit.** M reaches 0.46 where the scripted planner on the same map reaches 1.0. W1e
   showed V+ keeps improving to 500,000 episodes (0.70), so W2's 150,000 is young.
3. **How to treat the unknown is a brain question, not a detail.** Optimism ("unseen = open") sends the brain into
   the unknown when the known way is longer. That is curiosity's raw material, and it belongs in W3 (drives).
4. **For the starting brain:** keep the map memory (a fixed writer, labelled engineered) and V+ trained long. Do not
   rely on a plain recurrent memory for maps.

## Next
- **W3 (drives only):** survival, comfort, curiosity as the only motives, on this brain (map memory + V+), with the
  food hidden, so that exploring the unknown is the brain's own choice.
- Training budget for the planner: 500,000 episodes where time allows.
