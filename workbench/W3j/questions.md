# W3j: keep what the parent taught (plan, frozen before any code was run or data)

**Frozen** as git tag `W3j-frozen`.
- **Sign-off:**
  - the creator's standing "do not ask me go ahead bro";
  - and, 17 November 2026: "bro also do not forget about our main project you gotta do all things simultaneously".
- **Council:** `../W3j_council_2026-11-17.md` (GPT, Gemini).
- **Exploratory,** in the W3 series.

## Why
W3i's best brain (C: a 1.2M-step fading childhood within 2.8M steps) lives 1,248 steps and survives 0.255. But every
brain peaked soon after childhood and then declined while it kept learning alone. The hypothesis: adult learning from
sparse feelings wears away what the parent taught.

## Arms (C's settings unless stated: W3d's PYFR with a 1.2M fade; no pain; 8 seeds, W3i's; GitHub's machines)
| arm | change from C | role |
|---|---|---|
| **CK** | the learning rate × 0.1 for every update (actor-critic, "that worked!", replay) from the first life boundary after the fade | settle down |
| **CF** | the brain frozen at the end of the fade (CK's snapshot at the first life boundary after 1.2M; identical to C's own brain at that point) | the frozen control |
| **CV** | after the fade, the parent's copy weight stays at 0.05 (every 4th step) instead of 0 | a quiet parent |
| **C4** | 4.0M steps (1.2M fade) | more steps, the same childhood |
| **C2** | 4.0M steps, 2.4M fade | a longer childhood, the same steps as C4 |
| cited: **C** (W3i) | 2.8M steps, 1.2M fade | the reference, paired by seed |

- **The reproduction job:** C seed 1 retrained with W3j's code must equal W3i's `C_1.npz`.
- **Snapshots** at the first life boundary after the fade, then every 400,000 steps. The final checkpoint is primary.

## Measures (W3's 50 test lands, alone, learning off; the parent is never present in a test)
1. Lifespan; survival to 3,000 and to 1,000; survival on the 50 fresh lands (W3i's 910001–910050).
2. **Policy drift:** on the final brain's own test lives, the share of steps where its greedy move differs from the
   end-of-fade brain's greedy move.
3. **Agreement with the parent:** the share of steps where the final brain's greedy move equals what W3's Script would
   do on the same map view.
4. WX's death labels.

## Readings (95% bootstrap over the 8 seeds, paired by seed; numpy seed 20261139)
1. **Primary, "Settling down keeps it":** CK − C on lifespan, lower bound above 0.
2. **Secondary:**
   - "Adult learning hurts": CF − C, lifespan;
   - "A quiet parent keeps it": CV − C;
   - "A longer childhood, at equal steps": C2 − C4;
   - "More steps, the same childhood": C4 − C;
   - each reported with its interval, read with the same rule.
3. **Toward the bar:** the best final arm's fresh-land survival against 0.80.
4. **The reading of CF against CK** (GPT):
   - if CF ≥ CK, the adult learning itself is the problem, not the speed of adult learning;
   - if CK > CF, slow adult learning adds something.

## Validity (hard stops)
- **Checks All: PASS before data:**
  - CK's learning rate changes only after the fade snapshot;
  - CV's copy weight is 0.05 after the fade, on every 4th step;
  - C4 and C2 fade correctly;
  - a split run equals an unsplit run;
  - the same seed twice is the same;
  - the drift and parent-agreement measures on a hand-made case.
- The reproduction job is reported whatever it shows.

## The assistant's prior
- Reading 1 (primary): about 45%.
- CF − C positive: about 50%.
- CV − C: about 35%.
- C2 − C4: about 40%.
- Any arm reaches 0.80 on fresh lands: about 1%.
