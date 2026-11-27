# V2-1 Revise: FROZEN PLAN (Brain v2, step 1)

Frozen 27 Nov 2026 ~01:50 EST by the assistant under the creator's sleep-mode autonomy ("if u need permission i am
giving u right now just ask council then go ahead"; ACL docs/autonomous_decisions.md). Council: GPT, Gemini, DeepSeek
(`roundtable_v21_2026-11-27.md`); this is `questions_draft.md` revised by that round-table.

## Question
When the world changes what a look means, can Bob's within-life memory notice it was wrong, discard the old meaning
and learn the new one, without losing what was right?

## The part (no retraining; the frozen RMS walker)
- **SURPRISE (the new part): reset to unknown on a confident contradiction.** W3r's table: on an event (look c,
  consequence j, outcome y) with n = pos+neg fair trials for (c, j) and p = pos/n: if n >= 3 and |y − p| >= 0.75, ALL of
  look c's counts (all three consequences) are set to 0 before the event is added. CW1's model: on a step (situation,
  verb) whose most frequent next hand state has n >= 3 and a share >= 0.75, an observed different next hand state sets
  that key's counts (tries, gains, outcomes) to 0 before it is added. Fixed now; never tuned.
- **WINDOW:** every event first multiplies the counts it touches by 0.95 (W3r: that (c, j) cell; CW1: that key).
- **SHAM-SURPRISE:** at each moment SURPRISE would reset, a different look (key), drawn at random (seeded) among those
  with counts, is reset instead; the contradicted one is left as it is.
- **PLAIN:** today's counts (control).

## Test A (primary): W3r's mid-life swap
- RMS seeds 1-16 (W3r's RM kept copies), W3r's native MeaningWorld, 50 fresh lands per seed (960001-960050).
- Conditions: **swap** (W3r's probe: from step 1,500 the wall and food colours are exchanged) and **stable** (none).
- **Primary:** full-life survival under the swap, **SURPRISE − PLAIN**, per seed the mean over 50 lives, paired by seed,
  95% bootstrap over 16 seeds (10,000 resamples); a real gain if the lower end is above 0.
- **No-loss gate:** stable survival SURPRISE − PLAIN, lower end above −0.03.
- Named secondaries: SURPRISE − SHAM and SURPRISE − WINDOW (swap); WINDOW − PLAIN (stable, no-loss); post-swap table
  accuracy (at step 3,000 or death: does the table rank the true food colour first for fed and the true wall colour
  first for blocked); recovery latency (steps after 1,500 until both rankings are right); the stable-land reset rate
  (resets per life without any swap: should be near 0); **the hunger reflex's share of post-swap meals** (meals within
  a hunger-reflex episode vs all meals after step 1,500), per arm.

## Test B (prespecified secondary): CW1 with the join changed mid-life
- CW1's world and model (K = 4), the frozen RMS walker, 50 fresh lands per seed (970001-970050); from step 1,500 the
  joining operation becomes another (seeded per land, never the same). Arms as above on CW1's model.
- Measures: chains after step 1,500, SURPRISE − PLAIN (and − SHAM, − WINDOW); no-loss: chains before step 1,500 within
  0.3 of PLAIN.

## Checks before data (all must pass)
1. PLAIN reproduces W3r: with SURPRISE's code path present but switched to PLAIN, W3r's RMS on its own fresh lands
   (910001-910050) reproduces W3r's saved RMS-midswap and RMS test lives (seed 1, all 50 lives; lifespans identical).
2. The reset fires exactly at the thresholds (scripted events: n = 2 never; n = 3 with |y − p| = 0.75 yes; 0.74 no).
3. After a reset the look reads 0 in all three layers until new fair trials (W3r's own "no evidence").
4. SHAM resets another look with counts at the same moment and never the contradicted one.
5. WINDOW multiplies only the touched cell (key).
6. CW1's join change happens exactly at step 1,500 to a different operation; CW1 with no change and PLAIN reproduces
   CW1's own LEARN life (seed 1, land 930003: 7 chains).
7. Determinism.
A short pilot (seeds 1-2, pilot lands 980001-980005) checks only that everything runs and how long a life takes.

## Limits (written now)
- After a reset the walker sees "no evidence" as 0, the same as "known not" (GPT's caution).
- The written hunger reflex walks to remembered food by the true map; its share of post-swap meals is reported, and a
  gain carried by it is not a gain of the table alone.
- One swap time (1,500) and abrupt changes only (Gemini: vary it later); deterministic consequences.

## Compute
Test lives only: A 4 arms x 2 conditions x 16 seeds x 50 = 6,400; B 4 x 16 x 50 = 3,200. Oracle, Google, this PC.

## Expected (before data)
SURPRISE − PLAIN under the swap above 0: about 70%. No-loss passed: about 75%. SURPRISE − SHAM above 0: about 65%.
Test B SURPRISE − PLAIN above 0: about 60%.
