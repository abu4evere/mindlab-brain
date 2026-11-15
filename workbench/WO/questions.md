# WO: shown only once (when is holding a showing in mind worth it?) (plan, frozen before any code or data)

**Frozen** as git tag `WO-frozen`, before any code or data.
- **The creator** (15 November 2026): "go ahead with your road" (first this test, then the fast memory).
- **WL2 found:**
  - in a world where the same boxes are shown again and again, the brain whose memory is wiped before each try (Linf)
    learns best (1.000 by day 30);
  - holding the showing in mind made a parrot.
- **But a showing seen only once should need that memory.** This test asks where the balance lies.
- **Exploratory:** no council.

## The world: new boxes every day
- **New kinds:** on each day d (1–30), 2 new kinds of box appear (60 kinds in a life). Each has its own random look
  (16 numbers, N(0, 1)) and its own code (2 lids; each lid a random ordered pair of 4 acts; the two lids differ).
  - Draws: `[seed, 21]`. Each encounter adds look noise N(0, 0.2²) (`[seed, 22, day]`).
- **Each day, in this order:**
  1. **Retention tests** (greedy, no showing, no learning) on the kinds introduced 1 day ago and 7 days ago. Test look
     noise comes from `[seed, 23, day]`.
  2. **Review practice:** one learning try (no showing) on each kind introduced 1, 2, 4 and 7 days ago.
  3. **Each new kind:**
     - the grown-up shows it once (the arm's memory episode) and the child copies (rate 0.5);
     - an **immediate test** (greedy, with that same memory episode, no learning);
     - one learning try with that episode;
     - two more learning tries later that day without a showing.
- **Learning:** WS's rule (copy rate 0.5, learning rate 0.05, reinforcement from lids opened).
- **Food** = lids opened in learning tries.

## Arms (WL2's, memory children of 32 and 128 neurons; 48 children each, seeds 1–48; GitHub's machines)
- **L0:** perfect memory of the showing.
- **L2:** wait 8 steps with noise 0.6 (wait noise `[seed, 13]`).
- **Linf:** the memory is wiped before each try. The copy step, the immediate test and the try see no showing in
  memory.

## Measures (means over the kinds introduced on days 8–30; 95% bootstrap intervals over seeds, paired; numpy seed
20261124)
- **Immediate:** both lids right after the single showing.
- **Retention:** both lids 1 day later, and 7 days later.
- **Lifetime food.**
- **Paired differences:** L2 − L0, Linf − L0 and Linf − L2 at each size.

## The assistant's prior
- **Immediate:** L0 above Linf at size 128 (interval above 0): about 90%.
- **Retention 1 day:** Linf at least as good as L0 at size 128 (interval not below 0): about 50%.
- **Food:** L2 highest of the three at size 128: about 40%.
