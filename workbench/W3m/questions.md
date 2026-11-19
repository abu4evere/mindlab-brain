# W3m: the body's own mind (plan, frozen before any study data)

**Frozen** as git tag `W3m-frozen`.
- **The creator's idea and sign-off (19 November 2026):** "i think humans brain has like 2 minds one belongs to us and
  second belongs to brain itself … if we do not want to sleep we eventually sleep … there should be some things in brain
  neurons that react itself"; then "alr lets test this bro next".
- **Council:** `../W3m_council_2026-11-19.md` (GPT; Gemini's tab did not respond). Draft: `../W3m_draft.md`.
- **Exploratory,** in the W3 series. Calibration (below) used only W3's calibration lands.

## Why (W3k's saved tests, `../W3m_prep_deaths.md`)
The best brain (W3k's CS) dies mostly tired near food: 66% of deaths "exhausted", 66% "food known within 30 steps", 47%
both. Dying lives are exhausted for 28% of their steps, surviving lives for 3% (the Script: 2%). Resting is left wholly to
learning. Rest only works at the shelter (tiredness −10 per step there, +1 elsewhere; moves cost double above 100).

## Arms (`w3m.py`: W3k's run R, 4.0M steps, 2.4M fade, W3d's PYFR; its kept copies; 16 seeds; verified machines)
| arm | the inborn part |
|---|---|
| **SL, the sleep reflex** | at tiredness 90, with energy at least 40 and the shelter in the map memory, the body takes over: the shortest known way to the shelter, then it stays until tiredness is 0. Hunger wins: below energy 40 it lets go. |
| **SR, rest only (GPT)** | the same lines, but the body never walks: it only holds the brain at the shelter once the brain is there by itself, tired. Separates forced rest from the reflex's way-finding. |
| **UR, the urge** | nothing forced; each step, tiredness above 90 costs the reward 0.75 × (F − 90)/110 |
| R2, CS, CY (W3k, cited) | no inborn part. With the parts off, `w3m.py` trains W3k's run R bit for bit (checked), so W3k's tested brains are the control, on the same seeds and lands. |

- The reflex is part of the body: it acts in training and in every test of SL and SR. The brain still draws its own move
  every step (its random stream is unchanged); the body's move is the one taken, and **the brain learns from the steps as
  taken** (GPT advised masking the actor on those steps; kept as taken, so the reflex also teaches, and SLS-off reads
  what the brain learned with it).
- Each arm gives its end brain, its kept copy (S) and a copy at a step drawn in advance (Y, seed 20261201 + run seed).
  The kept copies of SL and SR are also tested with the reflex off (SLS-off, SRS-off).

## Calibration (before any study data; `calib_m.py`, W3's calibration lands 800001–800050 only)
W3k's CS brains (seeds 1–4), the walking reflex added at test, no retraining; hunger line 40, 60, 90, 120 against none:
| line | lifespan | full lives | steps exhausted |
|---|---|---|---|
| none | 1,683 | 0.39 | 0.20 |
| **40 (chosen)** | **2,416** | **0.72** | 0.045 |
| 60 | 2,310 | 0.66 | 0.05 |
| 90 | 2,062 | 0.53 | 0.07 |
| 120 | 1,952 | 0.45 | 0.085 |
Line 40 was best on all 4 brains. The tiredness line (90) and the urge's size were not tuned.

## Measures
Lifespan; survival to 3,000 and 1,000; fresh-land survival; the share of steps exhausted and hungry (per life, then per
seed); death labels; for SL and SR, the share of test steps the reflex takes over.

## Readings (`analyse_w3m.py`, frozen; paired by seed; bootstrap over 16 seeds, numpy seed 20261200)
1. **Two primary readings (Bonferroni, 97.5%, lower bound above 0):** **SLS − CS** ("the sleep reflex helps") and
   **URS − CS** ("the tiredness urge helps"), on lifespan. SL tests an inborn controller (with its way-finding), not a
   learned sleep instinct (GPT's wording).
2. **Secondary (95%):** SL − R2, UR − R2, SR − R2 (the ends); SRS − CS; SLS − SRS (what the way-finding adds);
   SLS-off − CS and SRS-off − CS (did the brain itself learn to rest?); the share of steps exhausted, SLS − CS.
3. **Toward the bar:** the best arm's fresh-land survival against 0.80.

## Validity (hard stops)
Checks All: PASS before data (`checks_w3m.py`, 9: settings; schedules; parts off = W3k's run R bit for bit; the urge's
values; the reflex on a hand-made body; SR never walks; SL trains differently, split = unsplit, repeatable; UR forces
nothing; a staged run saves its copies and tests with and without the reflex).

## The assistant's prior (GPT's beside it)
- SLS − CS above 0: about 75% (GPT: positive mean 75%, passing the interval about 45%). URS − CS: about 35% (GPT 40%,
  passing about 15%). SRS − CS: about 45%. SLS-off − CS: about 25% (GPT 30%). SLS exhausted less than CS: about 90%
  (GPT 90%). Any arm at 0.80 on fresh lands: about 15% (GPT 8%; the calibration's 0.72 on calibration lands raised mine).
