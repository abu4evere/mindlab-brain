# The Bob Profile: five abilities, 20 points each (v2, 21 November 2026; levels 2 and the built parts of 5 frozen as `BP-frozen`)

**Why.** The creator, 20 November 2026: "from this scale we should aim at least getting 60+ overall and each one at
least 10+". The assistant's first rating of the living brain (W3n's HRS) was about 13/100, a judgment. This draft turns
the scale into fixed tests with anchored levels, so that every brain gets a measured score, run the same way, and
nobody (the assistant included) can fool themselves.

It sits beside the scorecard's Parts A and B (`tests_draft.md`): those items are indicators and are never summed. The
Bob Profile is the creator's yardstick, and it is summed.

## v2 (21 November 2026, after the council: `bp_council_2026-11-21.md`, GPT and Gemini)
These changes override v1 where they differ.
1. **The five-number profile is the result; the floor decides.** "At least 10 in every ability" is the goal; the total is
   secondary. Levels are ordinal milestones, not equal steps.
2. **Every score names its source:** what the architecture (the designer) gives, and what was learned.
3. **A cheater control per test**, beside the positive (Script) and negative (random) controls: greedy for the detours;
   **memory erased** for memory 2; the bare body for autonomy; the frozen copy for learning 5.
4. **Statistics:** the unit is the training seed (at least 8); each seed is tested on W3's 50 test lands (the detours
   use the 36 lands that have a qualifying case); pass on the one-sided 95% bootstrap lower bound over seeds (numpy seed
   20261121).
5. **Split tests:** reasoning 5 = a detour half and a value half; autonomy 5 = bare survival and seeking information;
   generalization 10 = changed causes and a different world.
6. **Generalization 2** is now a topology shift: lands of a new kind (W3's generator with 8 wall segments, not 4; seeds
   940001–940050), against the brain's own standard test lifespan (ratio ≥ 0.5). Learning 2 keeps the held-out lands.
7. "No catastrophic forgetting" moves to learning 10; memory 10 becomes long-delay recall with a memory intervention.
8. Levels 15 and 20 are provisional. 20 = human performance under matched senses and budgets when that can be run;
   otherwise the grid-world ceiling (the best known agent with the same senses).

### The frozen tests (`bp/bp_tests.py`, `bp/bp_score.py`)
| test | what | pass |
|---|---|---|
| Learning 2 (L2) | lifespan on the 50 test lands, body as trained; normalised (brain − random) / (Script − random) | lower bound ≥ 0.50 |
| Reasoning 2 (R2) | memory knows walls, shelter and one food patch; hungry, no reflex; start at the easiest cell whose path is ≥ 5 and detour ≥ 4; reach the patch within 3 × the shortest path, with the brain's moves drawn as in its life | lower bound ≥ 0.80; Script ≥ 0.95; greedy and random ≤ 0.20 |
| Reasoning 5, detour half (R5d) | the same with path ≥ 10 and detour ≥ 10 | as R2 (the value half is not built: level 5 not awarded) |
| Memory 2 (M2, M2e) | food seen 100 steps ago, now out of sight (the cell nearest 8 steps away); the same with the food erased from memory | success lower bound ≥ 0.80 and the drop (M2 − M2e) lower bound ≥ 0.20; Script ≥ 0.95, random ≤ 0.20 |
| Memory 5 | needs a learned memory of its own | brains whose map memory is written by our code fail by construction |
| Generalization 2 (G2) | lifespan on the 50 new-kind lands / lifespan on the 50 test lands, body as trained | lower bound ≥ 0.50 |
| Autonomy 2 (A2) | on lands where the first step toward food and toward the shelter differ, memory known: first move when hungry (energy 60) vs tired (tiredness 150); tracks = ½[(P food|hungry − P food|tired) + (P shelter|tired − P shelter|hungry)] | lower bound ≥ 0.30; Script ≥ 0.90; random within ±0.15 |
| Autonomy 5, survival half (A5s) | bare (no reflexes) full lives on the 50 fresh lands | lower bound ≥ 0.50 (the information half is not built: level 5 not awarded) |

### Recorded honestly: what was seen before freezing
- While building, R2 and M2 were run on W3n's HRS seeds 1–3 and the controls.
  - R2 with the hardest detour on each land: 22–44% success.
  - R2 with the brain's most likely move instead of a drawn one: lower still.
  - M2: 90%.
- Two choices were then made, both following v1's text, and both in the brain's favour:
  - the detour start became the easiest qualifying cell ("behind one obstacle");
  - walks use moves drawn from the brain, as in its life.
- The 0.80 pass line was set in v1 before any run and was not changed.
- R2 still gave 19–42% on seeds 1–3 after these changes. The scored battery runs on seeds 1–3 again (the same code)
  and on 5 more seeds.

## The rules (v1)
1. **Anchors, not opinions.** Each ability has six levels: **0, 2, 5, 10, 15, 20**. A level counts only when its test
   passes. A brain's score in an ability is the highest level it passes, with every lower level passed too. Scores are
   therefore 0, 2, 5, 10, 15 or 20 per ability; finer steps may be added later, never invented after seeing results.
2. **20 = adult-human level** in that ability, on an equivalent test. Where a human can play the same test (through a
   simple game page), human players set the 20 anchor; otherwise 20 is described and not yet testable.
3. **Every test is frozen before it is run**, with:
   - a **positive control** that must pass (a scripted agent built to have the ability), so a failure means the brain
     failed, not the test;
   - a **negative control** that must fail (a random agent);
   - a pass rule on the **lower bound of an interval** over training seeds (at least 8), never on a point estimate.
4. **The designer's help is named.** Parts we wrote (sorted senses, the fixed map memory, the reflexes, the parent)
   are listed with every score. Memory must be the brain's **own** above level 2. Autonomy is tested **bare** (no
   reflexes) above level 2. The others are scored with the body as designed, and also reported bare.
5. **Untested is not zero and not a pass:** it is shown as "—". The total counts only measured levels.
6. Scores belong to a brain **version** (code, weights, seeds), and are re-measured, never carried over.

## The abilities and their levels

### Learning (new tasks, within a life)
| level | the test passes when |
|---|---|
| 2 | trained on its home task, it beats the random agent by a wide margin on held-out lands |
| 5 | after a lasting change (a food patch moves for good, or two foods swap value), it recovers to ≥ 80% of its earlier performance within a fixed number of steps (300), with no teacher and no retraining from outside the life |
| 10 | it learns a never-seen task within one life (for example a new object that feeds it only when visited after another), reaching ≥ 50% of a scripted solver within 3,000 steps |
| 15 | on new tasks in its world, it learns within 2× the number of tries human novices need |
| 20 | across a series of new tasks it gets faster each time (learning to learn), at human level |

### Reasoning (multi-step problems)
| level | the test passes when |
|---|---|
| 2 | a detour: it reaches a goal ≥ 5 steps away behind one obstacle, clearly better than a greedy agent |
| 5 | it solves detours that need a 10+ step move away from the goal, and chooses between a near small reward and a far large one by their value |
| 10 | it solves ordered sub-goal problems (for example key → door → food, order matters) on unseen layouts, ≥ 70% |
| 15 | it solves new puzzles that need inference from what it observed (which lever opens which door) and simple tool use |
| 20 | human-level on a battery of new multi-step puzzles in its world |

### Memory (long-term recall)
| level | the test passes when |
|---|---|
| 2 | it returns to something seen 100+ steps earlier and now out of sight (any memory, including one we wrote) |
| 5 | its **own learned** memory recalls a place or fact after 1,000 steps of distraction, ≥ 80% |
| 10 | it keeps what it learned: after learning task A, then task B, it still does A at ≥ 80% (no catastrophic forgetting), 10,000+ steps later |
| 15 | it recalls specific events (what, where, when) and uses them to plan |
| 20 | human-level long-term memory on equivalent tests |

### Generalization (new situations)
| level | the test passes when |
|---|---|
| 2 | on fresh lands of its world it keeps ≥ 50% of its training-land performance |
| 5 | when the surface changes but the rules hold (new colours or codes, a bigger map), it keeps ≥ 80% of its performance |
| 10 | in a world with changed causes (moving food, a new hazard, different body costs) it adapts within one life to ≥ 70% of a scripted agent; and it does better than chance in a different kind of world without retraining |
| 15 | it carries its skills into a substantially different world (for example ACL) with little adaptation |
| 20 | human-level transfer |

### Autonomy (its own goals)
| level | the test passes when |
|---|---|
| 2 | it acts from its own needs (no goal given from outside), and when two needs compete its choice follows their sizes |
| 5 | **bare** (no reflexes, no teacher) it survives ≥ 50% of lives on fresh lands, and with its needs met it chooses an informative observation over an equally new but useless one |
| 10 | the **Unassigned Problem Test** (scorecard Part A): it notices an opportunity, forms a goal that is not one of its built-in needs (for example storing food before a lean season), plans, and revises the plan when blocked |
| 15 | it holds a multi-step project across interruptions, chooses its own sub-goals, and turns away from a bad teacher |
| 20 | human-level self-directed goal pursuit |

## What exists today, and what each level needs (the assistant's reading, before any test)
| ability | expected now | evidence so far | what is missing for the next level |
|---|---|---|---|
| Learning | 2 | W3 brains far above random | 5: relearning within a life (WF showed it in box tasks with a fast memory; not in this brain) |
| Reasoning | 2, maybe 5 | the 30-round planner finds routes; drives trade off | 5: a frozen detour and near-small/far-large test |
| Memory | 2 | the map memory is our fixed writer | 5: a learned memory |
| Generalization | 2, maybe 5 | fresh lands 0.90 with reflexes; W3o (raw eyes) is testing level 5's surface change | 5: W3o's RE; a bigger map |
| Autonomy | 2 | its goals come from its drives | 5: bare fresh-land survival ≥ 0.50 (today 0.37, W3n preliminary) and the informative-observation test |
| **Total** | **about 10, at most 16** | | **the creator's goal: 60+, each ability 10+** |

## Steps
1. The creator reads this and changes what they want (levels, examples, the human anchor).
2. Council (GPT, Gemini), asked neutrally: are the anchors fair, testable, not gameable?
3. Build the tests as Mind Lab tasks, level 2 and 5 first (they run in W3's world and the box tasks), with their
   positive and negative controls.
4. Freeze (`BP-frozen`), then score the living brain (W3n's HRS), the W3o brains and the old 32-neuron brain. This is
   the baseline, and it is expected to be low.
5. Later: a "play it yourself" page so that people can set the human anchors.
