# Brain v2 roadmap: adding Bob's missing parts (DRAFT for the council and the creator; nothing started)

Drafted 27 Nov 2026 (EST, early hours) on the second computer at the creator's request: "draft the brain v2 roadmap
while it runs", after the creator said: "I would love to add all missing parts for Bob, as you say, preferential
cortex and other things also." Not frozen, not signed off. Each step below is its own study: plan -> round-table ->
the creator's sign-off -> frozen -> checks -> runs -> blind recompute, as always.

## Where Bob is today (Brain v1 plus Body v1)
| real brain part (analogy only) | what it does in people | Bob today | status |
|---|---|---|---|
| brainstem | keeps the body alive; fast reflexes | sleep and hunger reflexes (written; W3m, W3n); carry reflex (CW2, written) | has a version |
| hypothalamus | body needs -> feelings | hunger, tiredness (and pain where the world has harm, W3h) | has a version |
| parietal + motor cortex | a map of space; planning and making moves | the walker: MoveVIN on a remembered map (a learned network, trained in a long childhood, then frozen) | has a version |
| hippocampus | fast memory of events and places; replay in sleep | a fixed map writer; W3r's meaning table; CW2's place memory (counts, never forget) | rough |
| basal ganglia | choosing actions; habits; learning what actions are worth | CW1's consequence model (counts, value through hand states) | rough |
| dopamine (midbrain) | "better or worse than expected": the learning signal, all life long | the walker's actor-critic error, during training only; nothing during a life | rough |
| visual cortex | learns to see from raw light | colour codes per cell (no learned seeing) | rough |
| prefrontal cortex | holds a goal; plans steps toward it; self-control | **missing**: the walker is pulled only by food, shelter and staleness (CW2's round-table check) | missing |
| amygdala | fear; one-shot learning of danger | **missing** (pain proven as a teacher in W3h, but no fear memory) | missing |
| cerebellum | a model of one's own body; timing; smooth movement | **missing** (a grid body needs little) | missing |
| social brain | predicting others; whom to trust | copying a parent (W3d-W3f, WS); no model of other minds | rough |
The analogy is a design guide, not biology: real areas overlap and work together.

## Rules for every step (from CLAUDE.md and the approved neural-brain direction, 8 Nov 2026)
1. **Program the body, not the decisions.** A new part may be built in; what it should do must be learned.
2. **One new part per study**, against a control without it and a sham (the same machinery, wrong signal).
3. **Nothing old may be lost:** every new brain takes the Bob Profile (no regression beyond a margin set before data).
4. **Prefer learned over written.** Written parts (reflexes, the carry reflex, CW's counting models) are scaffolds; a
   later step should replace each with a learned part that does at least as well.
5. **No hand-made fitness, no named rewards** (energy, pain, rest and the brain's own learning progress only).
6. Mind Lab first, then Crafter (the outside exam), then ACL (the final exam; ACL's world stays frozen until 7 Dec).

## The steps, in a proposed order (each needs what came before)
### V2-1 Revise: a memory that can change its mind (hippocampus + a surprise signal) — small
- **Why first:** W3r's open failure: after a mid-life swap of meanings, survival fell by 0.61 and never recovered,
  because count tables never forget. Every later part needs a brain that can update.
- **Idea:** surprise-gated revision: when what happened differs strongly from what the table predicted, old evidence
  for that look counts less (a learned or fixed recency, opened only by surprise). Builds on WF (fast memory + rest
  replay relearned after a change: 0.45-0.51 vs 0.06-0.12, box task).
- **Test:** W3r's mid-life swap and CW1 with a mid-life change of the joining operation; arms: plain counts, a fixed
  recency window (DeepSeek's CW1 idea), surprise-gated. Pass: recovers after the swap without losing stable meanings.
- **Cost:** test lives only, about an hour on the VMs.

### V2-2 Keep learning for life: a lifelong learning signal (dopamine) with protection — medium
- **Why:** today the walker is frozen after childhood; people never stop learning their body and world.
- **Idea:** let the walker keep learning during adult life from its actor-critic error (our dopamine-like signal),
  protected against forgetting (G1's "grow and protect": slow down the weights that mattered; add capacity when its own
  surprise stays high). This is G0 -> G1 from the v1 plan, now with Body v1 underneath.
- **Test:** train in world A, move to world B, come back; arms: frozen, learn freely, learn with protection, grow and
  protect. Pass: learns B AND keeps A (Bob Profile) AND can still revise (V2-1's test).
- **Cost:** training runs (hours per brain) on the VMs.

### V2-3 Goals: a prefrontal part that can want any place, not only food — large
- **Why:** CW2 had to steer the walker by marking the station as food, or by a written carry reflex. A real goal system
  lets the value system say "go there" for any reason.
- **Idea:** retrain the walker with one more map layer, a **goal layer**, whose pull is set by the value system (the
  consequence model's best reachable energy), not by hunger. In childhood the goals come from the brain's own
  experience (places where good things happened), never from a designer's list.
- **Test:** CW2's world again; arms: goal layer, CW2's carry reflex, CW2's map mark, none. Pass: the goal layer at
  least matches the written carry reflex, so the reflex can be retired (rule 4).
- **Cost:** a new childhood for 16 walkers (about 18 h each on the VMs): the biggest step; best started before the
  cloud credits end (~19-20 Dec).

### V2-4 A body model and play (cerebellum + learning-progress reward) — medium
- **Why:** children spend years learning their body by play. Bob's body will grow richer (Body v2: more verbs, more
  senses), and the "Play" idea is already approved for after Body v1.
- **Idea:** a small network that predicts what each action will do to the senses (a forward model); its improving
  predictions give a reward for learning progress (not for surprise: the "noisy TV" guard), only when fed and rested;
  the body's needs always stronger.
- **Test:** free time with vs without the play reward; pass: later faster learning in a new body or world, no loss of
  survival.

### V2-5 Fear (amygdala + pain) — medium
- **Why:** the creator's rule (16 Nov): pain during development, so harm can be learned and fear may follow.
- **Idea:** a fast, one-shot "this hurt" memory tied to looks and places, that shapes the goal layer (avoid), and fades
  only with safe experience. Builds on W3h (pain teaches avoidance, no over-avoidance of food near thorns).
- **Test:** a Mind Lab world with hazards; arms: pain only, pain + fear memory, sham (fear tied to random looks). Pass:
  fewer harms after one experience, no extra hunger deaths from over-avoidance.

### V2-6 Seeing (visual cortex) — large, later
- From colour codes to learned seeing (small images of the nearby land, a convolutional eye; W1c showed convolution can
  learn to find food). Needed before the brain meets richer worlds (Craftax, then ACL's own senses).

### V2-7 Other minds (social brain) — later
- Copying already works (W3d-W3f, WS). Next: trust learned from how others' advice turned out (W3q's idea), then
  predicting what another person will do.

### Then: one brain with all its parts
Integrate, take the Bob Profile, then Crafter (CX-series), then ACL after the world review.

## What I'd do first (the assistant's recommendation)
1. **V2-1 Revise** right after CW2 (small, fixes a known failure, needed by everything else).
2. **V2-3 Goals** next, started early because its retraining is long and the cloud credits end around 19-20 Dec.
3. V2-2 alongside V2-3 on the other VM if capacity allows; V2-4, V2-5 after.

## Open questions for the council and the creator
1. Is this order right, or should goals (V2-3) come before revision (V2-1)?
2. Should the goal layer replace the hunger pull entirely (one general "want" map) or sit beside it?
3. How much of Bob's written scaffolding (reflexes, counting models) must be replaced by learned parts before the brain
   goes to ACL?
4. Fear and pain: Mind Lab only for now (ACL's world is frozen until 7 Dec)?
5. Is a growing brain (V2-2's "grow") worth its complexity now, or later?
