# W3l: the longer childhood with the kept copy, and longer still (plan, frozen before any data)

**Frozen** as git tag `W3l-frozen`.
- **Sign-off:** the assistant, under the creator's sleep-mode autonomy (18 November 2026: "from now on only focus on
  project in sleep mode just go ahead yourself").
- **Council:** `../W3l_council_2026-11-19.md` (GPT answered; Gemini's answer did not load, recorded there). Draft:
  `../W3l_draft.md`.
- **Exploratory,** in the W3 series. A **pre-specified follow-up** of W3k: CS is cited from W3k, where it was already
  seen, so reading 1 is not an independent confirmation of CS.

## Why (W3k)
- Keeping an earlier copy of itself works: CS − R2 +199 [+70, +347]. Best brain yet: CS, lifespan 1,835, full lives
  0.478, fresh-land survival 0.445 (bar 0.80). A copy at a step drawn in advance did about as well (CS − CY +43).
- The longer childhood (C3: 3.6M fade of 5.2M) was not separated on lifespan (C3 − R2 +117 [−193, +432]), but its curve
  stopped declining after childhood, and its fresh-land survival was the highest (0.460).
- W3k's C3 runs kept a copy too, but did not save it. Runs are bit-identical across machines, so retraining C3 gives
  the same brain, and this time both copies are saved.

## Arms (W3k's code and settings, `w3l.py`; 16 seeds, 1–16; GitHub's verified machines)
| arm | run | brain |
|---|---|---|
| **C3** | 5.2M steps, 3.6M fade (W3k's C3 again) | the end |
| **C3S** | the same run | the copy kept by its own lives (W3k's CS rule) |
| **C3Y** | the same run | the copy at a step drawn in advance (W3k's CY rule; draw seed 20261191 + run seed) |
| **C5** | 6.4M steps, **4.8M fade** (the same 1.6M alone) | the end |
| **C5S** | the same run | the copy kept by its own lives |
| **C5Y** | the same run | the copy at a step drawn in advance |
| CS (cited) | W3k's run R (4.0M steps, 2.4M fade) | its kept copy, tested in W3k on the same lands |

- **The one code change from W3k:** every run saves its two copies (W3k saved them for run "R" only), and CY's step is
  drawn for every run. Training is W3k's: the copies only read the brain.
- **The reproduction check (GPT's wording taken):** C3's end weights against W3k's C3, every named weight array (not
  file hashes), and C3's kept-copy step against the one W3k recorded. W3k's files stay untouched in `W3k/output`.
  Reported whatever it shows.
- Snapshots after the fade every 400,000 steps (tested), as W3k.
- **One fixed final test for every arm (GPT):** W3's 50 test lands and the 50 fresh lands (910001–910050), alone,
  learning off, the parent absent. The copies are chosen only from the brain's own training lives, never a test.

## Measures (W3k's)
Lifespan; survival to 3,000 and 1,000; fresh-land survival; drift; parent agreement; the step each copy comes from.
**Exploratory (after the readings, local, read-only):** the death causes (WX's labels) of the best arm's test lives.

## Readings (`analyse_w3l.py`, frozen; paired by seed; bootstrap over 16 seeds, numpy seed 20261190)
1. **Two primary readings (Bonferroni: 97.5% intervals, lower bound above 0):**
   - **"The longer childhood (and 1.2M more steps in total) adds to the kept copy":** C3S − CS on lifespan. It tests a
     longer childhood and more training together, both under the kept copy (GPT); the time alone is equal (1.6M).
   - **"An even longer childhood helps":** C5S − C3S on lifespan (the deployable brain of each recipe). C5 − C3 (the
     ends) is reported beside it: if C5S gains and C5 does not, the gain is in the chosen copy, not the end.
2. **Secondary (95%):** C3S − C3; C5 − C3; C3S − C3Y; C5S − C5Y.
3. **Toward the bar:** the best arm's fresh-land survival against 0.80.
4. Medians, seeds above 0 and leave-one-seed-out means beside the two primary readings.

## Validity (hard stops)
- Checks All: PASS before data (`checks_w3l.py`, 10 checks: settings; schedules; hooks leave training unchanged; the
  copies follow their rules; a run other than R saves both copies; split = unsplit; outputs in W3l).
- The reproduction check is reported, whatever it shows; if it fails, reading 1 is still read (paired by seed), and the
  failure is stated.

## What comes next (decided now)
If W3l shows no clear gain, childhood length is set aside (GPT: three lengths are enough), and the next study goes at
the deaths directly: finding food, remembering where it regrows, and managing tiredness.

## The assistant's prior
- C3S − CS above 0: about 30% (GPT 32%). C5S − C3S above 0: about 35% (GPT 27%). C3S − C3 above 0: about 25%.
- The reproduction check exact: about 85% (GPT 92%). Any arm at 0.80 on fresh lands: about 2% (GPT 2%).
