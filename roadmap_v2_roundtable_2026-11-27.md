# Brain v2 roadmap round-table, 27 Nov 2026 — each answer is that model's opinion, not sign-off

The creator: "run the council on the brain v2 roadmap" (then, during it, sleep-mode autonomy: "ask council then go
ahead"). Question: `roadmap_v2_round1_prompt.txt` (identical to all four, about 00:45 EST 27 Nov). Where: GPT = the
creator's main ChatGPT chat (Instant); Gemini = "Body v1 Test Evaluation"; DeepSeek = "Bob Body v1 council round 1";
Grok = "ACL and Mind Lab Research Briefing for Grok": **no answer in either round** (the page showed "Free tier limit
reached"; nothing bought). Reading note: `=`, `&`, `?`, `;` are shown as spaces (the browser tool withholds them); GPT's
table was read as page text (cells on separate lines, kept as read). Gemini's replies ended with embedded video cards
(a Crafter talk; a video titled "Introducing Mind Lab" about another product of that name), left out.

## Round 1

### GPT (confidence 91%)
1. Research order

Revision first, goals second, lifelong learning third. Start preparing the goal architecture immediately because cloud credits are limited.

Revision is a relatively cheap experiment that addresses a demonstrated weakness. Goals address a fundamental architectural limitation. Lifelong learning becomes more valuable once the brain has a general mechanism for pursuing goals.

However, freeze the architecture before testing lifelong learning so architectural changes do not confound forgetting.

2. General want map or separate goal layer 

Initially, keep them separate. Hunger is an internal biological drive  a goal is a predicted opportunity to satisfy a drive or another learned objective.

Eventually, both should contribute to a shared decision system. Replacing hunger immediately risks destroying established survival abilities.

3. Written scaffolding before ACL

Do not require everything to become neural. Count tables are legitimate learning mechanisms, despite their simple architecture.

Distinguish between:

Written laws: bodily needs, physical constraints and learning mechanisms.

Written decisions: where to go, what to make and whom to trust.

Prioritize replacing written decisions. Keep survival reflexes until learned alternatives demonstrate comparable reliability.

4. Fear and pain

Develop them in Mind Lab first. Distinguish immediate pain from learned anticipation of danger. Test whether fear generalizes appropriately and whether Bob can overcome outdated fears after circumstances change.

Fear without revision could permanently prevent useful exploration.

5. Growing brain

Later. First establish whether a fixed-capacity brain can learn continuously without catastrophic forgetting.

Growth should address demonstrated capacity limitations, not compensate for an unstable learning algorithm. Eventually compare growth against a fixed larger brain with equivalent capacity.

6. What is missing 

Three important capabilities:

Uncertainty: distinguishing what Bob knows from what he merely predicts.

Temporal abstraction: learning reusable sequences of actions rather than repeatedly planning individual movements.

Goal arbitration: deciding between competing needs and learned goals, including when to abandon an unsuccessful goal.

Also, separate the forward model and play into independent studies. Learning progress is an engineered intrinsic objective, even if it is not a task-specific reward. Document that distinction.

My recommended roadmap
(table, as read: V2-1 Revision: Can Bob change his mind? / V2-2 Goals and arbitration: Can Bob pursue learned
objectives? / V2-3 Lifelong learning: Can Bob improve without losing abilities? / V2-4 Forward model: Can Bob predict
consequences? / V2-5 Play: Can Bob discover what is worth learning? / V2-6 Fear: Can Bob anticipate and avoid danger? /
V2-7 Learned seeing: Can Bob discover useful representations? / V2-8 Other minds: Can Bob learn to predict and trust
others? / V2-9 Adaptive growth: Can Bob expand his own learning capacity?)

Overall recommendation: Prioritize revision and goals before the cloud credits expire. Keep the Bob Profile as a fixed regression battery, but also maintain unseen evaluation worlds to prevent indirectly optimizing for the battery itself.

One philosophical caution: use human brain areas as inspiration, not as an architectural checklist. Bob does not necessarily need artificial equivalents of every human brain region. He needs the capabilities those regions help provide.

Confidence: 91%. This is an architectural recommendation based on the supplied results, not an inspection of the implementation. The precise scheduling also depends on available cloud compute.

The most important transition in Brain v2 should be from a brain that learns how to survive to a brain that learns what to pursue.

### Gemini (confidence 90%)
1. Is the proposed order right (V2-1 Revise -> V2-2 Lifelong -> V2-3 Goals), or should Goals or Lifelong Learning come first 

Start with V2-1 Revise, then immediately do V2-3 Goals before V2-2 Lifelong Learning (especially given your December 19–20 cloud credit deadline).

Reason: V2-1 requires zero retraining (test-time surprise-gated count decay/reset on existing frozen brains), making it an instant, high-leverage fix for non-stationarity. V2-3 Goals is your biggest architectural bottleneck (retiring the written carry reflex and giving MoveVIN a general goal interface) and requires ~18h per brain  you should train the goal-capable walker before building continual weight updates (V2-2), otherwise you will have to re-run V2-2 after changing the walker's input layers for V2-3.

2. Should the goal layer replace the hunger pull (one general want map) or sit beside it 

Keep the goal layer beside the existing food/hunger and shelter/tiredness layers—do not collapse them into one merged want map.

Reason: Homeostatic drives (food, shelter) have fixed, survival-critical physical semantics and urgency curves (as CW2 showed, hunger deficit scales food reward dynamically), whereas instrumental subgoals (stations, tools, switches) are transient and conditional on current inventory. Keeping them as separate map channels preserves Bob's hard-won survival instincts while letting the goal channel express flexible, consequence-driven subgoals without competing gain distortion.

3. How much written scaffolding (reflexes, count models) must become learned before ACL 

Retire all task-specific navigation reflexes (carry, hunger, sleep route-followers) and fixed-schema count tables before ACL, keeping only primitive sensorimotor reflexes and biological learning rules.

Reason: In ACL, survival depends on multi-step tool chains, social coordination, and open-ended environmental shifts where hard-coded route-followers and rigid count tables break down. Before ACL, Bob needs: (a) a learned goal-directed planner (V2-3), (b) adaptive/revisable world   consequence models (V2-1 + V2-4), and (c) active adult plasticity (V2-2). Only low-level physiological drives (hunger, thirst, tiredness, pain signals) and physical actuation constraints belong in the "body."

4. Fear and pain in Mind Lab only for now 

Yes—validate one-shot fear (V2-5) in Mind Lab first, before Crafter or ACL.

Reason: Mind Lab lets you run paired, controlled hazard-swap experiments (e.g., a colour or tile suddenly inflicting pain) to verify that one-shot avoidance cleanly overrides positive attraction without inducing permanent paralysis or ruining the Bob Profile. Once verified in Mind Lab, it transfers directly into Crafter (monsters/lava) and ACL.

5. Is a growing brain worth it now or later 

Later—defer structural network growth until after V2-3 and fixed-capacity V2-2 prove insufficient.

Reason: Dynamic architecture growth (adding neurons/columns when surprise stays high) introduces tricky credit-assignment and optimizer-state resets, and risks masking a flawed continual-learning rule by simply throwing parameters at a tiny gridworld. Test fixed-capacity consolidation/replay first  only add capacity growth if multi-world (A -> B -> A) testing hits a hard capacity ceiling.

6. What is missing from this roadmap, or should be cut 

Cut: Defer structural brain growth (V2-2 optional add-on) and push V2-6 Learned Seeing to the end of Mind Lab / start of Crafter (since Mind Lab uses discrete symbolic colour codes where learned visual encoders add overhead without new signal).

Add (Crucial Missing Piece): Arbitration / Executive Control (Prefrontal Gating) between competing drives—specifically how the brain arbitrates between hunger, tiredness, instrumental goals, fear, and curiosity/play when multiple channels are active simultaneously, without relying on hand-written if energy < 100 survival floors.

Overall Recommendation

Execute V2-1 (surprise-gated memory revision) immediately on existing brains, then spend your remaining pre-Dec 20 cloud VM credits on V2-3 (retraining MoveVIN with an explicit goal channel alongside food/shelter) so the written carry reflex can be retired cleanly. Defer V2-2 (fixed-capacity lifelong plasticity, cutting network growth for now) until after the V2-3 architecture is locked, follow with V2-5 (one-shot fear in Mind Lab) and V2-4 (forward body model + gated play), and add an explicit learned drive-arbitration step before entering Crafter or ACL.

Confidence: 90%

### DeepSeek (confidence 79%)
(1) Order: V2-1 (Revise) first is right—it is small, test-only, and de-risks the tables every later part depends on. Then V2-2 (lifelong learning) before V2-3 (Goals): goals sit on top of a walker that must keep learning, and V2-2 is the cheaper prerequisite. But start V2-3's retraining early in parallel because of the 18 h/cloud-credit constraint, not after V2-2 finishes.

(2) Goals should sit beside the hunger pull first, not replace it. Replacing hunger with one general want map is a bigger, unvalidated jump and would confound the V2-3 test  the stated bar—match CW2's carry reflex—is a beside-test, and retirement of the reflex comes only after that passes on held-out lands.

(3) Before ACL, at minimum: revision (V2-1), a persistent learning signal (V2-2), and goals that replace the carry reflex. The hunger and sleep reflexes can stay written longer if the Bob Profile shows they are cheap and not blocking  the count tables should be the first written thing retired, then the carry reflex.

(4) Yes—fear and pain in Mind Lab only for now. Crafter has hazards but adding fear there before it is validated in Mind Lab would violate one-new-part-per-study and risk the ACL timeline.

(5) Growing capacity: later. Do V2-2 with a fixed-capacity protected learner first  only grow capacity if its own surprise stays high after protection is tuned. Growing now would confound forgetting with architecture.

(6) Missing: (a) an explicit "no-loss" gate after each part, not just the Bob Profile at the end  (b) a revision study for the consequence model, not only the colour table (CW1's join change is listed—keep it)  (c) a credit/timeline fallback if cloud credits end before V2-3 finishes  (d) a stated criterion for when a written reflex is retired. Cut: V2-7 (other minds) from this roadmap—it is the least connected to Body v1 and the most likely to eat the remaining budget.

Overall: V2-1 → V2-2 → V2-3, with V2-3 retraining started early in parallel  goals beside hunger  retire count tables then carry reflex  fear/pain Mind Lab only  no growth yet  cut other minds. Confidence: 79%.

## Round 2 (question: `roadmap_v2_round2_prompt.txt`, the divided points; about 01:00 EST)

### GPT (confidence 93%)
Order: Revise → Goals → Lifelong learning. I disagree with DeepSeek: establish the new walker architecture before investing heavily in lifelong learning experiments.

Scaffolding: I disagree with Gemini. Count tables genuinely learn  replacing them merely because they are non-neural is unjustified. Retire written decisions before learning mechanisms.

Arbitration: Separate study immediately after Goals. First demonstrate goal pursuit, then learned prioritization between competing goals.

Other minds: Keep as Brain v2's final milestone, conditional on earlier capabilities passing.

Additions: Include regression gates with prespecified tolerances, retirement criteria, unseen evaluation worlds, uncertainty, and separate forward-model/play studies. Defer temporal abstraction until longer action sequences expose its necessity. If cloud credits expire, checkpoint and postpone full training rather than weaken validation.

Final recommendation: Revise → Goals → Arbitration → Lifelong learning → Forward model → Play → Fear → Learned seeing → Other minds.

Confidence: 93%, based on the reported architecture and results.

### Gemini (confidence 91%)
I disagree with DeepSeek on running lifelong learning before Goals—retraining MoveVIN's input channels for goals changes the architecture, forcing any continual-learning run to be repeated, and keeping written hunger/sleep route-followers forever violates the core design rule against written decisions. I also disagree with DeepSeek on cutting "other minds"  keeping it as the final bridge into multi-agent ACL preserves the roadmap's arc.

Final Recommendation:

Order: V2-1 Revise -> V2-3 Goals + Arbitration -> V2-2 Lifelong Learning -> V2-5 Fear -> V2-4 Forward Model   Play -> V2-6 Seeing -> V2-7 Other Minds.

Written scaffolding: Adopt GPT's distinction—keep general learning rules (like revisable tabular memory), but retire all written navigation decisions (carry, hunger, sleep reflexes) before ACL using DeepSeek's no-loss retirement rule.

Arbitration: Bundle learned goal/drive arbitration directly into V2-3 Goals so the survival floor is retired simultaneously.

Other minds: Keep at the end (V2-7) as the ACL bridge.

Adds: Adopt DeepSeek's no-loss gate, retirement rule, and credit-expiry fallback (V2-1 + V2-5 need zero GPU retraining) plus GPT's unseen evaluation worlds now  defer uncertainty and temporal abstraction to Brain v3.

Confidence: 91%

### DeepSeek (confidence 81%)
Direct to GPT: I agree lifelong learning on a walker whose inputs change must be rerun, but starting V2-3’s retraining in parallel is not a rerun—it is a checkpoint kept current  freeze only its final head.

Final: (1) Goals then lifelong learning, with V2-3 retraining started in parallel and a freeze-and-refresh rule so the input change is a known rerun cost, not a surprise. (2) Tables first, then the carry reflex  hunger and sleep reflexes stay until Goals match them. Written decisions (survival floor, arbitration) retire before written learning rules—GPT’s distinction is right, Gemini’s blanket retirement is too broad. (3) Arbitration inside Goals, as GPT’s table has it, but with a named sub-test that drops failing goals. (4) Other minds cut from this roadmap  revisit after ACL. (5) In Brain v2: no-loss gate per step, retirement rule, credit fallback, unseen evaluation worlds, uncertainty. Later: temporal abstraction, forward model, play as separate studies. Confidence: 81%.

## Summary (who argued what, what survived checking)
| point | GPT | Gemini | DeepSeek | into the roadmap |
|---|---|---|---|---|
| first step | Revise | Revise | Revise | **V2-1 Revise** (all) |
| then | Goals, then arbitration, then lifelong | Goals + arbitration, then lifelong | Goals then lifelong (revised), goal retraining early | **V2-2 Goals (+ arbitration), V2-3 Lifelong** (all three after round 2) |
| goal layer | beside hunger | beside | beside | **beside hunger and shelter** (all) |
| scaffolding | keep learning rules; retire written decisions | keep learning rules; retire all written navigation decisions before ACL | written decisions first; hunger and sleep stay until goals match | **keep count tables as learning rules (revisable after V2-1); retire written decisions one by one, by a stated rule** |
| arbitration | its own study right after Goals | inside Goals | inside Goals with a named sub-test | **inside Goals, with a named sub-test (drop a failing goal)** (2 of 3) |
| fear | Mind Lab first | Mind Lab first | Mind Lab first | **Mind Lab first** (all) |
| growth | later | later | later | **later (Brain v3)** (all) |
| other minds | keep, last, conditional | keep, last | cut | **keep last, conditional** (2 of 3) |
| adds | gates, retirement rule, unseen worlds, uncertainty, separate forward model and play | gates, retirement rule, fallback, unseen worlds | gates, retirement rule, fallback, unseen worlds, uncertainty | **all of these, cross-cutting; temporal abstraction later** |
Checks against the records: V2-1 needs no retraining (W3r's meaning table and CW1's model are test-time); the walker's
reward map reads only fixed layers (CW2's round-table check), so a goal layer means retraining (Gemini right); W3h shows
pain teaches avoidance without over-avoiding food near thorns (the basis for V2-5). Gemini's "the survival floor is a
written decision" is correct (CW1/CW2's floor is a fixed rule in the life loop).
