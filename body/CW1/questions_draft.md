# CW1: Body v1 step 2 — a small crafting world: can the brain find, within one life, a useful combination of
# things in its hands? (DRAFT, not frozen; for the council and the creator)

Drafted 26 Nov 2026 (EST) at the creator's request ("Yes, draft step 2"). **Not frozen; nothing built.**
Sources: `body/body_v1_draft.md` (step 2: "two or three things combine via operate(k); can the brain discover one
useful combination within a life?"), the 25 Nov round-table (operate(k) as each world's native motor repertoire with
shuffled numbers; one shared scoring rule over a table keyed by action number with a bonus for untried actions; a
separate light consequence model; a pain-gated poke; padded/randomised operation lists and a no-make arm), the BV1
round-table ("Step 2 should establish whether Bob can learn through that body"), and the creator, 25 Nov: "start with
things in hands then add station".

## Why
BV1 showed the body connects today's brain to Mind Lab's world with nothing lost, but it exercised no hands, use or
operations. Step 2 is the first test of learning THROUGH the body: a consequence that exists only if the brain
combines things it carries, which nothing in its wiring or training knows about.

## The world (W3r's lands, plus loose things; no station)
- Two kinds of loose things, **A** and **B**, lie on the land (a few of each, regrowing like food); their looks are two
  more colour codes dealt anew on each land (as W3r's colours), so the brain cannot know them in advance.
- Body v1's verbs now all matter: **take** (pick up the thing underfoot into a free hand; 2 hands), **drop**, **use**
  (on what is held in hand 1: if it is edible, eat it), and **operate(k)**, k = 1..K, the world's own operations on
  what is held, as shuffled numbers (no names, order or grouping shown). K = 4 here: one of them joins the two held
  things; the others act on them in ways that lead nowhere (the draft's guess: split, turn, rub).
- The physics (written before data, and the same in every arm): joining A with B gives **C**; using C gives a large
  meal (2 x a food meal) and C keeps (it does not spoil or move); using A or B gives nothing; every other operation
  on any held pair changes nothing but takes the step. No named recipe is shown to the brain: it sees only looks,
  hand contents as counts per look, and the signed changes after each action.
- Food and the shelter stay as in W3r, so the useful chain (take A, take B, join, use C) is a help, not a necessity.

## The brain
- **Moving:** W3r's RM kept copy (frozen), as in BV1.
- **New: a consequence model** (light, count-based; the round-table's): per (action number, what is held as looks),
  the mean signed changes that followed (energy, hands), plus a bonus for actions never tried in that situation. It
  learns within each life and resets at birth. It never sees what A, B or C are.
- **Choosing:** one shared scoring rule over the consequence table for the non-move verbs (take, drop, use,
  operate(k)), so any number of operations needs no new parameters. **Open (council question 1):** when the
  consequence model acts instead of the moving brain (for example: when something is underfoot or in hand and its
  best score beats a threshold set in a pilot on pilot seeds only).
- No new reward is written in: the consequence model values only what the body feels (energy rising), as W3r's table
  did.

## Arms (16 seeds = RMS 1-16, frozen; each life on fresh test lands; the consequence model learns within the life)
| arm | operations | the non-move verbs chosen by |
|---|---|---|
| **LEARN** | K = 4 | the consequence model (the primary) |
| **RANDOM-OPS** | K = 4 | random choice at the same moments as LEARN (same rate of non-move steps) |
| **NO-MAKE** | none (take, drop, use only) | the consequence model |
| **PAD** | K = 4 + 8 dummy (no effect) | the consequence model |
Every arm: operation numbers shuffled per land; the adapter audited first (BV1's audit, extended to hands and
operations: availability, ordering and legality carry no information about which operation joins).

## Measures (to be fixed before data)
- **Primary (draft):** the share of test lives in which the useful chain (A and B held, join, use C) is completed at
  least 3 times, **LEARN − RANDOM-OPS**, paired by seed, 95% bootstrap over seeds.
- Secondary: LEARN − NO-MAKE in lifespan and full-life survival (does making help living?); PAD − LEARN (do extra
  operations slow discovery?); steps to the first join; dead-action rate; the Bob Profile beside it (does the new
  part cost any old ability?).

## Checks before data
Zero check: with the consequence model switched off and no loose things on the land, every arm reproduces BV1's BODY
bit for bit; the physics of every operation on every held pair, scripted; the adapter audit; same seed, same result.

## Open questions for the council
1. When should the consequence model act instead of the moving brain (the arbitration)?
2. Is one useful chain out of K = 4 operations and 2 kinds the right first difficulty, and is "3 completions in a life"
   the right reading of "found and used"?
3. Should failed operations cost something (time only, or a little energy), and should the poke be pain-gated here?
4. Does RANDOM-OPS at the same moments make a fair control, and is PAD worth an arm now?
5. What the creator asked for next ("then add station"): keep it for CW2.

## Compute
Test lives only (the moving brain is frozen; the consequence model learns within each life): 4 arms x 16 seeds x 50
fresh lands, a few hours on Oracle (or this PC at low priority).

## Expected (before data, the assistant's first guess)
LEARN − RANDOM-OPS above 0: about 65% (the bonus for untried actions should find the join; the risk is the
arbitration never giving the consequence model the chance).

## Revised after round 1 of the round-table (26 Nov 2026; `roundtable_cw1_2026-11-26.md`; still a draft, not frozen)
- **C is used up when eaten** (it only keeps until then): each use of C needs a new join.
- **Delayed credit (GPT's point, checked):** joining gives no energy by itself, so the consequence model learns the
  transitions (held looks, action) -> (next held looks, energy change) and values each action by the best energy
  reachable within a few steps through hand states (a small value iteration over hand states, like the mover's
  planner). Only energy is valued; nothing about A, B or C is written in.
- **Arbitration at affordance moments (Gemini, checked: the frozen mover is blind to loose things):** the consequence
  model acts only when something is underfoot with a free hand, or something is held, and only while energy and
  tiredness are above a survival floor set before data; otherwise the mover acts. The same rule in every arm.
- **RANDOM-OPS:** the same moments and opportunities, uniform over the legal non-move verbs.
- **Plain counts** for CW1 (all four); forgetting gets its own study with a mid-life change (DeepSeek's recency arm is
  an open question for round 2).
- **Measures:** partial progress (took A, took B, joined, ate C) and first-join latency reported for every arm.
- **Open for round 2 and the creator:** the primary (≥3 chains in a life vs mean chains per life vs discovery then
  reuse); pain-gated poking (inert here: no hazard brings pain); a cost on failed operations beyond the step; PAD as an
  arm or a secondary check.

---------------------------------------------------------------------------------------------------------------------
# PROPOSED FINAL PLAN (after round 2 of the round-table, 26 Nov 2026 ~20:45 EST; for the creator's sign-off)
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
