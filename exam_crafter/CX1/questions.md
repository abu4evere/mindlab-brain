# CX1: the Outside Exam, first sitting. Mind Lab's best brain, as it is, in Crafter (draft for freezing)

The creator, 23 Nov 2026: "what i want to do is just put our current best ai inside and lets see what score it will
get then learn other ai brain's how they work how they survived and is there anything that we should borrow from their
mind ... mind lab then crafter then acl".

## Why
Every world our brain has lived in (Mind Lab's lands, ACL) was written by us, so a good result may be our world's
quirk ("bug = law"), and our Bob Profile is our own ruler. Crafter (Hafner, ICLR 2022; `sources/hafner2021_crafter.pdf`,
full text read) is a survival world nobody of us wrote, with published scores for other brains and for expert humans.

## The question
What Crafter score does MBb (W3p's MoveVIN, seed 1, 236 learned numbers, NOT trained further) reach, as it is, through
a translation-only bridge, compared with Crafter's random floor measured by the same scorer on the same worlds?
Descriptive, not a hypothesis test: this is the brain's first outside measurement, the "before" mark.

## What runs (frozen code: `bridge.py`, `play.py`, `brain_mv.py`, `brains3.py`, `world3.py`, `mbb_seed1.npz`)
- **The bridge** (translation only, described in `bridge.py`'s header): Crafter's 9 x 7 view written into a 64 x 64
  map memory (W3's fixed writer); a 15 x 15 window in W3's 5 channels (wall = cannot step in; food = water, cow, ripe
  plant; shelter = own place; staleness 1 - exp(-age/200)); the 3 drives (hunger = the worse of food and drink, tired,
  curiosity by W3's rule); the hand: sample the brain's own softmax; a move into food = face it, then "do"; stay =
  "sleep". No chopping, placing or making move exists for it.
- **Arms** (after the council, 23 Nov; `CX1/council_2026-11-23.md`):
  - BRAIN: MBb through the bridge, as it is (the primary arm);
  - RANDOM-5: the same bridge and hand, each of the 5 moves uniformly at random (the matched floor: it isolates the
    brain's choices from the bridge's hand);
  - RANDOM: a uniformly random action of Crafter's 17 each step (Crafter's own floor, for scale);
  - SATED (secondary, labelled "assisted perception"): as BRAIN, but a food kind shows in the food channel only while
    the body is not full of it (water while drink < 9; cow and ripe plant while food < 9); hidden food is a wall (the
    body still cannot step in). A translation of Mind Lab's rule that food is eaten only when not full;
  - RANDOM-5S: RANDOM-5 with the same gating (SATED's matched floor; GPT's addition).
- **Protocol (Crafter's, section 3.3):** lives on Crafter seeds 1, 2, 3, ... (default `crafter.Env`, 64 x 64, view 9,
  length 10,000), played in order until the total reaches 1,000,000 steps (the life that crosses 1M is completed and
  counted, as in a training run's last episode). Each arm's random stream: `np.random.default_rng(seed)` per life.
  The smoke seeds 900001+ are not used.
- **Machine:** one machine for both arms, recorded (the PC or a Linux VM).

## Measures (written before the data; `analyse_cx1.py`, frozen with the plan)
1. **Primary:** BRAIN - RANDOM-5 in Crafter score, with its bootstrap interval. Each arm's Crafter score, S = exp(mean_i ln(1 + s_i)) - 1, s_i = % of lives with achievement i at least
   once (the paper's footnote 2), with a 95% bootstrap interval over lives (2,000 resamples, seed 0), and the
   differences (lives resampled within each arm): BRAIN - RANDOM-5 (primary), BRAIN - RANDOM (scale),
   SATED - RANDOM-5S and SATED - BRAIN (secondary).
2. The 22 success rates for each arm, beside the published table (README scoreboard, `D:\acl\docs\research\
   crafter_scoreboard_2026-11-23.md`; the published numbers are other people's runs, a comparison of scale only).
3. Life length (steps) mean and median; share of lives ending by health vs the 10,000-step limit.
4. What the brain did: share of its actions that were moves, "do", "sleep"; drinks and cow kills per life; places
   visited per life; the success rates of the 4 achievements the hand can reach on purpose (collect_drink, eat_cow,
   eat_plant, wake_up), since the 22-achievement score mostly counts things this brain cannot do.
Every number with its population (lives, steps).

## What would count
- Primary interval entirely above 0: "the brain's own choices beat random choices through the same bridge"; entirely
  below 0: "its choices are worse than random ones here"; otherwise: "not separable".
- BRAIN vs RANDOM is reported for scale (expected below: no move for wood or tools, which random play gets by accident).
- SATED is assisted perception, never reported as the brain's unassisted result. If gating helps a lot, that shows an
  interface mismatch (one food channel for two needs), not necessarily a reasoning failure (GPT).
- Either way the result is the "before" mark; it says nothing yet about a trained or upgraded brain.

## Known limits (named before the data)
- The bridge is an approximation; the brain was raised on one food kind in a 15 x 15 land, where eaten food
  disappears. In Crafter water never runs out (the smoke: it drank hundreds of times in a row while its food ran out).
  This is reported, not fixed: fixing it would be writing decisions for the brain.
- The published agents LEARN during their 1M steps; MBb does not learn here. The published scores are for scale only.
- The bridge reads Crafter's map (semantic view), not its picture: at night the picture darkens for image-based
  brains, but the map does not; a small advantage for MBb, named here.
- Sleeping is risky in Crafter (a zombie deals 7 damage to a sleeper, 2 to one awake; crafter/objects.py): shelter =
  own place is where rest is possible, not a protection.
- Pilot (smoke, seeds 900001+, about 3,000 steps per arm, not part of the study): BRAIN 0.60%, SATED 0.80%,
  RANDOM-5 0.57%, RANDOM-5S 0.54%, RANDOM 1.31%; about 100 steps per second on the loaded PC (about 3 hours per arm).

## Checks before the run (`checks_cx1.py`, All: PASS required; 8 checks, All: PASS on 23 Nov)
1. Semantic ids: the bridge's names match Crafter's `_mat_ids` and object order.
2. The window: a known world cell appears at the expected window place (orientation x/y).
3. The hand: a food cell to the east gives move_right, then "do" once facing east.
4. The score: a hand-made set of lives gives the formula's value; all 0 gives 0; all 100 gives 100.
5. Determinism: the same seed gives the same life twice (both arms).
6. The brain is the W3p brain: MBb's 236 numbers loaded unchanged (hash of the npz equals W3p's kept copy).
7. RANDOM-5 shares the hand (into food when facing it = "do"; stay = "sleep").
8. SATED gating: water hidden and a wall while drink = 9, shown while drink < 9, cows by food; the primary bridge
   unchanged.

## Then (not part of CX1)
Read how the published brains work (DreamerV3, Curious Replay, PPO-ResNet, Achievement Distillation, Plan2Explore,
RND, SPRING), with labels for what was read, and list what could be borrowed; any borrowed idea is built and tested
in Mind Lab first (the creator's order: Mind Lab, then Crafter, then ACL).

Status: FROZEN, 23 Nov 2026. Signed off by the creator in chat ("yes go ahead start it"), after the council.
Machine: the creator's PC (Windows), all 5 arms, at most 2 at a time at Idle priority; output in `CX1/output/`.
