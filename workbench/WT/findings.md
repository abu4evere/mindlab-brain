# WT findings: a teacher who is sometimes absent (exploratory; numbers from `analyse_wt.py`)

Plan: `questions.md` (WT-frozen). Checks All: PASS before data (`checks.log`). Run 14 November 2026, 16:11–19:35,
locally at Idle: 4 evolution runs (p = 0.5 and p = 0.2, two each) × 30 generations × 32 children, then 5 brains × 48
fresh children in each world. Full tables: `analysis.md`. Mind Lab: exploratory, no council, no blind recompute.

## 1. Evolution still chose big brains, born big, in every run
| world | run | born (median) gen 0 → gen 29 | evolved schedule |
|---|---|---|---|
| p = 1 (WE) | 1, 2 | 24 → 100; 39 → 182 | born 100 → 119; born 182 → 205 |
| p = 0.5 | 1, 2 | 57 → 141; 24 → 174 | born 141 → 149; born 174 → 203 |
| p = 0.2 | 1, 2 | 38 → 214; 18 → 218 | born 213 → 225; born 218 (no growth) |

- **Priors:**
  - "born at 64 or less" (p = 0.2: about 50%; p = 0.5: about 30%): **no** in all four runs;
  - if anything, the rarer the teacher, the bigger the brain.

## 2. With a teacher often absent, the big brains are the better learners too
**Teacher present on 1 try in 5 (p = 0.2), 48 fresh children each:**

| brain | own skill day 30 | own skill day 60 | after a showing, day 30 | lifetime food |
|---|---|---|---|---|
| E1 (born 213) | 0.653 | 0.875 | 0.976 | 1284 |
| E2 (born 218) | 0.646 | 0.858 | 0.990 | 1268 |
| M128 | 0.583 | 0.826 | 0.778 | 1140 |
| GA (16→128) | 0.139 | 0.608 | 0.104 | 727 |
| M32 | 0.118 | 0.476 | 0.080 | 641 |

- **E − GA, day 60:** E1 +0.267 [+0.215, +0.319]; E2 +0.250 [+0.198, +0.306].
- **E − M128, day 60:** E1 +0.049 [0.000, +0.097]; E2 +0.031 [−0.024, +0.083].
  The prior "at least as good as M128" (about 65%): **yes**.
- **M32 − M128, food:** −499 [−545, −452]. **GA − M128, food:** −412 [−450, −374].
  The prior "M32 or GA earns more food than M128" (about 45%): **no**.

**Teacher present on half the tries (p = 0.5):**
- **Day 60:**
  - E1 0.889, E2 0.892, M128 0.882;
  - GA 0.764, M32 0.712.
  - E1 − GA +0.125 [+0.083, +0.167]; E − M128 about 0.
- **Day 30:** E1 0.625, M128 0.656, GA 0.403, M32 0.420.

## 3. What changed from WE (a reading, not a tested cause)
**Big brains own the skill differently depending on the world:**

| own skill at day 30, M128 | own skill at day 30, M32 | world |
|---|---|---|
| 0.049 | 0.274 | teacher on every try (WE) |
| 0.656 | 0.420 | teacher on half the tries |
| 0.583 | 0.118 | teacher on 1 try in 5 |

- **With a teacher on every try,** the big brain leans on the showing and barely learns alone (WN and WE).
- **When the teacher is often missing,** it has to try alone. Its size then makes it a fast learner from few
  showings: by day 60, 0.83 to 0.89 in every world.
- **The small and growing brains depend on plenty of teaching.** M32 at day 60: 0.90 with a teacher always there,
  0.71 at half, 0.48 at 1 in 5.
- **So big was never bad in itself.**
  - Big with a teacher always present made a copier.
  - Big with a teacher often absent made the best learner of all.
  - Evolution chose big in every world. In the two absent-teacher worlds that was also the best choice for owning
    the skill, not only for food.

## Limits
- Small populations; 30 generations; two runs per world.
- **No cost for neurons:** a cost would press against big brains, and choosing one belongs to the creator.
- One small task; fixed learning rates. "Big" here is at most 256 neurons.

## For the brain plan
- **WN's "32 is best" holds only when a teacher shows every try.** With scarce teaching, more neurons (here up to
  about 220) learn better from each showing.
- **The parrot risk comes from a world that always teaches, not from size.** Bob's world should not hand him a
  teacher on every try.
- Next questions (the creator's choice):
  - a cost for neurons;
  - larger sizes;
  - a task that changes, where old copies go stale.
