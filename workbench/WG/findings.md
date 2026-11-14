# WG findings: growing with awake neurons (exploratory; 48 children per brain; numbers from `analyse_wg.py`)

Plan: `questions.md` (WG-frozen). Checks All: PASS before data (`checks.log`). Run 14 November 2026, 13:41–13:51,
locally at Idle, 336 children. Full table: `analysis.md`. Mind Lab: exploratory, no council, no blind recompute.

## Manipulation check: waking the new neurons made them used, but less than the born ones
- Mean |outgoing weight to the hands| at day 60, added over born:
  - G 0.023 [0.022, 0.024];
  - **GA 0.155 [0.149, 0.162]**;
  - GF 0.330 [0.319, 0.340];
  - GA32 0.237 [0.225, 0.250].
- GA's added neurons carry about 5 times G's weight (0.053 against 0.010).
- The prior ("at least half the born neurons'", about 75%) **did not hold**: used, but far less than the born
  neurons.

## Q1: waking makes growth work
- **GA − G:**
  - day 60: **+0.139 [0.097, 0.188]**;
  - after a showing at day 30: +0.240 [0.188, 0.295];
  - day 30: −0.028 [−0.083, 0.028].
- **GF − G:**
  - day 60: +0.125 [0.073, 0.177];
  - after a showing: +0.337;
  - **day 30: −0.125 [−0.177, −0.073]**. The jolt of fully awake neurons cost own skill during the teaching.
- The prior ("GA beats G at day 60", about 40%) was too low: it does.

## Q2: growing awake beats being born big
- **GA − M128:**
  - day 30: **+0.323 [0.264, 0.382]**;
  - day 60: **+0.128 [0.080, 0.177]**;
  - after a showing: −0.104 [−0.139, −0.073] (M128 is perfect, 1.000).
- **GF − M128:** day 30 +0.226; day 60 +0.115; after a showing −0.007 [−0.017, 0.000].
- The prior ("GA ahead of M128 at day 30", about 60%) held.
- **Descriptive, not a planned comparison:**
  - GA's day-60 skill, 0.934 [0.903, 0.962], is the highest of all seven brains;
  - next is M32, 0.920 [0.885, 0.951] (the intervals overlap);
  - GA ends with 128 neurons, while M128 born at that size reaches 0.806.
- **Reading (interpretation, not tested):**
  - while GA is small during the teaching, it learns the skill as its own (day 30: 0.365, like M16's 0.392);
  - the big-born brain leans on the teacher (0.042);
  - later, the added neurons give room.

## Q3: growing into 32 from 8 is worse than being born at 32
- **GA32 − M32:** day 30 +0.042 [−0.035, 0.118]; **day 60 −0.146 [−0.194, −0.101]**; after a showing −0.312.
- The prior ("level at day 60", about 55%) **did not hold**.
- So starting smaller is not always better. Starting at 8 seems too small, but this sweep cannot say why.

## Limits
- One small task; 60 days; fixed learning rates.
- One growth schedule per brain. GA beat M128, but it did not clearly beat M32 (a born brain of the best size).
- **The "start small" idea is known in the literature:** Elman 1993, "Learning and development in neural networks:
  the importance of starting small", from memory, not re-read today. It should be read before any next step.

## For the brain plan
- **If a brain grows, new neurons must start awake** (active inputs). Their outputs may start quiet (GA): that kept
  own skill during the teaching, and the brain still gained by day 60.
- **Growing from a modest start beat being born big,** both early (+0.32) and late (+0.13).
- **Growing from too small a start hurt** (GA32).
- Next questions (each needs the creator's OK): more than one task; a longer life; growth timed by the brain's own
  need instead of by the calendar; and growth as evolved genes (when and how much to grow).
