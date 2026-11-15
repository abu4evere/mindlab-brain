# WC: a world that changes (plan, frozen before any code or data)

**Frozen** as git tag `WC-frozen`, before any code or data.
- **The creator** (14 November 2026): "go ahead with the changing task test", after WT.
- In WT, with a teacher present on only some tries, evolution chose big brains (141–218 neurons), and they owned the
  skill best.
- **Here the world changes after the teacher has gone.** Old copies go stale, and the new answers must be found alone,
  by trial and error. This is the creator's aim: "It's learning from them" (from mistakes).
- **Exploratory, as WN to WT:** the creator asked for it directly, so there is no council.

## The world
- **WT's world with p = 0.5:** on days 1–30 the teacher is present on each try with probability 0.5 (the world's
  draws, `[seed, 5, day]`), showing the codes as they are then. No teacher on days 31–60.
- **The change:**
  - **at the start of day 31,** kinds 0, 1 and 2 (group A) get new codes;
  - **at the start of day 46,** kinds 3, 4 and 5 (group B) get new codes.
- **New codes** are drawn by the world (`[seed, 8]`): for each lid of a changed kind, a new ordered pair of acts,
  never the same as that lid's old pair. The two lids of a kind stay different.
- **Everything else is WE/WT's:** 2 lids; 3 tries per kind per day; 60 days; copy rate 0.5; learning rate 0.05; the
  memory ring; "awake in, quiet out" growth.
  - **Food** = lids opened in the practice tries, judged by the codes of that day.

## Evolution (WE's, unchanged, in this world)
- 4 genes; population 32; 30 generations; 2 runs.
- Evolution seeds `[run, 78]`; child seeds as WE.
- Parents in proportion to food + 1; no cost for neurons.

## Final test (48 fresh children, seeds 1001–1048, in this world)
- **The brains:**
  - **E1, E2:** evolved here (the median genes of each run's last generation);
  - **T1, T2:** WT's p = 0.5 evolved schedules (evolved without change; `../WT/evolved_p50.json`);
  - GA, M32, M128 and M256.
- **Tests:** at days 30, 33, 38, 45, 48, 53 and 60; no showing; each kind tried once; full box = success.
- **Measures:**
  - own skill on group A and group B at each test day;
  - **relearning:** group A at days 33, 38 and 45; group B at days 48, 53 and 60;
  - **keeping:** group B at day 45, before its change;
  - **stale habit:** the share of changed kinds whose first lid still gets its old pair, at days 33 and 48;
  - lifetime food;
  - paired differences with 95% bootstrap intervals (numpy seed 20261118, 10,000 resamples).
- **Gene paths:** each run's mean genes, and the median born and final size per generation.

## The questions (descriptive)
1. Do bigger brains relearn changed codes faster or slower than small ones? M256 − M32 and M128 − M32 on group A at
   day 45 and group B at day 60.
2. Does evolution in a changing world choose differently from WT's (born size, growth)?
3. Do brains evolved here relearn better than brains evolved in a world without change? E − T on group A at day 45
   and group B at day 60, and food.

## Limits (stated now)
- Small populations; 30 generations; two runs.
- No cost for neurons; one small task; fixed learning rates.
- Two changes only, at fixed days.

## The assistant's prior
- **Q1:** M128 relearns at least as well as M32 (on both readings, the interval not below 0): about 55%.
- **Q2:** evolution here ends with a median born size of 64 or less, in both runs: about 20%.
- **Q3:** E beats T on group B at day 60 (interval above 0): about 25%.
- **The stale habit:** at day 33, at least half of group A still gets its old first-lid pair, for M128: about 50%.
