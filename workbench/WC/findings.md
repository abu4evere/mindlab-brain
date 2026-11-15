# WC findings: a world that changes (exploratory; numbers from `analyse_wc.py`)

Plan: `questions.md` (WC-frozen). Checks All: PASS before data (`checks.log`). Run 14 November 2026, 20:08–22:11,
locally at Idle: 2 evolution runs × 30 generations × 32 children, then 8 brains × 48 fresh children. Full tables:
`analysis.md`. Mind Lab: exploratory, no council, no blind recompute.

## 1. The main result: no brain relearned the changed codes on its own
Own skill on the changed kinds (full boxes; 48 children each; means):

| brain | group A before (day 30) | A, 2 / 7 / 14 / 29 days after its change (days 33, 38, 45, 60) | group B before (day 45) | B, 2 / 7 / 14 days after (days 48, 53, 60) |
|---|---|---|---|---|
| M32 | 0.38 | 0.00 / 0.01 / 0.04 / 0.07 | 0.65 | 0.00 / 0.00 / 0.01 |
| M128 | 0.61 | 0.01 / 0.05 / 0.11 / 0.21 | 0.89 | 0.00 / 0.00 / 0.00 |
| M256 | 0.51 | 0.00 / 0.01 / 0.08 / 0.24 | 0.76 | 0.00 / 0.02 / 0.04 |
| E1 (evolved here) | 0.50 | 0.02 / 0.06 / 0.10 / 0.21 | 0.87 | 0.00 / 0.00 / 0.02 |
| T1 (evolved without change) | 0.56 | 0.01 / 0.05 / 0.09 / 0.15 | 0.89 | 0.00 / 0.01 / 0.02 |

- **Every brain fell to about 0 at once,** as expected.
- **Then none came back in any useful time:**
  - 14 days after a change (about 42 tries per kind), the best was 0.11;
  - after 29 days, at most 0.24.
- **The old habit lasted:**
  - 2 days after group B changed, 0.85–0.95 of the changed kinds still got the old first-lid pair;
  - after 7 days, still 0.62–0.82.
- **The tries were not wasted:** stale use fell, from 0.46–0.64 at day 33 to 0.23–0.46 at day 38. But finding a new
  two-step code by trial alone was far too slow.

## 2. The questions
- **Q1 (size):**
  - M128 − M32: group A at day 45 +0.069 [+0.028, +0.118]; group B at day 60 −0.007 [−0.021, 0.000];
  - M256 − M32: +0.042 [−0.014, +0.097] and +0.028 [−0.007, +0.069].
  - The prior (M128 at least as good on both readings, about 55%) holds formally, **but everything is near the floor.**
- **Q2 (evolution):**
  - both runs went big again: born 24 → 193 and 32 → 196, with little growth;
  - the same as WT's no-change world. The prior ("64 or less", about 20%): no.
- **Q3 (evolved for change):**
  - E − T on relearning, every interval includes 0: group A at day 45 −0.014 to +0.007; group B at day 60 −0.021 to
    +0.007;
  - food: E − T1 +71 and +78; E − T2 +14 [−19, +47] and +21 [−8, +53].
  - The prior (E beats T on group B at day 60, about 25%): no.
- **The stale habit:** M128 at day 33, 0.576 [0.486, 0.660]. The prior ("at least half", about 50%): yes.
- **Food:** the big brains earn about twice what M32 and GA do (about 830–895 against about 425), almost all of it
  from the kinds that had not yet changed.

## 3. What it means (the assistant's reading)
- **This brain cannot yet learn from its mistakes in useful time.**
  - When its old answer stops working, its only tool is the slow trial-and-reward rule. That rule lowers a failing
    move a little after each failure, but a confident old habit takes many failures to undo. A new two-step code then
    has to be found almost by chance.
- **Evolution could not fix it,** because its genes only set size and growth, and no size relearns well. With nothing
  to select, the changing world chose the same brains as the stable one.
- **What animals and people have that this brain lacks (ideas from the literature, from memory, not checked
  today):**
  1. **"Lose, shift":** after a failure, try something different next time. It needs a short memory of what was just
     tried on this thing.
  2. **Surprise:** a sudden drop from success to failure is a strong signal (a large prediction error) that should
     speed learning and widen exploring for a while.
  3. **Not repeating a failed option in the same search:** a memory of which options already failed.
- **This is a missing brain part, not a world problem.** It is the creator's aim exactly: "learning from them"
  (mistakes).

## Limits
- One task, with a hard search: 16 pairs per lid, two lids in order.
- Fixed learning rates.
- No teacher after day 30, and no peers. WP adds peers.

## For the brain plan (needs the creator's OK)
- **Build and test the "learning from mistakes" part next:**
  - a memory of the last try on each kind and its result (lose-shift);
  - and/or a surprise signal that raises the learning rate and the exploring after an unexpected failure.
- **Retest on WC's world, one change at a time.**
