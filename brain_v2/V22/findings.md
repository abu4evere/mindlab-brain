# V2-2 findings (Brain v2 step 2, Goals): NEGATIVE. The walker did not learn to use a goal layer by adult fine-tuning,
# and adult fine-tuning without a parent wore down some old abilities

Frozen plan: `questions.md` (tag V22-frozen; signed off by the assistant under the creator's sleep-mode autonomy after
the council). Length by the frozen rule: 1M steps (`length_rule.md`; neither pilot settled). Run 27 Nov 2026 (EST) on
Oracle, Google and the second computer (tests of seed 12 moved from Google to this PC for capacity; seeds' training
stayed where it ran); numpy 2.5.3. 64 fine-tuned walkers (+2 pilots); test files complete (80 test, 64 unseen, 32
reference, 80 plain-land; 640 Bob Profile results; every jsonl 50 distinct lives). Numbers from `output/analysis.md`
(the frozen `analyse_v22.py`, committed before any test life); recomputed blind (`recompute_v22_blind.md`).

## Before data
Checks `checks_v22.log`: **All: PASS (22/22)**, including the exact zero check (with the new weights at 0, every arm's
walker lived CW2's NO-GUIDE life step for step, also with the goal layer active), learning rate 0 changes nothing, the
reward unchanged, the sham rule, resume and run determinism.

## Results (per seed the mean over 50 lives; paired by seed; 95% bootstrap over 16 seeds)
1. **Primary: chains per life GOAL − FT-NOGOAL = −0.096 [−0.230, +0.038] (5+/11−) -> no gain.** Without the pilot
   seeds: −0.096 [−0.244, +0.057]. Recompute: −0.096 [−0.225, +0.039].
2. **The walker does not use the goal input:** GOAL − GOAL-ABLATE (the same walker with the goal input emptied) +0.004
   [−0.059, +0.070]; GOAL − SHAM-GOAL −0.066 [−0.217, +0.086]; the share of goal steps that moved closer is the same for
   the real goal and the sham (about 0.41-0.43, hungry or fed).
3. **Retirement test failed:** chains GOAL − the written carry reflex −1.009 [−1.388, −0.636] (1.749 vs 0.740); survival
   +0.026 [−0.033, +0.089]; the Bob Profile gate failed. The carry reflex stays.
4. **No-loss gates:** plain-land survival vs the RMS parent: GOAL −0.006 [−0.044, +0.036] and FT-NOGOAL −0.016
   [−0.060, +0.029] miss the gate (lower end above −0.03) narrowly; GOAL-NOFLOOR and SHAM-GOAL pass. **The Bob Profile
   gate fails for every fine-tuned arm, with or without a goal:** e.g. A5s about −0.10 and R2 −0.07 to −0.11 for GOAL and
   FT-NOGOAL alike (recompute agrees; under its bootstrap seed A2 also dips just past the margin for GOAL, −0.054).
   Plain-land survival itself barely moved (0.85 either way): what was lost is in the profile's probes.
5. The unseen world: GOAL − FT-NOGOAL chains +0.070 [−0.079, +0.220], survival −0.026 [−0.060, +0.012]: nothing either way.
6. GOAL-NOFLOOR (the floor removed for the goal) − GOAL: chains +0.081 [−0.131, +0.295], survival +0.003: no difference
   (the goal layer was not used, so the arbitration test says nothing).

## Why, as far as the records show
- **Too little goal experience:** the goal was active in only 32% of test lives (about 5 goal starts per life), because a
  goal needs a join at the station to have been experienced first (CW2: 25% of lives); the learned goal weights grew to
  a norm of about 0.1 in 1M steps, small beside the walker's own weights.
- **The body's reward rarely pays for it:** the drive rewards energy only below 150 of 200, and Bob is usually above it
  (GPT's and DeepSeek's main worry; Gemini's hunger-scaled goal level was the named fallback).
- **Fine-tuning without a parent costs old skills:** FT-NOGOAL lost as much on the Bob Profile as GOAL, so the loss comes
  from the adult learning itself, not from the goal part (the roadmap's V2-3 problem: learning for life needs
  protection).

## Reading against the guesses written before data
GOAL − FT-NOGOAL above 0: guessed ~60%, did not happen. Retirement test passed: guessed ~30%, did not happen. No-loss
gates passed: guessed ~60%, did not happen.

## What it means for Bob
A goal part cannot simply be bolted onto the frozen walker and learned in a million adult steps from today's reward: the
signal is too rare and too weak, and unprotected adult learning erodes what the walker knew. The written carry reflex
stays for now. Two lessons for the roadmap: (1) V2-3 (keep learning for life, WITH protection) should come before
another goal attempt, since every fine-tune here cost old abilities; (2) a goal attempt needs a learning signal that
reaches the walker when Bob is fed (Gemini's fallback), or goals learned during childhood rather than adulthood. Both
are new studies for the council.
