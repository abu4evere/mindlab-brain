# WL4: forgetting when things follow a rule (does it hurt generalising?) (plan, frozen before any code or data)

**Frozen** as git tag `WL4-frozen`, before any code or data.
- **The creator** (15 November 2026): "go ahead … find something useful".
- **Why:**
  - WL3 found that forgetting the showing helps more with more things and longer sequences, but its codes were random.
  - Rohde and Plaut (1999) found that limited memory hurt where the task had shared structure.
  - Here the codes follow a rule, and new boxes never seen test generalising.
- **Exploratory:** no council.

## The worlds (WN's teaching: a showing before every try on days 1–30, none after; 60 days)
- **30 kinds:** 24 practised (3 tries per kind per day, 72 a day) and 6 held out (never shown, never practised; tests
  only).
- **Looks:** each kind's look is N(0, 1) in 16 numbers; each encounter adds noise N(0, 0.2²).
- **RULE world:** the code follows the look.
  - Lid 1's first act is the arg-max of look[0:4] and its second act the arg-max of look[4:8].
  - Lid 2's acts are the arg-max of look[8:12] and look[12:16].
  - (Taken on the kind's own look, without the noise.)
- **RAND world (the control):** the same 30 looks; codes drawn at random (WS's draw: 2 different pairs per kind). A
  held-out kind can then only be guessed.
- **Draws:** looks and random codes from `[seed, 31]`; daily orders and noise from WS's `Home.day` arithmetic, over
  the 24 practised kinds.

## Arms (WL2's episodes; memory children of 32 and 128 neurons; 24 children each, seeds 1–24; WS's learning)
- **L0:** perfect memory of the showing.
- **L2:** wait 8, noise 0.6.
- **Linf:** the memory wiped before each try (the copy step also without the showing).

## Measures (descriptive; 95% bootstrap intervals over seeds, paired; numpy seed 20261128)
- Own skill (full boxes, no showing) on practised kinds and on **held-out kinds** at days 15, 30 and 60. Test looks
  carry noise from `[seed, 6, day, 0]`.
- Linf − L0 and L2 − L0 on both, per world and size.
- **Floor:** in RAND, held-out success is expected near 0 (1 in 256 by chance). If RULE's held-out success is below
  0.05 for every arm, generalising is "not shown at this scale".

## The questions
1. Does a rule let these brains generalise to boxes never seen (RULE held-out above RAND held-out)?
2. **Does forgetting hurt generalising** (Linf − L0 on RULE held-out kinds, day 60)?

## The assistant's prior
- **Q1:** RULE held-out success above 0.20 for at least one arm at day 60: about 55%.
- **Q2:** Linf at least as good as L0 on RULE held-out at day 60 (interval not below −0.05): about 55%.
- Linf still beats L0 on practised kinds at day 30 in RULE: about 80%.
