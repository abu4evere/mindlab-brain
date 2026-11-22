# W3o findings: raw eyes (22 Nov 2026)

**Status: final (22 Nov 2026). The blind recompute (`recompute_w3o.md`, a fresh session that did not see the analysis
script) agrees on every key number and verdict; see the end.**

- Plan: `questions.md`, frozen as tag `W3o-frozen` (20 Nov 2026); checks All: PASS (`checks.log`, `checks_gcp.log`,
  `checks_oci.log`). Exploratory, in the W3 series.
- **Runs:** 16 (arms RE and RV, seeds 1–8; 4.0M steps each), on three machines, each run's machine in
  `output/machine_*.json`:
  - the creator's PC (Windows): RE 1, RE 2, RV 1;
  - the Oracle VM (AMD EPYC 7742): RV 2, RE 3, RV 3, RE 4, RV 4;
  - the Google VM (Intel Xeon): RE 5–8, RV 5–8.
  The two Linux machines train bit-identically; the PC differs in the last digits. Every run is a valid sample of its
  arm (questions.md, "Machines").
- The cloud outputs were downloaded into `dl/oci/` and `dl/gcp/` and merged into `output/` (1,040 files, no name
  clashes). The frozen `analyse_w3o.py` gives `analysis.md`; the frozen `probe_w3o.py` gives `probe.json`. Both were
  run on the PC with one maths thread (the PC was short of memory); n = 8 seeds × 50 test lives (and 50 fresh lands).

## The frozen readings (lifespan on the test lands, capped at 3,000 steps; paired by seed with W3n's HR)
| arm | eyes | lifespan | survived | fresh lands: survived | deaths per 1,000 steps |
|---|---|---|---|---|---|
| HRS (W3n) | sorted layers (wall, food, shelter) | 2,803 | 0.897 | 0.877 [0.855, 0.902] | 0.22 |
| **RES** | **mixed colours (fixed)** | **2,731** | **0.875** | **0.877 [0.850, 0.907]** | 0.35 |
| RVS | colours dealt anew on each land | 1,321 | 0.208 | 0.270 [0.195, 0.353] | 1.81 |
| HRS-bare (W3n) | sorted, both reflexes off | 1,608 | 0.338 | 0.375 [0.287, 0.450] | 1.33 |
| RES-bare | mixed, both reflexes off | 1,556 | 0.340 | 0.323 [0.230, 0.412] | 1.55 |
| RVS-bare | changing, both reflexes off | 385 | 0.005 | 0.005 [0.000, 0.015] | 3.60 |
| RES-swap | mixed, wall and food colours exchanged at test | 323 | 0.003 | 0.003 | 4.67 |

1. **Primary, RE (97.5%, Bonferroni; margin −200 steps):**
   - **RES − HRS: −72 [−150, +4] → small** (within the margin); 3 of 8 seeds above 0.
   - **RES-bare − HRS-bare: −52 [−264, +146] → unclear** (the interval reaches below −200); 4 of 8 seeds above 0.
2. **RV, the ceiling test (95%):** RVS − HRS −1,482 [−1,624, −1,340]; RVS-bare − HRS-bare −1,222 [−1,395, −1,025]: a
   large loss, as expected.
3. **Secondary (95%):**
   - **The manipulation check passes:** RES-swap − RES −2,409 [−2,503, −2,328]. Exchanging the wall and food colours
     at test nearly kills every life, so RE's brain really uses what the colours mean.
   - RE − HR +80 [−76, +239]; RV − HR −1,223 [−1,420, −1,035]; RVS − RES −1,411 [−1,585, −1,217].
4. **The probe** (no reflex, the map memory fully known; share of first moves toward food when hungry, toward the
   shelter when tired; paired by seed):
   - hungry: HRS 0.868, RES 0.843, RVS 0.555, RES-swap 0.148 (chance 0.292). RES − HRS −0.025 [−0.060, +0.010];
     RVS − HRS −0.312 [−0.388, −0.223]; RES-swap − HRS −0.720 [−0.780, −0.660].
   - tired: HRS 0.752, RES 0.700, RVS 0.603, RES-swap 0.853 (chance 0.348). RES − HRS −0.052 [−0.188, +0.128];
     RVS − HRS −0.150 [−0.282, +0.010].
5. **Toward the bar (fresh-land survival 0.80):** RES 0.877 [0.850, 0.907] meets it, the same as HRS; RVS 0.270 does
   not; bare brains do not (HRS-bare 0.375, RES-bare 0.323).

## What it means
- **Mixed colours cost little.** When "food", "wall" and "shelter" are not handed to the brain as separate layers but
  mixed into colours (each colour layer on for two kinds of thing), the brain learns to untangle them: its life with
  reflexes is within the fixed margin of the sorted brain's, its fresh-land survival is the same (0.877), and alone in
  the probe it steps toward food almost as often (0.843 vs 0.868). The swap shows it is the colours' meaning it uses.
  So the sorted eyes were not doing the brain's work for it, as long as a colour always means the same thing.
- **Changing colours break it.** When the colours are dealt anew on each land, the brain cannot work out within a life
  which colour is food. It still does better than chance (the probe: 0.555 toward food, chance 0.292, so shape and
  place carry a little), but its lives are half as long and fresh-land survival falls to 0.27. What it lacks is not
  eyes but **learning a meaning within one life**: noticing "I ate where it was this colour, so this colour is food
  here". That is fast learning within a life, one of the approved directions for Bob's brain, and a direct target for
  a later study.
- **The brain alone (bare) stays where it was:** RES-bare and HRS-bare both live about 1,550–1,600 steps and survive
  0.32–0.38 of fresh lands; the bare reading for RE is unclear at this sample size, not a loss.

## Against the priors (questions.md)
- RES − HRS within the margin: the assistant 65%, Gemini 55%, GPT 75% → **yes**.
- RVS a real loss: 75% (GPT 85%, Gemini 92% bare) → **yes**.
- The swap check passes: 80% (GPT 65%, Gemini 85%) → **yes**.
- RVS fresh-land survival ≥ 0.80: 15% (Gemini 5%/45%, GPT 25%) → **no** (0.270).

## Named limits
- The body's two reflexes still read the world's own sorted memory, so with reflexes on, the body "knows" food even
  when the brain's eyes do not (named in the plan). The bare readings are the brain alone.
- The parent (W3's Script) also reads the sorted memory during childhood: a second privileged channel (GPT, council).
- Eight seeds are a pilot; the unclear bare reading for RE could be settled by more seeds if it ever matters.
- Lifespan is capped at 3,000 steps, so the arms near the cap (HRS, RES) are compared on a squeezed scale.

## The blind recompute (22 Nov 2026, `recompute_w3o.md`, `recompute_w3o_blind.py`)
A fresh assistant session, which did not open `analyse_w3o.py`, its outputs or these findings, recomputed from the raw
files (50,000 bootstrap resamples, numpy seed 20261122, an exact bootstrap and a t interval beside it):
- RES − HRS −71.7 [−151.8, +3.7] → small (same verdict); RES-bare − HRS-bare −51.9 [−261.3, +142.6] → unclear (same);
- RVS − HRS −1,482 [−1,629, −1,341]; RVS-bare − HRS-bare −1,222 [−1,395, −1,020]; RES-swap − RES −2,409 [−2,502,
  −2,328] (passes);
- fresh-land survival HRS 0.878, RES 0.878 (both reach 0.80), RVS 0.270 (does not);
- probe differences identical to the frozen analysis (RES − HRS hungry −0.025 [−0.060, +0.010]).
Every mean is identical and every interval end within about 2 steps; the t intervals give the same verdicts. It also
noted: the RE bare reading turns on two seeds each way; RES − HRS sits just short of "real" (upper bound +4); HRS seed 7
is an outlier on the tired probe.
