# V2-1 Revise: can Bob change his mind when the world changes? (DRAFT, not frozen; for the council)

Drafted 27 Nov 2026 ~01:25 EST under the creator's sleep-mode autonomy ("ask council then go ahead"), as the first step
of the Brain v2 roadmap (`brain_v2_roadmap_draft.md`, revised order; round-table `roadmap_v2_roundtable_2026-11-27.md`).

## Why
W3r (final): learning what colours do within a life works (RMS fresh-land survival 0.859 vs 0.211), but after a
mid-life swap (from step 1,500 the wall and food colours are exchanged) RMS falls to 0.250 (RMS-midswap − RMS −0.609
[−0.642, −0.575]), about the level of a brain that never learned meanings: the count table never forgets. The same
holds for CW1's consequence model (plain counts). Every later Brain v2 part needs a memory that can revise.

## The part (one new part: a revision rule for the count tables; no retraining)
- **SURPRISE (the new part):** when an event contradicts a confident prediction, old evidence for that look counts
  less. For W3r's table: on an event (look c, consequence j, outcome y), with the table's prediction p = pos/(pos+neg)
  for (c, j) and n = pos+neg fair trials: if n >= 3 and |y − p| >= 0.75, all of look c's counts (all three
  consequences) are multiplied by 0.25 before the event is added. For CW1's model: on a step (situation, verb) whose
  most frequent outcome (next hand state) has n >= 3 and a share >= 0.75, an observed different outcome multiplies that
  key's counts by 0.25 before it is added. The numbers are fixed here, before any data, and never tuned.
- **WINDOW (a fixed recency, DeepSeek's CW1 idea):** every event first multiplies the counts it touches by 0.95 (a
  half-life of about 14 events), surprise or not.
- **SHAM-SURPRISE (the same machinery, the wrong signal):** at the same moments SURPRISE would decay, the decay hits a
  different look (or key), drawn at random from those with counts.
- **PLAIN:** today's counts (the control).

## Test A (primary): W3r's mid-life swap
- Brains: W3r's RM kept copies (RMS seeds 1-16), frozen. 50 fresh lands per seed (new seeds 960001-960050).
- Two conditions per arm: **swap** (W3r's probe: wall and food colours exchanged from step 1,500) and **stable** (no
  swap: the no-loss gate).
- **Primary: full-life survival under the swap, SURPRISE − PLAIN**, paired by seed, 95% bootstrap over 16 seeds; a real
  gain if the lower end is above 0.
- **No-loss gate:** stable survival SURPRISE − PLAIN above −0.03 at the lower end (SURPRISE must not cost stable lives).
- Secondaries: SURPRISE − SHAM and SURPRISE − WINDOW under the swap; WINDOW's no-loss on stable lands; steps after the
  swap until the table ranks the new food colour first for "fed" (relearning time); deaths after step 1,500.

## Test B (key secondary): CW1 with the join changed mid-life
- CW1's world and arms on the consequence model (K = 4), the frozen RMS walker, 50 fresh lands per seed (970001-970050);
  from step 1,500 the joining operation becomes another, seeded per land.
- Measure: chains completed after step 1,500, SURPRISE − PLAIN (and − SHAM, − WINDOW); no-loss: chains before 1,500
  and in CW1-style lives without a change, within 0.3 chains of PLAIN.

## Checks before data
Zero check (with no surprise ever reaching the thresholds, SURPRISE = PLAIN bit for bit; scripted); the decay fires
only above both thresholds (scripted events); the sham decays the same amount at the same moments on another look;
W3r's probe reproduced (PLAIN under the swap on W3r's own fresh lands 910001-910050 gives W3r's RMS-midswap lives);
determinism.

## Limits
- The revision rule is written (a learning rule, which the roadmap allows: "written laws vs written decisions"); its
  numbers are a guess fixed before data.
- One kind of change (a swap of two meanings, a changed operation); slow drifts are not tested.

## Compute
Test lives only: A: 4 arms x 2 conditions x 16 seeds x 50 = 6,400 lives; B: 4 x 16 x 50 = 3,200 lives. A few hours on
Oracle, Google and this PC.

## Expected (before data, the assistant's guess)
SURPRISE − PLAIN above 0 under the swap: about 65%. No-loss passed on stable lands: about 75%. SURPRISE better than
SHAM: about 60%. WINDOW also helps under the swap but costs stable lives: about 50%.

## Questions for the council
1. Is surprise-gated decay of the whole look the right first rule, or decay only the contradicted consequence?
2. Are the fixed numbers (n >= 3, |y − p| >= 0.75, keep 0.25; window 0.95) sensible, given they cannot be tuned?
3. Is swap survival the right primary, with stable survival as the no-loss gate?
4. Is Test B (CW1's join changed) worth running in the same study, or its own?
5. Anything that would make a positive result misleading (e.g. the walker never trying cells it believes are walls, so
   the table never sees the evidence it needs)?
