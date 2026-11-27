# V2-3 round-table, 28 Nov 2026 — each answer is that model's opinion, not sign-off

Under the creator's sleep-mode autonomy. Question: the round-1 paragraph (same text to GPT, Gemini, DeepSeek; about
02:10 EST); Grok at its free limit, not asked. Reading note: `=`, `&`, `?`, `;` shown as spaces; Gemini's rendered
symbols given in words (Ws, Wc, W0, Wf).

## Round 1

### GPT (confidence 94%)
1. Is B a good new world

Potentially, but verify learnability before freezing. Slower food regeneration may simply reduce available resources rather than create a problem that better decisions can solve.

Run a small independent pilot to establish that adaptation can improve survival. If not, consider changing food distribution or regeneration patterns, where learning better navigation strategies could provide a measurable advantage.

2. Protection mechanisms

ANCHOR and REHEARSE are appropriate first candidates. They represent two fundamentally different approaches: protecting important parameters and maintaining skills through experience.

However, REHEARSE receives fewer B experiences if every other life occurs in A. Match B exposure across arms and report total computational cost separately.

Defer larger brains, replay buffers and parental teaching. First establish whether these two simple protections work.

3. Primary and controls

The two-part primary is correct: new knowledge gained AND old knowledge preserved.

However, also require a direct comparison against FREE to establish that protection actually reduces forgetting.

Keep SLOW. It helps distinguish genuine protection from simply reducing the amount of learning. Report B improvement alongside home retention, since a method that prevents all learning would trivially prevent forgetting.

4. Training duration

Use 1M B steps initially, matching V2-2, with prespecified evaluations at 0, 250k, 500k and 1M steps.

These intermediate evaluations reveal whether forgetting accumulates gradually or occurs early. Do not select the best checkpoint retrospectively as the primary result.

5. What could make success misleading

Reflex masking: Written hunger and sleep reflexes could preserve survival despite deterioration in the learned brain.

Weak adaptation challenge: B may require little genuinely new learning.

Importance estimation: Squared policy gradients may underestimate parameters important for rarely encountered situations.

Unequal experience: REHEARSE may benefit from additional training rather than its protection mechanism specifically.

Temporary retention: Preserving skills for 1M steps does not establish lifelong stability.

Statistical uncertainty: With 16 brains and multiple no-loss probes, an inconclusive result must not automatically be interpreted as forgetting.

Overall recommendation

Proceed with ANCHOR, REHEARSE, FREE, SLOW and FROZEN after confirming that B is learnable. Match B exposure, report total training cost, and evaluate all arms on held-out lands.

Do not introduce brain growth yet. First determine whether Bob's existing capacity can accommodate new knowledge without sacrificing old abilities.

Confidence: 94%. Based on the supplied experimental design, not independent code inspection.

The milestone is not merely that Bob remembers his childhood. It is that Bob can continue learning without destroying what his childhood taught him.

### Gemini (confidence 91%)
1. Is food twice as slow a good new world, or should B be different (it must be one where learning can help)

Food regrowing twice as slowly is a risky choice for B unless a pilot confirms FREE actually improves over FROZEN there.

Reason: Slowing food regrowth lowers the survival ceiling in B, which is fine only if the walker can adapt its foraging urgency (Ws) or exploration (Wc) to survive measurably better than FROZEN. If FROZEN is already near the physical survival limit of scarce B lands—or if FREE gains nothing in B—then ANCHOR and REHEARSE cannot demonstrate plasticity without forgetting. Run a quick 2-seed pilot (FROZEN vs. FREE on B) first  if FREE - FROZEN is less than +0.08 survival, switch B to an environment where policy adaptation yields a clear margin (such as higher basal energy burn or a shifted hunger/tiredness trade-off).

2. Are ANCHOR and REHEARSE the right first protections  anything missing (a larger fixed brain, a replay buffer of old states, a parent present)

ANCHOR and REHEARSE are the right first pair, and you should add a lightweight experience-replay buffer (REPLAY) while excluding parent supervision and architecture growth.

Reason: ANCHOR (diagonal Fisher EWC) tests synaptic consolidation without extra data, while REHEARSE tests interleaved environment revisits. However, REHEARSE requires physically re-entering world A (which does not exist in single-world deployment), whereas storing a tiny reservoir buffer of past (map, drives, action, return) transitions from A and mixing them into B's actor-critic updates (REPLAY) tests internal consolidation without changing the world schedule. Keep the parent absent (adult learning must be autonomous) and keep network size fixed.

3. Is the two-part primary right, and is SLOW the right control

Yes to both.

Reason: Requiring both a statistically significant survival gain in B (arm - FROZEN) and strict retention at home (Bob Profile lower bound > -0.05 and home survival > -0.03) prevents a degenerate solution where an arm passes merely by refusing to learn. SLOW (0.1x learning rate) is an essential control because it isolates selective protection (ANCHOR / REPLAY) from uniform under-training—proving the brain is protecting home-critical weights rather than simply moving too slowly to forget.

4. How long should adult learning run, given V2-2's 1M steps

Run 300k–500k steps (with checkpoints every 100k), rather than a full 1M steps.

Reason: DriveVIN only adapts low-dimensional reward weights (W0, Ws, Wf, Wc) and a small value-iteration/policy head  in V2-2, 1M steps already caused measurable Bob Profile drift (-0.07 to -0.11). Stopping at 500k steps (and logging curves at 100k, 200k, 300k, 500k) cuts VM compute in half while capturing the exact stability–plasticity knee before critic noise erodes rare probe skills.

5. What would make a positive result misleading

Three failure modes could invalidate a seemingly positive outcome:

Uniform under-plasticity: If SLOW also passes both criteria, ANCHOR has not demonstrated selective consolidation—only a lower effective step size.

No true adaptation in B: If FREE fails to beat FROZEN in B by a meaningful margin, any arm that barely updates weights wins by default.

Probe-blind drift: If an arm preserves the specific Bob Profile probes (A5s, R2) and easy home lands while degrading on rare edge cases (e.g., simultaneous starvation and exhaustion), test on a held-out stressed home split alongside the Bob Profile.

Overall Recommendation

Verify via a 2-seed pilot that FREE beats FROZEN on B (2x slower food regrowth, or higher metabolic cost if regrowth hits a hard ceiling) before launching all 16 seeds. Run FROZEN, FREE, SLOW (0.1x lr), ANCHOR (EWC), and REPLAY (reservoir replay of home transitions, or REHEARSE if environment interleaving is preferred) for 500k steps (saving 100k checkpoints). Keep the two-part primary (gain in B + Bob Profile > -0.05 and home survival > -0.03 no-loss gates), and require the winning method to beat SLOW on the B-gain vs. home-retention frontier.

Confidence: 91%

### DeepSeek (confidence 81%)
(1) Food twice as slow is a fair first B, but weak: it is one number and the same rules, so FREE may adapt quickly and all arms may look alike. Better B: same rules, slower regrowth plus a moved shelter or a new look for food, so learning must change what the walker attends to, not just how long it waits. Pre-register B now  do not change it after seeing arms.

(2) ANCHOR and REHEARSE are the right first pair. Missing: a small replay buffer of home states with their old policy outputs (cheap, no parent), and a larger-fixed-brain arm as the capacity control the roadmap already agreed. The parent present is not needed and would confound—this is the brain’s own experience.

(3) Two-part primary is right: gain in B and no loss at home, both needed. SLOW is the right control for learning less, but add FT-NOGOAL-style “same steps in A only” to separate B-specific gain from generic fine-tuning drift. Also pre-register the Bob Profile margin (−0.05) before data, not after.

(4) Use the V2-2 length (1M) as the default and set the pilot on 2 seeds  do not shorten to make results kinder. If FREE does not gain in B at 1M, that is a finding, not a reason to extend only FREE.

(5) Misleading if: gain in B comes only from SLOW-like reduction  home no-loss passes because the Bob Profile is too easy  REHEARSE wins by spending half its lives in A (report compute-matched FREE)  ANCHOR wins by freezing everything (check it still gains in B)  or B’s gain does not transfer to a held-out C. Also misleading if the B choice or margins are set after arm results.

Recommendation: run as drafted, with a harder B (slower regrowth plus one structural change), replay-buffer and larger-fixed-brain arms added, SLOW plus A-only fine-tuning controls, pilot-set 1M steps, margins pre-registered. Confidence: 81%.

## Summary and what goes into the plan
| point | GPT | Gemini | DeepSeek | into the plan |
|---|---|---|---|---|
| B | pilot first: is it learnable? | pilot: FREE − FROZEN ≥ +0.08 or switch | harder: + one structural change | **a 2-seed pilot decides B by a rule fixed now** (below) |
| protections | ANCHOR, REHEARSE | + REPLAY (home transitions mixed into updates) | + REPLAY, + larger fixed brain | **ANCHOR, REHEARSE, REPLAY**; larger brain later (GPT, Gemini) |
| controls | SLOW; compare to FREE; match B exposure | SLOW; must beat SLOW | SLOW; + A-only fine-tuning; compute-matched FREE | **SLOW; REHEARSE gets the same B steps as the others (its home lives are extra, reported)** |
| length | 1M, evaluated at 250k/500k/1M (no picking) | 300-500k | 1M | **1M** (2 of 3), with snapshots at 250k and 500k reported as secondaries, never as the primary |
| primary | gain in B AND no home loss | same, + beat SLOW | same | **same; the Bob Profile margin −0.05 fixed now** |
Round 2 not run: the open points have a majority or are settled by a pre-registered pilot rule.
