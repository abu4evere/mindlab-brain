# W3p: a planner that must plan (plan, DRAFT; to freeze after the pilot and the council)

**Status:** draft, 21 November 2026.
- **Go-ahead:** the creator, 21 Nov: "go ahead with the detour study", then the handover ("i am giving you permission to
  do all of job").
- **Council:** to follow (GPT, Gemini, asked neutrally).
- **Exploratory,** in the W3 series. Runs are local only (the PC and the Google VM; never GitHub Actions).

## Why
The Bob Profile's first measured profile of the living brain (W3n's HRS, `BP-HRS-scored`) was 6/100. Reasoning scored
0: detours behind a wall succeed 0.27 (pass 0.80; Script 1.00, greedy 0.00).

The diagnosis (`explore/`, exploratory, no retraining) found that **the brain is not planning paths**:
- its learned value map, followed uphill, reaches the food in 0–11% of detour cases and 36% of open cases (while the
  brain itself succeeds 90% in the open);
- pushing value down at walls does not help (0.36), or breaks it.
The 30 rounds of free learned channels (Wq, Wv) found a shortcut that works in the open and fails around walls.

## The change (one): MoveVIN (`brain_mv.py`)
The feelings part is DriveVIN's, unchanged. The thinking loop becomes the body's own physics, with one learned
perception:
- **the 4 moves:** trying to move into a place you cannot enter leaves you where you are, as the world does;
- **"can I enter here?":** a learned 3 × 3 filter on the senses, with no wall label given;
- **how much the future counts:** learned;
- **30 rounds**, and the hand reads the 5 move values at its own place.
It has 236 learned numbers (DriveVIN: 379). Everything else is W3n's HR exactly: the body and its reflexes, the
parent's childhood, the recipe, the 4.0M-step schedule with a 2.4M fade, the kept copies, the test lands.

**Before data, already done (exploratory):**
- the gradients are exact (`gradcheck_mv.py`);
- with hand-set ideal weights the design solves R2, R5d and M2 at 100% (`capacity_mv.py`), so it can;
- the faster code is bit-identical to the reference (`brain_mv_ref.py`).
- **Pilot (exploratory, labelled):** PMV vs PHR, seed 1, 800k steps (480k fade). Does MoveVIN learn detours at all with
  W3's recipe? It guides the plan; it is not a result.

## Arms (seeds 1–8, paired with W3n's HR)
| arm | brain |
|---|---|
| **MV** | MoveVIN, W3n's HR body and recipe |
| HR, HRS (W3n, cited) | DriveVIN |

## Readings (frozen with the plan; analysis written before data)
1. **Primary:** the Bob Profile's **R2 detour success** (BP-frozen probe), MVS − HRS, paired by seed; bootstrap over
   seeds, one-sided 95% lower bound above 0. And the **Bob Profile verdict for Reasoning 2** (MVS's lower bound ≥ 0.80).
2. **Secondary:**
   - R5d (long detours);
   - M2 (memory 2) and its erased control;
   - L2, G2, A2, and A5's survival half;
   - lifespan and fresh-land survival, MVS − HRS;
   - bare survival;
   - the full Bob Profile of MVS.
3. **Mechanism check:** MVS's value map followed uphill reaches the food in detour cases (the diagnosis measure; HRS:
   0–11%).

## The assistant's prior (before the pilot)
- MoveVIN learns detours better than DriveVIN (MVS − HRS on R2 above 0): about 70%.
- MVS passes Reasoning 2 (lower bound ≥ 0.80): about 35%.
- Lifespan not worse: about 55% (the learned "can I enter here" may make it slower to learn early on).
