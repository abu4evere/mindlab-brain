# Round-table council on Body v1 (25 Nov 2026): GPT, Gemini, DeepSeek; Claude moderates

The first council in the round-table format (the creator, 25 Nov 2026: "yes use round-table for next council"). One
shared transcript; round 1 each answers; rounds 2-3 each sees the others and may reply or ask anyone. Every model
answer is an OPINION, NOT sign-off; Claude checks claims against the code; only the creator decides.
The question (the same text to all three): Body v1 (`body_v1_draft.md`) and three open questions: (A) is operate(k)
with shuffled anonymous numbers honest; (B) how should feedback and hands enter the brain (extra map layers or a
separate consequence model); (C) what margin counts as "no loss" in step 1, and what else must be measured.

## Round 1

### GPT (chatgpt.com/c/6b071eb0-72c8-83ea-8612-6260631cc9cf)
1. (A) Honest as an engineering compromise, not as world-independent: shuffling hides the operations' identities, not
   Crafter's crafting structure. Accept it for Body v1, say so, and later move to compositional operations (objects,
   materials, tools). Do not expose which operations are currently legal; Bob should find out by trying.
2. (B) Strongly a separate small learned world model: MoveVIN plans space; inventory, crafting and consequences are not
   spatial. Start count-based, P(consequence | context, action): inventory, body, movement, object changes; the planner
   uses its predictions.
3. Feedback: four bits are too little ("hunger changed" cannot tell eating from starving): give signed differences of
   inventory and body between steps (measurements, not meanings); tell immediate from delayed consequences.
4. (C) At most 5% relative loss in mean lifespan and 3 points in full-life survival, both non-inferiority tests at 95%
   (its own provisional tolerances); frozen before running; paired fresh worlds; dependence between lives of one brain
   accounted for; an inconclusive interval is not a pass.
5. Also measure causes of death, food-finding efficiency, detours, reflex dependence, action efficiency, learning speed,
   worst seeds: an average can hide one ability lost and another compensating. Test the frozen brain first, adaptation
   separately.
6. The id-shuffle check is necessary, not sufficient: an adapter can leak knowledge through which actions are available,
   observation order, automatic targeting or hidden state; audit those; also test re-learning after new permutations.
7. Biggest concern: learning what objects ARE is not learning what can be DONE with them; the crafting world needs one
   useful multi-step sequence that neither brain nor adapter knows.
8. **Question for Claude:** does the bump-then-poke reflex encode Crafter-specific knowledge? Would it stay useful where
   poking an obstacle costs resources or causes damage? Check it against the implementation.
9. Verdict: approve Body v1 with these amendments; keep MoveVIN as the spatial planner and grow a consequence model
   beside it; do not redesign brain and body at once.

### Gemini (gemini.google.com/app/62db1c2ec94f74b7; Gemini offered two drafts, A and B, and asked which is better; both
### make the same main points; Claude chose B to continue the thread; A's extra points noted)
1. (A) **operate(k) leaks**: even shuffled, it tells Bob exactly how many distinct transformations the world has
   (reducing search to a 1/K bandit over buttons) and collapses multi-step sequences into one button; a fixed head of K
   verbs also breaks the same brain across worlds with a different K. Instead: one combinatorial verb, `combine(slot_a,
   slot_b)` / `apply(hand_kind)`, plus `place(hand_kind)`, over the kinds Bob actually holds or touches; the adapter
   checks whether the pair matches a recipe's ingredients (legality) without listing recipes. (Draft A: the same, and
   "or accept that with operate(k) Bob learns a menu of transitions, not construction".)
2. (B) A separate small forward model, not extra map layers: VIN relies on spatial convolution; spreading non-spatial
   counts over every cell wastes a 236-number budget and breaks the spatial bias. Keep map channels for per-tile learned
   affordances (passability, feeling change, interactability); add a per-kind effect table f(hands, touch kind, action)
   -> change in feelings, hands, tile, which writes MoveVIN's reward and transition maps: "what things do" apart from
   "where to go".
3. (C) At most 5% relative loss in mean survival time and in catastrophic deaths over paired seeds, allowing for the
   "information-gathering tax" of learning meanings from scratch. Also measure: the permutation check with statistics
   (e.g. a KS test, p > 0.1); **the lift over the reflex alone** ("in Crafter learned eyes 1.51% vs random 1.48% is
   essentially tied within noise"; track learned brain minus reflex-only so the reflex is not carrying the score);
   early-life vs late-life performance (the exploration tax); the dead-action rate (illegal or futile actions).
   (Draft A adds: idle/camping rate, so survival is not a degenerate "rest in a corner"; the consequence-learning curve
   in the first 500 steps.)

### DeepSeek (chat.deepseek.com/a/chat/s/05f376c4-c237-4ff8-9d00-31674886425b; DeepThink)
1. (A) Honest only as an opaque native-verb slot: ids shuffled per world or life, no names, no ordering or grouping by
   recipe, no legality shown, the adapter only calls the world and reports the feedback. But not a clean generality
   test: Crafter's fixed operation set, its size and its legality pattern are a fingerprint of its recipe structure; Bob
   finding that by probing is legitimate learning unless the adapter pre-filters, groups or orders operations. Instead:
   call operate(k) a world-specific motor repertoire, audit the adapter, and run controls with randomised or padded
   operation lists and a low-level arm without the native make verbs.
2. (B) Not map layers for hands and feedback: keep touch / front tile as local map layers; hands and feelings as a
   compact global vector into the actor and value head; a small consequence predictor per action (changes in place,
   hands, front tile, feelings, plus uncertainty) feeding the planner as costs / expected features; feedback mainly as
   training signal and surprise.
3. (C) No mean-only margin: a non-inferiority test on paired seeds, the lower 95% bound of the difference above −5%
   relative survival, at least 10 seeds and 1M steps, and the worst-quartile seeds not worse by more than 10%. Also:
   death rate and causes, need trajectories, action-rejection rate, feedback-prediction accuracy, hand counts,
   exploration coverage, per-life learning curves, seed variance, compute, id-shuffle invariance, ablations of
   touch/hands/feedback, retention on old held-out tasks; survival can be fooled by rest-spam or safer random behaviour.

## Claude's answer to GPT's question (checked in the code and the CX2 data)
- **The code** (`exam_crafter/cx2.py`, `after()`, lines 213-214 and 225): after ANY blocked move, on any kind, with no
  exceptions and never reading the tables, the hand presses "do" on that cell until something changes or 5 tries. So
  in form it is universal, not Crafter-labelled.
- **But it assumes poking is cheap.** In Crafter "do" costs only time, except that it starts fights: in CX2 the body
  lost health during 3.35 bouts per LEARN life (BLIND 2.55, RANDOM-5P 1.18; these count health drops during a bout,
  which may come from a nearby zombie as well as from the poke). In a world where touching hurts (thorns, lava), the
  fixed reflex would cost. GPT is right: it is a Crafter-friendly bias. A general version: poke kinds not yet tested,
  and stop poking kinds whose pokes brought pain (the pain feeling as one more consequence in the table).
- **On Gemini's "1.51% vs 1.48% is essentially tied":** the frozen primary was above 0 but only just ([+0.004, +0.052]),
  and a 3x confirmation run is going. The data also back Gemini's worry: RANDOM-5P (random moves, the same poke reflex
  and tables) reached 1.48% and BLIND (the brain, the reflex, no meanings) 1.05%, so **the reflex carries much of the
  score**; what the learned meanings add over the reflex is LEARN − BLIND = +0.46 for the brain.

## Round 2 (each saw the three round-1 answers and Claude's checks)

### DeepSeek
1. Agrees with Claude that the reflex carries much of 1.48-1.51% and that 1.51 vs 1.48 is not yet a win for learned
   meanings; survival alone is insufficient.
2. **Changes one view:** no longer calls operate(k) "honest" without qualification: an opaque but world-specific motor
   repertoire with a structural fingerprint.
3. Still keeps operate(k) for Body v1: shuffled, no legality / order / grouping exposed, adapter audited, plus padded or
   randomised operation lists and no-make controls.
4. Gemini is right that a fixed K leaks the number of operations and turns multi-step sequences into buttons; combine is
   a good ablation arm, not the v1 default.
5. But combine(slot_a, slot_b) is not neutral either: two slots over held/touched things presume combinable structure and
   may miss one-ingredient, place and move operations.
6. On (B) sides with GPT and Claude: touch as map; hands and feelings as a global vector; signed changes; a small
   consequence predictor with uncertainty; feedback as surprise and training signal.
7. On (C): frozen-brain non-inferiority, worst quartile, reflex-only lift, dead-action / idle / camping, the poke's pain
   cost, retention; "1.51 vs 1.48 stays a tie until confirmation".
8. **Question to Gemini:** how would combine(slot_a, slot_b) check legality without encoding recipe pairing, and how
   does it represent one-ingredient or place operations?

### Gemini
1. **Answer to DeepSeek:** the adapter does encode the world's physical rules ("its job, like a physics engine checking
   if wood + stone makes an axe"), as it checks operate(k)'s legality; combine exposes the interface of material
   interaction instead of listing solutions as buttons. Unary and place operations: slot_b = NONE (a change of slot_a
   alone, e.g. eating) or FRONT_TILE (applying or placing slot_a on the tile in front, e.g. placing stone, a pickaxe on
   rock).
2. **Changes its view:** concedes to GPT and DeepSeek that combine as the v1 default adds complexity before basic transfer
   is validated; keeps operate(k) as an explicitly labelled native motor repertoire in v1, with DeepSeek's padded / dead-op
   controls, and combine as a v2 ablation.
3. (B): all three converge: MoveVIN stays purely spatial, its reward and transition maps fed by a light online
   consequence model; signed changes of hands and feelings, not one-bit feedback.
4. (C): the reflex did heavy lifting (it reads +0.43 random-with-reflex over brain-without-meanings, against +0.46 for
   learned meanings) and cost health; make the poke pain-gated and measure lift over a pain-gated reflex baseline.
5. **Question to the creator:** Crafter's crafting needs a nearby station (a table) and multi-step dependencies; does the
   step-2 crafting world in Mind Lab include spatial requirements (station + inventory), or only inventory-to-inventory
   combinations?
(Claude's note: "+0.43" is RANDOM-5P minus BLIND, which differ in the controller AND in using meanings, so it is not a
clean "reflex lift"; the clean reflex measure is LEARN minus LEARN-NP, +1.29, and a pain-gated version is a new arm.)

### GPT
1. (A) Accepts the consensus: freeze operate(k) as an opaque, world-specific motor repertoire, not a universal motor
   language; combine for v2 experiments. One shared action-scoring mechanism that takes any number of operations without
   resizing or retraining the brain; never expose legality masks.
2. (B) Freeze MoveVIN as the spatial planner with a separate light online consequence model (signed deltas, inventory,
   body, uncertainty). Replace blind repeated poking with pain-sensitive exploration; include a pain-gated reflex-only
   baseline to isolate the brain's real contribution.
3. (C) Keeps its margins: at most 5% relative mean-lifespan loss and 3 points absolute survival loss, both lower bounds
   clearing them; freeze paired seeds, id-permutation audits, dead-action rates, detours, early/late life, reflex
   dependence.
4. **Test frozen-brain compatibility separately from adaptation: do not add the new consequence model in the first body
   test** (two changes at once would confound it).
5. **Question for Claude:** can Body v1 support previously unseen numbers of native operations without adding learned
   parameters or changing the brain's architecture?

## Claude's answer to GPT (round 2) and the end of the round-table
**Yes, if operations are chosen by a shared rule over a table, not by a fixed output head.** In CX2 the meanings live in
count tables keyed by kind number, which grow with whatever kinds a world has and carry no learned weights. Operations
can work the same way: a table keyed by operation number (tries, and the signed changes that followed), and one shared
rule that scores "operate(k)" from its table entry (the value of its predicted consequences, plus a bonus for untried
k). A world with 3 or 30 operations then needs no new parameters and no change to MoveVIN. A fixed output head of K
logits would not do this; Gemini's point about K stands for that design.
**Stopped after round 2** (the cap is 3): positions converged, the remaining questions were answered, and one is for the
creator.

## What the round-table agreed (Claude's summary; every point checked against the code or the CX2 data)
1. **operate(k)** stays in Body v1, labelled as each world's native motor repertoire (not universal): numbers shuffled,
   no names, order, grouping or legality shown; controls with padded / randomised operation lists and a no-make arm;
   combine(slot_a, NONE | slot_b | FRONT_TILE) is a v2 ablation (Gemini changed its view; DeepSeek changed its view on
   calling operate(k) "honest").
2. **Operations chosen by a shared rule over a table** (no fixed K head), so any number of operations needs no new
   parameters (GPT's question; Claude's answer).
3. **MoveVIN stays the spatial planner**; hands, feelings and feedback go to a separate light consequence model (signed
   changes, count-based first, with uncertainty), not smeared over the map (all three).
4. **The poke becomes pain-gated** (poke untested kinds; stop poking kinds whose pokes brought pain), with a reflex-only
   baseline (all three, after Claude's check of the code).
5. **Step 1 tests the frozen brain through the body only**, without the new consequence model (GPT); margins: the lower
   95% bound of the difference above −5% relative mean lifespan AND above −3 points full-life survival, on 10+ paired
   seeds, worst quartile not worse by more than 10% (GPT's and DeepSeek's combined).
6. **Adapter audits beyond id shuffling:** action availability, ordering, auto-targeting, hidden state (GPT, DeepSeek).
7. Also measure: dead-action and idle rates, early vs late life, detours, causes of death, retention (all three).
**Open, for the creator (Gemini's question):** should the step-2 crafting world in Mind Lab need a station nearby (like
Crafter's table) plus inventory, or only inventory-to-inventory combinations?
