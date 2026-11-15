# WR findings: the recipe in one brain (exploratory; numbers from `analyse_wr.py`)

Plan: `questions.md` (WR-frozen). Checks All: PASS before data (`checks.log`; the one generic child reproduces WY's
Base and TBYS, WF's RP and WL2's L0 and Linf child for child). Run 15 November 2026 on GitHub's machines, 24 jobs of
48 children (each job ran the checks again: All: PASS in 24 of 24). Full tables: `analysis.md`. Mind Lab: exploratory,
no council; an independent blind recompute is recorded in `recompute.md`.

The four parts: **L** learn without the showing in mind (WL2), **T** don't repeat a failure (WM), **Y** "that worked!"
(WY), **R** a fast memory replayed at night (WF). **LTYR** is the recipe; **TYR** is WF's replay brain, the best so far.

## 1. The changing world: the recipe relearns as well as the replay brain, and no better
Own skill on the changed kinds (tests use the network only), 128 neurons, 48 children each:

| arm | before the change (A30 / B45) | A, 14 days after (A45) | B, 14 days after (B60) | stale habit day 33 | food |
|---|---|---|---|---|---|
| Base | 0.61 / 0.89 | 0.11 | 0.00 | 0.58 | 828 |
| L alone | 1.00 / 1.00 | **0.00** | **0.00** | 0.98 | 938 |
| TY (WY's TBYS) | 0.71 / 0.84 | 0.12 | 0.06 | 0.81 | 1058 |
| TYR (WF's replay brain) | 1.00 / 1.00 | 0.51 | 0.45 | 0.84 | 1487 |
| **LTYR, the recipe** | 1.00 / 1.00 | **0.44** | **0.44** | 0.88 | **1513** |
| LTY (no replay) | 0.96 / 0.94 | 0.08 | 0.08 | 0.95 | 1170 |
| LYR (no don't-repeat) | 0.99 / 1.00 | 0.01 | 0.00 | 0.99 | 1073 |
| LTR (no "that worked!") | 1.00 / 1.00 | 0.35 | 0.28 | 0.96 | 1422 |

- **LTYR − TYR (size 128):** A45 −0.062 [−0.118, −0.007]; B60 −0.007 [−0.056, +0.042]; A30 and B45 0.000 (both at
  1.00); food +25 [+17, +33].
- **Size 32:** A45 −0.007 [−0.049, +0.035]; B60 +0.028 [−0.021, +0.076]; food +84 [+72, +97].
- **Reading 1 ("loses nothing", lower bounds above −0.05): NO,** by the group-A reading at size 128 (−0.118) and,
  by 0.006, the group-B reading (−0.056, a tie in substance). Before the change it is an exact tie. **Reading 2
  ("gains"): NO.**
- So adding L to the replay brain gives the same relearning (a little less on group A at size 128), the same perfect
  skill before the change, and a little more food.

## 2. Which parts carry it (size 128; the recipe minus the recipe without that part)
| part removed | A45 | B60 | food |
|---|---|---|---|
| **R, night replay** (LTYR − LTY) | **+0.368 [+0.285, +0.451]** | **+0.361 [+0.285, +0.438]** | +343 |
| **T, don't repeat** (LTYR − LYR) | **+0.431 [+0.340, +0.521]** | **+0.444 [+0.368, +0.521]** | +440 |
| Y, "that worked!" (LTYR − LTR) | +0.090 [+0.049, +0.139] | +0.160 [+0.097, +0.222] | +91 |
| L, no showing in mind (LTYR − TYR) | −0.062 [−0.118, −0.007] | −0.007 [−0.056, +0.042] | +25 [+17, +33] |

- **Reading 3 ("each part earns its place"): YES by the frozen rule,** but read it with care: **L earns its place
  through food only** (+25 at size 128, +84 at size 32), not through skill. R and T are the relearning: without either,
  relearning falls to about 0. Y adds a clear share (+0.09 and +0.16).
- **Linf alone is the worst relearner of all:** perfect before the change (1.00 and 1.00) and **0.00** after it, with
  the deepest stale habit (0.98 at day 33, 1.00 at day 48). Learning everything from its own knowledge made the old
  codes a habit that nothing in it can undo. That is the parrot's opposite failure.
- At size 32 the picture is the same (R +0.31, T +0.34, Y +0.11 to +0.13; L ties on skill, +84 food).

## 3. The stable world: the recipe keeps Linf's perfect learning and starts faster
Own skill (no showing), 48 children each:

| arm | size 128: day 7 / 15 / 30 / 60 | size 32: day 7 / 15 / 30 / 60 | food (128 / 32) |
|---|---|---|---|
| L0, perfect memory | 0.05 / 0.03 / 0.04 / 0.81 | 0.02 / 0.15 / 0.35 / 0.92 | 1494 / 1189 |
| L (WL2's Linf) | 0.82 / 1.00 / 1.00 / 1.00 | 0.10 / 0.73 / 1.00 / 1.00 | 1859 / 1558 |
| TYR (no L) | 0.80 / 1.00 / 1.00 / 1.00 | 0.18 / 0.85 / 1.00 / 1.00 | 2012 / 1766 |
| **LTYR, the recipe** | **0.88** / 1.00 / 1.00 / 1.00 | **0.42 / 0.98** / 1.00 / 1.00 | 1984 / 1863 |

- **Reading 4 ("no cost"): YES.** LTYR − L is exactly 0.000 at days 30 and 60 at both sizes (all at 1.00).
- **The recipe starts faster:** LTYR − L at day 7 +0.062 [+0.021, +0.104] (size 128) and **+0.319 [+0.253, +0.385]**
  (size 32); at day 15, size 32, +0.250 [+0.194, +0.309]. Food +125 (128) and +305 (32).
- **Reading 5 ("night replay alone cures the parrot"): YES.** TYR-128, with the showing held in memory during every
  try, reaches **1.000** at day 30 (L0: 0.04). Night replay from its own successes trains the network without the
  showing, which is what Linf does by day. The after-showing skill is 1.00 for every arm at size 128.

## What it means (the assistant's reading)
- **The four parts fit together without fighting.** Nothing broke: before any change the recipe is perfect at both
  sizes, in both worlds, and it earns the most food of any learned brain so far (1,513 in the changing world, 1,984 and
  1,863 in the stable one).
- **But the recipe is not more than the replay brain.** Relearning 14 days after a change is about 0.44 either way.
  The ceiling is the same one WF met: the slow network's habit (stale 0.88 two days after the change). What was learned
  from one's own successes becomes as fixed as what was copied from a teacher.
- **Two of the four parts are the relearning:** a search that does not repeat failures (T) finds the new code; a fast
  memory replayed at night (R) writes it in. "That worked!" (Y) helps on top. **Learning without the showing in mind
  (L) is a cure for the parrot, and night replay is another cure for the same disease;** having both gives a faster
  start and more food, not more relearning.
- **For Bob:** the brain's next missing piece is not a fifth learning part but a way to **loosen a habit when it
  fails**, so that what the fast memory finds can replace it faster than 14 days. WF's acting store (WSLS, engineered)
  showed the size of the prize (1.00 within a week). The creator's doubting test and the Red Pill idea
  (`D:\acl\docs\OPEN_DECISIONS.md`) point the same way.

## Limits
- One task family; the parts keep their own studies' numbers; two sizes; 48 children per cell; no evolution.
- Tests count the slow network only; a brain whose fast store also acts is a separate question.
- The plan was reviewed by the assistant alone (three critic sessions stopped on a usage limit; recorded in
  `questions.md`).
