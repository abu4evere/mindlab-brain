# WL findings: a leaky memory (the creator's idea) (exploratory; numbers from `analyse_wl.py`)

Plan: `questions.md` (WL-frozen). Checks All: PASS before data. L0 reproduces WN's children. Run 14 November 2026 on
GitHub's machines, 9 jobs of 48 children. Full table: `analysis.md`. Mind Lab: exploratory, no council, no blind
recompute.

## 1. A leaky memory stopped the parrot, at every size
**Own skill (no showing), 48 children each:**

| size | level | day 15 | day 30 | day 60 | after a showing, day 30 |
|---|---|---|---|---|---|
| 32 | L0 (perfect memory) | 0.153 | 0.351 | 0.920 | 0.913 |
| 32 | L1 (wait 4, noise 0.3) | 0.559 | 0.785 | 0.993 | 0.979 |
| 32 | L2 (wait 8, noise 0.6) | 0.455 | **0.962** | 0.986 | 0.885 |
| 128 | L0 | 0.028 | 0.042 | 0.806 | 1.000 |
| 128 | L1 | 0.358 | 0.403 | 0.965 | 1.000 |
| 128 | L2 | 0.625 | **0.823** | **0.997** | 0.806 |
| 256 | L0 | 0.021 | 0.024 | 0.694 | 1.000 |
| 256 | L1 | 0.111 | 0.125 | 0.854 | 1.000 |
| 256 | L2 | 0.236 | 0.344 | 0.958 | 0.913 |

- **Q1: L − L0, own skill at day 30:**
  - L2-128 **+0.781 [+0.733, +0.826]**; L2-256 +0.319 [+0.264, +0.375];
  - L1-128 +0.361 [+0.292, +0.434]; L1-256 +0.101;
  - size 32 also: L1 +0.434, L2 +0.611.
  - The priors (L2 at least +0.10, about 50%; L1 about 40%): **yes, far beyond.**
- **Q2, the final skill gained too.** Day 60: L2-128 +0.191 [+0.153, +0.229]; L1-128 +0.160; L2-256 +0.264.
  The prior "no loss" (about 55%): **yes, a gain.**
- **Q3, big and leaky against small and perfect, day 60:**
  - L2-128 − L0-32: +0.076 [+0.045, +0.108];
  - L2-256 − L0-32: +0.038 [0.000, +0.076].
  - The prior (about 45%): **yes.**
- **Q4, manipulation check (after-showing success):**
  - falls with L2: −0.194 at 128, −0.087 at 256;
  - but not with L1 (1.000 at 128 and 256).
  - The prior (falls at size 128, about 85%): **only for L2.**
- **Food:** L1 earned more at every size (+232, +165, +84). L2 earned less at 128 and 256 (−146, −131), where replaying
  the showing pays during the teaching.

## 2. What it means (the assistant's reading)
- **The creator's idea held strongly in this task.** When the memory of the showing fades and gets noisy before the
  try, the brain cannot simply replay it. It learns the skill as its own, much earlier.
  - The leaky big brain (L2-128) owns 82% of the boxes at day 30, against 4% with a perfect memory.
  - By day 60 it is near perfect (0.997).
- **The best brains of all Mind Lab box tests so far are the leaky ones:** day 60 at 0.99 for L1-32, L2-32 and
  L2-128.
- **The cause is not yet separated.** Three explanations fit:
  1. forgetting the details forces learning the rule (the creator's idea);
  2. noise during learning acts like a known training aid (noise makes networks more robust; "dropout" is a cousin);
  3. a wait makes practice look more like the test, which has no showing.
  
  These overlap. A follow-up (noise without a wait, and a wait without noise) would separate them.
- **For Bob:** a big brain with an imperfect short-term memory, on purpose. If the follow-up confirms it, this becomes
  a design rule.

## Limits
- One task; the two leak levels fixed, not tuned. Noise only in the wait.
- The teacher shows every try. Leaks in a world with a rarer teacher are untested.
