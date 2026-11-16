# WX findings: why the best learned brains die (a diagnosis; 16 November 2026)

**Plan:** `questions.md` (WX-frozen, before logging). It replays W3d's PYFR test lives (8 seeds × 50) with a recorder.
- The replay reproduces W3d's test lifespans (checked on seed 2's first lives).
- Script, on the same lands, is beside it. Read-only; summary from `analyse_wx.py` (`summary.txt`).

## The deaths (W3d PYFR; 349 of 400 lives ended in death; labels can overlap)
| label | share of deaths (mean of seeds) |
|---|---|
| **no food known** (the map memory held no cell remembered as full food at death) | **0.80** |
| **exhaustion** (fatigue above 100, so moving costs double, for at least half of the last 100 steps) | **0.63** |
| food known but not reached (a full-food cell remembered within 30 steps during the last 100) | 0.27 |

## Against the hand-written Script (which sees the same map memory)
| | PYFR (mean of seeds) | Script |
|---|---|---|
| deaths, of 50 lives per seed | 30–50 | 2 of 50 |
| time exhausted | **0.25** | **0.02** |
| land seen by step 500 | 0.83 | 1.00 |
| meals per 100 steps | 2.7 | 3.6 |
| steps to the first meal | 24 | 20 |

## What it means (the assistant's reading)
- **Finding the first food is not the problem** (24 steps against Script's 20), and the brains explore their land well
  (0.83 seen by step 500).
- **Two things kill them:**
  1. **Not resting.** They spend a quarter of their lives exhausted, where Script spends 2%. Exhausted, each move
     costs double energy. Script goes to the shelter when tired (fatigue above 80) and rests until fresh. The
     children copied the parent's foraging, but not this.
  2. **Running out of known food.** At 80% of deaths the brain had emptied what it remembered and held no full food
     in mind. Food regrows after 200 steps, but the map memory shows an eaten cell as empty until it is seen again.
     - Script then searches the stalest places;
     - the brains do not go back to check where food used to be.
- **The gap to 80% survival is therefore specific:** rest when tired, and go back to where food grows.
- **Candidates for the next study (chosen by the assistant, under "just go ahead"):**
  - a longer or denser childhood on resting (the copy weight while tired);
  - or a "where food grows" memory (when a meal was last eaten at each patch), so returning after regrowth is
    something the brain can see.
  - **The second is more general:** it gives the brain a sense of time since a place last fed it.

## Limits
- Labels by fixed rules; overlapping; one world; the W3d brains only.
