# WL2 findings: why does the leaky memory work? (exploratory; numbers from `analyse_wl2.py`)

Plan: `questions.md` (WL2-frozen). Checks All: PASS before data; L0 and L2 reproduce WL. Run 15 November 2026 on
GitHub's machines, 12 jobs of 48 children. Full table: `analysis.md`. Mind Lab: exploratory, no council, no blind
recompute.

## 1. Results (own skill, no showing; 48 children each)
| arm | size 32: day 30 / day 60 | size 128: day 7 / day 30 / day 60 |
|---|---|---|
| L0, perfect memory | 0.351 / 0.920 | 0.045 / 0.042 / 0.806 |
| L2, wait + noise (WL) | 0.962 / 0.986 | 0.215 / 0.823 / 0.997 |
| W8, wait only | 0.816 / 1.000 | 0.184 / 0.184 / 0.917 |
| NS, noisy memory, no wait | 0.528 / 0.865 | 0.049 / 0.222 / 0.913 |
| NP, noise everywhere in practice | 0.333 / 0.729 | 0.035 / 0.062 / 0.816 |
| **Linf, the memory wiped before each try** | **1.000 / 1.000** | **0.819 / 1.000 / 1.000** |

**Day-30 gain over L0, as a share of L2's gain:**
- size 32: Linf 1.06, W8 0.76, NS 0.29, NP −0.03;
- size 128: **Linf 1.23**, NS 0.23, W8 0.18, NP 0.03.
- Linf − L2 at day 30: +0.038 [+0.017, +0.062] (size 32); **+0.177 [+0.135, +0.219] (size 128).**

## 2. The readings
- **(2) General noise as a training aid: no.** NP carries nothing (shares −0.03 and 0.03) and lowers the final skill
  at size 32 (day 60 −0.191).
- **(1) Forgetting the showing: yes, and the more complete the better.**
  - **Linf, total forgetting, is the best brain of all:** perfect by day 30 at both sizes, and 0.82 at day 7 for the
    big brain.
  - Waiting alone works for the small brain (0.76 of the gain), whose memory fades by itself. It works far less for
    the big brain (0.18), which holds the showing through a silent wait.
  - The big brain remembers too well. That is the creator's point, seen inside one experiment.
- **(3) Practice like the test: it fits too.** In Linf, every try is made exactly as in the test, from the child's own
  knowledge. (1) and (3) are the same thing seen from two sides: a child that cannot replay must use what it has
  learned.
- **The priors:** W8-128 carries (about 35%): no. NS-128 (about 50%): no. NP-128 (about 40%): no. Linf-128 below L2 at
  day 60 (about 60%): **no**, it is level or better.

## 3. A check after the data (exploratory, labelled)
- Linf beat everything, so it was checked for a fault: the same blank-memory child, but with no recurrence within
  the try (WS's B0 learning), seeds 1–4.
  - Recurrent: day 30 = 1.0 in all four.
  - Not recurrent: 0.50–0.67 at day 30; 0.50–0.83 at day 60.
- **So the loop within a try matters a lot, even with nothing carried over from the showing.**
- This corrects the reading of WS (appended there): the memory child's day-60 advantage over B0 can come from the loop
  within the try. Holding the showing is not needed for it.

## What it means (the assistant's reading)
- **In this task, the best brain does not carry the teacher's showing into its own try.** It learns from the showing
  (the copy step), then acts from its own knowledge.
- **Holding a showing in mind is useful in the moment** (WS's deferred imitation, 0.91 after a showing). **It is
  harmful for learning when showings come again and again:** the brain leans on the replay instead of learning.
- **For Bob, two separate uses of memory:**
  - a working memory for in-the-moment use (one-off showings, new situations);
  - learning that does not rely on replaying it.
  - A human's fading short-term memory gives this split naturally.
- **Not yet tested:** a world where each thing is shown only once (novel boxes), where in-the-moment memory should
  matter more. There, Linf would lose its edge, and a leaky memory might be the best trade.

## Limits
- One task, with repeated showings of the same boxes; fixed noise levels.

## Note from the literature (15 November 2026, appended; abstracts only, `D:\acl\docs\research\mindlab_sources_2026-11-15.md`)
- **For:** Elman (1993) found that starting with limited memory helped recurrent networks learn complex sentences.
  Newport's "less is more" makes a similar argument about children.
- **Against:** Rohde and Plaut (1999) found that limits on memory or input were not needed, and hindered learning,
  once the language was made more natural.
- **So the forgetting gain here may depend on the task:** the same few boxes are shown again and again. It should be
  tested in a richer task before it becomes a design rule.
