# W3g: a memory of where it has eaten (plan, frozen before any code or data)

**Frozen** as git tag `W3g-frozen`, before any code or data.
- **Sign-off:** the assistant, under the creator's "do not ask me for next steps just go ahead" (16 November 2026).
- The creator was told of it (about 16:3x) and answered "alr good".
- **Exploratory; no council** (the creator's direct go-ahead on this line).

## Why
WX found that 80% of the best brains' deaths came with no food remembered as full.
- Food regrows after 200 steps, but the map memory shows an eaten cell as empty until it is seen again, and the brains
  do not return to check old feeding places.
- Script survives by searching the places it has not seen for longest.

## The new part: "I have eaten here"
- **A sixth map channel:** 1 on every cell where the brain has eaten in this life, 0 elsewhere.
- **It says nothing about regrowth or timing.** Whether and when to return must be learned, with W3's existing
  staleness channel.
- **The weights for the new channel start at zero,** and every other starting weight is W3d's. So at birth the brain
  acts exactly like W3d's PYFR child of the same seed, and differs only as it learns to use the new sense.

## The design
- **W3d's PYFR exactly** (parent childhood fading over 400,000 steps, the recipe Y + FR, 2,000,000 steps, W3's world
  and test), plus the channel.
- **Arm FM;** reference W3d's PYFR (cited, paired by seed: the same starting weights, lands and test).
- 8 seeds, on GitHub's machines.

## Measures and readings (95% bootstrap intervals over the 8 seeds, paired; numpy seed 20261136)
1. **"It lives longer":** FM − PYFR on lifespan and on survival to 3,000.
2. **"It dies less for lack of known food":** WX's death labels for FM (the same recorder), against W3d's 0.80 for "no
   food known".
3. **Toward the bar:** FM's survival against the creator's readiness bar (0.80).

## Validity (hard stops)
- **Checks All: PASS before data:**
  - with the new channel held at zero, the training reproduces W3d's PYFR training exactly;
  - the channel marks exactly the cells eaten at;
  - the new channel's weights start at zero;
  - a split run equals an unsplit run;
  - the same seed twice is the same.

## The assistant's prior
- FM − PYFR lifespan, interval above 0: about 40%.
- "No food known" deaths fall below 0.60: about 35%.
- FM survives ≥ 0.80: about 3%.
