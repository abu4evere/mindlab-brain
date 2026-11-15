# WF findings: a fast memory beside the slow habit (exploratory; numbers from `analyse_wf.py`)

Plan: `questions.md` (WF-frozen). Checks All: PASS before data; Base and TBYS reproduce WY. Run 15 November 2026 on
GitHub's machines, 10 jobs of 48 children. Full tables: `analysis.md`. Mind Lab: exploratory, no council, no blind
recompute.

## 1. Night-time replay from a fast memory made the slow network relearn
Own skill on the changed kinds (**tests use the network only**, no store):

| arm, 128 neurons | A, 7 days after change (A38) | A, 14 days (A45) | B, 7 days (B53) | B, 14 days (B60) | food |
|---|---|---|---|---|---|
| Base | 0.05 | 0.11 | 0.00 | 0.00 | 828 |
| TBYS (WY) | 0.07 | 0.12 | 0.01 | 0.06 | 1058 |
| **RP (TBYS + nightly replay)** | 0.14 | **0.51** | 0.13 | **0.45** | 1487 |
| FMin (store as senses) | 0.11 | 0.18 | 0.04 | 0.10 | 1158 |

- **RP − TBYS, size 128:** A45 **+0.389 [+0.312, +0.465]**; B60 **+0.389 [+0.299, +0.479]**.
- **Size 32:** +0.326 and +0.312.
- **Before the change, RP is perfect:** A30 1.00 and B45 1.00 at both sizes (TBYS 0.71 and 0.84 at size 128).
- **The prior** (RP at least +0.15 on B60, about 35%): **yes.** The first real relearning in Mind Lab.
- **FMin − TBYS:** A45 +0.062, B60 +0.035 (size 128); +0.139 and +0.090 (size 32).
  The prior (about 25%): **no.** The network barely learned to use the store as a sense.

## 2. The engineered ceiling: a fast memory that acts relearns almost at once
- **WSLS** (a fresh stored pair is done; otherwise search without repeating failures; tests count the whole child):
  - **A38 0.89, A45 1.00, B53 0.83, B60 1.00** at size 128 (0.91, 1.00, 0.85, 1.00 at size 32);
  - food 1904 (size 128).
- **The stale habit is lowest here:** 0.39 at day 33, against 0.81 for TBYS. The fast memory notices the failure and
  moves on.
- The prior (B60 above 0.60, about 75%): **yes.** This is engineered, not learned. It shows what a working fast
  memory gives.

## What it means (the assistant's reading)
- **The relearning gap is closed in two ways, both through a fast memory:**
  1. **Acting from it** (win-stay, lose-shift): near-perfect relearning within a week. Engineered.
  2. **Teaching the slow network from it at night** (replay): the network itself relearns about half the changed
     boxes within two weeks, and learns everything perfectly before the change.
- **This matches the complementary-learning-systems idea:** a fast memory for the moment, sleep replay to build the
  slow habit. That is a reading from memory, not re-read today.
- **For Bob, a brain with two memories:** a fast store of what just worked (and what just failed), and a slow network
  trained from it during rest. With WL2's lesson, Bob also learns from a teacher without replaying the showing.

## Limits
- One task; replay counts and rates fixed (2 steps at rate 1.0 per kind per night).
- The store is engineered (a table per kind and lid). A learned fast memory is a later step.
