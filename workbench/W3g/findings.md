# W3g findings: a memory of where it has eaten (16 November 2026)

**Plan:** `questions.md` (W3g-frozen; exploratory; no council, the creator's go-ahead). Checks All: PASS before data
(6).
- One deviation is recorded: with the channel held at zero, training matches W3d's within 1e-10, not bit for bit.
- 8 cloud jobs, all closed by 20:37. The frozen `analyse_w3g.py` gives `analysis.md`.
- n = 8 seeds × 50 test lives.

## The frozen readings
1. **"It lives longer": no, it lives shorter.** FM − PYFR lifespan −153 [−316, −3]; survival −0.055 [−0.120, 0.000].
   FM lives 654 steps and survives 0.073; PYFR lives 806 and survives 0.128.
2. **"It dies less for lack of known food": no.** "No food known" is still 0.77 of FM's 371 deaths (W3d: 0.80).
   Exhaustion is 0.52 (W3d: 0.63), and food known but not reached is 0.31 (W3d: 0.27).
3. **Toward the bar (0.80):** 0.073, far below.

**The priors:** reading 1 about 40%: no (the other way). Reading 2 about 35%: no. Reading 3 about 3%: no.

## Exploratory (after the data, labelled): did it use the new sense?
The mean absolute weight on the "eaten here" channel in the first layer, against the other five channels, over the 8
brains: 0.04–0.07, against about 0.07–0.42.
- **It learned to read the channel a little,** but not into "go back to where I ate".
- With the same learning budget, the extra input seems to have cost more than it gave.

## What it means (the assistant's reading)
1. **Giving the memory is not enough:** the brain must also learn when to return, and its sparse reward does not
   teach that within one childhood.
2. **Where it should be fixed:**
   - in the parent's teaching: the Script parent does return to old patches, but its returns are rare moments in the
     copying;
   - or as an inborn pull: like hunger's link to food, staleness × "eaten here" as a built-in value. This is
     engineered, and would have to be labelled.
3. W3d's PYFR stays the best brain (survival 0.128).
