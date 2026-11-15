# W3b: implementation notes (written before any data)

## The files
- **w3b.py:** W3's loop (`run_w3.train_net`) rewritten with hooks for Y, FR and RR; W3's `world3`, `brains3` and
  `run_w3` are imported unchanged. `step0` runs the diagnostic on W3's saved weights. `FPolicy` is the ceiling.
- **checks_w3b.py** (→ `checks.log`), **analyse_w3b.py** (→ `analysis.md`, written before the data).
- **Cloud:** `run.yml` gained an optional `resume_run_id` input: the job downloads that run's artifact into the study
  folder first, so a paused training run (the 4.5-hour guard) continues from its checkpoint in a new job.

## Pre-data corrections (no data existed)
1. **"The need is high" thresholds for Y's events and F's trigger: Script's lines instead of 0.8.**
   - **The fault:** the council's rule "need ≥ 0.8 of full scale" was written for a generic body. In W3's body,
     s ≥ 0.8 means energy ≤ 30, a few steps from death, and f ≥ 0.8 means fatigue ≥ 160. Meals are almost never eaten
     that late, so Y would almost never fire, and F would start walking too late to arrive.
   - **The fix:** "high" = W3's Script's own calibrated lines: hunger s ≥ 0.2 (E < 120) and fatigue f ≥ 0.4 (F > 80).
     The rest of the rule (relief ≥ mean + 2 sd and ≥ 0.05, warm-up 1,000 steps) is unchanged.
   - Appended to `questions.md` as a pre-data correction, not rewritten.

## Choices where questions.md is silent
- **Y's supervised step** uses W3's `apply` (learning rate 0.01, total gradient clipped to 1.0); the critic's gradient
  is zero in that step.
- **Y's event and the actor-critic update of the same step:** the actor-critic update (every 64 steps or at a life's
  end) runs first, then Y's step, then the replay.
- **FR's and RR's draws** come from their own generator (`[seed, 21]`), so an arm without them consumes the same act
  draws as W3's D3 (checked: D3 with no parts reproduces W3's training bit for bit).
- **The time guard** (4.5 hours) is checked at life boundaries; the checkpoint holds the weights, both generators'
  states, the counters, the running statistics, the store and the per-life log (pickle).
- **RR's "windows cover the life":** the check verifies contiguous windows (one per 15 steps) with weight 1.0, which
  is what makes their mean relief equal the run's mean (except the last partial block of each life).
- **F's shelter place** is the shelter cell as soon as it is on the map memory; its food place is the cell of the last
  meal.
- **Step 0's walk (a)** re-runs W3's test with the same draws, so it reproduces W3's test lives while logging the
  agreement and the hungry-step contributions.
