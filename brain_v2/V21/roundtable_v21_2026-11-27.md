# V2-1 Revise round-table, 27 Nov 2026 — each answer is that model's opinion, not sign-off

Under the creator's sleep-mode autonomy. Question: `roundtable_round1_prompt.txt` (identical to GPT, Gemini, DeepSeek;
about 01:35 EST). Grok: not asked (its free limit was reached earlier the same night; nothing bought). Reading note: `=`,
`&`, `?`, `;` shown as spaces (browser tool); ">= " therefore reads ">  "; replies read in chunks and joined at their
overlaps.

## Round 1

### GPT (confidence 92%)
1. Revision rule

Reset the whole colour to unknown on confident contradiction. Decaying counts by 0.25 preserves unsupported predictions, while revising only the contradicted consequence leaves other potentially obsolete meanings intact.

However, distinguish unknown from known false. Zero counts should represent uncertainty, not certainty that a consequence cannot occur.

Keep partial decay as a comparison arm if compute permits.

2. Fixed thresholds

Reasonable starting values, but three trials provide weak evidence of confidence. Three consistent observations can occur by chance.

Keep the proposed numbers frozen, but measure:

False resets on stable lands.

Number of observations needed to recover after the swap.

Repeated resets caused by noisy outcomes.

The WINDOW half-life of approximately 14 observations is reasonable, but remember that observations are not equivalent to elapsed time.

3. Primary measure

Yes. Swap survival is the correct functional primary, with stable survival as the no-loss gate.

However, directly measure recovery of colour meanings as a key secondary. Improved survival alone does not establish successful revision.

4. Test B

Keep it within V2-1 as a separate, prespecified secondary experiment. Demonstrating revision across perception and action consequences is stronger evidence of a general learning mechanism than success in either domain alone.

Do not require identical effect sizes across the two environments.

5. What could make a positive result misleading 

Reflex assistance: The hunger reflex may supply corrective experiences that the learned planner could not independently discover.

Reset rather than revision: Bob might survive by abandoning incorrect beliefs without acquiring correct replacements.

Deterministic environments: Aggressive resets may work under abrupt swaps but fail under noisy or probabilistic consequences.

SHAM imbalance: Randomly resetting another colour may destroy more useful knowledge than resetting the contradicted colour, artificially favoring SURPRISE.

Overall recommendation

Use whole-colour reset as the primary revision mechanism, with PLAIN, WINDOW and SHAM controls. Include partial decay if affordable. Measure forgetting incorrect meanings, acquiring correct replacements and retaining unaffected knowledge separately.

Most importantly, audit how much recovery depends on the written hunger reflex.

Confidence: 92%. Based on the supplied design and Claude's code findings, not independent implementation inspection.

The scientific milestone should be that Bob can recognize when his knowledge is wrong, discard it, and learn what is true now.

### Gemini (confidence 91%)
1. Which revision rule: keep-0.25 of the whole colour, reset the whole colour to unknown, or decay only the contradicted consequence 

Reset the whole colour (or key) toward unknown (zeroing counts or decaying both numerator and denominator to 0) on a verified surprise.

Reason: Claude's code check exposes a fatal flaw in proportional scaling (× 0.25): because pos / (pos + neg) is scale-invariant, multiplying counts by 0.25 preserves the old fed   1.0 prediction on the old food colour (now a wall) forever, since Bob cannot step onto walls to generate fed   0 trials. Decaying only the contradicted consequence (blocked) still leaves the old food colour marked as edible in the food layer! Resetting the whole colour's counts to 0 (unknown) on a high-confidence contradiction immediately clears both the stale fed belief and the stale passability belief, letting fresh evidence rebuild the entry cleanly. (For CW1's categorical hand-transition table, resetting that (situation, verb) key's transition counts to 0 accomplishes the same clean slate.)

2. Are n >  3, |y - p| >  0.75, and the window 0.95 sensible as fixed numbers 

Yes—they are well-calibrated for deterministic/near-deterministic gridworlds.

Reason: Requiring n >  3 prevents premature resets from single noisy or edge-case trials during early exploration. Setting |y - p| >  0.75 triggers only when a high-confidence belief (p >  0.75 or p <  0.25) is sharply contradicted (y   0 or 1), avoiding false resets in mildly stochastic transitions. Likewise, a 0.95 sliding window (~14-event half-life) gives WINDOW a fair, standard recency baseline against which to test whether surprise-gating avoids stationary forgetting.

3. Is swap survival the right primary with stable survival as the no-loss gate 

Yes—this pairing directly captures the core trade-off of non-stationary learning.

Reason: Swap survival (SURPRISE - PLAIN) directly tests whether Bob recovers from mid-life environmental shifts, while the stable-land no-loss gate (lower bound > -0.03) ensures surprise-gating does not induce destructive "belief thrashing" in stationary environments (where WINDOW typically pays an exploration tax). Keep SHAM-SURPRISE as a mandatory mechanistic secondary to prove recovery comes from targeted revision of the contradicted colour rather than random table resets.

4. Test B in the same study or its own 

Include Test B in the same study as a co-primary or key secondary benchmark (since both are zero-retraining, fast test-time evaluations).

Reason: Because V2-1 requires zero neural retraining and runs purely on existing frozen brains, running Test A (W3r colour-meaning swap) and Test B (CW1 mid-life operation swap) together costs minimal compute and immediately verifies that the revision rule generalizes across two distinct tabular schemas (per-colour consequence rates vs. (situation, verb) -> next_hand transitions) before locking Brain v2's memory module.

5. What would make a positive result misleading 

Three specific failure modes could produce a misleading positive result:

Reflex-carried survival without map revision: Because Bob's written hunger reflex walks to remembered food coordinates on the true map, Bob could survive after a colour swap even if the old food colour remains falsely labeled as food—making post-swap colour-table accuracy and post-swap foraging path efficiency essential diagnostics alongside raw survival.

Single-trial noise sensitivity: If any stochastic edge case (e.g., full-energy meal capping or bump-into-moving-entity) triggers false |y - p| >  0.75 resets in stationary worlds, a high survival score might hide erratic memory wiping  check stationary reset rate (should be near zero).

Overfitting to a single swap time (step 1,500): Confirm that post-swap recovery holds across varied swap steps (or multiple swaps), not just when the pre-swap count table happens to hit a specific count magnitude.

Overall Recommendation

Adopt full colour/key reset to unknown (counts   0) upon a high-confidence contradiction (n >  3, |y - p| >  0.75)—rejecting proportional 0.25 scaling so stale fed predictions on new walls are immediately erased. Run Test A (W3r swap) and Test B (CW1 operation swap) together in V2-1 with SURPRISE, PLAIN, WINDOW (0.95), and SHAM-SURPRISE, using swap survival as primary, stable-land survival (> -0.03) as the no-loss gate, and post-swap table accuracy + stationary reset rate as sanity checks against reflex-carried survival.

Confidence: 91%

### DeepSeek (confidence 82%)
(1) Decay only the contradicted consequence, plus reset that consequence toward unknown (counts to 0) on a confident contradiction. Claude’s check is decisive: keep-0.25 preserves the ratio, and the old-food colour cannot collect new fed evidence on walls, so whole-colour decay revises only blocked. Zeroing the contradicted consequence is the honest “unknown” the body can actually test.

(2) n≥3 is sensible  |y−p|≥0.75 is too strict for binary outcomes where p is near 0 or 1 and fine otherwise—pre-register it, but expect few triggers. Window 0.95 (half-life ~14) is reasonable as a comparison arm, not the primary  keep both fixed.

(3) Yes: swap survival primary, stable survival no-loss gate, both paired and pre-registered. Add swap recovery latency as a secondary.

(4) Test B in its own study—CW1’s join change is a different table and would confound attribution.

(5) Misleading if: stable-land no-loss fails, the SHAM-SURPRISE matches SURPRISE, gains come only from the hunger reflex’s map memory, or recovery is measured on colours Bob never re-tests. Also misleading if the result depends on a threshold tuned after seeing data.

Recommendation: SURPRISE   contradicted-consequence decay to unknown  PLAIN primary comparison  SHAM at same moments  Test B separate. Confidence: 82%.

## Claude's check and the summary
- **The rule:** GPT and Gemini: reset the whole colour (or key) to unknown. DeepSeek: reset only the contradicted
  consequence. Checked against the swap: the contradiction that arrives for the OLD food colour is "blocked" (Bob bumps
  into what are now walls); resetting only "blocked" leaves its "fed" at its old value, so the walker's food layer keeps
  marking walls as food (Gemini's point). DeepSeek's reasoning ("whole-colour decay revises only blocked") holds for the
  0.25 scaling, not for a reset to 0. **Adopted: whole-colour (whole-key) reset to unknown.** In W3r's table "unknown"
  already reads as 0 in every layer (prediction 0 before any fair trial), which is "no evidence", not "known false"
  (GPT's caution; recorded as a limit: the walker cannot tell the two apart).
- **Numbers:** kept as drafted (all three); a stationary false-reset rate is added as a measure (GPT, Gemini).
- **Primary:** swap survival SURPRISE − PLAIN, no-loss on stable lands (all three); added: post-swap table accuracy
  (meaning recovery), recovery latency, and **the hunger reflex's share of post-swap meals** (all three warned that the
  written hunger reflex, which walks to remembered food by the true map, may carry the recovery).
- **Test B:** in V2-1 as a prespecified secondary (GPT, Gemini; DeepSeek wanted its own study).
- **Partial decay (0.25) as an extra arm (GPT, "if affordable"):** not added: it cannot revise "fed" on walls by
  construction (the check), so it would only show a known failure.
- **Gemini's "vary the swap time":** recorded as a limit (one swap time, as W3r).
- Round 2 not run: the one real split (the rule) is decided by a code check that all three accepted in round 1.
