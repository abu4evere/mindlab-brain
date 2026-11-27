# CW1 (Body v1 step 2): FROZEN PLAN

Frozen 2026-11-26 20:33 EST with the creator's sign-off (in the Claude Code session on the second computer: "yes, sign off CW1"). Text below is the "PROPOSED FINAL PLAN" section of `questions_draft.md` (commit 679125f), unchanged. Round-table: `roundtable_cw1_2026-11-26.md`.

Everything above stays as the record. This section is the complete plan that becomes `questions.md` (tag
`CW1-frozen`) only after the creator's explicit yes. Round-table: `roundtable_cw1_2026-11-26.md` (2 rounds; every
open point settled by a clear majority with reasons checked against the code).

## Question
Can Bob's brain, through Body v1, discover within one life a useful combination of things held in its hands, and
use it again and again, when nothing in its wiring or training says what the things or the operations are?

## World (W3r's lands plus loose things; no station)
- Two kinds of loose things, A and B, a few of each, regrowing like food; their looks are two more colour codes dealt
  anew on every land.
- Verbs: move (4) and stay as before; take (thing underfoot into a free hand; 2 hands); drop; use (on hand 1: eat it if
  edible); operate(k), k = 1..K, on what is held, as numbers shuffled per land.
- K = 4: one operation joins A and B (in either hand order) into C; the other three change nothing. Every action,
  failed or not, costs only the ordinary step (no extra cost on failed operations: unanimous in round 2).
- Using C: a meal of 2 x a food meal, and C is used up; C does not spoil or move until eaten. Using A or B: nothing.
- Food and the shelter as in W3r, so the chain helps but is not needed.
- No pain in this world (the pain channel stays 0), so **no pain-gated poking in CW1** (3 of 4; it goes to the first
  world with a hazard).

## Brain
- **Mover:** W3r's RM kept copy (RMS seeds 1-16, frozen), exactly as in BV1.
- **Consequence model (new, learns within each life, reset at birth, plain counts):** it counts transitions
  (what is held as looks, action) -> (next held looks, energy change), and values each action by the best energy
  reachable within H = 4 steps through hand states (a small value iteration over the learned transitions). Actions
  never tried in a hand state get an optimistic value equal to one food meal (the "untried bonus"). Only energy is
  valued; nothing names A, B or C.
- **Arbitration (the same in every arm):** the consequence model chooses the step only at affordance moments
  (something underfoot with a free hand, or something held) and only while hunger and tiredness are both below 0.5;
  otherwise the mover chooses. Its choices: take, drop, use, operate(k), or "pass" (hand the step back to the mover).
- No forgetting and no recency window (3 of 4): CW1's world never changes; revision gets its own study.

## Arms (16 seeds = RMS 1-16; each seed's brain lives 50 lives on fresh test lands 920001-920050; full life 3,000 steps)
| arm | operations | non-move choices at affordance moments made by |
|---|---|---|
| **LEARN** | K = 4 | the consequence model |
| **RANDOM-OPS** | K = 4 | uniform over the legal non-move choices (incl. pass), at the same kind of moments |
| **NO-MAKE** | none (take, drop, use) | the consequence model |
| **PAD** | K = 4 + 8 that change nothing (K = 12) | the consequence model |

## Measures (fixed now)
- **Primary:** mean completed chains per life (one chain = C made from held A and B, then eaten), **LEARN − RANDOM-OPS**,
  per seed the mean over its 50 lives, paired by seed, 95% bootstrap over the 16 seeds (10,000 resamples). Read as a
  real gain if the interval's lower end is above 0. (3 of 4 in round 2; GPT and DeepSeek revised to it.)
- **Named secondaries:** the share of lives with 3+ chains and with at least 1 (LEARN − RANDOM-OPS; Grok's and
  DeepSeek's "found and used"); chains per 1,000 steps alive; steps to the first join; partial progress (took A, took
  B, joined, ate C); reuse after discovery (chains after the first, per life; GPT); the dead-action rate.
- **Other comparisons:** LEARN − NO-MAKE in lifespan and full-life survival (does making help living?); PAD − LEARN in
  mean chains and first-join latency (does a bigger list of operations slow discovery?).
- The Bob Profile beside it, if it can run with the consequence model attached; otherwise noted as not measured.
- Populations beside every number (lives, seeds).

## Checks before any test data (all must pass)
1. Zero check: with the consequence model off and no loose things, every arm reproduces BV1's BODY bit for bit.
2. Physics: every operation on every held pair, scripted (join in both hand orders; the other operations change
   nothing; C eaten gives 2 meals and is gone; A or B used gives nothing).
3. **Delayed credit (GPT's condition):** a scripted life where the model has seen take A, take B, join, use C once:
   it must then value join above the dead operations in the hand state (A, B), and take B above drop in the state (A).
4. Adapter audit extended to hands and operations: availability, ordering and legality carry nothing about which
   operation joins (BV1's audit, with renamings of the operation numbers).
5. Same seed, same result.
A short pilot (brains 1-2, pilot lands 930001-930005) only checks that everything runs and how long a life takes;
no value above is changed by it.

## Limits (written now)
- The survival floor gives control back to the mover when hungry or tired, in every arm alike; it protects the mover's
  survival and caps how much the consequence model can act (GPT's note). Results hold for this rule.
- One world, one useful chain; the mover is frozen and blind to loose things, so A and B are met by passing over them.
- No hazard, no pain, no forgetting, no station (the creator's "then add station" is CW2).

## Compute and recompute
4 arms x 16 seeds x 50 lives on the Oracle VM (16 threads), the Google VM and this PC (Idle priority), each run's
machine recorded. The primary and its interval, the 3+ share and the zero check are recomputed blind by a fresh
session from the raw output files before the findings are final.

## Expected (before data, the assistant's guess)
LEARN − RANDOM-OPS above 0 in mean chains: about 70% (planning through hand states should find the join and repeat
it; the risk is that affordance moments are too rare for the model to learn in time). PAD slower to the first join
than LEARN: about 75%. LEARN outliving NO-MAKE: about 40% (food alone already sustains most lives).
