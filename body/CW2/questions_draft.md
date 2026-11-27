# CW2: Body v1 step 3 — a station: can the brain learn that a combination works only at one place, and get the
# walker to carry things there? (DRAFT, not frozen; for the council and the creator)

Drafted 26 Nov 2026 ~23:30 EST at the creator's request (email, 26 Nov: "Yes, please!" to "Should I draft [CW2]?").
**Not frozen; nothing built.** Sources: CW1 (`body/CW1/findings.md`, tag CW1-done), `body/body_v1_draft.md` (step 2:
"start with things in hands then add station"; the consequence model "feeds MoveVIN's reward and passability maps"),
the 25 Nov round-table (Gemini's question about Crafter's table: "spatial requirements (station + inventory)").

## Why
CW1 showed a consequence model can find and repeat a combination of things in hands within one life (5.73 chains per
life vs 0.65 random). But everything happened where Bob stood: the walker (W3r's frozen RM brain) is blind to loose
things and was never asked to go anywhere for them. Crafter's crafting needs a table nearby. CW2 adds that: the join
works only at a station, so a chain needs a place, and the walker must get there with the things in hand. This is
the first test of the body plan's link "the consequence model feeds the planner's map".

## The world (CW1's, plus one station)
- Everything in CW1 stays (A and B spots regrowing, 2 hands, take / drop / use / operate(k), K = 4 shuffled, C = a
  meal of 2 x food, used up when eaten).
- **One station:** a fixed cell per land with its own look (a fourth free colour code, dealt per land), placed at
  least 5 steps from every A and B spot; passable; it never moves.
- **The join works only when Bob stands on the station** (the other 3 operations do nothing anywhere; the join does
  nothing off the station). Open: on the cell, or within 1 step (Crafter's "nearby")?
- Food, shelter and the walker's world as before (W3r's lands).

## The brain
- **Walker:** W3r's RM kept copy, frozen (RMS 1-16), as in BV1 and CW1.
- **Consequence model (CW1's, two additions):**
  1. operations are keyed by what is held AND the look underfoot (as take already was), so "join on the station" and
     "join elsewhere" are different situations it can tell apart;
  2. a **place memory**: the cells where each look was felt underfoot (station, spots), kept for the life.
- **Guidance (the new link):** when the model's best reachable energy from what is held now runs through a look felt
  at a remembered place (e.g. holding A and B, the join's value is only on the station's look), it marks that place
  in the walker's **food layer** (the walker already walks to where it expects energy). Only above the same survival
  floor as CW1 (hunger and tiredness below 0.5); the walker's own food memory is untouched.
- Arbitration at affordance moments exactly as CW1.

## Arms (16 seeds = RMS 1-16; 50 fresh test lands each; new land seeds)
| arm | consequence model | guidance into the walker's food layer |
|---|---|---|
| **GUIDE** | CW1's + place keys + place memory | to the remembered place its value runs through |
| **NO-GUIDE** | the same | none (joins only when the walker passes the station by chance) |
| **SHAM-GUIDE** | the same | to a remembered cell drawn at random from its place memory, at the same moments |
| **RANDOM-OPS** | random at the same moments (as CW1) | none |

## Measures (draft)
- **Primary (draft): mean completed chains per life, GUIDE − NO-GUIDE**, paired by seed, 95% bootstrap over seeds.
- Secondary: GUIDE − SHAM-GUIDE (is it the right place, or any goal?); GUIDE − RANDOM-OPS; steps from holding A and B to
  the next join (carrying time); share of joins made after a guided trip; survival and lifespan GUIDE − NO-GUIDE (does
  being steered cost living?); dead-action rate.

## Checks before data
Zero check (no things, no station, model off: BV1's BODY bit for bit); with guidance off, NO-GUIDE equals a CW1-style
life on the same land when the station rule is removed; the physics (join only on the station, every pair, every
operation); the guidance writes only remembered cells and only above the floor; the walker's own memory unchanged;
delayed credit through place (after one chain at the station, holding A and B makes the station the guided target);
determinism.

## Open questions for the council
1. Is guiding through the walker's food layer a fair "feed the planner's map", or does it smuggle in a written reward
   (it reuses the walker's drive to eat)? Is there a cleaner way without retraining the frozen walker?
2. The station rule: on the cell, or within 1 step? One station or two?
3. Is GUIDE − NO-GUIDE the right primary, and is SHAM-GUIDE the right control for "any goal changes movement"?
4. CW1's making did not lengthen lives (food alone sustains most). Keep the world as is (the question is learning a
   place), or make C matter more (fewer food patches, a bigger meal), knowing that changes the world between studies?
5. Multi-step dependencies (Crafter: wood -> table -> pickaxe): add a second recipe now, or keep one and add it in CW3?

## Expected (before data, the assistant's guess)
GUIDE − NO-GUIDE above 0: about 60% (the guidance is new and the walker's food drive may fight it when food is near);
GUIDE − SHAM-GUIDE above 0: about 60%; GUIDE survival not lower than NO-GUIDE by more than 0.03: about 70%.

## Compute
Test lives only, as CW1: 4 arms x 16 seeds x 50 lives, about an hour on Oracle, Google and this PC.

---------------------------------------------------------------------------------------------------------------------
# PROPOSED FINAL PLAN (after 2 rounds of the round-table, 27 Nov 2026 ~00:20 EST; for the creator's sign-off)
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
