# WL4 findings: forgetting when things follow a rule (exploratory; numbers from `analyse_wl4.py`)

Plan: `questions.md` (WL4-frozen, 14:14 on 15 November); code and checks before data (WL4-checked, 14:15). Run locally,
14:15–14:31 (`run0.log`, `run1.log`; 288 of 288 children). The frozen analysis was run, and these findings written, at
the 16:47 sleep-mode heartbeat; the session that started WL4 had gone quiet. Full table: `analysis.md`. Mind Lab:
exploratory, no council, no blind recompute. n = 24 children per cell.

## 1. Generalising to boxes never seen: a little, not much
**Held-out success at day 60** (6 kinds never shown or practised):

| | L0 | L2 | Linf |
|---|---|---|---|
| RULE world, size 32 | 0.056 | 0.049 | 0.062 |
| RULE world, size 128 | 0.097 | 0.118 | 0.111 |
| RAND world (the control), every arm | 0.000–0.014 | | |

- **RULE − RAND, held out, day 60:** +0.049 to +0.104, every interval above 0 (for example L2-128 +0.104
  [+0.049, +0.167]).
- So the brains picked up a little of the rule: about 1 in 10 never-seen boxes opened at size 128, against near 0 by
  chance.
- **The frozen floor** ("not shown" if every arm is below 0.05): not met, since three arms are 0.097–0.118. So
  generalising is shown, but weak.
- **Q1 prior** (above 0.20 for at least one arm, about 55%): **no.**

## 2. Forgetting did not hurt generalising
- **Linf − L0, RULE, held out, day 60:** +0.007 [−0.042, +0.056] at size 32; +0.014 [−0.042, +0.069] at size 128.
- **At day 30:** +0.069 [+0.021, +0.125] and +0.111 [+0.049, +0.174]. The wiped-memory brain was ahead early.
- **L2 − L0 at day 60:** −0.007 and +0.021, both including 0.
- **Q2 prior** (Linf at least as good as L0, interval not below −0.05, about 55%): **yes.**

## 3. On practised boxes, forgetting won as before
- **RULE, Linf − L0:**
  - day 30 +0.898 [+0.872, +0.924] (size 32) and +0.946 [+0.922, +0.967] (size 128);
  - day 60 +0.243 and +0.248.
- **RAND:** the same pattern (day 60 +0.378 and +0.479).
- **The prior** (Linf beats L0 on practised kinds at day 30 in RULE, about 80%): **yes.**
- **The rule also made practised boxes easier.** At day 60, RULE against RAND: L0-128 0.752 against 0.477; Linf-32
  0.991 against 0.929.

## What it means (the assistant's reading)
- **Rohde and Plaut's warning** (limited memory hurts where the task has shared structure) **did not show up here.**
  Wiping the showing did not cost generalising to new boxes, and it learned the practised ones far faster.
- **But these brains generalise only a little** (about 0.1 on never-seen boxes, even with a simple rule). Generalising
  from a rule is a weak ability at this size and teaching length, for every memory type.
- **Together with WL3** (forgetting helps more in richer worlds; another session's study), the forgetting rule held in
  three settings: repeated boxes (WL/WL2), richer boxes (WL3) and rule-following boxes (WL4).
- **It is still one family of box tasks.**

## Limits
- One simple rule (arg-max over look segments); 24 children per cell; 6 held-out kinds; fixed learning rates.
