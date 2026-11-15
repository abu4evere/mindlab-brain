# WL3 findings: forgetting helps even more in richer worlds (exploratory; numbers from `analyse_wl3.py`)

Plan: `questions.md` (WL3-frozen). Checks All: PASS before data; K6L2 reproduces WL2. Run 15 November 2026, 14:02–14:13,
locally at Idle (2 processes). 24 children per cell. Full table: `analysis.md`. Mind Lab: exploratory, no council, no
blind recompute.

## Results (own skill, no showing)
| world | size | L0 (perfect memory): day 30 / 60 | L2 (leaky): day 30 / 60 | Linf (wiped): day 30 / 60 |
|---|---|---|---|---|
| K6L2 (WN's) | 32 | 0.396 / 0.931 | 0.965 / 0.986 | 1.000 / 1.000 |
| K6L2 | 128 | 0.069 / 0.812 | 0.792 / 0.993 | 1.000 / 1.000 |
| **K24L2 (24 kinds)** | 32 | 0.045 / 0.530 | 0.639 / 0.839 | 0.852 / 0.917 |
| **K24L2** | 128 | 0.016 / 0.477 | 0.382 / 0.783 | **0.936 / 0.962** |
| **K6L3 (3 lids)** | 32 | 0.132 / 0.632 | 0.653 / 0.861 | 0.889 / 0.965 |
| **K6L3** | 128 | 0.014 / 0.681 | 0.660 / 0.979 | **1.000 / 1.000** |

**Linf − L0:**

| world | size | day 30 | day 60 |
|---|---|---|---|
| K6L2 | 32 | +0.604 [+0.514, +0.694] | +0.069 |
| K6L2 | 128 | +0.931 | +0.188 |
| K24L2 | 32 | +0.807 [+0.774, +0.840] | +0.387 [+0.359, +0.415] |
| K24L2 | 128 | +0.920 [+0.898, +0.943] | **+0.484 [+0.448, +0.521]** |
| K6L3 | 32 | +0.757 [+0.694, +0.819] | +0.333 [+0.257, +0.410] |
| K6L3 | 128 | +0.986 [+0.965, +1.000] | +0.319 [+0.250, +0.382] |

- **The floor rule:** every world is readable.
- **Q1** (Linf above L0 at day 30 in both richer worlds, size 128; prior about 60%): **yes.**
- **Q2** (Linf at least as good as L0 at day 60; prior about 55%): **yes, and far better.** The gap at day 60 grows
  from +0.07–0.19 in WN's world to +0.32–0.48 in the richer ones.
- **The perfect-memory parrot gets worse as the world grows.**
  - L0 at day 60: 0.48–0.53 with 24 kinds and 0.63–0.68 with 3 lids, against 0.81–0.93 with 6 kinds and 2 lids.
  - Yet it still replays a showing almost perfectly (after-showing 0.96–1.00 with 24 kinds).
- **The leaky memory (L2) sits between them** in every world.

## What it means (the assistant's reading)
- **"Do not replay the teacher's showing while trying" held, and grew stronger, with more things to learn and with
  longer sequences.**
  - A brain that leans on the replay never builds the skill. The more there is to learn, the more that costs.
- **On Rohde and Plaut (1999):** their richer task was a language with graded meaning, where generalising across items
  matters.
  - Here every box's code is random, so there is nothing to generalise; the richness is in amount and length only.
  - WL3 therefore answers "more and longer", not "more structured". **A task with shared structure** (boxes whose codes
    follow a rule) is the remaining test before forgetting becomes a design rule for Bob.

## Limits
- Random codes (no shared structure); one teaching schedule (a showing before every try); 24 children per cell.
