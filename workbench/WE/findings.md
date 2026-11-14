# WE findings: genes decide how the brain grows (exploratory; numbers from `analyse_we.py`)

Plan: `questions.md` (WE-frozen). Checks All: PASS before data (`checks.log`). Run 14 November 2026, 14:14–16:05,
locally at Idle: 2 evolution runs × 30 generations × 32 children, then 5 brains × 48 fresh children. Full tables:
`analysis.md`.
- The analysis script's first run wrote its files but failed printing a minus sign to the Windows console. It was
  re-run with `PYTHONIOENCODING=utf-8`; the numbers are unchanged.
- Mind Lab: exploratory, no council, no blind recompute.

## 1. Evolution chose big brains born big, not "born small, then grow"
- **Run 1:**
  - born size (median) 24 at generation 0 → 118 by generation 9 → 100 at generation 29;
  - growth gene g fell from 1.64 to 0.34;
  - evolved schedule: born 100, growing slowly to 119 over days 34–54.
- **Run 2:**
  - born 39 → about 50–72 in the middle generations → 182 at generation 29; g fell from 1.44 to 0.18;
  - evolved schedule: born 182, growing to 205 over days 21–28.
- **Mean food per child rose** in both runs: 1290 → 1539 and 1272 → 1528.
- The prior ("born at about 8–32 and grow during the teaching, both runs", about 45%) **did not hold**.

## 2. Final test (48 fresh children each)
| brain | own skill day 30 | own skill day 60 | after a showing, day 30 | lifetime food |
|---|---|---|---|---|
| E1 (born 100) | 0.073 | 0.830 | 1.000 | 1502 |
| E2 (born 182) | 0.042 | 0.792 | 1.000 | 1552 |
| GA (WG's hand-set growth, 16→128) | 0.382 | 0.927 | 0.896 | 1158 |
| M32 | 0.274 | 0.899 | 0.941 | 1191 |
| M128 | 0.049 | 0.812 | 1.000 | 1520 |

- **E − GA:**
  - E1: food +344 [314, 374]; day 60 −0.097 [−0.142, −0.052]; day 30 −0.309.
  - E2: food +395 [354, 436]; day 60 −0.135 [−0.188, −0.087].
- **E − M128:** level on every measure. E1 food −18 [−46, 10]; E2 food +33 [−3, 70]; day 60 intervals include 0.
- **Priors:**
  - "the evolved schedule beats GA at day 60" (about 25%): **no**, it is worse;
  - "the evolved schedule earns more food than M128" (about 70%): **no**, it is level.
- **In short, evolution rediscovered M128,** the brain born big.

## 3. Why (a reading, not a tested cause)
- In this world the demonstrator shows the box right before every try on days 1–30. A big memory replays the showing
  perfectly (1.000), so it earns full food through half its life without owning the skill.
- The smaller and growing brains own the skill better: day 30 0.38 against 0.07; day 60 0.93 against 0.83. But they
  earn about 30% less food over a life.
- **Selection by the world's payoff picked the copier, because this world pays the copier.**
  - The skill of one's own pays only on days 31–60, and the big brains are only somewhat worse there.
  - A world where the teacher is often absent, or where skill decides survival later in life, may select differently.
    This sweep cannot say.
- **This resembles a known result (Rogers 1988):** social learning can spread without making a population better at
  its own learning. Recalled from memory, not re-read today.

## Limits
- Small population, 30 generations, two runs.
- No cost for neurons. A cost would push against big brains, but it would be a design choice, so it needs the
  creator.
- One small task; fixed learning rates; the teacher always present on days 1–30.

## For the brain plan (the creator's aim: a mind that learns, not only copies)
- **The genes find what the world pays for.**
  - If Bob's world always hands him a teacher, evolution may build a perfect copier that learns less on its own.
  - What evolution builds depends on when teachers are there and when one's own skill decides food.
- **Possible next questions (each needs the creator's OK):**
  - the same evolution with a teacher who is sometimes absent;
  - the same with a longer life after the teaching;
  - the same with a cost for neurons.
