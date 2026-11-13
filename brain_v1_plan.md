# The starting brain for ACL: plan (draft, 12 November 2026)

**Goal (the creator):** "we gotta build good basic starting brain to put into acl". It goes into the Long World only
after one frozen test shows it is valid: the new brain against the old minds, by ACL's survival rule (extinct at most
the old minds' + 3; population ratio upper bound ≥ 0.80).

## The parts, and the evidence for each
| part | what it does | evidence | status |
|---|---|---|---|
| **seeing space** | a convolutional view of the nearby land (food, water, kin, danger), centred on the person | W1b: a flat network cannot learn to walk to visible food; W1c: convolution can (0.95 in empty rooms from reward) | proven in the workshop |
| **planning** | a value-iteration layer that spreads "how far is what I need" over the map | W1d: helps (iteration and the max both matter), value map 0.71–0.83 like a true distance map; detours still 0.15–0.25 | being fixed (W1e: corners, read-out) |
| **memory** | a short window of recent things (or a recurrent state) | Cradle C1: needed to keep up with routines; a window is as good as recurrence there | proven in Cradle |
| **copying** | an imitation step toward what others are seen doing | Cradle C2: watching alone teaches no method; copying does (×3) | proven in Cradle |
| **feelings** | an inborn reluctance to harm (on the choice); hunger, rest, love of one's child | ACL NB3: the reluctance ended the killing; learned feelings did not | proven in ACL |
| **drives** | survival, comfort, curiosity (the creator's three) as the only motives | – | to test (Mind Lab "drives only") |

## What ACL needs for it
- **A map input:** each week, a small egocentric grid of the person's surroundings (food, water, people, kin, danger),
  from the world's own state. Read-only from the world; a brain change only.
- **Moves as the network's own choices:** at first, the network scores ACL's existing options (as NB2/NB3 did), with
  the planner's value at each option's target added. Later, perhaps, the options are replaced by moves.
- **Demographics:** NB3-A's trap (more children, less sharing) is a brain question too: the "drives" must weigh
  another child against food. It is to be tested in the workshop before ACL.

## Order of work
1. **W1e** (running): a planner that does not cut corners, and a read-out check.
2. **W2:** a partial view plus a remembered map (a person cannot see the whole land). Planning on what one remembers.
3. **W3:** the drives only (survival, comfort, curiosity), no task reward: does the brain keep pushing on its own?
4. **W4:** the parts together in one brain on a small food world with others (sharing, copying, restraint).
5. **The ACL validity test** (frozen; council; recompute). If it passes, the Long World starts with this brain.
