# WM findings: learning from mistakes (exploratory; numbers from `analyse_wm.py`)

Plan: `questions.md` (WM-frozen). Checks All: PASS before data. Run 14 November 2026 on GitHub's machines (`run.yml`),
10 jobs of 48 children.
- **Correction 1** (before any TB or SUTB data; `IMPLEMENTATION.md`): a lid whose 16 pairs had all failed starts its
  search again.
- Full tables: `analysis.md`. Mind Lab: exploratory, no council, no blind recompute.

## 1. No part made the brain relearn the changed codes
Own skill on the changed kinds (48 children each):

| arm, 128 neurons | group A, 14 days after its change (day 45) | group B, 14 days after (day 60) | lifetime food |
|---|---|---|---|
| Base | 0.11 | 0.00 | 828 |
| SU (surprise) | 0.05 | 0.01 | 738 |
| TB (don't repeat a failure) | 0.04 | 0.01 | 856 |
| LSi (learned lose-shift) | 0.11 | 0.02 | 833 |
| SUTB | 0.04 | 0.01 | 806 |

- **Arm − Base at size 128:**
  - A45: SU −0.062 [−0.111, −0.014]; TB −0.069 [−0.118, −0.021]; LSi 0.000 [−0.049, +0.049]; SUTB −0.076;
  - B60: every arm between +0.007 and +0.021, with lower bounds at 0.000.
- **Size 32:** the same picture; every relearning reading 0.00–0.04.
- **The priors** (TB about 50%, SU about 30%, LSi about 20%, a gain of at least 0.15): **no** for all three.

## 2. Don't-repeat found the new answers in the moment, but did not learn them
- **TB raised lifetime food:** +28 [+10, +46] at size 128; **+133 [+115, +154] at size 32** (SUTB +104).
- So the blocked search did find new codes during practice: it was fed for them.
- **But the tests, which use only the connections, stayed at about 0.**
- **Finding is not learning.** A success after a search moves the connections only a little, while the old habit is
  strong. The next try returns to the habit, fails, and the search begins again.

## 3. Some parts harmed skill before the change
- **Group B before its change (day 45), arm − Base:**
  - size 128: TB −0.132 [−0.208, −0.056], SUTB −0.257 [−0.340, −0.174], SU −0.056 [−0.104, −0.007];
  - size 32: SU −0.104, TB −0.104, SUTB −0.201.
- **The prior "no part harms" (about 65%): no.** More exploring in practice means less practice of the right habit.
- LSi did not harm (B45 0.000 at size 128).

## 4. Why (the assistant's reading, not a tested cause)
- **The weak point is the learning rule itself.**
  - The brain learns from reward by small steps. Its reward baseline is a slow running average, so after a change a
    rare success gives only a small push (advantage about 0.5 minus a baseline still near 0.3–0.4).
  - Failures keep pushing away from whatever was tried.
- **What is missing is strong learning from one's own unexpected success:** a "that worked!" moment that writes the
  success in at once, the way the copy step writes in a showing.
  - In animals this resembles the dopamine burst on an unexpected reward (a positive prediction error).
  - In machine learning, "self-imitation" copies one's own good tries (Oh et al., 2018).
  - Both are from memory, not read today.
- **SU used only negative surprise** (failure when success was expected). The positive side, success when failure was
  expected, was not in it.

## Limits
- One task; the parts' numbers were fixed, not tuned; fixed learning rates.
- TB's list grows to 16 pairs before it clears.

## For the brain plan (the creator's choice)
- **Next part to test:** learning from one's own unexpected success. When a lid opens after failures, copy that try at
  full rate, as if it had been shown.
- It could stand alone or join TB, whose search finds the answers that this part would then keep.
