# CW1 round-table (Body v1 step 2, the crafting world), 26 Nov 2026 — each answer is that model's opinion, not sign-off

The creator: "Run the CW1 council". Question: `roundtable_round1_prompt.txt` (identical text to all four, sent about
20:15 EST). Where: GPT = the creator's main ChatGPT chat; Gemini = "Body v1 Test Evaluation"; DeepSeek = "Bob Body v1
council round 1"; Grok = "ACL and Mind Lab Research Briefing for Grok" (Fast mode).
**Reading note:** the browser tool withholds text containing some characters, so each answer was read with `=`, `&`,
`?` and `;` replaced by spaces (e.g. "K   4" is "K = 4"); otherwise verbatim. Gemini's answer contained a rendered
formula, shown as the page gave it.

## Round 1

### GPT (confidence 90%)
1. Arbitration — when should the consequence model act 

Use a shared action-selection mechanism with movement as the default. The consequence model should compete for control based on expected bodily benefit and curiosity. Avoid programmer-written triggers such as "operate when both hands are full" because that implicitly teaches the crafting sequence. Both LEARN and RANDOM-OPS should have the same arbitration mechanism.

2. Difficulty and primary outcome

Two kinds and four operations are appropriate for a first experiment. However, C is reusable, so three uses of C do not demonstrate three successful crafting chains.

Distinguish:

Discovery: independently produces C.

Exploitation: repeatedly uses C.

Reproduction: independently produces C again.

I'd make discovery followed by repeated beneficial use the primary outcome. Measure reproduction separately. Also, verify that the agent can discover delayed benefits: joining A and B provides no immediate energy, so a one-step consequence model may undervalue it.

3. Failed operations and poking

Every failed operation should consume ordinary time and energy, but no artificial punishment. Pain-gated exploration is a good general principle, provided pain comes from actual world consequences rather than programmed judgments about which actions are undesirable.

4. Controls and PAD

RANDOM-OPS is necessary, but "same moments" must not mean replaying LEARN's decisions or using knowledge unavailable to the random agent. Both should have equivalent action opportunities and arbitration rules.

Keep PAD. Unlike BV1, additional operations can genuinely affect exploration here. It tests whether learning remains effective as irrelevant possibilities increase.

5. Forgetting

Keep plain counts for CW1. Establish whether consequence learning works in a stationary world before introducing adaptive forgetting. Then conduct a separate experiment where operation meanings change mid-life. Otherwise, two new mechanisms are being tested simultaneously.

Overall recommendation: Proceed after resolving arbitration and delayed credit assignment. My biggest concern is that the consequence model learns immediate effects but may not learn why an intermediate action is useful. A successful crafting sequence discovered accidentally is not necessarily evidence that the agent understands its causal structure.

Confidence: 90%. This is a design-level assessment  I have not inspected the implementation.

CW1 should demonstrate that Bob can discover and exploit an unfamiliar action sequence without being taught its purpose—not merely that random exploration occasionally produces something useful.

### Gemini (confidence 89%)
1. When should the consequence model act instead of the moving brain (arbitration) 

Use a deterministic, strictly gated override when standing on an item or holding items while hungry, yielding immediately to the moving brain when starving/exhausted.

Reason: Because W3r's moving brain is frozen and blind to loose items (A, B, C), it will simply walk past them unless the consequence model takes control at affordance moments (item underfoot with a free hand, or holding items when hunger < threshold). However, letting the consequence model hijack steps when energy or rest is critically low will sabotage survival and confound lifespan comparisons against NO-MAKE. Keep the arbitration rule identical across LEARN and RANDOM-OPS.

2. Is one useful chain (K   4, 2 kinds) and ≥3 completions the right first difficulty/metric 

Yes on difficulty (K   4, 2 kinds)  no on the binary ≥3 completions threshold—use continuous mean completions per life (with ≥3 as a secondary).

Reason: With 2 hands, 2 item types, and K   4 operations (plus use and drop), the state-action space has roughly 3×3×7≈63 situation-action pairs—small enough to explore within a 3,000-step life, yet large enough to distinguish systematic discovery from lucky button-mashing. However, dichotomizing completions at ≥3 throws away statistical power on 16 seeds  mean chain completions per life (plus survival-adjusted rate per 1,000 steps) is cleaner and less noisy.

3. Should failed operations cost something, and should poking be pain-gated here 

No extra failure penalty beyond the 1-step metabolic tick, and no pain-gating yet.

Reason: Each failed operate(k) or use already incurs an opportunity cost (1 step of basal energy/rest decay and delayed foraging). Adding synthetic pain penalties introduces an ungrounded scalar hyperparameter and risks teaching risk-aversion rather than causal discovery. Keep CW1 purely focused on positive/neutral affordance discovery  test pain-gated exploration in a subsequent step with actual hazards.

4. Is RANDOM-OPS at the same moments a fair control, and is PAD worth an arm 

RANDOM-OPS at identical arbitration moments is a fair control (provided drop isn't spammed)  PAD (K   4 + 8 dummy ops) IS worth an arm here.

Reason: Unlike BV1 (where the brain couldn't emit operations), CW1's consequence model can select dummy actions. PAD tests whether untried-action exploration bonuses scale gracefully or drown out real affordances when 8 of 12 operations are dead ends. For RANDOM-OPS, ensure uniform sampling over valid non-move actions so it tests causal credit assignment rather than arbitration timing.

5. Should the consequence model include forgetting from the start, or keep plain counts 

Keep plain cumulative counts in CW1  test recency weighting (forgetting) in a dedicated non-stationary CW2.

Reason: Adding a decay/forgetting rate introduces a free tuning parameter (alpha) that isn't even exercised in stationary CW1 worlds—and worse, can cause the agent to forget A + B -> C if items spawn sparsely. Keep CW1 minimal and isolate mid-life revision (exponential moving average / leaky counts) in a follow-up where object meanings actually swap mid-life.

Overall Recommendation

Keep CW1's minimal world (2 item types, K   4 operations, normal step-tick cost, no pain-gating) and plain cumulative counts without forgetting. Define a crisp, safety-bounded arbitration gate (triggered only when an item is underfoot or held, and only when hunger/rest are above a critical survival floor), switch the primary endpoint from a ≥3 binary threshold to mean chain completions per life (LEARN - RANDOM-OPS), and retain PAD (K   12) alongside RANDOM-OPS and NO-MAKE to verify that exploration bonuses survive action-space bloat.

Confidence: 89%

### DeepSeek (confidence 80%)
(1) Arbitration: let the RM brain own movement  the consequence model intervenes only when the brain would take a non-move action (take/drop/use/operate), and only if its best table entry beats a pre-registered confidence threshold  otherwise default to no-op/stay. Log every intervention. This keeps the planner spatial and makes the model's contribution measurable.

(2) Yes: 2 kinds, K 4, one chain is right for a first difficulty, but require the chain to be found on fresh looks and report partial progress (take A, take B, join) separately. "3 completions in a life" is a reasonable found-and-used bar only if lives are long enough  also report completions per 1,000 steps and first-join latency so short lives don't hide success.

(3) Failed operations should cost the step, not health  poking should be pain-gated in CW1 (stop poking a kind whose pokes brought pain) so the model learns cheap-vs-costly probing. Otherwise CW1 rewards blind button-mashing.

(4) RANDOM-OPS at the same moments is fair and necessary  keep it. PAD is worth keeping only as a weak invariance check, not a primary arm, since dummy ops cannot reach the frozen mover and add little beyond SHUF.

(5) Keep plain counts for CW1 and test revision later, but add a cheap recency window as a secondary arm from the start—W3r's swap failure is a known risk, and CW1 should show whether forgetting is needed before step 3.

Overall: freeze CW1 with movement-only RM, thresholded non-move arbitration, partial-progress metrics, pain-gated poking, RANDOM-OPS primary, PAD secondary, plain counts primary plus recency arm.

Confidence: 80%.

### Grok (confidence 78%)
Answers

(1) Arbitration: the consequence model proposes only when the moving brain's top action is stay or when the agent is already holding something and the situation matches a high-value table entry. Otherwise the frozen mover decides. This keeps locomotion dominant and lets the new model specialise in the sparse, high-stakes hand/operate choices without fighting the mover on every step.

(2) One useful chain among K   4 and two kinds is the right minimal difficulty: sparse enough to be non-trivial, dense enough that random exploration can discover it within 3 000 steps. Three completions is a good primary reading—proof of both discovery and repeated voluntary use—provided secondary measures (first-join latency, dead-action rate) are also reported.

(3) Failed operations should cost a small fixed energy or time penalty (body physics, not a shaped reward). Poking should be pain-gated from the start: the body already has a pain channel  gating the poke reflex on it is consistent with the earlier design and prevents free "probe everything" behaviour.

(4) RANDOM-OPS at the identical decision moments is a fair and strong control  it isolates the value of the learned table. PAD is worth keeping: it tests whether the model is distracted by extra null actions and whether the adapter's numbering remains meaning-free under larger K.

(5) Start with plain counts. W3r already showed revision failure is a real problem  adding forgetting now confounds the first test of whether the consequence model can discover and exploit a chain at all. Test explicit recent-weighting or decay in a later dedicated revision study.

Overall recommendation
Run CW1 essentially as drafted, with the arbitration rule above, a small cost on failed ops, pain-gated poking, and plain counts. Keep all four arms. Primary and secondary measures are well-chosen for a first crafting-style interface test.

Confidence: 78 %

## Claude's check after round 1 (against the code and the draft)
- **GPT's delayed-credit point is the central design problem, and it is real.** Joining A and B changes only the hands;
  only using C changes energy. A consequence model that values each action by the energy change that immediately
  followed scores "join" at 0 after its first try (no untried bonus left), so it would not repeat it except by chance.
  The model must carry value through hand states: learn the transitions (held looks, action) -> next held looks and
  energy change, then value each action by the best energy reachable within a few steps from its next hand state (a
  small value iteration over hand states, the same idea as the moving brain's planner). This keeps "no written
  reward": only energy, propagated.
- **Gemini is right that the frozen mover is blind to the loose things**: W3r's memory writer records only wall, food
  and shelter, so the RM brain never walks to A or B on purpose; it only passes over them. Arbitration therefore needs
  affordance moments (something underfoot with a free hand; something held). DeepSeek's "when the brain would take a
  non-move action" cannot happen: the frozen brain's outputs are 4 moves and stay.
- **GPT read "C keeps" as reusable**: the draft meant C does not spoil or move until it is eaten; eating C uses it up.
  So each use of C needs a new join; to be stated plainly in the revision.
- **Agreed by all four:** 2 kinds and K = 4 are the right first difficulty; RANDOM-OPS needs the identical arbitration
  and opportunities (uniform over the legal non-move verbs); plain counts for CW1, forgetting tested in its own
  non-stationary study (DeepSeek also wants a recency arm as a secondary).
- **Still divided:** the primary measure (≥3 chains in a life: Grok, DeepSeek; mean completions per life: Gemini;
  discovery then repeated use, reproduction separate: GPT); pain-gated poking (DeepSeek, Grok yes; Gemini no until
  there are hazards; GPT only from real world consequences: CW1 has none, so it would be inert); a cost on failed
  operations (Grok small energy; the others time only); PAD as an arm (GPT, Gemini, Grok) or a secondary check
  (DeepSeek).
Round 2 was not run in this session (the session's context was nearly full); the revised draft takes the checked
points, and a round 2 on the still-divided points can run in a fresh session before sign-off.
