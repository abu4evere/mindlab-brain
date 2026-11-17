# W3f findings: choosing whom to learn from, over generations (16 November 2026)

**Plan:** `questions.md` (W3f-frozen, council `../W3f_council_2026-11-16.md`; exploratory). Checks All: PASS before
data.
- **Runs:** three stages of 16 cloud jobs. The manager crashed once on a network error and was restarted with retries.
  The chains all closed at 20:20.
- The frozen `analyse_w3f.py` (unchanged since before data) gives `analysis.md`.
- n = 8 lineages × 50 test lives, each tested alone. Mind Lab: no blind recompute.

## The frozen readings
| | survived to 3,000 | lifespan |
|---|---|---|
| G2 pool (W3e) | – | 549 |
| CH1 / RN1 | 0.118 / 0.140 | 701 / 886 |
| CH2 / RN2 | 0.110 / 0.070 | 653 / 611 |
| CH3 / RN3 | 0.070 / 0.080 | 543 / 576 |

1. **"Choosing helps in one generation": no.** CH1 − RN1, lifespan −185 [−443, +84].
2. **"Choosing beats the average teacher": not shown.** CH1 − the G2 pool +152 [−135, +460].
3. **"A ratchet": no. Both arms decline.**
   - CH3 − CH1: −158 [−262, −44].
   - RN3 − RN1: −310 [−415, −211].
   - CH3 − RN3: −34 [−256, +176].

**The priors:** reading 1 about 55%: no. Reading 2 about 60%: not shown. Reading 3 about 25%: no.

## Exploratory (after the data, labelled): is the success cue the problem?
How well does "visible success" (the mean lifespan on 5 demonstration lands) rank the adults by their real test
lifespan (Spearman, 8 adults)?

| pool | Spearman |
|---|---|
| CH generation 1's children | 0.67 |
| CH generation 2's children | 0.74 |
| RN generation 1's children | −0.24 |
| RN generation 2's children | 0.33 |

- In the CH pools the cue picks the better adults fairly well, yet CH still does not beat RN.
- So a noisy cue is not the main reason. **The copying itself loses skill each generation.** A child copies only about
  two-thirds of its teacher's choices (W3e), and it copies only during a fading childhood. Every generation starts a
  little below its teacher, and choosing the teacher cannot make up for that.

## What it means (the assistant's reading)
1. **Cumulative culture needs more than picking good teachers here.** The transmission is too lossy: the child ends
   up below the teacher whoever the teacher is.
2. **Candidates for the next rung:**
   - a longer or stronger childhood with the chosen teacher, so the copy is closer to the original;
   - several teachers per life (learning the best of each);
   - the child's own learning adding on top (W3g's food memory, the box-task recipe), so that each generation can
     exceed its teacher, not only approach it.
3. **For the starting brain:** a parent's childhood is the strongest part so far (W3d), but skill does not yet
   accumulate across generations. The readiness bar (survival ≥ 0.80) is still far: the best is 0.14.
