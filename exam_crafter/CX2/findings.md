# CX2 findings: learned meanings in Crafter (final; 25 Nov 2026)

Plan `questions.md` (tag CX2-frozen; the creator's sign-off "yes go ahead freeze it and start"); analysis
`analyse_cx2.py` (written before data); blind recompute from the five raw files only (`recompute_cx2_blind.md`):
**every score, interval and reading agrees** (its primary lower bound +0.0027 vs +0.004 here: the rng order; the reading
is the same either way). Each arm about 1,000,000 Crafter steps; PC (Windows); arms ran partly in parallel (the creator:
"max capacity"); Crafter is not repeatable within one process (amendment 2), so lives are not paired across arms.

| arm | lives | Crafter score [95%] | drink | wood | eat cow | wake up | zombie | cells/life |
|---|---|---|---|---|---|---|---|---|
| **LEARN** (meanings learned in each life) | 5,320 | **1.51%** [1.49, 1.52] | 91.5 | 86.8 | 15.6 | 30.1 | 18.8 | 65.8 |
| NAMED (meanings told, as CX1) | 5,284 | 0.60% [0.59, 0.62] | 93.4 | 0.4 | 22.9 | 7.3 | 0.2 | 35.7 |
| BLIND (no meanings) | 5,852 | 1.05% [1.03, 1.07] | 57.2 | 45.5 | 6.2 | 20.8 | 5.3 | 17.1 |
| LEARN-NP (no poke) | 5,734 | 0.21% [0.21, 0.21] | 0 | 0 | 0 | 69.7 | 0 | 112.9 |
| RANDOM-5P (random moves, same hand and tables) | 5,501 | 1.48% [1.46, 1.50] | 39.1 | 72.8 | 19.1 | 97.6 | 45.4 | 42.5 |
For scale: CX1's BRAIN (= NAMED with the old hand) 0.56%; Crafter's own random agent 1.54% (published 1.6%).

## The frozen readings
1. **Primary, LEARN − RANDOM-5P: +0.027 [+0.004, +0.052] -> above** (narrowly): with meanings it learned itself, the
   brain beats random choices through the same hand.
2. **LEARN − BLIND: +0.46 [+0.43, +0.48] -> above:** the learned meanings matter for the same brain and hand.
3. **LEARN − NAMED: +0.90 [+0.88, +0.93] -> above.** The "close" reading does not apply (it required NAMED above
   RANDOM-5P; NAMED − RANDOM-5P −0.88 [−0.90, −0.85]): **learning the meanings did better than being told them.**
4. LEARN − LEARN-NP: +1.29 [+1.28, +1.31]: without the poke the brain never learns what water or cows do (0 lives).

## Why LEARN beat NAMED (descriptive, from the raw logs)
- **Told meanings stop the body from touching the world.** NAMED's map says trees and stone are walls, so its brain
  plans around them: 0.1 blocked moves per life, so it almost never pokes anything but food (wood in 0.4% of lives).
  It drinks over and over (77% of its actions are "do", as CX1's brain).
- **Not knowing makes it touch things, and touching teaches.** LEARN starts each life not knowing what blocks: it bumps
  about 4.5 times per life (once per new kind, then the table knows), each bump becomes a poke, and poking a tree gives
  wood (86.8% of lives); it also hits zombies (18.8%), sleeps more (wake up 30.1%) and explores twice the cells (66).
- **It still finds food and water almost as well as when told:** drink 91.5% vs 93.4%; cow 15.6% vs 22.9%.
- The score gain is mostly Crafter giving points for touching things (wood, zombies, waking up), which the poke reflex
  makes happen. It is not crafting (no table, no tools: those actions are not in this body).

## Named limits
1. The poke reflex is ours, and it is what turns not-knowing into touching (LEARN-NP: 0.21%). The finding is "learning
   meanings + a touch reflex", not learning alone.
2. Crafter's score rewards touching; a world that punished touching (more lava) could reverse LEARN − NAMED.
3. The discovery measure ("water ranked first") is stricter than the achievement (LEARN: 56.4% of lives vs drink in
   91.5%); the recompute noted the gap; its cause is not yet checked (a measurement question for a follow-up, not a
   change to the readings).
4. MBb is fixed; only the eyes learn. Health and danger are not in the tables.

## What it means for Bob
The brain, told nothing about Crafter, learned within each life what blocks, what feeds and what waters, and did
**better** than with our hand-told meanings, almost matching Crafter's own random agent (1.51% vs 1.54%; CX1 0.56%).
The lesson is GPT's principle in data: what we told it made it rigid; what it found out for itself made it explore.
Next steps (for the creator): the Body v1 draft (`D:\mindlab\body\body_v1_draft.md`) with use/operate hands, so the
same learner can reach crafting; and a check of the discovery-measure gap.
