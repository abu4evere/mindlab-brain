# W3b: independent review of the Fable session's work (the Opus session, 15 November 2026)

The creator, 12:07: "Lets fable give it a try then you will check". At about 13:45 the Fable session was deleted, and
the Opus session took over. This review covers the plan, code and checks as Fable left them (commits 7c396a4,
3968638), read before any training result. Step 0 and F outputs had been downloaded; they were not opened before this
review was written.

## Plan (`questions.md`)
- Frozen (W3b-frozen) after a council of GPT, Gemini and DeepSeek in two rounds (`../W3b_council_2026-11-15.md`),
  before code. The creator's sign-offs are quoted.
- **Pre-data correction 1** ("need is high" = Script's lines, s ≥ 0.2 and f ≥ 0.4, instead of 0.8) is sound. In W3's
  body, 0.8 means energy ≤ 30, a few steps from death. It is appended, not rewritten.
- The readings, validity rules and priors are stated before data. Step 0 is explicitly barred from changing the arms.

## Code (`w3b.py`) against the plan: matches on every point checked
- **Y's trigger:** the need before the step ≥ the high line; relief ≥ 0.05; relief ≥ the running mean + 2 sd. The
  statistics come from past steps only (the event is computed before the step is added). There is a 1,000-step
  warm-up, and the statistics carry across lives and across resume (pickled).
- **The window:** at most 15 steps, stopping at the previous event in the life. The weight is
  min(3, z) × 0.9^k with k = 0 at the event step (oldest first in the list, matching the records).
- **Y's update:** one supervised step through the planner and head; the critic's gradient is zero. It runs after the
  actor-critic update of the same step, as IMPLEMENTATION.md says.
- **FR:** an event stores its window (FIFO 256). Replay happens on steps spent on the shelter cell, at most 64 per
  life, with a draw from its own generator.
- **RR:** contiguous 15-step windows of the brain's own experience, weight 1.0, on the same trigger and cap.
- **Map snapshots** are fresh arrays (`world3.obs_map` builds a new array each call), so stored paths cannot change
  after storage.
- **Resume:** the weights, both generators, counters, statistics, store and logs are checkpointed. The per-life
  buffers are rebuilt at each life, and runs pause only at life boundaries.
- **F (ceiling):** the food place is the last meal's cell and the shelter place is the shelter once known. When the
  need is at or above the line, it walks by BFS on the map memory (unknown counts as open); otherwise W3's D3 acts.
- **Step 0:** (b) moves to the open neighbour with the highest max-q, staying if none beats its own cell; (c) looks
  one step ahead.

## Checks (`checks.log`, All: PASS)
- **Strong:**
  - D3 with no parts reproduces W3's training and test bit for bit;
  - a split run equals an unsplit run;
  - Y's trigger and window rules hold;
  - F's behaviour is right;
  - test lands are identical; the same seed twice gives the same result.
- **Weak (noted, not a fault):**
  - "FR: at most 64 replays per life" and the RR check passed with **0 replays**. The short check lives never reached
    the shelter, so the replay path was exercised only in the split-run check (1 replay).
  - The plan's "RR's mean relief equals the run's mean" is checked only through contiguity and weight 1.0.
  - The arms' logged update counts (`*_lives.json`, `updates`) will show whether replay actually happened in the full
    runs. **This is to be checked before any reading is taken.**

## Verdict before results
**The plan and code are sound and faithful to the frozen plan.** The one thing to confirm from the data is that FR
and RR replays actually occur in training.
