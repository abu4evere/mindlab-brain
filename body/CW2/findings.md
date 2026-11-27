# CW2 findings (Body v1 step 3, a station): steering the walker to a learned place doubles the reuse of a found
# combination; the walker's own planner can be steered too, but only a little

Frozen plan: `questions.md` (tag CW2-frozen; the creator's sign-off by email, 26 Nov 2026: "Sounds good to me").
Run 26-27 Nov 2026 (EST, night) on three machines, each seed's six arms on one machine: Oracle (seeds 1-8), Google
(9-12), the second computer (13-16, Idle priority); numpy 2.5.3 everywhere. 96 jobs, all exit 0; 4,800 lives (6 arms x
16 seeds x 50 fresh lands 940001-940050). Every number is from `output/analysis.md` (the frozen `analyse_cw2.py`); the
key ones were recomputed blind (`recompute_cw2_blind.md`).

## Before data (recorded)
- Checks `checks_cw2.log`: **All: PASS (70/70)**: the zero check (no things, no station, model and steering off: all 6
  arms reproduce BV1's BODY bit for bit on RMS seeds 1-8); the station's placement and physics (the join only on the
  station, both hand orders; the station cannot be taken); guidance never from the untried bonus; delayed credit
  through place; the map mark only in the planner's copy (2,501 forced marked steps); the sham never the target's
  look; adapter audit; determinism.
- Two build faults fixed before data: "take" on the station tried to take the station; a check compared against a
  world left over from an earlier life (the check's fault, not the study's).

## Results (800 lives per arm; per seed the mean over 50 lives; paired by seed; 95% bootstrap over 16 seeds)
1. **Primary: mean completed chains per life, GUIDE-REFLEX − NO-GUIDE = +0.627 [+0.430, +0.843], 16 of 16 seeds ->
   a real gain** (1.110 vs 0.483). Blind recompute: +0.627 [+0.432, +0.843], 16/16.
2. **Key secondary (GPT's reading rule): GUIDE-MAP − NO-GUIDE = +0.108 [+0.060, +0.160], 12+/2− of 16 -> a real but
   small gain** (0.590 vs 0.483). Recompute: +0.108 [+0.060, +0.161].
3. Is it the right place? GUIDE-REFLEX − SHAM-REFLEX +0.804 [+0.574, +1.051] (16/16); GUIDE-MAP − SHAM-MAP +0.091
   [+0.046, +0.145] (12+/1−). Being steered to a wrong place costs chains (SHAM-REFLEX 0.306 < NO-GUIDE 0.483).
4. **Discovery is unchanged: 0.255 of lives make at least one chain in every model arm, the same 204 of 800 lives**
   (recompute), because guidance starts only after a join on the station has been experienced (the plan's rule). The
   whole gain is in reuse after discovery.
5. How: returns to the station after the first join 50.2 (REFLEX) / 8.7 (MAP) vs 2.7 (NO-GUIDE); carrying time from
   holding A and B to the join 114 / 242 vs 292 steps (REFLEX −178 [−214, −146], 16/16; MAP −50 [−78, −23]).
6. Cost (a cost check only): survival GUIDE-REFLEX − NO-GUIDE −0.015 [−0.026, −0.005]; lifespan −16 steps [−29, −4];
   GUIDE-MAP −0.003 [−0.007, +0.002]. Hand acts per carrying step about 0.06 in every model arm (GPT's concern that
   holding things would block walking: not seen).
7. RANDOM-OPS: 0 chains in all 800 lives (random choices never carried A and B to the station and joined there).

## A measurement fault (recorded, not corrected in the frozen script)
"Joins made on a station guide" reads 0 in both GUIDE arms: the guidance is cleared on the step Bob reaches the
target, before the hand step that joins, so the counter never sees an active station guide at a join. The measure is
not interpretable; returns to the station and carrying time (5) carry the same question.

## Reading against the guesses written before data
GUIDE-REFLEX − NO-GUIDE above 0: guessed ~75%, came true. GUIDE-MAP − NO-GUIDE above 0: guessed ~45%, came true but
small. GUIDE-REFLEX − SHAM-REFLEX above 0: guessed ~70%, came true. GUIDE-REFLEX survival within 0.03: guessed ~70%,
came true (−0.015).

## Limits
- The carry reflex is written route-following; only the destination is learned. By GPT's rule only the MAP gain shows
  the learned consequence steering the learned planner, and it is small: the walker's food pull is weak when fed (the
  round-table's check), so most of the carrying is still done by a written reflex.
- Discovery of the first join is left to chance (25.5% of lives); guidance helps only after it.
- One station, one recipe, the world unchanged.

## What it means for Bob
Bob can learn WHERE a combination works and go back there to repeat it: once a join at the station has been
experienced, steering by its own learned value about doubles the chains in a life. But the strong effect needs a
written carry reflex; through the walker's own planner the pull is small. That is the Brain v2 roadmap's next step:
V2-2, a goal layer the planner learns to use (so the reflex can be retired), with learned arbitration between needs and
goals.
