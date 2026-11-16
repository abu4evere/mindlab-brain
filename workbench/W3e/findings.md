# W3e findings: generations (16 November 2026)

**Plan:** `questions.md` (W3e-frozen after a council; the creator's "just go ahead"). Checks All: PASS before data (8).
- **Stage 1 (G2):** 8 cloud jobs, closed 06:04. **Stage 2 (G3):** 8 jobs, closed 09:26.
- The frozen `analyse_w3e.py` gives `analysis.md`. n = 8 lineages (seeds) × 50 test lives, tested alone.
- Mind Lab: no blind recompute.

## The frozen readings
| generation | taught by | survived to 3,000 | to 1,000 | lifespan | land known |
|---|---|---|---|---|---|
| recipe only (W3b) | nobody | 0.000 | 0.010 | 248 | 0.63 |
| G1 = W3d PYFR | the script | 0.128 | 0.243 | 806 | 0.83 |
| **G2** | G1 (learned) | 0.070 | 0.133 | **549** | 0.74 |
| **G3** | G2 (learned) | 0.050 | 0.113 | **473** | 0.69 |

1. **"Skill passes on" (G2 − its parent): no, it partly passes.** Lifespan −257 [−445, −66]; survival −0.058
   [−0.122, +0.002].
2. **"A learned parent beats no parent": yes.** G2 − recipe-only: lifespan +301 [+92, +530]; survival +0.070
   [+0.028, +0.118].
3. **"Ratchet or decay" (G3 − G2): neither clearly.** Lifespan −76 [−228, +71]; survival −0.020 [−0.058, +0.018].
4. **"The child copies its parent": yes.**
   - G2 agrees with its parent's choice 0.660 [0.565, 0.746] of the time, against 0.281 for W3's D3 (+0.379);
   - G3 agrees 0.679 against 0.236 (+0.443).

**The priors:**
- reading 1 (at least the parent, about 35%): no;
- reading 2 (about 80%): yes;
- reading 3 (G3 at least G2, about 40%): an interval spanning 0;
- reading 4 (about 85%): yes.

## Exploratory (labelled): the lineages, lifespan by generation (from the test files)
| lineage | G1 | G2 | G3 |
|---|---|---|---|
| 1 | 415 | 484 | 711 |
| 2 | 1528 | 1147 | 731 |
| 3 | 883 | 811 | 457 |
| 4 | 1005 | 393 | 306 |
| 5 | 992 | 370 | 543 |
| 6 | 307 | 291 | 325 |
| 7 | 1119 | 658 | 482 |
| 8 | 201 | 237 | 230 |

- **The strong lineages lost skill each generation** (lineage 2: 1528 → 1147 → 731).
- **A weak one improved** (lineage 1: 415 → 484 → 711), and the weakest stayed flat.
- By G3 the lineages sit closer together (230–731) than in G1 (201–1528).

## What it means (the assistant's reading)
- **Skill does pass from learned parent to learned child:**
  - children copy two thirds of their parent's choices;
  - and they live twice as long as brains with no parent.
- **But each generation keeps only part of it.** The script-taught first generation's edge fades toward a middle
  level (about 500 steps), where the generations seem to settle.
- **There is no ratchet:** nothing makes a child better than its parent on average. Some lineages rose and others
  fell, which looks like drift toward a shared level, not improvement.
- **What the literature says cumulative culture needs** (the 15 November source note: Enquist et al. 2007, "critical
  social learning"):
  - high-fidelity copying (here, about 0.67);
  - plus the child's own learning to improve on it (the recipe);
  - **plus choosing better models.** Here each child had exactly one parent, whatever its skill.
- **Next (chosen):** let a child choose whom to learn from among several learned adults, by the success it can see.
  That is the "whom to copy" ingredient (Cradle C2-S, C2-E, C2-K3) brought into living. Does choosing a better model
  give a ratchet?

## Limits
- 8 lineages; two learned generations; one teaching dose (W3d's); one world. No council beyond W3e's.
