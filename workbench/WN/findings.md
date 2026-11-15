# WN findings: how many neurons? (exploratory size sweep; 24 children per brain; numbers from `analyse_wn.py`)

Plan: `questions.md` (WN-frozen). Code checked before data (`checks.log`, All: PASS; one wrong check fixed before
data, IMPLEMENTATION.md correction 1). Run 14 November 2026, 12:47–12:56, locally at Idle, 240 children. Full table:
`analysis.md`. Mind Lab rule: no blind recompute (exploratory, no council, as the plan says).

## 1. Own skill after the teaching stops (day 60): best at 32 neurons, then falls
- Memory child, day 60, mean [95% interval]:
  - M8 0.576 [0.479, 0.674]; M16 0.806 [0.736, 0.875];
  - **M32 0.931 [0.882, 0.972]**;
  - M64 0.882 [0.833, 0.931]; M128 0.812 [0.750, 0.875]; M256 0.688 [0.618, 0.757].
- The assistant's prior ("rises to about 32–64, then flattens or falls", about 60%) held.

## 2. Copying in the moment: bigger is better
- After a showing at day 30: M8 0.451, M16 0.660, M32 0.924, and **M64, M128 and M256 all 1.000**.
- **But the big children had not learned the skill as their own while they were being shown.**
  - Own skill at day 30: M32 0.396, M64 0.146, M128 0.069 [0.035, 0.111], M256 0.035.
  - A big memory holds the whole showing and repeats it, so it leans on the teacher.
  - Its own skill comes only from practice after the teaching stops, and by day 60 it is still behind M32.
- This reading (leaning on the teacher) is an interpretation, not a tested cause.

## 3. Memory against no memory
- **Day 60, own skill: memory wins at every size:**
  - M8 − F8: +0.111 [0.014, 0.194]; M32 − F32: +0.389 [0.319, 0.465]; M128 − F128: +0.333 [0.236, 0.431].
- **After a showing at day 30: memory wins at every size:** +0.153, +0.486, +0.576.
- **Own skill at day 30: no gain;** at 128, memory is worse:
  - M128 − F128: −0.375 [−0.458, −0.292];
  - at sizes 8 and 32 the intervals include 0.
- The prior ("memory beats no memory at every size", about 80%) holds at day 60 and after a showing, **not** for own
  skill during the teaching.
- No-memory skill does not grow with size: F8 0.465, F32 0.542, F128 0.479 at day 60.

## 4. Growing (G: 16 neurons doubling to 128) behaved like the small brain it was born as
- **G − M16:** −0.021 at day 30, −0.021 at day 60, +0.014 after a showing; all intervals include or touch 0.
- **G − M128:** +0.285 [0.208, 0.361] at day 30; −0.028 [−0.118, 0.062] at day 60; −0.326 after a showing.
- The prior ("reaches M-128 by day 60 but is behind at day 30", about 45%) **did not hold**. It is level at day 60,
  only because M128 and M16 are level there, and it is ahead at day 30.
- **Exploratory, after the data** (`explore_g_use.py`, seeds 1–4):
  - G's added neurons barely reached the hands by day 60. Mean |outgoing weight|: born 16 about 0.41–0.44, added
    112 about 0.008–0.009 (M128: about 0.12–0.14 for all its neurons).
  - The new neurons started silent and with tiny inputs. Their learning signal is in proportion to their own
    activity, so they stayed nearly unused.
  - **What this sweep shows is that this way of growing (silent new neurons) adds nothing. It is not that growing
    cannot work.**

## 5. Cost
- CPU seconds per child: M8 0.92, M32 1.15, M128 2.02, M256 6.02.

## Limits
- One task: small, 6 kinds, 2 lids. Only 60 days.
- **Fixed learning rates at every size:** bigger brains might need other rates or longer lives. So "bigger is worse
  here" is about this setting.

## What it means for the brain plan
- **Size is not the bottleneck at this scale:**
  - a right-sized ring (about 32) learns its own skill best;
  - extra neurons make it a better copier in the moment, but slower to own the skill.
- **Next questions (each needs the creator's OK):**
  - growth with new neurons that start awake (or that grow connections, as a child's brain does);
  - whether evolved starting wiring helps.

## Correction 1 (14 November 2026, appended after WT)
"Best at 32 neurons" holds in this setting, where a teacher shows every try on days 1–30. In WT, with the teacher
present on only some tries:
- **teacher on 1 try in 5, own skill at day 60:** M32 0.476, M128 0.826, and evolved brains of about 215 neurons
  0.86–0.88;
- **teacher on half the tries:** M32 0.712, M128 0.882.

With scarce teaching, more neurons learn better. See `../WT/findings.md`.
