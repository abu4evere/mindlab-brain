# V2-1 findings (Brain v2 step 1, Revise): resetting a belief when it is confidently contradicted lets Bob survive a
# changed world as well as an unchanged one, with no loss in the unchanged one

Frozen plan: `questions.md` (tag V21-frozen; signed off by the assistant under the creator's sleep-mode autonomy after
the council). Run 27 Nov 2026 (EST, night) on Oracle (seeds 1-8), Google (9-12) and the second computer (13-16, Idle
priority; resumed from its saved lives after an app restart, no life repeated); numpy 2.5.3. 192 jobs; 9,600 lives
(Test A: 4 arms x 2 conditions x 16 seeds x 50 lands 960001-960050; Test B: 4 x 16 x 50 lands 970001-970050). Every
number is from `output/analysis.md` (the frozen `analyse_v21.py`); the key ones were recomputed blind
(`recompute_v21_blind.md`).

## Before data
Checks `checks_v21.log`: **All: PASS (14/14)**, including PLAIN reproducing W3r's saved RMS lives on all 50 of W3r's
lands, swap and stable (lifespans equal); two check-script mistakes were fixed before the run (a model built before
its mode was set; a loop one step short).

## Results (per seed the mean over 50 lives; paired by seed; 95% bootstrap over 16 seeds)
1. **Primary: survival under the mid-life swap, SURPRISE − PLAIN = +0.625 [+0.580, +0.667], 16/16 seeds -> a real
   gain.** SURPRISE 0.851 vs PLAIN 0.226 (W3r's failure reproduced). Blind recompute: +0.625 [+0.581, +0.667], 16/16.
2. **No-loss gate passed:** stable survival SURPRISE − PLAIN −0.001 [−0.007, +0.005] (0.848 vs 0.849). Recompute agrees.
   SURPRISE under the swap (0.851) matches its own stable survival (0.848): the change no longer costs Bob anything.
3. **It is the right target, not any reset:** SHAM (the same resets on a wrong look) 0.251 under the swap, SURPRISE −
   SHAM +0.600 [+0.551, +0.650], 16/16.
4. **A fixed recency window barely helps here:** WINDOW 0.290 under the swap (WINDOW − PLAIN +0.064 [+0.019, +0.106]);
   SURPRISE − WINDOW +0.561 [+0.495, +0.623], 16/16; WINDOW's stable cost −0.004 [−0.010, +0.004].
5. **Not carried by the written hunger reflex** (all three council members' worry): the reflex's share of post-swap
   meals fell from 0.383 (PLAIN) to 0.047 (SURPRISE) (−0.337 [−0.359, −0.315], 16/16): the table, revised, led Bob to
   food himself.
6. **False resets on stable lands:** 0.62 per life (SURPRISE), with no survival cost (2). Under the swap: 2.35 per life.
7. **Test B (the joining operation changed at step 1,500):** chains after the change SURPRISE − PLAIN +0.865 [+0.656,
   +1.081] (15/16; 1.68 vs 0.82); WINDOW does as well (+0.924; SURPRISE − WINDOW −0.059 [−0.172, +0.059]); SHAM hurts
   (−0.190). Chains before the change identical in every arm (2.73), as they must be.

## Two honest readings the numbers force
- **Relearning what is used, not a fully correct table (GPT's caution "reset rather than revision"):** the strict
  measure "the table ranks the true food colour first for fed AND the true wall colour first for blocked at the end" is
  LOWER for SURPRISE under the swap (0.095 vs 0.203; −0.108 [−0.140, −0.078]). A look Bob never meets again can keep a
  stale value (a tie or an old rank) after its partner is reset; Bob survives because the looks he acts on are relearned.
  Among lives where both rankings did become right, SURPRISE got there faster (70 vs 359 steps after the swap).
- **Which rule depends on the table:** for W3r's colour table, gating by surprise matters enormously and a fixed window
  does little; for CW1's hand-transition table (Test B), a fixed window works as well as surprise. A single rule for both
  is not shown to be better than the window in Test B.

## Reading against the guesses written before data
SURPRISE − PLAIN under the swap above 0: guessed ~70%, came true (large). No-loss passed: guessed ~75%, came true.
SURPRISE − SHAM above 0: guessed ~65%, came true. Test B SURPRISE − PLAIN above 0: guessed ~60%, came true.

## Limits
- One abrupt change at one time (step 1,500); deterministic consequences; the reset rule and its numbers are written.
- After a reset the walker reads "no evidence" as 0, the same as "known not" (GPT).
- The frozen RMS walker; nothing here retrains a network.

## What it means for Bob
W3r's open failure is fixed: Bob can now notice that a belief is wrong, drop it, and learn what is true now, within the
same life, without forgetting what still holds. Every later Brain v2 part (goals, lifelong learning, fear) needs this.
