# The starting brain for ACL: plan (draft, 12 November 2026)

**Goal (the creator):** "we gotta build good basic starting brain to put into acl". It goes into the Long World only
after one frozen test shows it is valid: the new brain against the old minds, by ACL's survival rule (extinct at most
the old minds' + 3; population ratio upper bound ≥ 0.80).

## The parts, and the evidence for each
| part | what it does | evidence | status |
|---|---|---|---|
| **seeing space** | a convolutional view of the nearby land (food, water, kin, danger), centred on the person | W1b: a flat network cannot learn to walk to visible food; W1c: convolution can (0.95 in empty rooms from reward) | proven in the workshop |
| **planning** | a value-iteration layer (plus-shaped, V+) that spreads "how far is what I need" over the map | W1d: iteration and the max matter; W1e: the plus pays with training (150k: 0.54 vs 0.35; 500k exploratory: 0.70, still rising) | works; needs long training |
| **map memory** | a fixed writer that keeps what was seen (wall / open / unknown); the planner runs on it | W2: lifts familiar-room detours 0.09 → 0.46; erased or wrong maps take it away; a recurrent memory did not learn to use the tour | proven in the workshop (engineered memory, learned planner) |
| **memory** | a short window of recent things (or a recurrent state) | Cradle C1: needed to keep up with routines; a window is as good as recurrence there | proven in Cradle |
| **copying** | an imitation step toward what others are seen doing | Cradle C2: watching alone teaches no method; copying does (×3) | proven in Cradle |
| **feelings** | an inborn reluctance to harm (on the choice); hunger, rest, love of one's child | ACL NB3: the reluctance ended the killing; learned feelings did not | proven in ACL |
| **sequence memory** | a learned recurrent state that carries what was just shown through the try | WS: deferred imitation 0.91 vs 0.43; skill after teaching stops 0.92 vs 0.54; nightly replay = only extra copying | proven in the workshop; WS correction 1: the own-skill gain comes from the loop within a try, not from holding the showing (WL2). |
| **drives** | survival, comfort, curiosity (the creator's three) as the only motives | W3: no learned brain survived (survival 0 for every brain; lifespans 195–246 steps, random 174, script 2,963); curiosity explores (land known +0.10; curiosity-only 0.86); the hunger link never pointed reliably at food | **failed as built**: learning from sparse reward too slow (W3b proposed, needs the creator) |
| **learning without replaying the teacher** | copy a showing, then try from one's own knowledge (memory of the showing wiped or fading) | WL (the creator's idea): big brain own skill at day 30 0.82 vs 0.04; WL2: forgetting, not noise; wiped memory 1.000 by day 30. Caution: Rohde & Plaut 1999 found limits did not help in a richer task | proven in the box task; to test in a richer world |
| **"that worked!"** | learn strongly from one's own surprising success | WY: first learning +0.13 to +0.15; food much higher | proven in the box task |
| **don't repeat a failure** | a short list of what just failed, avoided while searching | WM: finds new answers (food up) but alone keeps none | engineered; works with the fast memory |
| **fast memory + rest replay** | a store of what just worked, replayed at night into the slow network | WF: relearning after a change 0.45–0.51 vs 0.06–0.12; acting from the store (engineered) about 1.00; WR: all four parts together fit, relearning 0.44 | proven in the box task; the first real learning from mistakes |

## What ACL needs for it
- **A map input:** each week, a small egocentric grid of the person's surroundings (food, water, people, kin, danger),
  from the world's own state. Read-only from the world; a brain change only.
- **Moves as the network's own choices:** at first, the network scores ACL's existing options (as NB2/NB3 did), with
  the planner's value at each option's target added. Later, perhaps, the options are replaced by moves.
- **Demographics:** NB3-A's trap (more children, less sharing) is a brain question too: the "drives" must weigh
  another child against food. It is to be tested in the workshop before ACL.

## Order of work
1. **W1e** (done): V+, the plus-shaped planner; train long.
2. **W2** (done): a remembered map works; how to treat the unknown is left to the drives.
3. **W3:** the drives only (survival, comfort, curiosity), no task reward: does the brain keep pushing on its own? **Done 15 November: no** (W3/findings.md). The box-task recipe (14–15 November: WL2, WY, WM, WF, WR) is the candidate fix (W3b, with the creator).
4. **W4:** the parts together in one brain on a small food world with others (sharing, copying, restraint).
5. **The ACL validity test** (frozen; council; recompute). If it passes, the Long World starts with this brain.
