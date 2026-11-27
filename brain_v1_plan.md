# The starting brain for ACL: plan (draft, 12 November 2026)

**Goal (the creator):** "we gotta build good basic starting brain to put into acl". It goes into the Long World only
after one frozen test shows it is valid: the new brain against the old minds, by ACL's survival rule (extinct at most
the old minds' + 3; population ratio upper bound ≥ 0.80).

## The parts, and the evidence for each
| part | what it does | evidence | status |
|---|---|---|---|
| **seeing space** | a convolutional view of the nearby land (food, water, kin, danger), centred on the person | W1b: a flat network cannot learn to walk to visible food; W1c: convolution can (0.95 in empty rooms from reward) | proven in the workshop |
| **planning** | a value-iteration layer (plus-shaped, V+) that spreads "how far is what I need" over the map | W1d: iteration and the max matter; W1e: the plus pays with training (150k: 0.54 vs 0.35; 500k exploratory: 0.70, still rising) | works; needs long training |
| **map memory** | a fixed writer that keeps what was seen (wall / open / unknown); the planner runs on it | W2: lifts familiar-room detours 0.09 → 0.46; erased or wrong maps take it away; a recurrent memory did not learn to use the tour | proven in the workshop (engineered memory, learned planner) |
| **memory** | a short window of recent things (or a recurrent state) | Cradle C1: needed to keep up with routines; a window is as good as recurrence there | proven in Cradle |
| **copying** | an imitation step toward what others are seen doing | Cradle C2: watching alone teaches no method; copying does (×3) | proven in Cradle |
| **feelings** | an inborn reluctance to harm (on the choice); hunger, rest, love of one's child | ACL NB3: the reluctance ended the killing; learned feelings did not | proven in ACL |
| **sequence memory** | a learned recurrent state that carries what was just shown through the try | WS: deferred imitation 0.91 vs 0.43; skill after teaching stops 0.92 vs 0.54; nightly replay = only extra copying | proven in the workshop; WS correction 1: the own-skill gain comes from the loop within a try, not from holding the showing (WL2). |
| **drives** | survival, comfort, curiosity (the creator's three) as the only motives | W3: no learned brain survived (survival 0 for every brain; lifespans 195–246 steps, random 174, script 2,963); curiosity explores (land known +0.10; curiosity-only 0.86); the hunger link never pointed reliably at food | **failed as built**: learning from sparse reward too slow (W3b proposed, needs the creator) |
| **learning without replaying the teacher** | copy a showing, then try from one's own knowledge (memory of the showing wiped or fading) | WL (the creator's idea): big brain own skill at day 30 0.82 vs 0.04; WL2: forgetting, not noise; wiped memory 1.000 by day 30. Caution: Rohde & Plaut 1999 found limits did not help in a richer task | proven in the box task; to test in a richer world |
| **"that worked!"** | learn strongly from one's own surprising success | WY: first learning +0.13 to +0.15; food much higher | proven in the box task |
| **don't repeat a failure** | a short list of what just failed, avoided while searching | WM: finds new answers (food up) but alone keeps none | engineered; works with the fast memory |
| **fast memory + rest replay** | a store of what just worked, replayed at night into the slow network | WF: relearning after a change 0.45–0.51 vs 0.06–0.12; acting from the store (engineered) about 1.00; WR: all four parts together fit, relearning 0.44 | proven in the box task; the first real learning from mistakes |
| **need gate (W3c)** | a strong need damps the base map and curiosity in the reward map | W3c: no gain alone (G − D3 lifespan +4.5); worse with given links (Gi − D3i −21.6); the recipe still helps (GYFR − G +104); one GYFR seed lived full lives (5 of 50); fair ceiling (remembered full food) lives 3.3× longer but survives 0.055 | **failed as built**; next: a need-specific gain and better exploring |
| **a parent's childhood** | a fair parent (sees only what the child sees) shows the move; copied every 4th step, fading out over childhood | W3d: with the recipe (PYFR) lifespan 806 vs 204, survival 0.128, to 1,000 steps 0.243; parent alone 388; parent forever 272 | **the first rung where learned brains mostly live long**; next: dose/length, and a learned parent (generations) |
| **generations (learned parents)** | a learned child teaches the next, with W3d's childhood and the recipe | W3e: G2 549, G3 473 steps (no parent 248; script-taught G1 806); children copy 0.66-0.68 of the parent's choices; strong lineages fade, weak ones rise; no ratchet | **transmission works, partly; no improvement across generations yet**; next: choosing whom to learn from |
| **choosing whom to learn from** | each life, the child copies the most visibly successful of 4 adults (CH) vs a random one (RN), 3 chained generations | W3f: CH1 701 vs RN1 886 (no gain); both decline over generations (CH3 543, RN3 576); the cue ranks adults fairly well (Spearman 0.67–0.74), so the loss is in the copying itself | **no ratchet**; next: a closer copy or own learning on top |
| **"I have eaten here" memory** | a sixth map channel marking cells eaten at; when to return is left to learning | W3g: lifespan 654 vs PYFR 806 (−153 [−316, −3]); "no food known" deaths 0.77 (was 0.80); the channel was weighted a little | **failed as built**; returning must be taught or inborn |
| **pain** (during development) | an immediate pain at each harmful step, proportional to the harm (thorns: 6 energy, pain 0.75) | W3h: pain cuts thorn steps by 40% (35.6 → 22.2); a careful parent teaches avoidance fast but it wears off after childhood without pain (6 → 23) and holds with pain (→ 14); no over-avoidance of food near thorns; lifespan gain not shown | **proven as a teacher of avoidance**; keep with a parent's childhood |
| **a longer childhood** (and not too much practice alone) | the parent's fade stretched from 0.4M to 1.2M steps | W3i: C (2.8M steps, 1.2M fade) lifespan 1,248 vs 806, survival 0.255 (fresh lands 0.235) vs 0.128; LC − L +377; more practice alone hurts (L 603), and every brain peaks soon after childhood and then declines | **the strongest lever so far**; next: keep the parent's lesson after childhood |
| **an even longer childhood** (W3j) | fade 2.4M of 4.0M steps; also tested: slower adult learning, a quiet parent | W3j: C2 lifespan 1,594, survival 0.363, fresh lands **0.380** (best yet); C2 − C4 +764; slower learning (CK − C −136) and a quiet parent (CV − C −649) do not keep the lesson; the brain frozen at the end of childhood is worse than C (adult learning first helps, then wears away); cloud runs are not bit-identical, so pairing is partial (stated) | **childhood length confirmed a third time**; next: fade 3.6M, stop adult learning at its peak, replay the parent's examples |
| **keep the brain's best copy** (W3k) | from 0.2M steps after the fade, keep a copy whenever the brain's recent training lives are the longest so far; also tested: fade 3.6M of 5.2M, replaying parent examples | W3k (16 seeds, runs now bit-identical): CS lifespan 1,835, survival 0.478, fresh lands **0.445** (best yet); CS − R2 +199 [+70, +347]; a copy from a fixed window does about as well (CS − CY +43 [−21, +109]); C3 − R2 +117 [−193, +432] (not shown, but its curve stops declining); parent replay hurts (CR − R2 −969) | **keeping an earlier copy works**; the parent belongs in childhood only; next: C3's childhood with CS's copy, and what still kills the brain |
| **a longer childhood still** (W3l) | fade 4.8M of 6.4M (C5) and 3.6M of 5.2M (C3), each with its kept copy | W3l (16 seeds; C3 reproduced W3k bit for bit): C5S lifespan 2,041, full lives 0.555, fresh lands **0.559** (best yet); C5S − C3S +344 [+102, +651]; C5 − C3 +278; the kept copy adds nothing after a long childhood (C3S − C3 −56; C5S − C5Y −30); C3S − CS −138 (not shown) | **childhood length confirmed a fourth time**; next: W3m (the sleep reflex), then the two combined |
| **the body's own mind: a sleep reflex** (W3m; the creator's idea) | at tiredness 90 (energy at least 40) the body walks the brain to the known shelter and rests it; also tested: rest only, a tiredness urge | W3m (16 seeds; W3k as the bit-identical control): SLS lifespan 2,223, full lives 0.614, fresh lands **0.646** (best yet); SLS − CS +388 [+101, +689]; exhaustion deaths 0.66 → 0.25; the urge adds nothing (+6); rest only adds nothing (SLS − SRS +371); without its reflex the brain is no better (SLS-off − CS −241) | **an inborn reflex works where reward did not**; hunger near known food is now the main killer; next: W3n (hunger reflex, cheaper rest) |

## What ACL needs for it
- **A map input:** each week, a small egocentric grid of the person's surroundings (food, water, people, kin, danger),
  from the world's own state. Read-only from the world; a brain change only.
- **Moves as the network's own choices:** at first, the network scores ACL's existing options (as NB2/NB3 did), with
  the planner's value at each option's target added. Later, perhaps, the options are replaced by moves.
- **Demographics:** NB3-A's trap (more children, less sharing) is a brain question too: the "drives" must weigh
  another child against food. It is to be tested in the workshop before ACL.

## Order of work
1. **W1e** (done): V+, the plus-shaped planner; train long.
2. **W2** (done): a remembered map works; how to treat the unknown is left to the drives.
3. **W3:** the drives only (survival, comfort, curiosity), no task reward: does the brain keep pushing on its own? **Done 15 November: no** (W3/findings.md). The box-task recipe (14–15 November: WL2, WY, WM, WF, WR) is the candidate fix (W3b, with the creator).
4. **W4:** the parts together in one brain on a small food world with others (sharing, copying, restraint).
5. **The ACL validity test** (frozen; council; recompute). If it passes, the Long World starts with this brain.

## When the brain goes to ACL (the creator, 16 November 2026)
"we are not gonna test it on acl yet because we gotta make sure when we put new brain to acl we gotta see big benefit from new one compared to old one".
- So the ACL exam waits until Mind Lab shows the new brain clearly ahead, not only in abilities but in staying alive.
- The assistant's proposed readiness bar (for the creator to confirm):
  - in W3's world, a learned brain survives full lives at least 0.80 (Script: 0.96; today: 0.14 at best);
  - it relearns after a change;
  - it learns from others across generations without decaying.

## One ACL comparison, then back to the brain (the creator, 20 November 2026)
"when it comes to second one i think we will test this brain inside acl once to compare current brain data with last acl brain data and then we will go back to brain itself again by stoping acl".
- **The decision:** the best Mind Lab brain (W3n's winner, once W3n's findings are final) goes into ACL **once**, to compare its data with the last ACL brain's data. Then ACL stops again and the work returns to the brain itself.
- This is the creator's call; it replaces the 16 November wait-for-the-bar rule for this one comparison.
- It is a frozen study like any other (plan, the creator's sign-off on the plan, checks, recompute). ACL's nature stays frozen (v17): only the people's brain changes.
- Before that comes the "raw eyes" test (W3o, the creator: "yes u can go ahead with first one"): does the brain still work when its world is not sorted into wall, food and shelter layers for it?

## W3n (finished 22 November 2026; `workbench/W3n/findings.md`)
- A hunger reflex (walk to the nearest remembered food at energy 80): HRS − SLS +527 [+346, +742], yes.
- **Fresh-land survival HCS 0.902 [0.873, 0.929], HRS 0.884 [0.861, 0.905]: the survival part of the ACL readiness bar
  (0.80) is met by the whole agent.** Without its reflexes the brain survives about 0.38; the brain itself did not
  improve.
- Cheaper rest (the creator's idea) backfired: CRS − SLS −610 [−796, −355]. Resting became too attractive and the
  brains starved.
- Next limit: deaths are now almost all "no food known" (searching, not reaching).

## W3p (finished 23 November 2026; `workbench/W3p/findings.md`, tag W3p-done) — the new best brain
- The brain is **MoveVIN**: the thinking loop is the body's own physics (4 moves, blocked = stay, 30 rounds), with a
  learned "can I enter here?" filter that **learns walls from its bumps**. 236 numbers (HR's 379).
- **MBb (balanced bump lessons) is the new best Mind Lab brain:** solves every detour (R2 1.00, held out on 200 new
  lands too), long detours 0.88; and **keeps the body alive with both reflexes off** — bare survival 0.988 and lifespan
  2,983/3,000, where W3n's HR was 0.38 and 1,608. The brain itself now does what the reflexes did.
- The planner alone (MV, no bumps) ties the old brain on detours (0.28); the bumps carry it (MB − MV +0.52).
- **Bob Profile: MBb 10/100** (HR 6), the first brain to score in all five abilities (Reasoning, stuck at 0, now 2).
  Capped at 10 only because the level-5+ tests are not built; building them is the next step toward ≥ 60, ≥ 10 each.
- Blind recompute (a fresh session) agrees on every number. Candidate for the one ACL comparison.

## W3o (finished 22 November 2026; `workbench/W3o/findings.md`, tag W3o-done)
- Raw eyes: the brain sees mixed colours instead of sorted wall, food and shelter layers.
- **Mixed colours that always mean the same cost little:** RES − HRS −72 [−150, +4] (within the −200 margin); fresh-land
  survival 0.877, the same as HRS; the brain steps toward food alone almost as often (0.843 vs 0.868). The swap check
  passes (−2,409): it really uses what the colours mean. The bare reading is unclear (−52 [−264, +146]).
- **Colours dealt anew on each land break it:** RVS − HRS −1,482; fresh-land survival 0.27; toward food 0.555 (chance
  0.29). **The gap is learning a meaning within one life** ("I ate where it was this colour, so here this colour is
  food"): fast learning within a life, an approved direction, and a study to draft.
- Recomputed blind by a fresh session; every number and verdict agrees.

## The Bob Profile goal (the creator, 20 November 2026)
"from this scale we should aim at least getting 60+ overall and each one at least 10+".
- The scale: five abilities, 20 points each: learning (unfamiliar tasks), reasoning (multi-step problems), memory
  (long-term recall), generalization (new situations), autonomy (own goals). The assistant's anchor: 20 = adult-human
  level in that ability.
- The assistant's rating of the living brain (W3n's HRS, 20 Nov): learning 3, reasoning 3, memory 2, generalization 3,
  autonomy 2, about 13/100 (a judgment, not a measurement). The old 32-neuron Memory Child: about 5.
- **The goal:** at least 60 overall and at least 10 in each ability.
- **First measured profile (21 Nov 2026, `BP-frozen`, `scorecard/bp/findings_HRS_2026-11-21.md`):** W3n's HRS: learning 2,
  reasoning 0 (detours 0.27), memory 0 (lower bound 0.69 vs 0.80), generalization 2, autonomy 2 = **6/100**. First
  targets: detours, a learned memory of its own, survival without reflexes.
- To make it a measurement, not an opinion, each ability needs fixed tests with anchored levels (the scorecard's job),
  run the same way on every brain.

## Rejecting garbage (the creator, 21 November 2026)
"so we gotta make sure we are not limiting our agents as u said big difference humans can reject garbage but ai cannot so our agent should do same".
- **The principle:** a brain must never be built so that it can only absorb what it is given. It must be able to doubt
  and turn away from bad teaching or bad information, and check it against its own experience.
- **Where it stands:**
  - Mind Lab's big brains became parrots when a teacher was always there;
  - W3f's children chose whom to learn from by visible success (a first filter);
  - the "that worked!" recipe lets its own experience weigh in.
- **Measured by** the scorecard's selective learning (Part A, test 4) and the Bob Profile's autonomy 15 ("turns away
  from a bad teacher").
- **A study to draft (after W3o): the bad teacher.** A parent that is sometimes wrong (it walks to remembered food that
  has gone, or wastes time). Can the child learn to trust its own experience over the wrong lessons, and keep the right
  ones?

## Pain (the creator, 16 November 2026)
"i think for growth there should be suffering also at least for some period maybe when we move one agent to another we will remove pain but i think for beginning there should be pain".
- **The decision:** the growing brain has pain during its development (a body signal of harm that does not kill), so that it can learn to avoid harm, and fear may follow. Pain may be removed later, when a brain moves into another body or world.
- **Practice:** pain is a teacher, not a punishment:
  - kept proportional to real harm;
  - logged in every study;
  - measured for what it teaches (avoidance, one-shot learning, fear, learning by watching).

## 24 Nov 2026: three results (all final, each recomputed blind)
- **W3q, the bad teacher** (tag W3q-done): manipulation check failed narrowly (frozen verdict). Descriptively: a weakly
  learned childhood lie faded once the lying parent left; a parent who stays keeps the lie alive (BP − RP +0.125); and
  ANY parent who never leaves costs the child heavily (RP − HR lifespan −1,063). Rejecting garbage while it keeps coming
  is not in this brain. Idea: trust in teachers learned from how their advice turned out.
- **CX1, the Outside Exam** (tag CX1-done): MBb in Crafter, untrained for it: 0.56%, above random choices through the
  same bridge (0.53%; +0.028 [+0.017, +0.039]), below Crafter's own random agent (1.54%). It finds water and food on
  purpose but has no sense of "enough" (SATED 0.81%) and cannot make anything.
- **ACL's BX1 school** (D:\acl, findings final): MBb raised for 300 ACL lives became as good as ACL's hand-written mind
  (+1.2 years [−2.5, +4.7]) and 8 years better than the untrained MBb.
- **W3r** (learning what colours do within one life; the Crafter brains' consequence model) is running.

## Lessons from Ava (Ex Machina) for Bob (25 Nov 2026; GPT's list, which the creator added to the plan)
The creator watched Ex Machina, shared GPT's list of what Bob could take from Ava, and said: "Yea i want to add it to
plan". The list is GPT's words (labelled), adopted by the creator; the status column is the assistant's.
| Ava's design (GPT) | For Bob (GPT) | Status (25 Nov 2026) |
|---|---|---|
| Reconfigurable brain | neural plasticity and adaptive architecture | researched, not built (`D:\acl\docs\research\mind_evidence_and_growing_brains_2026-11-25.md`: grow when stuck; a new part per new skill) |
| Persistent memories | continual learning without forgetting | measured from now on: every new brain takes the Bob Profile (W3r amendment 5); the post-childhood decline (W3i-W3k) is the open problem |
| Observing humans | learning by observing other agents | done several times: the parent's childhood (W3d-W3f), ACL's brain school (BX1), the bad teacher (W3q) |
| Understanding behaviour | predicting other minds | not started; first step: trust learned from how a teacher's advice turned out (`D:\acl\docs\research\whom_to_trust_2026-11-24.md`) |
| Physical embodiment | intelligence grounded in sensory experience | under way: Body v1 draft (`body/body_v1_draft.md`), CX2 (meanings learned by touching) |

GPT: "The most interesting technical concept to me is a brain capable of reorganizing itself while preserving previous
knowledge." **The proposed next big study (after W3r and Body v1; a draft for the creator and the council, not
started): G1, grow and protect.** When the brain meets a new world or a new sense, it adds a new part (as progressive
networks do) and slows learning in the old parts that mattered (as EWC does), against a fixed-size brain; judged by
learning the new world AND by the Bob Profile on the old one (no loss beyond a margin set before data).

### G1 revised after GPT's critique (25 Nov 2026; GPT's opinion, checked by the assistant; still a proposal)
- **G0 first, a cheap diagnosis** (read-only on saved snapshots of W3i-W3n brains): is the post-childhood decline
  forgetting (an old skill relearns fast), lost plasticity (it relearns slowly) or unstable learning (weights drift and
  swing)? Our data so far: the decline starts after the parent fades; slowing all adult learning did not help (W3j); a
  brain frozen at the end of childhood does worse than one that keeps learning a while (W3j).
- **G1's arms (GPT):** A fixed; B larger fixed (same capacity, no growth); C grow without protection; D grow and protect.
- **Growth triggered by the brain itself** (GPT: "we are managing his development, not Bob"): grow when its own
  surprise stays high, not when we announce a new world.
- **No rigidity (GPT):** judged on three things: learns the new world, keeps the old (Bob Profile), and can still revise
  a meaning when the world changes (W3r's mid-life swap as the test).
- **Order:** W3r -> Body v1 -> G0 -> G1. Meta-learning ("learning how to learn", GPT) is already in the approved
  neural-brain direction (8 Nov: "genes set the starting brain and how it learns, and they evolve"): ACL's deep time.
- The next council on any of these uses the round-table format (the creator, 25 Nov).

### Check before G0 (25 Nov 2026; numbers from the saved test files, by script): the post-childhood decline is gone
Mean test-land lifespan (of 3,000) at each copy, 2.4M (end of childhood) / 2.8M / 3.2M / 3.6M / final 4.0M:
- W3n HR (16 seeds): 2,540 / 2,617 / 2,578 / 2,605 / 2,531 (final below 2.4M in 7 of 16 seeds);
- W3p MBb (8 seeds): 2,964 / 2,978 / 2,978 / 2,962 / 2,994 (MB 2,916-2,983; MV 2,806-2,902).
The decline after childhood (W3i-W3k) is not seen in the current brains (long childhood, both reflexes, MoveVIN).
**So G0 changes:** not "why does the brain decline within its world" (it no longer does) but **forgetting between
worlds**: train the brain on a new world, bring it back, and read the Bob Profile at home (W3r's amendment 5 gives a
first reading). GPT's and the assistant's earlier premise for G0 is corrected here.

### Idea (25 Nov 2026, from the creator's questions "What is entertainment for brain" / "do our brain contain
### entertainment too?"): PLAY, not started
Today MBb's curiosity is staleness-seeking (one of its three drives, a lens on places not seen for a while): novelty,
not fun. Entertainment in the scientific sense would need (1) a brain that predicts (Body v1's consequence model), (2) a
reward for its own learning progress (Oudeyer 2007; Schmidhuber's "compression progress"), fading as things are mastered
(boredom), and (3) free time when fed and rested. A later study, "Play": with free time, does the brain practise or
explore, and does that make it better at surviving later (as young animals' play does)? After Body v1.
**Dopamine (added 25 Nov 2026; the creator: "does that mean we should add dopamine to our brain" ... "ok add that to the
plan too"):** the brain already has a dopamine-like signal: actor-critic's temporal-difference error (what happened vs
what the critic predicted), the same quantity dopamine neurons were found to signal (reward prediction error; Schultz,
Dayan & Montague 1997, cited from memory, to check before use). Today it fires only for body needs (hunger, tiredness)
and a little for staleness. The Play study would let **learning progress** feed the same signal (an intrinsic reward from
the brain's own predictions getting better), with two guards named before any design: (1) the body's needs stay
stronger (no "addiction" to fun over survival); (2) reward learning PROGRESS, not surprise itself (avoids the "noisy TV"
trap, where unlearnable randomness stays surprising forever). The reward comes from Bob's own body and brain, never a
score handed to him (ACL's rule: no named rewards).

## 26 Nov 2026: CX2-C confirms CX2 (final, recomputed blind)
- In Crafter, with meanings learned within each life from what the body feels (not told), MBb beats random choices again on new seeds at 3x the data: LEARN − RANDOM-5P +0.025 score points [+0.012, +0.038] (first run +0.027 [+0.004, +0.052]). Small but real; it rests on the poke reflex. `exam_crafter/CX2/findings.md`, tag CX2C-done.

## 26 Nov 2026: BV1 (Body v1 step 1) gate PASSES
- Through the standard body (senses, verbs, two-part feedback, a Mind Lab adapter) W3r's RM brain lives bit for bit as with its own wiring on 8 seeds, also with all colour and verb numbers renamed; the adapter audit passes first. An interface check only; step 2 (a crafting world, things in hands) is next and needs its own plan. `body/BV1/findings.md`, tag BV1-done (independent re-run still to do).

## 26 Nov 2026: W3r final (recomputed blind): learning what colours do works; revising does not yet
- On lands whose colours change, the brain that learns within its life what each colour does (blocked, fed, rested) survives full fresh lives 0.859 vs 0.211 (RMS − RVS +0.647 [+0.578, +0.714], 16/16 seeds), level with the told-kinds ceiling (−0.026 [−0.068, +0.010]); not an extra-layer effect (vs the sham +0.376); one meal is enough (toward food 0.41 -> 0.85). But after a mid-life colour swap it does not recover (−0.609): a count table never forgets. Next limit: revising a meaning (G1's third criterion; CW1's consequence model). `workbench/W3r/findings.md`, tag W3r-done; the Bob Profile reading follows.

## 26 Nov 2026: CW1 (Body v1 step 2) final (recomputed blind): a combination of things in hands is found and reused within one life
- Through the standard body, a consequence model that plans through hand states (told nothing about A, B, C or the 4 shuffled operations) makes and eats C 5.73 times per life vs 0.65 for random choices at the same moments (LEARN - RANDOM-OPS +5.08 [+4.75, +5.41], 16/16 seeds; first join at step ~296 vs ~1,641); 12 operations instead of 4 slow the first join by ~59 steps only. Making did not lengthen lives (LEARN - NO-MAKE survival +0.001). Limits: one chain, frozen mover blind to things, hand-built planner. Next: CW2 (a station, the creator: "then add station") and revision when the world changes. `body/CW1/findings.md`.
