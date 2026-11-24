# W3r: learning what things DO within one life (DRAFT, not frozen; 24 Nov 2026)

**Why:** W3o's open gap: when the colours of wall, food and shelter are dealt anew on each land (RV), the brain breaks
(RVS − HRS −1,482; fresh-land survival 0.27): it cannot learn "I ate where it was this colour, so here this colour is
food" within one life. BX1's ACL school showed the same gap from the other side (it learned how a week felt, not which
choice caused it). The top Crafter brains all learn a **model of consequences** (`D:\acl\docs\research\
crafter_brains_borrow_2026-11-24.md`); Plan2Explore adds **curiosity = disagreement** of a small ensemble of such models.
The creator, 24 Nov 2026: "learn it and if there are things we should take, take it use in ours".

**The question:** can a brain that learns, within each life, what each colour DOES to its body see through colours
that change from land to land?

## The borrowed part: a meaning module (body only; no names, no new rewards)
- Three consequences the body itself feels, at a cell: **blocked** (tried to step in and did not move), **fed**
  (energy rose by a meal there), **rested** (tiredness fell there).
- An ensemble of K = 5 tiny linear predictors (Plan2Explore's ensemble size) maps a cell's 3 colour values (+ bias) to
  the 3 consequences: 5 × 4 × 3 = 60 numbers, **reset at birth** (it learns within the life only), each member with
  its own random start and its own random subset of the events (bootstrap, as in the paper).
- Each step it learns from what just happened (one gradient step on the squared error, at the cell the body tried to
  enter or stood on). Learning rate, initial spread: to set in a calibration before the study (named below).
- **What the brain sees:** in place of the 3 colour layers, the module's mean predictions for each remembered cell:
  [blocked, fed, rested], i.e. learned wall, food and shelter layers. The brain (W3n's HR brain, trained on sorted
  layers) is unchanged.

## Arms (W3o's RV land rules, W3n's HR body and parent, the same seeds, paired)
| Arm | The brain sees | Curiosity layer |
|---|---|---|
| **RV** (control, rerun on the same machine) | the colours (W3o) | staleness (as now) |
| **RM**, meaning | the learned consequences | staleness |
| **RMD**, meaning + disagreement | the learned consequences | the ensemble's disagreement (variance) about each remembered cell, in place of staleness (Plan2Explore) |
| **HR** (ceiling, existing W3n data or rerun) | the sorted layers (the truth) | staleness |

## Measures (as W3o, so results compare)
Lifespan, full lives, fresh-land survival (the primary), steps toward food alone, deaths by cause; plus the module's
own: how soon in a life its "fed" prediction ranks the food colour first (steps), and its error.
Primary: **RMS − RVS** (the kept copy, fresh lands), the paired difference with a 95% bootstrap interval; second:
RMDS − RMS (does disagreement-curiosity add?); the gap left to HRS.

## Named limits and open questions for the council
1. The module sees colours exactly (3 clean bits); a real eye is noisier. A first rung.
2. Its three consequences are chosen by us (blocked, fed, rested): they are the body's own signals, not named things,
   but the choice of three is ours. Alternative: predict the whole body change (ΔE, ΔF, moved) and let the brain read
   it.
3. The brain was trained with sorted layers that are exactly 0/1; learned layers are soft. Should the brain also train
   with the module in place (yes in the main arms: the whole life history runs with it)?
4. The parent (W3's script) and the reflexes read the world's own memory, as before: only the brain's view changes.
5. Compute: 4 arms × 16 seeds × 4.0M steps on the Oracle and Google VMs (never GitHub), each machine's runs paired on
   that machine.

Next: council (GPT, Gemini, DeepSeek), then the frozen plan, checks (RM with a perfect module = HR bit for bit),
calibration, the creator's sign-off.
