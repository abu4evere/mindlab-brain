# Council on a general body for Bob (24 Nov 2026): GPT, Gemini, DeepSeek

The creator asked: "Do you think for Bob does it need more than general body? Then ask the council about the general
body." The same one-paragraph question went to each in a fresh chat (the Standard Body proposal: senses eyes/touch/
hands/feelings; verbs look, go, use, take, drop, put-together, eat/drink, rest, signal; rules: verbs before rewards,
three worlds incl. the real one, adapters translate formats never meanings, growth only by general additions; the
Crafter named-recipe problem; what else Bob needs; the smallest first test; a probability). Each answer is an
OPINION, NOT sign-off.

## GPT (chatgpt.com, fresh chat), opinion, not sign-off
1. **Yes, but as a standard sensorimotor INTERFACE, not a universal physical body.** Traps: a body too abstract to be
   useful; intelligence moving into the adapter; a Crafter body believed universal; confusing portable code with
   portable learned intelligence. Relax the three-world rule (a safeguard, not a law).
2. Add: **proprioception** (my position, orientation, movement), **action feedback** (did my action change anything),
   **object targeting** (choose which object), **time perception**, **object properties** (shape, quantity, motion).
   Remove or change: "look" as an action (vision is always on); eat/drink as commands (make them learned uses of
   objects); fixed 4 directions (relative movement); put-two-things-together is too narrow (some transformations need
   several materials, tools or places); signal later, not in the first test. Hunger and pain are fair biological
   priors; knowing which objects satisfy them is not.
3. **The recipe problem:** a general `transform(operation_id)`: the world's native operations exposed as OPAQUE ids
   (no names, recipes, prerequisites or outcomes); the adapter must not pick the right one or hide the ones that fail;
   **randomise the ids between worlds** so Bob learns effects, not numbers. Limit: it shows learning an unfamiliar
   action vocabulary, not discovering crafting physics.
4. Bob needs more than a body, and these matter more: a world model (what my action does here), continual learning,
   object memory, temporal planning (an action with no payoff now may enable one later), uncertainty-driven
   exploration, skill composition, context recognition (telling worlds apart without being told). Do not keep 236
   numbers as a permanent limit.
5. Smallest test, "B1 Cross-World Sensorimotor Learning": one frozen body, brain and learning rule; Mind Lab and Crafter
   with opaque object and action ids; arms A Mind Lab only, B Crafter only, C Mind Lab -> Crafter -> Mind Lab,
   D Crafter -> Mind Lab -> Crafter, E random through the same interface; 8+ seeds; measure learning curves, survival,
   action-effect prediction, transfer speed, retained abilities, achievements. Success: beats random in both, no
   world-specific brain changes, keeps 80% of earlier performance when returning (its own proposed bar), positive
   transfer in at least one direction. Failure: one world only, forgetting, needing semantic adapters, gains that vanish
   when ids are shuffled.
6. Within a year (its subjective forecast): the same interface works in both worlds 95%; the same architecture learns in
   both 85%; one persistent brain learns both in sequence 70%; keeps 80% of old abilities 50%; positive transfer 40%;
   beats Crafter's random agent 65%; general compositional skills 20%. **Overall 70%**, if the brain may grow beyond
   236 numbers (no LLMs, CPU-friendly).
7. Biggest criticism: "Do not spend the next six months engineering the perfect universal body." A universal interface
   is infrastructure, not intelligence. Freeze a minimal Body v1, run B1, let failures decide every addition. "Bob
   should not need the creator to explain a new world. But equally, the creator should not have to redesign Bob every
   time he enters one."

## Gemini (gemini.google.com, fresh chat), opinion, not sign-off
1. **Right idea, but avoid "the robot trap":** a real robot brings continuous physics, partial views, latency and noise
   that would drown a tiny CPU brain in engineering. Keep the standard body for discrete grid survival worlds (Mind
   Lab, Crafter, Craftax, ACL) for now.
2. Remove: "look" (eyes are always on), "take" and "drop" (redundant if "use" acts on tiles and "combine" handles the
   inventory), "signal" (until multi-agent communication is the bottleneck). Keep: a local grid of raw ids, the facing
   tile's id, inventory counts, drives (0-1), and **the missing sense, proprioception / action feedback** ("did my last
   action succeed, fail or get blocked?"). Verbs: move (4), turn/face, interact/use (eat, drink, mine, attack, sleep
   all through it), combine/craft.
3. **The recipe problem:** a parameterless "put together" cannot map onto Crafter without the adapter guessing.
   Parameterise it by slots: `combine(slot_A, slot_B)` over hand or facing-tile slots; the adapter keeps the universe's
   table of valid combinations ("like real chemistry: flint + steel makes a spark"); invalid pairs fail with a
   "blocked" feedback. Bob must discover which raw ids make useful things.
4. Missing: **long-horizon credit assignment and compositional memory**: crafting chains give no immediate relief, so
   without intrinsic motivation (novelty, empowerment, state-change curiosity) or subgoals Bob will never complete a
   6-step chain often enough; and **forgetting protection** (weight consolidation, replay, modular or frozen parts).
5. Smallest test: freeze Body v1 (raw-id grid, facing id, inventory, 4 drives, proprioception; 4 moves, use,
   combine(A, B)); the same architecture, no per-world tuning, run separately in Mind Lab and Crafter. Success: learns
   which raw ids relieve hunger, thirst and tiredness, and makes 1-2 multi-step crafts in Crafter well above random,
   while keeping its Mind Lab survival. Failure: cannot learn which ids feed it without tags, or combine is too sparse
   to ever hit a recipe on a CPU budget.
6. **Probability 35%** (Crafter is light on CPUs and survival from raw ids is tractable; continual learning and
   multi-step crafting without language priors on little compute is hard).

## DeepSeek (chat.deepseek.com, fresh chat, DeepThink with web search), opinion, not sign-off
1. **Right direction, "a high-risk trap if you mistake standard for universal."** Verbs at the wrong grain break it:
   too primitive ("push") and Crafter becomes unlearnable; too composite ("put-two-things-together") and the body
   smuggles in world knowledge. "A body that is general in principle but has never been shown to support learning in
   any single world is worse than a hand-made bridge."
2. Missing: **proprioception of effort/change** (did my action succeed?), **memory of recent interactions** ("I tried
   to put these together and it failed"), **object permanence / local spatial memory**. Remove: "signal" (premature);
   "put-two-things-together" as one verb is the hardest problem.
3. **The recipe problem:** a compositional primitive `put-together(A, B, context)`; the adapter checks which recipe (if
   any) is LEGAL given the inventory and what is near; exactly one legal -> it happens and the outcome is returned;
   several -> an ambiguity failure, not a choice; none -> failure. "The adapter is a physics engine for legality, not a
   recipe selector." Mapping to the nearest recipe would make the standard body "theatre".
4. Bob also needs: **an intrinsic learning signal defined by the body** (prediction error, affordance change,
   competence progress), not the world's score list; **a curriculum controller** proposing goals at the edge of his
   competence without a hand-made task list; **a memory that survives the adapter** (episodic memory of body-level
   outcomes), or "keeping old abilities" is just weight retention.
5. Smallest test: **Mind Lab only first**; a fixed budget (e.g. 10,000 steps); does Bob discover one contingent
   interaction not specified in the body (e.g. "use" on a kind of object changes a feeling consistently)? Pass: that
   interaction becomes more frequent than with random verbs, and stays when the layout is reshuffled. Fail: verb use
   stays random, or only the adapter learned. "If the body cannot support learning in the simplest world you control,
   it will not support learning in Crafter."
6. **15-20%** within a year on a CPU budget; it rises above 40% only if compositional discovery is first shown in a toy
   crafting world we control (simple legality, dense feedback), before Crafter.

## The council (Claude): where they agree, disagree, and what survives
**All three agree:**
- A standard body is right if it is a standard **interface** (senses and verbs), not a universal physical body; keep
  it to discrete grid worlds for now (Gemini: avoid the robot trap; GPT: interface, not physics).
- **Add proprioception / action feedback** ("did my last action change anything?"): all three name it as missing.
- **Drop "look" and "signal"** for now; eat/drink become learned uses of "use".
- **The recipe problem has a clean answer:** the adapter is a physics engine for LEGALITY, never a recipe chooser.
  The three versions differ in how Bob addresses a recipe (GPT: opaque operation ids, shuffled between worlds; Gemini:
  combine(slot A, slot B); DeepSeek: put-together(A, B, context) with ambiguity reported as failure). GPT's opaque ids
  are the simplest and the most honest about the limit (Bob learns an unfamiliar action vocabulary; Crafter's recipes
  are fixed by Crafter).
- **The body is not the bottleneck alone:** Bob also needs a world model (W3r/CX2's direction), intrinsic motivation
  for chains with no immediate payoff, protection against forgetting, and memory of outcomes.
**They disagree on the odds:** GPT 70% (if the brain may grow), Gemini 35%, DeepSeek 15-20% (40%+ with a toy crafting
world first).
**What survives (Claude's synthesis):** GPT's warning ("do not spend six months engineering the perfect body") and
DeepSeek's order (show it in Mind Lab first; a toy crafting world we control before Crafter) point the same way: a
**minimal Body v1** (raw-id eyes, facing tile, hands as counts, feelings, action feedback; move, use, and an opaque
"operate(k)" for world operations; no look, no signal), tested first in Mind Lab with W3r's learned meanings, then a
small crafting addition in Mind Lab, then Crafter. Not started: it waits for W3r and CX2, and for the creator.
