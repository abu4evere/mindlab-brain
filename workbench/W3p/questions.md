# W3p: a planner that must plan, and learns walls from its bumps (plan; frozen as tag `W3p-frozen`, 22 Nov 2026)

- **Go-ahead:** the creator, 21 Nov: "go ahead with the detour study", then the handover ("i am giving you permission to
  do all of job").
- **Council:** GPT and Gemini, asked neutrally (`../W3p_council_2026-11-22.md`).
- **Exploratory,** in the W3 series. Runs are local only (the PC, the Google VM and the Oracle VM; never GitHub Actions).

## Why
The Bob Profile's first measured profile of the living brain (W3n's HRS, `BP-HRS-scored`) was 6/100. Reasoning scored
0: detours behind a wall succeed 0.27 (pass 0.80; Script 1.00, greedy 0.00).

The diagnosis (`explore/`) found that **the brain is not planning paths**: its learned value map, followed uphill,
reaches the food in 0–11% of detour cases and 36% of open cases. Pushing value down at walls does not help.

## The change: MoveVIN that learns walls from its bumps (`brain_mv.py`, `w3p.py`, arm **MB**)
- **The thinking loop is the body's physics.** It has 4 moves; trying to enter a place you cannot enter leaves you
  where you are. It runs 30 rounds, and the hand reads the 5 move values at its own place. The feelings part is
  DriveVIN's, unchanged. 236 learned numbers.
- **"Can I enter here?"** is a learned 3 × 3 filter on the senses, with no wall label given.
- **It learns from bumps.** During training, every attempted move is a lesson for that filter: the place it tried to
  enter (its 3 × 3 memory patch before the step) and whether it got there. One logistic step every 64 attempts
  (learning rate 0.05); nothing is learned in tests. The world's physics gives the feedback, as a child learns walls by
  walking into them.
- Everything else is W3n's HR exactly: the body and its reflexes, the parent's childhood, the recipe, 4.0M steps with a
  2.4M fade, the kept copies, the test lands.

## The pilot (exploratory, labelled; 800k steps, 480k fade, seeds 1–3; `explore/pilot_*.json`)
| brain | R2 detours | M2 memory | value map reaches the food (detours) | "can I enter here?" walls / open |
|---|---|---|---|---|
| PHR (DriveVIN) | 0.28, 0.00, 0.22 | 0.80, 0.54, 0.58 | 0.03, 0.00, 0.11 | (none) |
| PMV (MoveVIN, no bumps) | 0.14, 0.19, 0.11 | 0.98, 0.96, 0.98 | 0.22, 0.33, 0.28 | 0.87 / 0.87 (never learned) |
| **PMB (MoveVIN + bumps)** | **0.53, 0.53, 0.31** | **1.00, 1.00, 1.00** | **0.75, 0.72, 0.61** | **0.33–0.53 / 0.99** |
The pilot chose the arm. It is not a result.

**Before data, already done:**
- the gradients are exact (`gradcheck_mv.py`);
- with hand-set ideal weights the design solves R2, R5d and M2 at 100% (`capacity_mv.py`);
- the faster code is bit-identical to the reference.

## After the council and two diagnoses (22 Nov, before any study data)
- **"Ideal walls"** (`explore/oracle_walls.py`, GPT's suggestion): the pilot's bump brains, with their passability
  replaced by the truth from their own memory and no retraining, solve **R2 1.00 and R5d 1.00 on all 3 seeds** (learned
  walls: 0.31–0.53 and 0.00). The planner and what it learned work; the leaky "can I enter here?" filter is the whole
  remaining gap.
- **The horizon** (Gemini): the probes' longest shortest path is 21 steps; the planner runs 30 rounds.
- **Balanced lessons** (both councils): when bumps grow rare, "I moved" lessons drown the "blocked" ones. A third arm
  gives blocked and moved lessons half the weight each in every batch. It is a design remedy for imbalance, not a tuned
  rate; the pilot's rate (0.05) is kept everywhere.
- **The control without bumps** (both councils): MoveVIN alone on the full schedule, to separate what the planner
  gives from what the bumps give.

## Arms (seeds 1–8, paired with W3n's HR; 4.0M steps, 2.4M fade)
| arm | brain | answers |
|---|---|---|
| **MB** | MoveVIN + bump lessons (the pilot's) | primary: does it detour better than the old brain? |
| **MBb** | MoveVIN + balanced bump lessons | do balanced lessons close the leaky walls (and pass Reasoning 2)? |
| **MV** | MoveVIN, no bumps | what the planner alone gives; what the bumps add (MB − MV) |
| HR, HRS, HRS-bare (W3n, cited) | DriveVIN | the old brain |

## Readings (`analyse_w3p.py`, frozen before data; bootstrap over seeds, numpy seed 20261122, one-sided 95%)
1. **Primary:** the Bob Profile's **R2 detour success** (BP-frozen probe), MBS − HRS, paired by seed: one-sided 95%
   bootstrap lower bound above 0. Beside it, the **Bob Profile verdict for Reasoning 2** (MBS's success lower bound ≥
   0.80), kept distinct from the improvement test.
2. **Secondary:**
   - R5d (long detours);
   - M2 and its erased control;
   - L2, G2, A2, and A5's survival half;
   - lifespan with reflexes and bare, and fresh-land survival, MBS − HRS;
   - the full Bob Profile of MBS (`bp_score.py MB`).
3. **Mechanism (pre-registered, both councils):** the value map followed uphill reaches the food in detour cases (HRS:
   0–11%); and "can I enter here?", open minus walls, on the 50 test lands (`bp_mv.py WALLS`).
4. **Arms compared (95%):** MBbS − MBS (balanced lessons), MBS − MVS (what the bumps add), MVS − HRS (the planner alone);
   MBbS's Reasoning 2 verdict.
5. **Named limits:** the bump lesson is a dedicated learning channel we designed (the target and the loss are ours, the
   signal is the world's physics); the planner is a designer-built structure with learned parts. The memory probe's
   full memory is injected (the brain's own map memory is the designer's writer), so M2 measures use of memory, not
   learned memory. Eight seeds make a 0.80 lower bound hard to reach; the improvement test is the primary.

## Validity
Checks All: PASS before data (`checks_w3p.py`), on the PC and on the Oracle VM:
- settings; the MB arm;
- exact gradients; fast = reference;
- capacity;
- MB trains, with bump lessons only while training; split = unsplit, the lessons travelling with the state; repeatable;
- a bump lesson moves the filter, and nothing is learned outside training;
- a staged run saves its copies and runs every test, and writes nothing into W3n's folder.

## The assistant's prior
- MBS − HRS on R2 above 0: about 85% (the pilot). GPT 80%, Gemini 92%.
- MBS passes Reasoning 2 (lower bound ≥ 0.80): about 30%. GPT 15%, Gemini 18%.
- MBbS passes Reasoning 2: about 40% (the ideal-walls diagnosis says the filter is the whole gap).
- MBS − MVS on R2 above 0 (the bumps help): about 85%.
- MBS's lifespan not worse than HRS's: about 55%. GPT 45%, Gemini 65%.
- MBS passes Memory 2 (M2 lower bound ≥ 0.80, drop ≥ 0.20): about 70%.
