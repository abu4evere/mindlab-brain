# W3j findings: keep what the parent taught (18 November 2026, about 04:30 UTC)

**Plan:** `questions.md` (W3j-frozen; council `../W3j_council_2026-11-17.md`). Checks All: PASS (9) before data.
- **Runs:** 33 cloud jobs (8 seeds × 4 arms, and the reproduction job). The 4M runs paused and resumed. All closed at
  23:24 on 17 November (local time).
- The frozen `analyse_w3j.py` gives `analysis.md`. n = 8 seeds × 50 test lives.
- **The reproduction job is NOT exact.** See the section below: it changes how three readings can be read.

## The frozen readings
| arm | change from C | lifespan | survived | to 1,000 | fresh lands: survived | drift | agrees with the parent |
|---|---|---|---|---|---|---|---|
| C (W3i, cited) | | 1,248 | 0.255 | 0.405 | 0.235 | – | – |
| CK | learning rate × 0.1 after the fade | 1,112 | 0.208 | 0.363 | 0.170 | 0.50 | 0.30 |
| CF | frozen at the end of the fade | 856 | 0.105 | 0.263 | – | – | – |
| CV | the parent stays, copy weight 0.05 | 599 | 0.048 | 0.140 | 0.045 | 0.42 | 0.50 |
| C4 | 4.0M steps, 1.2M fade | 830 | 0.145 | 0.242 | 0.165 | 0.65 | 0.23 |
| **C2** | 4.0M steps, **2.4M fade** | **1,594** | **0.363** | **0.535** | **0.380** | 0.51 | 0.31 |

1. **PRIMARY, "settling down keeps it": no.** CK − C −136 [−504, +191].
2. **Secondary:**
   - "Adult learning hurts" (CF − C): −393 [−688, −108]. **No: the opposite.** The brain at the end of childhood is
     worse than the same brain after its adult learning. Adult learning first helps, then (W3i's curves) wears away.
   - "A quiet parent keeps it" (CV − C): −649 [−982, −308]. **No: it hurts a lot.** The child agrees with the parent
     more (0.50 against 0.30) and lives much shorter.
   - **"A longer childhood, at equal steps" (C2 − C4): +764 [+376, +1,154]. Yes.**
   - "More steps, the same childhood" (C4 − C): −419 [−813, −69]. More practice alone hurts again (as in W3i).
   - CK against CF: +256 [−209, +690], not separated.
3. **Toward the bar:** the best arm is **C2, the best brain yet**: fresh-land survival 0.380 [0.275, 0.493] (W3i's C
   0.235). The bar is 0.80.

**The priors:**
- reading 1 (about 45%): no;
- CF − C positive (about 50%): no, negative;
- CV − C positive (about 35%): no;
- C2 − C4 positive (about 40%): yes.

## The learning curves (exploratory: snapshot tests, mean lifespan over seeds)
| | 1.2M | 1.6M | 2.0M | 2.4M | 2.8M | 3.2M | 3.6M | final |
|---|---|---|---|---|---|---|---|---|
| CK | 856 | 1,255 | 1,127 | 1,079 | | | | 1,112 (2.8M) |
| CV | 499 | 558 | 345 | 362 | | | | 599 (2.8M) |
| C4 | 792 | 1,255 | **1,315** | 1,283 | 1,068 | 1,074 | 833 | 830 (4.0M) |
| C2 | | | | 1,375 | **1,832** | 1,773 | 1,810 | 1,594 (4.0M) |

- **CK, C4 and C2 peak 0.4 to 0.8M steps after their childhood ends, then decline.** Slowing the learning (CK) did
  not stop the decline. CV, with a little copying kept on, stays low throughout (345 to 599).
- C2's peak (1,832 at 2.8M) is the highest lifespan seen in the W3 series. It was picked after the data, so it is
  an optimistic number, not a result.

## The reproduction job, and what it changes (stated, not hidden)
- **The frozen check:** C seed 1, trained again with W3j's code, should equal W3i's `C_1.npz`. It does not (largest
  weight difference 0.27).
- **Exploratory, after the data** (`explore/repro_check.py`): on the same 50 test lands, the reproduced brain lives
  797 steps, against 1,547 for W3i's. Same seed, same settings, half the lifespan.
- **Where the runs split:** the training logs are identical for 2,642 lives (775,879 steps), then differ. Comparing
  every pair of runs that should match:

  | seed | C vs CK | C vs C4 | CK vs C4 | CK vs CV |
  |---|---|---|---|---|
  | 1 | 1,200,667 | 775,879 | 775,879 | 1,199,300 |
  | 2 | 555,740 | 555,740 | 1,200,155 | 555,740 |
  | 3 | 1,200,029 | the whole 2.8M | 1,200,029 | 1,200,029 |
  | 4 | 204,190 | the whole 2.8M | 204,190 | 203,974 |
  | 5 | 1,202,100 | 525,024 | 525,024 | 525,024 |
  | 6 | 1,200,203 | 58,755 | 58,755 | 58,755 |
  | 7 | 46,401 | the whole 2.8M | 46,401 | 1,199,149 |
  | 8 | 374,676 | 374,676 | 1,200,017 | 1,200,017 |

  (the step where two runs first differ; about 1.2M is the fade, where the arms are meant to split)
- **The assistant's reading:** the code is the same for these runs: some pairs match for all 2.8M steps, and the code
  paths for C were compared line by line. Runs on GitHub's machines are not bit-identical: a tiny numerical difference
  (most likely a different processor on a different runner) appears at a random step and then grows. W3i's
  reproduction was exact, probably by landing on the same kind of machine. Not confirmed; the runner hardware was not
  logged.
- **What it changes:**
  - The pairing by seed is only partly real. In about half the seeds the arms are not the same brain up to their
    split. The intervals still estimate the mean differences, but they are wider than a true pairing would give.
  - **CF is "C's own brain at the end of childhood" only in seeds 1, 3, 5 and 6.** In those four, CF lives shorter
    than C in three (669 vs 1,547; 466 vs 785; 816 vs 1,971; the fourth 1,252 vs 1,057). This agrees with the frozen
    reading.
  - Where C4 really is C plus 1.2M more steps (seeds 3, 4, 7), the extra steps lowered lifespan in all three (785 → 194,
    1,671 → 1,530, 1,371 → 1,272). This agrees with "more practice alone hurts".
  - **C2 − C4 does not depend on this.** Both are W3j's own runs, and the gap is large.
  - **Seed noise is huge.** One tiny numerical difference halved a brain's lifespan. Eight seeds are few for effects
    this size. Future studies should log the runner's processor and use more seeds.

## What it means (the assistant's reading)
1. **A longer childhood is the strongest lever, for the third time** (W3d, W3i, W3j). Doubling the fade from 1.2M to
   2.4M steps, at equal steps, gave the best brain yet. Fresh-land survival is 0.38: about halfway from W3d's start
   (0.13) to the bar.
2. **The decline after childhood is real, and the simple fixes fail.** A slower learning rate does not stop it, and a
   lingering parent makes it worse. So "learning alone wears away the lesson" is not about speed.
3. **A quiet parent is worse than no parent.** The child copies the parent more and lives shorter. Weak, rare copying
   seems to fight the brain's own learning instead of guiding it. This matches W3d, where "parent forever" was worse
   than a fading parent.
4. **Next steps, for the brain plan:**
   - a still longer childhood (fade 3.6M of 4.8M);
   - stopping adult learning at its best point, judged by the brain's own life, not by a test;
   - replaying the parent's examples during adult learning (the council's suggestion) instead of a live parent.
