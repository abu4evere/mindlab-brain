# WLP draft: a room with one toy, and a curiosity for getting better (DRAFT; not frozen; 16 November 2026)

*Drafted after WG2 (`D:\acl\docs\research\learning_progress_curiosity_2026-11-16.md`). The creator has asked the
assistant to choose next steps without asking. This goes to a freeze after one more look at the design's cost.*

## The room
- **WQ's silent room plus one toy:** a lever cell L and a lamp cell P, both visible in the map memory as an extra
  channel (lamp on or off).
- **Rule:** stepping onto L toggles P, but only if P has been off for at least 20 steps.
- The rule is learnable by watching what happens.

## The brain
- **W3c's GYFR planner, plus a small learned forward model:**
  - it predicts the lamp's state one step ahead from (the lamp now, the brain's cell, its action);
  - it is a 2-layer net, learned online.
- **Curiosity variants (the reward that replaces W3's staleness bonus):**
  - **S:** W3's staleness (WQ's GYFR living, as is);
  - **LP:** learning progress: the drop in the forward model's prediction error over a sliding window of 200
    predictions, rewarded when positive;
  - **E:** raw prediction error (the "noisy TV" contrast).

## The readings (draft)
1. **Does LP play with the toy** (lever presses per 1,000 steps) **while it is still learnable, then stop** (stage-like)?
2. **Does S patrol regardless** (as in WQ)?
3. **Does E keep pressing forever?**
4. **Pattern and reach,** as in WQ.

## Open design points (to settle before freezing)
- The lamp channel needs a 6th input channel for the planner, so the GYFR weights cannot be reused as is (a new
  channel's weights starting at zero keeps the rest).
- The cost is small: 10,000 steps × 8 seeds × 3 arms.
