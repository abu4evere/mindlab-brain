# W3b draft: living by feelings, with what the box tests taught (DRAFT for the council and the creator; not frozen)

*Drafted 15 November 2026 in a sleep-mode heartbeat. Nothing here is frozen, built or run. It needs the creator's OK,
then a council (GPT, Gemini, DeepSeek), then a frozen plan.*

## Why
- **W3:** no learned brain survived on drives alone (lifespans 172–246 steps; Rand 174; Script 2,963).
- **The telling detail: D3i also died (215 steps), although the designer's link was given** (hunger → food channel,
  fatigue → shelter, curiosity → uncertainty).
  - So the missing piece is not only the link from a feeling to its target. The path from the planner's values to
    good moves did not form in 2,000,000 steps of actor-critic from sparse reward.
- **The box tests of 14–15 November found what fixes slow learning from rare success:**
  - "that worked!" (WY: copying one's own surprising success);
  - a fast store of what just worked that acts at once (WF's WSLS, about 1.00);
  - night replay from that store into the slow network (WF's RP, WR).
- **Sources:**
  - episodic control helps most early in learning, before habits form (Lengyel & Dayan 2007; Blundell et al. 2016;
    `D:\acl\docs\research\episodic_control_2026-11-15.md`);
  - self-imitation learning (Oh et al. 2018; `mindlab_sources_2026-11-15.md`).

## Step 0 (diagnostic, read-only, on W3's saved weights; proposed first)
Before any new training, ask why D3i died. Test D3i's saved runs with two read-outs, on W3's 50 test lands:
- (a) its learned head, as in W3;
- (b) **walking greedily down the planner's own value map** (W1e's "map read-out").

**What it tells us:**
- If (b) lives, the planner and the given link are fine, and the learned head is the bottleneck.
- If (b) also dies, the planner's value map itself is wrong (for example, too short a horizon for food 15 cells away,
  or uncertainty swamping hunger).

This changes no data and decides which part W3b must fix. It would still be written down as an exploratory analysis
before it is run.

## W3b proper (the shape; numbers for the council)
- **World, drives, test:** W3's, unchanged (R = 200; the same 50 test lands; survival to 3,000 the main measure).
- **Brains** (all D3's drives: s, f, c; the links learned from zero unless said):
  - **D3:** W3's, as the reference (re-run, or cited from W3).
  - **D3+Y, "that worked!":** after a big unexpected drop in the drive (eating when hungry, resting when exhausted),
    the last N moves are copied (a self-imitation step), weighted by the positive surprise. This is the WY idea in
    time instead of in boxes.
  - **D3+F, a fast place memory that acts:**
    - the store keeps where each need was last relieved (the food cell, the shelter);
    - when a need is high and the store holds a place, the child walks there (engineered, like WSLS);
    - otherwise the learned brain acts.
    - The ceiling: how much a working episodic memory gives.
  - **D3+FR, fast memory + rest replay:** at rest in the shelter, the stored successful paths are replayed into the
    slow network. The learned brain acts; the store only teaches (like WF's RP).
  - **D3+Y+FR:** both.
- **Readings (draft):**
  - survival share for each against D3 (paired by seed);
  - lifespan;
  - land known;
  - whether the hunger link ends up pointing at food (consistent sign across seeds).
- **Budget:** run on GitHub's cloud (`run.yml`). A 2,000,000-step run took about 10 hours on the PC, so each run will
  likely need to be split into chunks under 6 hours. That is a design question for the council, not decided here.

## Open questions for the council and the creator
1. **Step 0 first?** (The assistant recommends yes: it is cheap and tells which part is broken.)
2. **Is D3+F (engineered acting from memory) acceptable,** given "program the body, not the decisions"? It is a
   ceiling, labelled. The learned arms are the real question.
3. **Should W3b keep the 3,000-step test,** or first ask a smaller thing (survive 1,000 steps)?
4. **The creator's leaky-memory lesson (WL2):** W3's map memory is engineered and perfect. Should the map fade?
