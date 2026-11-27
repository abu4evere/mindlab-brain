# CW2 (Body v1 step 3, a station): FROZEN PLAN

Frozen 2026-11-26 23:40 EST with the creator's sign-off (email reply to "Do you sign off CW2?": "Sounds good to me."; read as yes, with GUIDE-REFLEX - NO-GUIDE as the primary as written). Text below is the "PROPOSED FINAL PLAN" section of `questions_draft.md` (commit 5f68153), unchanged. Round-table: `roundtable_cw2_2026-11-26.md`.

Everything above stays as the record. This section becomes `questions.md` (tag `CW2-frozen`) only after the creator's
explicit yes. Round-table: `roundtable_cw2_2026-11-26.md` (round 1 all four; round 2 GPT, Gemini, DeepSeek; Grok's
free limit was reached).

## Question
Can Bob's brain learn within one life that a combination of held things works only at one place, and get the walker to
carry the things there, when nothing says what the things, the operations or the place are?

## World (CW1's, unchanged, plus one station; all four agreed)
- CW1's world exactly (A and B spots, 2 hands, take / drop / use / operate(k), K = 4 shuffled per land, C = 2 food
  meals, used up when eaten; food, shelter and lands as W3r).
- **One station:** one fixed passable cell per land with its own look (the fourth free colour code), dealt per land, at
  least 5 steps (shortest path) from every A and B spot, not on a food patch, the shelter or the start.
- **The join works only when Bob stands on the station cell**; off it, the join does nothing (like the other 3).

## Brain
- **Walker:** W3r's RM kept copy, frozen (RMS 1-16), with its reflexes, as in BV1 and CW1.
- **Consequence model:** CW1's (counts, value through hand states, H = 4, untried bonus = one food meal, only
  situations that can be met), with operations keyed by what is held and the look underfoot (as take already was),
  and a **place memory**: the cells where each look was felt underfoot this life.
- **When to guide:** when, from what is held now, the model's best reachable energy runs through a look that is not
  underfoot but is in its place memory (holding A and B after a join has been seen on the station's look, the station
  is that place); only above the survival floor (hunger and tiredness below 0.5, as CW1); cleared when the hands
  change or the place is reached, or when Bob drops below the floor.
- **Arbitration** at affordance moments exactly as CW1.

## Arms (16 seeds = RMS 1-16, 50 fresh lands each, land seeds 940001-940050)
| arm | how the walker is steered at a guiding moment |
|---|---|
| **GUIDE-REFLEX** | a carry reflex: walk by shortest path on the remembered map to the remembered place (like the sleep and hunger reflexes); hunger and sleep reflexes keep priority |
| **GUIDE-MAP** | the place marked as food in a copy of the map fed to the walker's planner (its memory untouched) |
| **SHAM-REFLEX** | the carry reflex to a remembered non-station place whose path distance is nearest the station's, same moments, same clearing |
| **SHAM-MAP** | that matched place marked as food in the planner's copy, same moments, same clearing |
| **NO-GUIDE** | none (joins only when the walker passes the station by chance) |
| **RANDOM-OPS** | random non-move choices at the same moments (as CW1), no guidance |

## Measures (fixed now)
- **Primary: mean completed chains per life, GUIDE-REFLEX − NO-GUIDE** (Gemini, DeepSeek; per seed the mean over 50
  lives, paired by seed, 95% bootstrap over 16 seeds, 10,000 resamples; a real gain if the lower end is above 0).
  **GPT's dissent, kept as a reading rule:** GUIDE-MAP − NO-GUIDE is the key secondary; only a MAP gain may be read
  as "a learned consequence steered the learned planner"; a REFLEX gain alone reads as "a learned consequence chose
  the destination and a written reflex carried the things there".
- Named secondaries: GUIDE-REFLEX − SHAM-REFLEX and GUIDE-MAP − SHAM-MAP (does the right place matter, beyond being
  steered anywhere? needed for any claim that the destination was learned); GUIDE − RANDOM-OPS; carrying time (steps
  from holding A and B to the next join); joins after a guided trip; returns to the station after the first join
  (GPT); hand acts per carrying step (GPT's concern); survival and lifespan, each GUIDE − NO-GUIDE (a cost check
  only, not a learning result: CW1 showed making does not lengthen lives).

## Checks before any test data
1. Zero check: no things, no station, model off: every arm reproduces BV1's BODY bit for bit (RMS 1-8).
2. Physics: the join only on the station, both hand orders; every operation, every held pair, on and off the station.
3. Guidance: it starts only from the model's own learned value (never before a join on the station's look has been
   experienced), only above the floor, to a cell in the place memory; it clears as stated; the walker's memory is
   never changed; the map copy differs from the walker's own map only at the marked cell.
4. Shams: the matched place is never the station, and its path distance is the nearest to the station's.
5. Delayed credit through place: after one scripted chain at the station, holding A and B makes the station the guided
   place.
6. Adapter audit (CW1's, plus the station's look and place); determinism.
A short pilot (brains 1-2, pilot lands 950001-950005) only checks that everything runs and how long a life takes;
no value above is changed by it.

## Limits (written now)
- The carry reflex is written route-following (like the sleep and hunger reflexes); only the destination is learned.
- The map channel goes through the walker's learned food weights, which pull weakly when Bob is well fed (round-table
  check b): a MAP null result may be a gain mismatch, not a failure to learn the place.
- One station, one recipe, the world unchanged; dependent recipes are CW3.

## Compute and recompute
6 arms x 16 seeds x 50 lives on Oracle, Google and this PC (Idle priority), each seed's arms on one machine; about
1.5 hours. The primary and its interval, GUIDE-MAP − NO-GUIDE and the zero check recomputed blind by a fresh session
before the findings are final.

## Expected (before data, the assistant's guess)
GUIDE-REFLEX − NO-GUIDE above 0: about 75%. GUIDE-MAP − NO-GUIDE above 0: about 45% (weak pull when fed).
GUIDE-REFLEX − SHAM-REFLEX above 0: about 70%. Survival of GUIDE-REFLEX within 0.03 of NO-GUIDE: about 70%.
