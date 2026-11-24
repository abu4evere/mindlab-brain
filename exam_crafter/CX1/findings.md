# CX1 findings: the Outside Exam, MBb in Crafter (final; 24 Nov 2026)

Plan `questions.md` (tag CX1-frozen; the creator's sign-off "yes go ahead start it"); analysis `analyse_cx1.py`
(frozen before data); blind recompute from the five raw files only (`recompute_cx1_blind.md`): **every score,
interval and reading agrees**. Each arm: about 1,000,000 Crafter steps (Crafter's protocol), seeds 1, 2, 3, ...

| arm | lives | Crafter score [95%] | what it achieved (% of lives) |
|---|---|---|---|
| BRAIN (MBb as it is, through the bridge) | 5,275 | **0.56%** [0.55, 0.57] | drink 93.5, eat cow 22.3, wake up 7.1 |
| RANDOM-5 (random choices, same bridge) | 5,923 | 0.53% [0.52, 0.54] | drink 32.9, eat cow 2.7, wake up 95.7 |
| RANDOM (Crafter's own random agent, 17 actions) | 5,944 | 1.54% [1.50, 1.57] | 13 achievements (sapling 50, plant 45, wood 24, table 4.2, ...) |
| SATED (water and cows hidden when full; assisted) | 5,321 | 0.81% [0.81, 0.81] | drink 90.1, eat cow 75.1, wake up 66.5 |
| RANDOM-5S (SATED's matched floor) | 5,909 | 0.53% [0.52, 0.54] | drink 32.8, eat cow 2.4, wake up 95.8 |

- **Primary, BRAIN − RANDOM-5: +0.028 [+0.017, +0.039] -> above.** The brain's own choices beat random choices through
  the same bridge, by a small margin: it finds water (93% vs 33%) and cows (22% vs 3%) far more often.
- **Scale, BRAIN − RANDOM: −0.98 [−1.01, −0.94] -> below.** Against Crafter's own random agent (published 1.6%; ours
  1.54%), the brain scores lower: through the bridge it can only move, "do" and sleep, so it never collects saplings,
  wood or makes anything, which is where a random agent's points come from.
- SATED − RANDOM-5S +0.28 [+0.27, +0.29]; SATED − BRAIN +0.25 [+0.24, +0.26].

## What it means
1. **The brain is not lost in a world it was never trained for**: through its own eyes (translated), it heads for
   water and food on purpose. That is the honest positive.
2. **It is a specialist**: it knows "find food and water", nothing else. 77% of its actions are "do" (mostly drinking
   when already full); it almost never sleeps (wake up 7%); it explores little (35 cells per life vs 41 random). When
   its satiety is shown to it (SATED), it stops over-drinking, explores 3x more cells (119) and eats cows in 75% of
   lives: it lacks a sense of "enough".
3. **Crafter's points come from making and collecting things** (22 achievements): a brain with no notion of tools,
   no hands beyond "do", and no learning within a life cannot earn them. This is the gap GPT's principle names: Bob
   must learn in a world, not be built for it. W3r (learning what things do within a life) is the first step toward it.

## Named limits
- The bridge (translation of Crafter's view into MBb's 5 layers, and a 5-move hand) is ours; RANDOM-5 shares it, so the
  primary comparison is fair, but the scale comparison is not like for like.
- RANDOM ran on the PC to 697,380 steps and on the Google VM for the rest (the creator needed the PC); Crafter lives
  are not bit-identical across machines (the amendment in questions.md).
- MBb does not learn in Crafter; the published agents learn for 1M steps. Their scores are for scale only.
