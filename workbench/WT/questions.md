# WT: a teacher who is sometimes absent (plan, frozen before any code or data)

**Frozen** as git tag `WT-frozen`, before any code or data.
- **The creator** (14 November 2026): "go ahead with the absent teacher test", after WE.
- In WE, with a teacher before every try on days 1–30, evolution chose brains born big (100 and 182 neurons) that
  replay the showing perfectly. They earned more food but owned the skill less (day 60: 0.83 and 0.79, against 0.93
  for WG's hand-set growing brain).
- **The question:** when the teacher is often absent, does evolution choose differently?
- **Exploratory, as WN, WG and WE:** the creator asked for it directly, so there is no council.

## The change (only this; everything else is WE's)
- **Days 1–30:** each try has the teacher present with probability p.
  - **Present:** as before. The box is shown, the child takes a copy step, then tries with the showing in memory.
  - **Absent:** no showing and no copy step. The child tries alone.
- **Days 31–60:** no teacher, as before.
- **Presence draws:** they come from the world (`[seed, 5, day]`, one per try), so every brain in the same world
  meets the same absences.
- **Two levels:** p = 0.5 and p = 0.2. WE is the p = 1 reference; its numbers are cited, not re-run.

## Evolution (WE's, unchanged)
- 4 genes (born size, growth, first and last growth day).
- Population 32, 30 generations.
- Parents in proportion to food + 1; WE's mutation; no cost for neurons.
- Two runs per level, evolution seeds `[run, 77, p×100]`. Child seeds as WE (100000 × run + 1000 × generation +
  index).
- Food = lids opened in the practice tries over 60 days.

## Final test (each level)
- Each run's evolved schedule (the median genes of its last generation) on 48 fresh children (seeds 1001–1048), in
  the same p world, beside WG's GA (16 → 128 at the end of days 8, 16 and 24), M32 and M128.
- **Measures:**
  - own skill at days 30 and 60;
  - after a showing at day 30;
  - lifetime food;
  - paired differences with 95% bootstrap intervals (numpy seed 20261117, 10,000 resamples).
- **Gene paths:** each run's mean genes and median born and final size per generation.

## Limits (stated now)
- Small populations; 30 generations; two runs per level.
- No cost for neurons; one small task; fixed learning rates.

## The assistant's prior
- **p = 0.2:** in both runs, evolution ends with a median born size of 64 or less: about 50%.
- **p = 0.5:** the same: about 30%.
- **The evolved brain at p = 0.2 owns the skill at least as well as M128 at day 60** (the E − M128 interval not
  below 0): about 65%.
- **At p = 0.2, M32 or GA earns more lifetime food than M128** (the interval above 0): about 45%.
