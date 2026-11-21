# Bob Profile council (20–21 November 2026): GPT's and Gemini's opinions, not sign-off

Question: `bp_council_prompt.txt` (asked neutrally), sent to GPT (https://chatgpt.com/c/6b012445-7384-83e9-9904-f075cb5c8037,
model 'Instant') and Gemini (https://gemini.google.com/app/c3864241c8a2066b). Both answers were read in full.

## Where they agree
- **The floor must dominate.** "At least 10 in every ability" matters more than the total. The five-number profile is
  the main result; the sum is secondary. (Gemini: an uneven specialist could reach 60 while failing as a mind; GPT: a
  balanced 10-10-10-10-10 = 50 is closer to the goal than an uneven 72.)
- **The levels are ordinal milestones, not equal steps.** Both see cliffs, mostly between 5 and 10 (learning: adapting
  values vs learning a new task; autonomy: homeostasis plus curiosity vs unassigned goals).
- **Narrow tricks can pass many tests.**
  - A hand-written planner (value iteration, A*) passes the detours.
  - A designer map passes memory 2.
  - A latch or lookup table passes memory 5.
  - Hard-coded drive arbitration passes autonomy 2.
  - A novelty bonus passes the curiosity half of autonomy 5.
  - Input preprocessing passes generalization 5.
  - So each score must say **where the ability comes from** (GPT: report the performance and its source, learned or
    designer-built).
- **Stronger controls are needed than random:** "cheater" controls that exploit each test without the ability. A test
  is valid only if they fail it (Gemini), or it records what the test really measures (GPT).
- **Split the mixed tests:**
  - reasoning 5: the detour, and the value trade-off;
  - autonomy 5: bare survival, and seeking information;
  - generalization 10: changed causes, and a different world.
- **Statistics:** the unit is the training seed (at least 8), each tested on many lands (Gemini: 20–30+); a one-sided
  interval with its method named.
- **20 = adult human is not measurable here yet.** GPT: set it later with human players under matched information and
  budgets. Gemini: redefine 20 as the grid-world ceiling, the ideal agent under Bob's exact senses. Both: levels 15–20
  are provisional.

## Where they differ, and other points
- GPT: add a **memory intervention** (erase, scramble or delay the memory; behaviour must change as predicted), and do
  not force advanced tests into this world: mark them untested until the right world exists.
- Gemini: move "no catastrophic forgetting" from memory into learning. Generalization 2 overlaps learning 2, so make it
  a topology shift (new kinds of wall layout). Learning 5 should include a food-type swap, so that a quickly fading map
  cannot pass it.
- GPT's confidence that levels 2–5 measure what they claim: learning 70%, reasoning 80%, memory 55%, generalization
  65%, autonomy 35%.

## The assistant's check against the first test results (R2, M2, run before the answers arrived)
- **Both models assume a value-iteration planner passes the detours "trivially". It does not:**
  - the scripted agent passes 100% and the greedy agent 0% (36 detour cases);
  - W3n's learned planner (seeds 1–3) passes only 19–42%, even at the easiest qualifying detour;
  - with no wall in the way (M2: food 8 steps off, seen 100 steps ago) it succeeds 90%.
  So a learned planner is not a hand-written one; the test separates them. Ishida and Henriques (2022) report this
  weakness of learned planners.
- The tests have to report the source of each ability (taken).

## Taken into v2 of the draft
1. The profile is primary, the floor rule decides, the total is secondary; levels are ordinal.
2. Every score names its source: the architecture (designer) and what was learned.
3. Controls: the positive control (Script), the negative (random), plus a **cheater control** per test:
   - greedy for the detours;
   - **memory erased** for memory 2;
   - the bare body for autonomy;
   - the frozen copy for learning 5.
4. Statistics: the unit is the training seed (at least 8), each on the 50 test lands (36 detour cases); a one-sided 95%
   bootstrap lower bound over seeds.
5. Split reasoning 5 (detour; value trade-off), autonomy 5 (bare survival; information seeking), generalization 10.
6. Generalization 2 becomes a topology shift: lands with twice the wall segments (seeds 940001–940050), against its
   own standard test lands.
7. "No catastrophic forgetting" moves to learning 10; memory 10 becomes long-delay recall with a memory intervention.
8. 15 and 20 are provisional. 20 is human performance under matched senses and budgets when that can be run, else the
   grid-world ceiling (the best known agent with the same senses).
