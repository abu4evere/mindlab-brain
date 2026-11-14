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
| **sequence memory** | a learned recurrent state that carries what was just shown through the try | WS: deferred imitation 0.91 vs 0.43; skill after teaching stops 0.92 vs 0.54; nightly replay = only extra copying | proven in the workshop |
| **drives** | survival, comfort, curiosity (the creator's three) as the only motives | – | to test (Mind Lab "drives only") |

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
3. **W3:** the drives only (survival, comfort, curiosity), no task reward: does the brain keep pushing on its own?
4. **W4:** the parts together in one brain on a small food world with others (sharing, copying, restraint).
5. **The ACL validity test** (frozen; council; recompute). If it passes, the Long World starts with this brain.
