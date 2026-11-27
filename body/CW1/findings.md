# CW1 findings (Body v1 step 2, a small crafting world): the brain found the combination and used it again and again

Frozen plan: `questions.md` (tag CW1-frozen; the creator's sign-off 26 Nov 2026). Run 26 Nov 2026 (evening, EST) on
three machines, each seed's four arms on one machine: Oracle (seeds 1-8; Linux, Python 3.14.10), Google (seeds 9-12;
Linux, Python 3.14.4), the second computer (seeds 13-16; Windows 10, Python 3.12.10, Idle priority); numpy 2.5.3
everywhere. 64 jobs, all exit 0; 3,200 lives (4 arms x 16 seeds x 50 fresh test lands 920001-920050). Every number
below is from `output/analysis.md` (the frozen `analyse_cw1.py`), and the key ones were recomputed blind
(`recompute_cw1_blind.md`).

## Before data (recorded)
- Checks `checks_cw1.log`: **All: PASS (53/53)**: the zero check (model off, no loose things: all 4 arms reproduce
  BV1's BODY bit for bit on RMS seeds 1-8), the physics of every verb on every held pair, delayed credit (GPT's
  condition: after one chain, join > dead operations in (A, B), take B > drop in (A)), only situations that can be met
  count, the adapter audit (the verb list, legality and senses do not depend on which operation joins), determinism.
- **A fault found by the pilot and fixed before any test data** (no setting changed): the value of empty hands kept
  the untried bonus of a situation that is never a decision moment (empty hands, nothing underfoot), so "pass" tied
  every real option and LEARN stopped after a little exploration (0 chains in all 10 pilot lives). After the fix the
  pilot's LEARN lives made 0-16 chains. The pre-fix pilot is kept in `output/pilot_prefix/`; a check now guards it.
- One live smoke test on each VM reproduced this PC's pilot life exactly (7 chains, 74 acts).

## Results (800 lives per arm; per seed the mean over 50 lives; paired by seed; 95% bootstrap over 16 seeds)
1. **Primary: mean completed chains per life, LEARN − RANDOM-OPS = +5.080 [+4.745, +5.411], 16 of 16 seeds
   positive -> a real gain** (frozen rule: lower end above 0). LEARN 5.73 chains per life, RANDOM-OPS 0.65.
   Blind recompute: +5.080 [+4.739, +5.405], 16/16 (another bootstrap seed; the means agree exactly).
2. Named secondaries, LEARN − RANDOM-OPS (all 16/16 seeds the same way):
   - share of lives with 3+ chains: 0.446 vs 0.030, +0.416 [+0.388, +0.444] (recompute: +0.416 [+0.388, +0.444]);
   - share with at least 1 chain: 0.930 vs 0.453, +0.478 [+0.441, +0.516];
   - chains per 1,000 steps alive: 2.03 vs 0.22, +1.81 [+1.71, +1.92];
   - steps to the first join (lives with a join): 296 vs 1,641, −1,345 [−1,429, −1,257];
   - partial progress: took A 0.976 vs 0.941, took B 0.965 vs 0.935, joined 0.931 vs 0.514, ate C 0.930 vs 0.453;
   - reuse after discovery (chains after the first): 4.80 vs 0.20, +4.60 [+4.27, +4.94];
   - dead-action rate: 0.460 vs 0.848, −0.388 [−0.398, −0.378]; acts per life 64 vs 933.
3. **LEARN − NO-MAKE: no difference in living**: lifespan +9.7 steps [−62.5, +79.0], survival +0.001
   [−0.024, +0.028] (LEARN 0.847, NO-MAKE 0.846; recompute agrees). Making did not make lives longer.
4. **PAD − LEARN** (12 operations instead of 4): mean chains −0.31 [−0.77, +0.21] (no clear loss; PAD higher on 4/16
   seeds); first join later by +59 steps [+27, +94] (13/16 seeds). Extra dead operations slow discovery a little,
   and the model still finds the join and repeats it.
5. Manipulation check: NO-MAKE 0 chains and 0 joins in all 800 lives; every file 50 distinct lands (recompute).
6. Also seen (not a planned comparison): RANDOM-OPS lived less (survival 0.763, lifespan 2,555) than LEARN: its
   ~930 hand acts per life cost time that the mover would have used.
7. The Bob Profile was not measured with the consequence model attached (allowed by the plan: "otherwise noted as not
   measured"); the mover is the frozen RMS brain, already profiled (6/100).

## Reading against the guesses written before data
LEARN − RANDOM-OPS above 0: guessed about 70%, came true (clearly). PAD slower to the first join: guessed about 75%,
came true. LEARN outliving NO-MAKE: guessed about 40%, did not happen.

## Limits
- One world, one useful chain of four steps, two kinds and one join; no hazard, no forgetting, no station.
- The mover is frozen and blind to loose things; A and B are met only by passing over them, and the consequence model
  acts only at affordance moments above the survival floor (the same rule in every arm; GPT's note on its bias).
- The consequence model is hand-built planning over counted transitions (value through hand states), not a learned
  network: it shows the body supports learning a combination within a life, not that a neural brain can.
- Making gave meals but no longer lives here: food alone already sustains most lives (NO-MAKE 0.846 survival).
- Different machines for different seeds (each seed's four arms on one machine, so the pairing holds).

## What it means for Bob
Through the standard body, a brain told nothing about the things or the operations discovered in one life that
holding two things and doing one unnamed operation leads to a big meal two steps later, and then did it again about
five times per life, where random poking found it in under half the lives and rarely twice. The value travelled back
through hand states (GPT's delayed-credit concern) as planned. What it did not show: that making helps survival here.
Next on the plan: the creator's "then add station" (CW2), and revision when the world changes (W3r's open failure).
