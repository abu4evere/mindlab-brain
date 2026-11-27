# CW2 round-table (Body v1 step 3, a station), 26-27 Nov 2026 — each answer is that model's opinion, not sign-off

The creator (email, 26 Nov): "Yes, please!" to drafting CW2. Question: `roundtable_round1_prompt.txt` (identical text
to all four, sent about 23:35 EST 26 Nov). Where: GPT = the creator's main ChatGPT chat (Instant mode); Gemini = "Body
v1 Test Evaluation"; DeepSeek = "Bob Body v1 council round 1"; Grok = "ACL and Mind Lab Research Briefing for Grok"
(Fast mode). Reading note: Gemini, DeepSeek and Grok were read with `=`, `&`, `?`, `;` shown as spaces (the browser
tool withholds them); GPT from the page text. Gemini's reply ended with an embedded video card (a Crafter talk),
left out.

## Round 1

### GPT (confidence 93%)
1. Guidance through the food layer

Acceptable as a temporary compatibility mechanism, but not as a permanent architecture. The destination is learned rather than programmed, so it is not directly a written reward. However, representing a station as food conflates two different meanings.

A cleaner approach without retraining is a temporary goal-map overlay derived from predicted energy benefits. Keep actual food memory separate, and ensure guidance cannot override urgent survival needs.

Also, the model must discover the station's usefulness through experience before guiding toward it. No privileged station identification.

2. Station rules

One station, exact cell. This isolates spatial dependency without introducing unnecessary complexity. Two stations would introduce destination selection, while adjacency adds interaction geometry. Both can come later.

3. Primary and controls

GUIDE − NO-GUIDE is the correct primary. Keep SHAM-GUIDE, but match destination distance, reachability and guidance duration where possible. Otherwise, random destinations could simply be more expensive to reach.

Also measure the time between the first successful join and subsequent intentional station visits. This distinguishes accidental discovery from learned exploitation.

4. Should crafting matter more?

Keep food availability and C's energy benefit unchanged. CW2 should answer whether Bob can connect learned action consequences to spatial planning, not whether crafting improves survival.

Test ecological necessity separately. Changing both the environment's difficulty and the planning mechanism would complicate interpretation.

5. Dependent recipes

Keep one recipe. CW2 introduces spatial planning; CW3 should introduce recipe dependencies. Combining them now would make failures harder to diagnose.

Overall recommendation: Proceed with CW2 after addressing three concerns:

Keep learned destinations separate from genuine food memory.

Ensure guidance emerges exclusively from experienced consequences.

Verify that holding objects does not cause repeated non-move actions that prevent the walker from reaching the station.

The important milestone is not simply making more C. It is whether Bob can discover that something useful happens somewhere and later deliberately return there to reproduce it.

Confidence: 93%. This is a design-level assessment; I have not inspected the implementation.

### Gemini (confidence 91%)
1. Guiding through the walker's food layer: fair bridge or smuggling a reward 

It is a fair architectural bridge for a frozen-walker test, provided the injection is strictly gated by the consequence model's own discovered energy value—not hard-coded station labels.

Reason: Because the walker is frozen and lacks an arbitrary goal-waypoint input channel, its food map layer is simply its learned spatial representation of "places that yield energy." Writing a station cell into that layer only after the consequence model independently discovers that (held A+B, station_look) -> C -> +energy does not smuggle in a written reward  it translates a learned symbolic subgoal into the spatial planner's native interface. To keep it clean without retraining the walker, inject the virtual food marker into a read-only copy of the map fed to the planner (leaving the walker's persistent memory untouched) and clear it immediately once the join completes.

2. Station rule: on the cell or within 1 step  one station or two 

Require standing directly on the station cell, and use one station (with a second non-functional "distractor" fixed look if needed, or keep 1 station + 4 operations).

Reason: Standing directly on the station keeps CW2's place-memory rule (look felt underfoot) completely consistent with CW1's item-underfoot rule—no adjacency sensors or facing-direction mechanics needed. One functional station is enough to test spatial routing (remember where look X was felt -> go there when holding A+B)  adding a second functional station just splits memory without testing a new capability, whereas adding a single non-functional landmark look (or keeping K   4 operations) already prevents trivial "walk to the only special tile" shortcuts.

3. Are GUIDE - NO-GUIDE (primary) and SHAM-GUIDE (control) the right endpoints 

Yes—both are well-chosen, though GUIDE - SHAM-GUIDE should be co-primary or tightly paired alongside GUIDE - NO-GUIDE.

Reason: GUIDE - NO-GUIDE measures the total value of spatial planning over random walk-by encounters, while GUIDE - SHAM-GUIDE isolates place-memory accuracy from mere movement disruption (proving Bob navigates to the right remembered tile rather than just breaking out of loops). Keep mean chains per life (GUIDE - NO-GUIDE) as primary, and elevate GUIDE - SHAM-GUIDE and carrying time (steps from holding A+B to join) as the key mechanistic secondaries.

4. Keep the world as is, or make C matter more to lengthen lives 

Keep the world's food/energy parameters identical to CW1 for CW2.

Reason: CW2 is specifically testing spatial credit assignment and planner-to-consequence coupling (can the consequence model direct the walker to a remembered tool/station location ). Changing food scarcity or meal size between CW1 and CW2 introduces a survival confound and breaks direct baseline comparison against CW1's 5.73 chains/life benchmark. Test survival-critical crafting pressure in a separate stress-test arm or CW3 once spatial routing works.

5. Add a second, dependent recipe now (wood -> table -> pickaxe), or defer to CW3 

Keep one recipe (A + B at station -> C) in CW2 and defer multi-step dependency chains to CW3.

Reason: Multi-step tool dependencies (like Crafter's hierarchical tech tree) simultaneously stress multi-hop value propagation, inventory capacity (2 hands holding intermediate tools), and sequential subgoal routing. Isolating single-station spatial guidance first ensures that if CW2 underperforms, you know immediately whether the bottleneck is place-memory lookup or planner override—not multi-hop credit decay.

Overall Recommendation

Keep CW2 tightly scoped as a clean spatial-routing test on the exact CW1 world: one station (activated underfoot), one recipe (A + B -> C), and virtual food-layer injection fed into a non-persistent planner input copy only after the consequence model discovers the station's energy path (and only above the survival floor). Keep mean chains per life (GUIDE - NO-GUIDE) as primary, pair it closely with SHAM-GUIDE and carrying time to verify true place-memory lookup, and save multi-step Crafter-style dependency chains and food-scarcity pressure for CW3.

Confidence: 91%

### DeepSeek (confidence 81%)
(1) Fair, with a caveat: marking the walker’s food layer is not a written reward, but it does reuse the walker’s eating drive to steer, so GUIDE can win by making Bob hungry near the station. Cleaner without retraining: write a neutral “expected-value place” layer the frozen walker ignores, and instead bias only the model’s affordance-time non-move choice plus a small deterministic move-preference override when the model’s best hand-value path needs a remembered look. If you keep the food-layer route, log every mark and run a sham that marks a random remembered look cell—already drafted—so any gain is place-specific, not drive-specific.

(2) Station: on the cell only. Within-1-step adds a hidden auto-targeting rule the adapter audit would have to chase  keep the body simple. One station for CW2  two stations as a later invariance check.

(3) Yes: GUIDE − NO-GUIDE is the right primary, and SHAM-GUIDE is the right control, but add a third control, GUIDE-FOOD-MARKED at the same moments on a random non-station look, to separate “marked cell” from “food layer salience.”

(4) Keep the world as is for CW2. The question is learning a place, and changing food density would confound it with a survival effect. Note explicitly that CW1 showed no lifespan gain and do not re-read CW2 survival as a learning result.

(5) Keep one recipe  add the dependent recipe in CW3. CW2 already adds station, place memory, and guidance—stacking a second recipe now would make a negative result uninterpretable.

Overall: freeze CW2 with on-cell station, GUIDE/NO-GUIDE/SHAM-GUIDE/RANDOM-OPS, plus a food-layer-salience control  one recipe  report survival as a cost check only. Confidence: 81%.

### Grok (confidence 76%)
Answers

(1) Guiding through the food layer is convenient but impure: it re-uses the walker’s existing hunger drive, so success partly reflects “I marked it as food” rather than pure place value. Cleaner without retraining: add a distinct, lower-priority “attractor” layer the frozen planner already consults (or a temporary boost that decays). If that is impossible, food-layer marking is acceptable for this first test provided SHAM-GUIDE quantifies the smuggling.

(2) Strictly on the station cell (not within 1). One station. Precision of place memory is the point  radius or multiple stations add noise before the basic link is proven.

(3) Yes. GUIDE – NO-GUIDE is the direct test of the new link. SHAM-GUIDE is the correct control for specificity of the marked place.

(4) Keep the world unchanged. Survival was never the claim in CW1  altering food density between studies breaks comparability. Measure carrying time and chains  survival is secondary only.

(5) Keep one recipe. A second dependent recipe belongs in CW3 once station guidance is shown to work. Stacking complexity now confounds the place-learning result.

Overall recommendation
Run CW2 largely as drafted: one station, on-cell only, food-layer guidance (with the impurity noted), GUIDE vs NO-GUIDE primary, SHAM and RANDOM-OPS controls, world unchanged. Accept the pragmatic link  clean it later if needed.

Confidence: 76 %

## Claude's check after round 1 (against the code)
- **Agreed by all four:** one station, the exact cell; the world unchanged (food and meal sizes: CW2 asks about a place,
  not survival); one recipe now, dependent recipes in CW3; GUIDE − NO-GUIDE as the primary; SHAM-GUIDE kept; survival
  a cost check only. Gemini's "a copy fed to the planner, memory untouched" and "clear the mark once the join
  completes" fit the draft.
- **Grok's "a distinct attractor layer the frozen planner already consults" does not exist:** the walker's planner
  (`workbench/W3/brains3.py`) reads exactly five layers (wall, unseen, food, shelter, staleness) through learned
  weights: r = W0·map + s·Ws·map + f·Wf·map + c·Wc·map. Without retraining, the only learned pull toward a place is
  the food layer.
- **New check: the food layer pulls weakly when Bob is well fed.** For RMS seed 1, a food cell's learned reward weight
  is 0.217 (W0) + 1.356 × hunger deficit − 0.338 × tiredness, where the deficit is max(0, 150 − energy)/150. Above
  energy 150 (of 200) only 0.217 is left; at the survival floor (energy 100) about 0.67. So guidance through the food
  layer may be weakest exactly when it is allowed (above the floor). This is DeepSeek's and Grok's point from the
  other side.
- **DeepSeek's alternative (a move override toward the remembered place) has a precedent in the body:** the walker
  already has two reflexes that walk by shortest path on its remembered map (the sleep reflex to the shelter, the
  hunger reflex to remembered food: `workbench/W3m`, `W3n`). A "carry reflex" (walk to the remembered place the
  model's value runs through, only above the floor) would be the same kind of written route-following with a learned
  goal.
- **GPT's concern (holding things causes repeated non-move actions)** is real in principle: in CW1 the model acts at
  every affordance moment until "pass" wins, and with operations keyed by the look underfoot each new look is a new
  situation to try. To be measured in the pilot (hand acts per carrying step) and reported.

## Round 2 (27 Nov 2026, sent about 00:05 EST)
Question: `roundtable_round2_prompt.txt` (identical text to all four; same chats). Same reading note as round 1.

### GPT (confidence 94%)
1. Steering: Keep both GUIDE-MAP and GUIDE-REFLEX, with GUIDE-MAP − NO-GUIDE as primary. I disagree with DeepSeek's reflex-only approach: it bypasses the learned planner, whereas CW2 should test whether learned consequences can guide it. GUIDE-REFLEX provides a useful diagnostic if map guidance fails due to hunger-dependent weights.

2. Sham: One distance- and duration-matched sham per steering channel is sufficient. Match reachability and steering strength too. A separate food-salience control is redundant if the map sham applies identical food-layer modifications at matched destinations.

3. Comparison: Keep GUIDE − SHAM as a prespecified secondary, but require it to support any claim that learned destination selection matters beyond generic steering.

Final recommendation: Test both channels. Distinguish learned destination selection from programmed route execution. A successful carry reflex alone would not demonstrate successful integration with the learned planner.

Confidence: 94%, conditional on Claude's code findings.

### Gemini (confidence 91%)
Claude's code check (b) breaks my round-1 proposal: because the frozen planner weights the food layer by hunger deficit, food-layer reward drops to 0.217 above energy 150—weakest right when GUIDE is allowed to run. Relying solely on GUIDE-MAP risks a false negative from planner gain mismatch rather than consequence-model failure. However, running only DeepSeek's carry reflex bypasses testing the body plan's map-feeding interface.

Final Recommendation:

Steering channel: Run both GUIDE-MAP and GUIDE-REFLEX against NO-GUIDE. Make GUIDE-REFLEX - NO-GUIDE the primary endpoint (cleanly tests consequence-driven spatial routing without gain attenuation), and keep GUIDE-MAP - NO-GUIDE as a secondary diagnostic for the food-layer bridge.

Sham control: One distance- and duration-matched random remembered-place sham per active steering channel (SHAM-REFLEX, SHAM-MAP) is sufficient  skip DeepSeek's extra food-salience arm.

Sham placement: Named secondary alongside carrying time.

Confidence: 91%

### DeepSeek (confidence 80%)
Direct to Gemini: one distance-matched sham per channel is fine, but it does not separate “correct place” from “food-layer salience,” so DeepSeek’s salience control is not redundant.

Final: (1) Both channels as separate arms, GUIDE-MAP and GUIDE-REFLEX, each against NO-GUIDE  primary is GUIDE-REFLEX − NO-GUIDE because Claude’s check (b) shows food-layer guidance is weakest exactly when allowed, and the reflex is the body’s existing route-following kind, not a new written reward. GUIDE-MAP is a bridge, reported as secondary. (2) One distance-and-duration-matched sham per channel, plus DeepSeek’s food-salience control for GUIDE-MAP only  reflex sham matches path length and clear-on-join. (3) GUIDE − SHAM as a named secondary, not co-primary  keep the primary clean. Confidence: 80%.

### Grok
No answer: the page showed "Free tier limit reached ... upgrade". Nothing was bought (CLAUDE.md: never buy). Grok's
round-1 view stands: food-layer guidance acceptable for a first test with SHAM-GUIDE quantifying it; strictly on the
station cell; one station; the world unchanged; one recipe.

## Claude's check after round 2, and the summary (who argued what, what survived)
| point | GPT | Gemini | DeepSeek | Grok (round 1) | into the plan |
|---|---|---|---|---|---|
| steering arms | both | both | both | food layer | **both: GUIDE-REFLEX and GUIDE-MAP** |
| primary | MAP − NO-GUIDE | REFLEX − NO-GUIDE | REFLEX − NO-GUIDE | GUIDE − NO-GUIDE | **REFLEX − NO-GUIDE** (2 of 3), MAP − NO-GUIDE a named key secondary; the choice is flagged to the creator |
| sham | one per channel, matched | one per channel, matched | one per channel + a salience control | SHAM-GUIDE | **one matched sham per channel** |
| GUIDE − SHAM | secondary, needed for "destination matters" | secondary | secondary | – | **named secondary** |
- **DeepSeek's food-salience control is the map sham itself:** SHAM-MAP marks a remembered non-station place in the food
  layer at the same moments, which is exactly "a random non-station look marked as food". So no separate arm (GPT,
  Gemini).
- **GPT's dissent on the primary survives as a reading rule:** a REFLEX win shows that a learned consequence can choose
  a destination and that written route-following gets the things there; only a MAP win would show the learned
  consequence steering the learned planner. The findings must say which one held.
- Round 3 not needed: the open points have a majority with checked reasons; the primary is put to the creator.
