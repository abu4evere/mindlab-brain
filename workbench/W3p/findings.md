# W3p findings: a planner that learns walls from its bumps (23 November 2026)

**Status: final.** Plan `questions.md` (tag `W3p-frozen`), frozen analysis `analyse_w3p.py` (written before data),
blind recompute by a fresh session (`recompute_w3p.md`) agrees on every number and verdict. Held-out confirmation on
200 new lands: `heldout/findings.md`.

- **Runs:** MB, MBb, MV, seeds 1-8 (24 runs of 4.0M steps), paired with W3n's HR. Oracle VM: all MB, MBb 1-3, MV 1-4.
  Google VM: MBb 4-8, MV 5-8. Each run's machine in `output/machine_*.json`; the two Linux VMs train bit-identically.
- The brain: W3n's HR exactly (DriveVIN, sleep and hunger reflexes, the parent's childhood, the recipe, the kept copy)
  except the brain is **MoveVIN** (`brain_mv.py`): the thinking loop is the body's own physics (4 moves; a move into a
  blocked place leaves you where you are, 30 rounds), with a learned 3 x 3 "can I enter here?" filter on the senses
  (no wall label given). 236 learned numbers (HR's DriveVIN: 379).
  - **MB:** every attempted move during training is a lesson for the filter (its 3 x 3 memory patch, and whether it
    moved); one logistic step every 64 attempts, lr 0.05; only while training.
  - **MBb:** the same, with balanced lessons (blocked and moved lessons carry half the weight each; the councils' fix).
  - **MV:** MoveVIN with no bump lessons (the control: what the planner gives without the bumps).

## The frozen readings (kept copies, paired by seed with W3n's HR; 95%)
| measure | MBb (balanced bumps) | MB (bumps) | MV (no bumps) | HR (old brain) |
|---|---|---|---|---|
| **R2 detours** | **1.000 [1.000, 1.000]** | 0.799 [0.740, 0.858] | 0.278 [0.205, 0.358] | 0.267 [0.215, 0.319] |
| R5d long detours | 0.875 [0.797, 0.938] | 0.062 | 0.047 | 0.125 |
| M2 memory | 1.000 | 1.000 | 0.988 | 0.825 |
| value map reaches food (PLAN) | 1.000 | 0.851 | 0.538 | 0.076 |
| lifespan, reflexes on (max 3,000) | 3000.0 | 2956.4 | 2901.1 | 2802.9 |
| **lifespan, bare (reflexes off)** | **2983.3** | 2843.3 | 2566.6 | 1607.5 |
| **bare fresh-land survival (A5s)** | **0.988 [0.982, 0.992]** | 0.925 | 0.840 | 0.375 |
| fresh-land survival, reflexes on | 0.998 | 0.990 | 0.955 | 0.877 |
| "can I enter here?" open − walls | 0.970 | 0.697 | 0.027 | 0.000 |

## Primary
- **MoveVIN with bump learning detours better than the old brain (R2, MBS − HRS):** +0.531 [0.448, 0.625] -> **yes**
  (MB beats HR on every one of 8 seeds, by 0.42 to 0.83).
- **MBS passes the Bob Profile's Reasoning 2 (lower bound ≥ 0.80):** 0.799 [0.740, 0.858] -> **no** (just short).
- **MBbS passes Reasoning 2:** 1.000 [1.000, 1.000] -> **yes** (every seed 1.00).

## What it means
- **The planner needs the bumps.** MoveVIN without bump lessons (MV) detours 0.28, the same as the old brain
  (MV − HR +0.010 [−0.087, 0.111], no difference). The bumps are what teach it where walls are: MB − MV +0.521. The
  "can I enter here?" filter learns walls only when fed its bumps (open − walls 0.70 for MB, 0.03 for MV).
- **Balanced lessons close the leak.** Plain bump lessons (MB) solve ordinary detours (0.80) but fail long ones (0.06,
  below HR): when bumps grow rare, "I moved" lessons drown the "blocked" ones, so the filter stays leaky. Balancing
  them (MBb) solves every ordinary detour (1.00) and 0.88 of long ones, and makes the filter near-perfect (0.97).
- **The brain now keeps the body alive on its own.** This was W3n's open weakness: with both reflexes off, the old
  brain survived 0.38 of fresh lands and lived 1,608 steps. MBb bare survives **0.988** and lives **2,983** of 3,000.
  The bump-learned walls let the planner reach food and shelter without the reflexes' help. MBb − HR bare: lifespan
  +1,376, survival +0.61.
- **Memory use also rose** (M2 0.82 -> 1.00), though the memory itself is still the designer's writer (a named limit;
  the brain has no learned memory of its own yet).

## The Bob Profile (`scorecard/bp/bp_score.py`)
| brain | Learning | Reasoning | Memory | Generalization | Autonomy | total |
|---|---|---|---|---|---|---|
| HR (old) | 2 | 0 | 0 | 2 | 2 | **6** |
| MB | 2 | 0 | 2 | 2 | 2 | 8 |
| **MBb** | 2 | **2** | 2 | 2 | 2 | **10** |
- MBb is the first brain to score in all five abilities. Reasoning, stuck at 0 (detours), now passes at level 2.
- The score is capped at 10 because the tests for levels 5-20 are not built yet, not because MBb failed them. Building
  them is the next step toward the creator's goal (≥ 60 overall, ≥ 10 each).

## Against the priors (questions.md)
- MBS − HRS on R2 above 0: the assistant 85%, GPT 80%, Gemini 92% -> **yes**.
- MBS passes Reasoning 2 (lower bound ≥ 0.80): 30% -> **no** (0.740).
- MBbS passes Reasoning 2: 40% -> **yes** (1.00).
- MBS − MVS on R2 above 0 (the bumps help): 85% -> **yes** (+0.521).
- MBS's lifespan not worse than HRS's: 55% -> **yes** (better, +153 reflexes, +1,236 bare).
- MBS passes Memory 2: 70% -> **yes** (1.00).

## Named limits
- The bump lesson is a learning channel we designed (the target and the loss are ours; the signal is the world's
  physics). The planner is a designer-built structure with learned parts. So this is "a learned wall model inside a
  designer-built planner", not planning invented from nothing (GPT's framing).
- The memory probe injects the full map (the brain's map memory is the designer's writer), so M2 measures use of
  memory, not learned memory. Memory 5 fails by construction for both MB and HR.
- Eight seeds. MBb is at the ceiling on R2, PLAN, M2 and reflex-on lifespan (every seed perfect); the held-out run on
  200 new lands (`heldout/findings.md`) confirms R2 1.00 there too, so it is not an overlap with the probe's 50 lands.
- HR seed 7 is a memory outlier (M2 0.36 vs 0.86-0.92); it inflates the M2 gap. Lifespan is capped at 3,000.

## The best brain now
MBb (balanced bump lessons) is the new best Mind Lab brain: it solves detours, keeps the body alive without reflexes,
and scores 10/100. It is the candidate for the one ACL comparison (the navigator transplant,
`acl_exam_scoping_2026-11-20.md`), after a plan and the creator's sign-off.
