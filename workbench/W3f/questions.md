# W3f: choosing whom to learn from, over generations (plan, frozen before any code or data)

**Frozen** as git tag `W3f-frozen`, before any code or data.
- **Sign-off:** the assistant, under the creator's "do not ask me for next steps just go ahead".
- **Council:** `../W3f_council_2026-11-16.md`. Adopted: an observable success cue (ChatGPT); chained generations
  (Gemini, DeepSeek).
- **Exploratory.**

## Why
W3e: skill passes from a learned parent but decays toward about 500 steps (806 → 549 → 473), with no ratchet.
Cumulative culture is thought to need choosing better models (Enquist et al. 2007). Here each child had one parent,
whatever its skill.

## The design
- **The adult pool for generation 1:** W3e's 8 G2 brains.
- **Visible success:** each adult in a pool is watched living on 5 demonstration lands (W3's calibration lands
  800001–800005, learning off, sampled with a generator per land). Its visible success is its mean lifespan there.
  - Computed once per pool, before the generation trains (`pool_<arm>_<gen>.json`).
- **The child:**
  - W3d's fading childhood (copy every 4th step, weight 0.5 → 0 over the first 400,000 of 2,000,000 steps) plus the
    recipe (Y + FR);
  - **in each life of its childhood it meets 4 adults** drawn from the pool, with `[seed, 61, gen, life]`;
  - it copies one adult's argmax act on its own view, the same adult for the whole life:
    - **CH:** the adult with the highest visible success among the 4;
    - **RN:** a random one of the same 4, with `[seed, 62, gen, life]`.
- **Chaining:** CH generation k + 1 draws from CH generation k's 8 children; RN from RN's. Generation 1 of both draws
  from the G2 pool.
- **Three generations (k = 1, 2, 3), 8 seeds each, on GitHub's machines;** each generation is a stage after the
  last.

## Measures
W3's test, alone, on the 50 test lands: survival to 3,000, to 1,000, lifespan.

## Readings (95% bootstrap intervals over the 8 seeds, paired by seed; numpy seed 20261135)
1. **"Choosing helps in one generation":** CH1 − RN1 on lifespan.
2. **"Choosing beats the average teacher":** CH1 − the G2 pool mean (549); CH1 against the best G2 adult.
3. **"A ratchet":** CH's lifespan across generations 1 → 3 (CH3 − CH1), against RN's (RN3 − RN1); and CH3 − RN3.

## Validity (hard stops)
- **Checks All: PASS before data:**
  - CH picks the pool adult with the highest visible success among its 4, and RN a random one;
  - draws are the same for CH and RN, so the same 4 adults are met;
  - the copied act is the chosen adult's argmax;
  - adults never change;
  - with no childhood, the loop reproduces W3b's YFR;
  - a split run equals an unsplit run.
- Every run finishes, or is reported.

## The assistant's prior
- **Reading 1:** about 55%.
- **Reading 2** (CH1 above 549): about 60%.
- **Reading 3** (CH rises over generations while RN does not): about 25%.
