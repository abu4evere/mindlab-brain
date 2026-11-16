# WG2 findings: dreams that leave a question (exploratory; 16 November 2026)

Plan: `questions.md` (WG2-frozen). Checks All: PASS before data. Run on GitHub's machines (2 jobs, 16 files). n = 8
seeds, paired. Mind Lab: exploratory, no council, no blind recompute.

## The frozen readings (`analysis.md`)
1. **"Dreams now reach waking life": no.** IQ − IM in the last window:
   - reach −6.1 [−19.1, +0.8];
   - pattern +0.006 [−0.005, +0.024];
   - activity −0.004 [−0.024, +0.011].
2. **"It goes to look": not readable as frozen.** The analysis gave NaN, because IQ seed 4 ate nothing in any dream and
   so posed no question. The frozen script did not allow for a seed with none.
3. **"No harm to skill": formally no.** IQ − IM lifespan after the room −40.9 [−116.4, −1.2]. But see the second
   caution below: the harm comes almost entirely from seed 5 (IM 846, IQ 545; the other seven differ by 0 to 12).

## Exploratory (after the data, labelled; `explore_answered.py`)
- **Over the 7 seeds that posed questions,** IQ's questions were answered within 500 steps 0.364 [0.117, 0.667] of the
  time, against 0.271 [0.120, 0.466] for random blocks under IM.
- IQ − IM +0.093 [−0.078, +0.315]. **Not clearly more than chance.**

## Two cautions, recorded openly
1. **The frozen analysis did not handle a seed with no questions** (reading 2, above).
2. **WG2's re-run of IM did not reproduce WI's IM for seed 5:**
   - its dreams diverged, giving a lifespan after the room of 846 here against 721 in WI;
   - the other 7 seeds matched exactly (dreams, room activity and lifespans), and seed 1 also matched locally in the
     checks.
   - **The likely cause:** `wg2.py` imports numpy before WI's module sets the BLAS thread count to 1. So the cloud ran
     with multi-threaded BLAS, whose sums can differ in the last bits, and a long chain of sampled actions can amplify
     that.
   - So WG2's IM and IQ are a fair paired comparison within one run. But seed 5 is not bit-reproducible, and reading
     3's "harm" rests mostly on that seed.
   - Future Mind Lab scripts set the thread count before importing numpy.

## What it means (the assistant's reading)
- **Marking a dream's place as "worth checking" did not make the brain go and look more than chance,** and did not
  change its waking pattern. Its curiosity link is weak compared with its habit loop.
  - The recipe brain paces its circuit (WQ). A few unknown cells elsewhere do not pull it off the circuit.
- **Imagination that reaches waking life needs more than a marker in memory.** The brain must want to resolve
  questions, which is a stronger, learned curiosity. That points to the "getting-better" (learning-progress)
  curiosity, the next study.

## Limits
- Engineered imagination and question-marking; one room; 8 seeds; seed 5's numerical non-reproducibility.
