# W3j: keep what the parent taught. (DRAFT)

**Why (W3i, W3h, W3f):**
- **The best brain yet** is W3i's C: a 1.2M-step fading childhood within 2.8M steps. Lifespan 1,248, survival 0.255
  (0.235 on fresh lands).
- **Every brain peaks soon after childhood and then declines** when it keeps learning alone. LC: 1,340 at 2M, 980 at
  6M. L: 840 → 603.
- **The same erosion appears elsewhere:**
  - W3h: a careful parent's lesson faded after it left, unless pain held it;
  - W3f: skill decays between generations.
- **The hypothesis:** after childhood, learning from sparse feelings overwrites the parent's policy with a worse one.
  Two ways to keep it:
  1. **Settle down (consolidation):** the learning rate drops after childhood, so the adult changes slowly. Like a
     critical period that closes.
  2. **The parent's voice:** a small copy weight stays for life (0.05 instead of 0). W3d's PA (0.5 for life) was
     worse, so this is ten times smaller.
- **And one more length:** a still longer childhood (2.4M fade within 4.0M; the curve has not been seen to peak).

## Arms (C's settings unless stated; 8 seeds; GitHub's machines)
| arm | change from C (2.8M steps, 1.2M fade) |
|---|---|
| **CK** | the learning rate × 0.1 for every update after the fade ends |
| **CV** | the copy weight floors at 0.05 after the fade (the parent stays as a quiet voice) |
| **C2** | 4.0M steps, 2.4M fade (1.6M alone, as C) |
| cited: **C** (W3i) | the reference, paired by seed |

## Measures
W3i's (test, fresh lands, death labels, disappointments), plus a learning curve: snapshots at the end of the fade and
every 400,000 steps after it.

## Readings (to be frozen; paired by seed; 95% bootstrap)
1. **"Settling down keeps it":** CK − C on lifespan, lower bound above 0.
2. **"A quiet parent keeps it":** CV − C on lifespan, lower bound above 0.
3. **"Longer still helps":** C2 − C on lifespan, lower bound above 0.
4. **Toward the bar:** the best arm's fresh-land survival against 0.80.

## Open questions for the council
1. Is a learning-rate drop a fair "critical period", or does it just freeze the brain (no adult learning at all)?
2. Is 0.05 a sensible quiet-parent weight, given that 0.5 for life was worse?
3. Should pain (W3h) be on in all arms, since it is now part of the starting brain?

## The assistant's prior
- CK helps: about 45%.
- CV helps: about 40%.
- C2 helps: about 40%.
- Any arm reaches 0.80 on fresh lands: about 2%.
