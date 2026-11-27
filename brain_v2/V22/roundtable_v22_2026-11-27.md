# V2-2 Goals round-table, 27 Nov 2026 — each answer is that model's opinion, not sign-off

Under the creator's sleep-mode autonomy. Question: `roundtable_round1_prompt.txt` (GPT, Gemini, DeepSeek; about 02:20
EST). Grok not asked (free limit). Reading note: `=`, `&`, `?`, `;` shown as spaces; replies read in chunks and joined
at their overlaps; Gemini's rendered formulas are given in words (W0, Ws, Wf, Wc, Wg, g, s).

## Round 1

### GPT (confidence 92%)
1. Adult fine-tuning or new childhood

Adult fine-tuning first. Zero-initialized weights preserve existing behavior at initialization, making this a clean architectural extension. A new childhood would introduce unnecessary retraining and confounds.

However, exact initial equivalence does not guarantee preservation after training. The no-loss gate remains essential.

2. Controls and sham

FT-NOGOAL and SHAM-GOAL are appropriate. Ensure identical training budgets, initialization and goal-activation opportunities.

Also, test GOAL with its goal input disabled after training. This reveals whether improvements depend on the new goal mechanism or simply improved general navigation.

3. Arbitration

Removing the floor is a useful preliminary test, but not sufficient evidence of learned arbitration. Genuine arbitration requires competing goals, changing urgency and opportunities to abandon unsuccessful pursuits.

Keep GOAL-NOFLOOR as a secondary arm. Conduct full arbitration separately.

4. Retirement margin

The 0.2-chain margin is reasonable provisionally, but needs justification relative to the carry reflex's absolute performance.

Retirement should require both non-inferior crafting performance and preserved survival. A learned mechanism that crafts equally well but causes more starvation is not an adequate replacement.

5. Set-point reward — the biggest concern

The current reward may provide insufficient incentive to pursue useful goals while fed. A goal layer supplies information, not motivation.

Keep the body's reward unchanged for this experiment. Measure goal pursuit separately across energy ranges and record whether successful crafting produces meaningful learning signals.

If GOAL fails because benefits above the set point are invisible to the learning rule, investigate motivation separately. Do not introduce a crafting-specific reward to rescue the experiment.

6. What could make success misleading

Goal selection remains external: The consequence model selects the destination. Success demonstrates learned goal pursuit, not autonomous goal generation.

Catastrophic forgetting: Improved crafting could conceal deteriorating navigation or survival abilities.

Station memorization: Evaluate on unseen layouts and independently shuffled looks.

Goal-strength leakage: Ensure goal intensity comes exclusively from experienced consequences, not hidden recipe knowledge.

Pilot overfitting: Exclude the two pilot seeds from confirmatory evaluation.

Overall recommendation

Proceed with adult fine-tuning, unchanged bodily rewards, the proposed controls and strict no-loss gates. Prioritize GOAL, FT-NOGOAL and SHAM-GOAL if cloud compute becomes limited.

One important distinction: V2-2 should establish learned pursuit of experience-derived goals, not yet independent motivation or executive control.

Confidence: 92%. Based on the supplied architecture and experimental results, without independent code inspection. The greatest uncertainty is whether the existing reward provides sufficient learning signal for goal pursuit while Bob is already fed.

### Gemini (confidence 90%)
1. Zero-initialised goal layer plus adult fine-tuning: a fair way to add a goal part, or a new childhood (~18 h per brain)

Zero-initialised goal channels plus adult fine-tuning is the right choice—do not run a new 18-hour childhood.

Reason: Because DriveVIN's value-iteration and policy layers already know how to route around walls toward positive reward peaks on the map, initializing the new goal weights (channel 6 in W0, Ws, Wf, Wc and Wg) at zero gives an exact behavioral identity at step 0 while allowing actor-critic gradients to immediately turn channel 6 into a local reward peak. Fine-tuning 16 seeds takes ~4 h per run instead of ~18 h, fitting cleanly inside your December 19–20 VM credit cutoff while directly testing adult plasticity. (Check the 2-seed pilot at 300k, 600k, and 1M steps to verify that Wg weights actually move.)

2. Are FT-NOGOAL and SHAM-GOAL the right control and sham

Yes—both are well-targeted, though SHAM-GOAL needs a careful reward-alignment check.

Reason: FT-NOGOAL isolates the effect of 1M extra actor-critic steps in CW2's environment from the goal input itself, preventing extra training time from masquerading as goal-following. SHAM-GOAL (feeding a distance-matched wrong tile into channel 6) tests whether the walker genuinely uses the spatial coordinates of the goal layer rather than just boosting movement speed whenever g>0. Note: during SHAM-GOAL fine-tuning, the critic/actor will naturally learn to ignore channel 6 because walking there yields zero reward—so SHAM-GOAL will likely converge to FT-NOGOAL, which is the exact behavior you want to confirm.

3. Is removing the floor for the goal pull (GOAL-NOFLOOR) enough as the arbitration test, or a separate study

Keep GOAL-NOFLOOR in V2-2 as a diagnostic sub-test, then run a dedicated arbitration study if it fails or shows survival loss.

Reason: Testing GOAL-NOFLOOR on the same 16 seeds costs only one extra arm and answers whether Wg and Ws naturally balance each other through learned weights (g * Wg vs. s * Ws) without a hard-coded survival floor. However, because CW2's food supply is abundant (as CW1/CW2 showed, survival stays ~0.85 even without crafting), CW2 rarely stresses starvation vs. goal pursuit—so passing GOAL-NOFLOOR here proves safe integration in mild worlds, not full executive arbitration under scarcity.

4. Is non-inferior within 0.2 chains a sensible retirement bar

Yes—-0.2 chains on the lower 95% bound is a reasonable and pragmatic retirement bar.

Reason: In CW2, the written carry reflex adds +0.63 chains/life over NO-GUIDE ([+0.43, +0.84]), whereas the unassisted food-layer bridge achieved only +0.11. Retaining at least ~70% of the reflex's gain (>  +0.43 over NO-GUIDE, i.e., within 0.2 chains of the reflex) while eliminating hard-coded pathfinding logic is a strong, clean threshold for retiring the written carry reflex—provided the no-loss gate (plain-land survival > -0.03 and Bob Profile parity) also passes.

5. The set-point reward (energy < 150 of 200): a problem for learning goals, and what to do without changing the body's law

Yes, it is a real bottleneck, and you can solve it cleanly without altering the body's energy law by gating g on the expected homeostatic value (energy deficit) rather than raw energy.

Reason: If the body only rewards energy gains below 150, eating C at energy   175 produces 0 TD error—teaching the critic that following the goal layer when well-fed yields zero reward, which suppresses Wg! Without touching the body's reward law, define the goal urgency scalar g to reflect the effective energy gain below the set point: e.g., scale g by the current hunger deficit s max(0,150−energy)/150 (or compute the consequence model's reachable value using effective energy below 150). That aligns the goal signal g with the body's actual reward law—and naturally suppresses goal chasing when Bob is already full (energy >  150), doing the survival-floor's job organically.

6. Anything that would make a positive result misleading

Three pitfalls to watch for in V2-2:

Spurious spatial heuristics ("walk to center/landmarks"): If FT-NOGOAL also jumps substantially over NO-GUIDE because the walker overfits to CW2's layout during 1M steps of fine-tuning, GOAL - FT-NOGOAL protects you—but verify on held-out station placements (>  5 steps away in novel quadrants) that Bob isn't just patrolling common station zones.

Catastrophic forgetting of shelter/sleep or starvation recovery: Fine-tuning purely on CW2 without parent guidance could erode rare edge-case reflexes (e.g., severe exhaustion recovery)  enforce the Bob Profile and unseen-world no-loss gate (> -0.03) strictly before retiring the carry reflex.

Dead g channel masked by W0 bias: Ensure that GOAL outperforms SHAM-GOAL at test time when the station's coordinates are swapped mid-episode or randomized per test land, proving channel 6's spatial peak—not just scalar g—drives navigation.

Overall Recommendation

Proceed with zero-initialised goal channels + adult fine-tuning (capped by your 2-seed pilot up to 1M steps), keeping FT-NOGOAL, SHAM-GOAL, and GOAL-NOFLOOR alongside GOAL. Most importantly, align the goal drive scalar g with the body's 150 energy set-point (scaling g by effective energy below 150) so the critic sees consistent positive reward whenever g>0 and never learns to ignore the goal channel when Bob is already fed. Hold the -0.2 chain retirement bar and the -0.03 Bob Profile / unseen-world no-loss gates strictly.

Confidence: 90%

### DeepSeek (confidence 80%)
(1) Zero-init + adult fine-tuning is a fair first test, not a childhood: starting at exact zero makes it a controlled addition and keeps the 4 h budget. But 1M steps may be too little for new channels to grow from zero  use the 2-seed pilot to set length, and pre-register a fallback to a longer run only if the pilot shows the goal weights moving. A full childhood is a later option, not now.

(2) FT-NOGOAL is the right control for extra training  SHAM-GOAL is the right sham for place specificity. Add one more: GOAL with the goal layer live but the consequence model’s value shuffled across moments, to separate “goal signal” from “more input.” Keep all three.

(3) Removing the floor is not enough as an arbitration test—it only tests one override. Keep it as a named sub-test here, and make learned arbitration its own study  do not let V2-2 carry both.

(4) Non-inferior within 0.2 chains is too loose given CW2’s reflex effect was +0.63  a learned goal that is 0.2 chains worse is a real loss. Tighten to −0.1 chains on the lower bound, or require non-inferiority on chains and no Bob Profile loss. Pre-register either, but 0.2 invites retiring a better reflex.

(5) Yes: the set-point reward means a C meal eaten when fed gives little learning signal, exactly the goal case. Without changing the body’s law, do not retune the drive  instead report goal learning separately for hungry vs fed states, and use the consequence model’s experienced value (already energy-based) as the goal pull—not the drive reward. If that fails, the set point is a body-law question for the creator, not a V2-2 tweak.

(6) Misleading if: gains vanish under the shuffled-goal control  the goal layer merely re-encodes hunger  survival drops but chains rise  fine-tuning alone (FT-NOGOAL) closes most of the gap  or the unseen world shows no transfer. Also misleading if the pilot-set training length is chosen after seeing GOAL results.

Recommendation: run V2-2 as drafted with the extra shuffled-goal arm, pilot-set length, tighter retirement bar (−0.1 chains plus Bob Profile), arbitration deferred to its own study, and the set-point issue reported as a body-law caveat. Confidence: 80%.

## Claude's check and the summary
| point | GPT | Gemini | DeepSeek | into the plan |
|---|---|---|---|---|
| zero-init + adult fine-tuning | yes | yes | yes | **yes** (all) |
| controls | + goal input disabled at test | SHAM may converge to FT-NOGOAL | + a shuffled-value arm | **+ GOAL-ABLATE at test (GPT); the shuffled-value arm not added** (SHAM-GOAL tests the place, ABLATE tests reliance on the goal input; compute) |
| arbitration | secondary arm; full study separate | diagnostic sub-test | named sub-test; own study | **GOAL-NOFLOOR kept as a diagnostic; learned arbitration becomes its own later study** |
| retirement bar | −0.2 plus survival kept | −0.2 plus gates | −0.1, or −0.2 plus Bob Profile | **−0.2 chains AND survival no-loss AND Bob Profile no-loss** (DeepSeek's second option, GPT's survival condition) |
| set-point reward | keep; report by energy | scale g by the hunger deficit | keep; report hungry vs fed | **g stays value-based (2 of 3); goal pursuit reported by energy band; Gemini's scaled g is the fallback study if GOAL fails** |
| pilot | exclude pilot seeds | check Wg at 300k/600k/1M | length fixed before GOAL results | **the length rule fixed now, blind to chains; the primary also reported without seeds 1-2** |
Check against the code: Gemini's "scale g by the hunger deficit" would make the goal pull vanish whenever Bob is fed,
which is CW2's food-layer weakness again; it stays a fallback. DriveVIN's update (brains3.update) and the actor-critic
return use the drive reward only, so no new reward is needed (all three agree). Round 2 not run: every split was
settled by a majority with a reason that survived the check.
