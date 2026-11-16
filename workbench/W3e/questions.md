# W3e: generations (does a learned parent pass its skill on?) (plan, frozen before any code or data)

**Frozen** as git tag `W3e-frozen`, before any code or data.
- **Sign-off:** the assistant, under the creator's standing instruction (16 November 2026): "do not ask me for next
  steps just go ahead".
- **Council:** `../W3e_council_2026-11-16.md`. Adopted: the argmax teacher; a G3 chain; an imitation-fidelity measure.
  Dropped: best-3 against worst-3.
- **Exploratory,** in the W3 series.

## The design (W3d's, with the parent replaced)
- **G2:** the child of seed s gets W3d's childhood (copy every 4th step, weight fading 0.5 → 0 over the first 400,000
  of 2,000,000 steps) plus the recipe (Y + FR).
  - **Its parent is W3d's trained PYFR brain of seed s,** weights fixed. It is shown the child's own map view, body
    levels and cell, and gives its **greedy (argmax)** act.
- **G3 (stage 2, run after G2 finishes):** the same, with the parent = G2's trained child of seed s.
- **The same seed means the same starting weights and the same training lands as W3d's PYFR child of seed s.** So
  G2 − W3d PYFR, paired by seed, isolates who taught: a learned parent against the script.

## Measures
- **W3's test, alone, on the 50 test lands:** survival to 3,000, to 1,000, lifespan, land known.
- **Imitation fidelity:**
  - the parent (learning off) lives on test lands 900001–900010, and every 10th step's (map, levels, cell) is
    recorded;
  - the child's argmax agreement with the parent's argmax on those states;
  - with W3's D3 (never taught by this parent) as the baseline.

## Readings (95% bootstrap intervals over the 8 seeds, paired; numpy seed 20261134)
1. **"Skill passes to the next generation":** G2 − its parent (W3d PYFR) on lifespan (survival beside it).
2. **"A learned parent beats no parent":** G2 − W3b's Y+FR (recipe only) on lifespan.
3. **"Ratchet or decay":** G3 − G2 on lifespan.
4. **"The child copied its parent":** G2's fidelity − D3's fidelity (to the same parent); G3's to G2 the same way.

## Validity (hard stops)
- **Checks All: PASS before data:**
  - with no parent present, the loop reproduces W3b's PYFR-free training (as W3d's check 1);
  - the parent's weights do not change;
  - the parent gives its argmax act on the child's view;
  - copy counts as planned;
  - a split run equals an unsplit run;
  - the same seed twice is the same.
- Every run finishes, or is reported.

## The assistant's prior
- **Reading 1** (G2 at least its parent's lifespan, interval not below 0): about 35% (the council's mean about 36%).
- **Reading 2** (G2 above recipe-only): about 80%.
- **Reading 3** (G3 at least G2): about 40%.
- **Reading 4** (G2 copies its parent above D3's agreement): about 85%.
