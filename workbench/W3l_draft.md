# W3l: the longer childhood with the kept copy, and longer still (DRAFT, 19 November 2026)

**Why (W3k):**
- **Keeping an earlier copy of itself works:** CS (the copy kept while its recent training lives were longest) beat the
  end of the same run, CS − R2 +199 [+70, +347]. The best brain yet: lifespan 1,835, full lives 0.478, fresh-land
  survival 0.445 (bar 0.80). A copy at a step drawn in advance did about as well (CS − CY +43 [−21, +109]).
- **A longer childhood (C3: 3.6M fade of 5.2M) was not separated on lifespan** (C3 − R2 +117 [−193, +432]), but its
  curve **stopped declining** after childhood, and its fresh-land survival was the highest (0.460).
- W3k's C3 runs kept a copy too, but it was not saved (only run R's were). Runs are now bit-identical across
  machines, so retraining C3 gives the same brain, and this time its copies are saved.

## Arms (W3k's code and settings; 16 seeds, 1–16; GitHub's verified machines)
| arm | run | brain |
|---|---|---|
| **C3** | 5.2M steps, 3.6M fade (W3k's C3 again) | the end |
| **C3S** | the same run | the copy kept by its own lives (W3k's CS rule) |
| **C3Y** | the same run | the copy at a step drawn in advance (W3k's CY rule, new draw seed) |
| **C5** | 6.4M steps, **4.8M fade** (the same 1.6M alone) | the end |
| **C5S** | the same run | the copy kept by its own lives |
| **C5Y** | the same run | the copy at a step drawn in advance |
| CS (cited) | W3k's run R (4.0M steps, 2.4M fade) | its kept copy, tested in W3k |

- **The reproduction check:** C3's end weights must equal W3k's C3 bit for bit (each seed). Reported whatever it shows.
- Snapshots after the fade every 400,000 steps (tested), as W3k.

## Measures (W3k's)
Lifespan; survival to 3,000 and 1,000; fresh-land survival; drift; parent agreement; the step each copy comes from.
**Exploratory (after the readings, local, read-only):** the death causes (WX's labels: no food known, exhaustion, food
known not reached) of the best arm's test lives, beside W3d's PYFR and the Script.

## Readings (paired by seed; bootstrap over 16 seeds)
1. **Two primary readings (Bonferroni: 97.5% intervals, lower bound above 0):**
   - **"The longer childhood and the kept copy add up":** C3S − CS (W3k) on lifespan.
   - **"An even longer childhood helps":** C5S − C3S on lifespan.
2. **Secondary (95%):** C3S − C3 (does a copy help a run that no longer declines?); C5 − C3; C3S − C3Y; C5S − C5Y.
3. **Toward the bar:** the best arm's fresh-land survival against 0.80.

## Open questions for the council
1. Is comparing C3S with W3k's CS fair (a different run, tested in an earlier study, same seeds and lands)?
2. Primary 2 compares copies (C5S − C3S), not the ends. Right, or should the ends be primary?
3. Is a fourth childhood length worth it, or is something else the better next step toward 0.80 fresh-land survival
   (the main deaths so far: no food known, exhaustion)?
4. Anything that could make the reproduction check pass for the wrong reason, or fail for a harmless one?

## The assistant's prior
- C3S − CS above 0: about 30%. C5S − C3S above 0: about 35%. C3S − C3 above 0: about 25%.
- The reproduction check exact: about 85%. Any arm at 0.80 on fresh lands: about 2%.
