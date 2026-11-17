# W3i: more practice, a longer childhood. Is the best brain just too young? (plan, frozen before any code was run or data)

**Frozen** as git tag `W3i-frozen`.
- **Sign-off:** the creator, 16 November 2026: "alr lets go with 2 and 1" (option 1: "train the best brain 3× longer,
  and give it a longer childhood").
- **Council:** `../W3i_council_2026-11-16.md` (GPT, Gemini; all changes listed there).
- **Exploratory,** in the W3 series.

## Why
- **The best brain** (W3d's PYFR) lives 806 steps and survives 0.128. The creator's bar is 0.80.
- **WX:** 0.80 of its deaths come with no food known.
- **Two levers not yet tried:**
  - **more practice** (in W1e the same planner was still improving at 500,000 episodes);
  - **a longer childhood** (W3d's parent fades out over the first 400,000 steps of 2,000,000; a parent who never
    leaves was worse).
- **The council's warning:** if the failure is stale memory, neither lever may fix it. The stale-food measures below
  are there to see.

## The arms (W3d's PYFR unchanged except steps and fade length; 8 seeds, the same as W3d's; GitHub's machines)
| arm | training steps | the parent fades out over | alone afterwards |
|---|---|---|---|
| **L** | 6,000,000 | 400,000 | 5,600,000 |
| **LC** | 6,000,000 | 1,200,000 | 4,800,000 |
| **C** | 2,800,000 | 1,200,000 | 1,600,000 (as PYFR) |
| cited: **PYFR** (W3d) | 2,000,000 | 400,000 | 1,600,000 |

- **Snapshots (exploratory):** L and LC are saved and tested at the first life boundary after 2,000,000 and
  4,000,000 steps.
- **The reproduction job (R):** W3d's PYFR seed 1 is trained again on GitHub, 2,000,000 steps, and its weights are
  compared with W3d's saved `PYFR_1.npz`.
- **Nothing is scheduled on the total steps** (learning rate, entropy and replay are constant; checked in code).

## Measures (W3's 50 test lands, alone, learning off)
1. Lifespan; survival to 3,000 and to 1,000.
2. **Stale-food arrivals:** steps arriving at a cell the memory shows as full food that is really empty, per 1,000
   steps.
3. **The time since the last meal at death.**
4. **WX's death labels:** no food known, exhaustion, food known but not reached.
5. Survival on **50 fresh lands** (seeds 910001–910050), every arm.

## Readings (95% bootstrap over the 8 seeds, paired by seed; numpy seed 20261138)
1. **"More practice helps":** L(6M) − PYFR on lifespan, lower bound above 0.
2. **"A longer childhood helps, with equal practice":** LC(6M) − L(6M) on lifespan, lower bound above 0.
3. **Secondary:** C − PYFR on lifespan (equal adulthood, more childhood), reported.
4. **Toward the bar:** the best arm at 6M (or C), its survival on the fresh lands against 0.80.
5. **Does the failure change:** stale-food arrivals and "no food known" deaths, L and LC against PYFR, reported.

## Validity (hard stops)
- **Checks All: PASS before data:**
  - the fade weights per arm (0.5 → 0 over the arm's fade, none after);
  - a split run equals an unsplit run;
  - the same seed twice is the same;
  - a snapshot does not change the run (a run snapshotted at a life boundary continues exactly as one that was not);
  - the stale-food counter counts only arrivals on remembered-full, really-empty cells.
- Every run finishes, or is reported.
- **The reproduction job is reported** whatever it shows. If it differs, the PYFR comparisons are read as "the same
  procedure on another machine", not as bit-replicas.

## The assistant's prior
- Reading 1: about 50%.
- Reading 2: about 35%.
- The best arm reaches 0.80: about 2%.
