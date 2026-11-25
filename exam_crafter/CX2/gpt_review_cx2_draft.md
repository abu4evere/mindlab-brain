# Council on the CX2 draft (24 Nov 2026): GPT, Gemini, DeepSeek

Each answer is the model's OPINION, NOT sign-off. The same one-paragraph question went to each in a fresh chat.

## GPT (chatgpt.com, fresh chat), opinion, not sign-off
1. Worthwhile but not ready to freeze: it tests whether a hand-designed consequence learner can replace hand-assigned
   meanings; the table does the semantic learning, MBb consumes it.
2. Bump-and-poke is fair as a general reflex if it applies to every blocked kind with no exceptions; acknowledge it as
   an inductive bias; record whether the extra actions use Crafter steps.
3. Blocked and fed suffice for a narrow survival test. Blocked = traversability, not "wall". **Learn food and drink
   separately** (water is useless for hunger, cows for thirst). Document the shelter layer (sleep anywhere). Record
   damage as a separate consequence.
4. NAMED with the new hand is right but not enough: **RANDOM-5P must have its own learning table**, updated like LEARN.
5. **Delayed consequences (the biggest problem):** a cow needs several hits; the first hits become false negatives
   (a cow hunted every time could read 0.33 < 0.5 threshold): it would measure the estimator's failure, not the brain's.
6. **Moving entities:** attribute consequences to the target seen just before the action, not the remembered one.
7. Bump-and-poke only discovers useful things that block movement; suggests a general chance of interacting with any
   adjacent observed tile, independent of its kind.
8. **The estimator is overconfident** (one trial = 1.0 or 0.0): smooth it; tell untested from tested-useless.
9. **The negative-evidence rule is flawed:** drink full but food low -> water shows no rise, wrongly counted against
   water. Judge food and drink each only when that one can rise.
10. Trees (materials) and zombies (danger) fit neither food nor wall: restrict the claim to survival affordances.
11. Recompute the full Crafter score in every bootstrap resample; count real environment steps toward the budget.
12. Report discovery probability beside discovery time (lives that never discover included).
13. Freeze instead: LEARN (table, MBb), NAMED (fixed true meanings, MBb), RANDOM-5P (table, random), **BLIND
    (constant uninformative meanings, MBb)**; identical interaction rules; CX1 as history only; a semantic-ID permutation
    test to catch hidden hard-coded meanings.
14. Probabilities (unchanged proposal): LEARN > RANDOM-5P with lower bound above 0: **35%**; LEARN close to NAMED: **25%**.
15. Fix attribution, separate hunger from thirst, general interaction exploration, add BLIND; "do not solve each new
    Crafter difficulty by introducing another Crafter-specific rule."

## Gemini (gemini.google.com, fresh chat), opinion, not sign-off
1. **Bump-and-poke is "a domain-specific hand-crafted reflex disguised as general curiosity"**: an artificially
   benevolent bias in a world with lava and monsters. RANDOM-5P shares it, so the primary comparison stays valid, but no
   claim that the agent discovered affordances without prior knowledge.
2. Blocked and fed are survival minimums; merging hunger and thirst into one "fed" is fine (MBb has one food layer);
   the shelter layer is dead weight. **Without a hurt/damage consequence** lava, zombies and grass look alike.
3. NAMED with the new hand is the right internal control; show CX1's numbers too, because the new hand may HURT NAMED
   (poking walls and trees it already knows) and make LEARN look "close" to a handicapped baseline.
4. Confounds: **the cow multi-hit problem** (every non-lethal hit is a fair negative, the cow reads 0.25-0.33, below
   0.5, and is never hunted again); **moving entities** leave stale cow ids in memory, poisoning the table; **the 0
   prior for walls** makes the brain plan through unexplored walls and bump each new obstacle kind; ripe plants revert.
5. Changes: an optimistic prior or a lower threshold (> 0.15, or +1 prior positive); keep only static terrain in the
   long memory (moving things only while in view); a damage consequence into the avoid/wall layer; report raw
   achievement rates (drink, eat cow) beside the score: 0.56 vs 0.53 is a small difference on a compressed scale.
6. Probabilities: LEARN > RANDOM-5P: **65%** (water is stationary, abundant and one-hit); LEARN close to NAMED: **40%**
   (unless the cow threshold and stale ids are fixed).

## DeepSeek (chat.deepseek.com, fresh chat, DeepThink), opinion, not sign-off
- Verdict: "not freezable as specified; CX2 tests a table+hand bundle, not cleanly learning meaning."
- **Bump-and-poke is a hidden hint** ("if blocked, try do" is exactly what discovers drinkable water); fair only if the
  same wrapper is used in every arm, never reads the table or the named labels to decide, is disclosed, and is
  ablated (LEARN and NAMED without the poke).
- Blocked is acceptable but conflates impassable with interactive. Fed collapses food and drink, ignores health,
  energy and wood; the fair-negative rule punishes the multi-hit cow and resource pokes. Sleep-anywhere makes "stay"
  non-neutral. Log food, drink, health and energy separately; positives and negatives per need.
- NAMED-with-the-new-hand is right for the eyes but the hand needs its own controls: a meaning-source x hand factorial
  (NAMED and LEARN with the old hand, CX1 as reference). Define "close" in absolute score units, and require NAMED to be
  clearly above random first.
- Confounds: stale memory of moving cows and zombies; the cow never ranks above 0.5; zombies hurt a brain with no
  health drive; trees and stone waste pokes; sparse per-kind trials per life; the 0 prior and 0.5 threshold brittle;
  the score is sparse and dominated by achievements this brain cannot reach.
- Before freezing: define RANDOM-5P exactly (does it update the table, poke, use predictions?); the factorial; no-poke
  and shuffled-kind ablations; per-life trial counts and rank curves; "fix the cow criterion to positive after kill";
  state zombie and death handling.
- Probabilities as specified: LEARN > RANDOM-5P **about 55%**; LEARN "close" to NAMED **about 15%**.

## The council (Claude): where they agree, checked against the code
| Point | Who | Checked | Verdict |
|---|---|---|---|
| The multi-hit cow becomes false negatives and never passes 0.5 | all three | Crafter: a cow takes several hits; CX1's hand already pokes until it eats | **Accepted.** A trial becomes an *interaction bout*: consecutive "do"s on the same target, ended when the target changes or the body turns away; positive if food or drink rose during the bout. General (no cow rule). |
| Negatives must be per need (drink full makes water look useless) | GPT, DeepSeek | the bridge's hunger = the worse of food and drink | **Accepted.** Two tables, fed-food and fed-drink; a negative for one only while that one is below its maximum; the food layer shows the larger of the two (as NAMED shows water and cows alike). |
| Attribute to the target seen at the moment, not the remembered one | GPT, Gemini, DeepSeek | the semantic view is current for the facing cell | **Accepted.** |
| RANDOM-5P must be defined exactly | GPT, DeepSeek | | **Accepted:** random moves, the same hand, the same table updated (so the hand's food rule works the same). |
| A no-meaning control (BLIND) and a no-poke ablation | GPT; DeepSeek | | **Accepted:** BLIND (MBb, all learned layers held at 0, same hand) and LEARN-NP (no poke). |
| The hand factorial with the old hand | DeepSeek | the old hand cannot discover water at all (water blocks walking; it only does "do" on named food) | **Partly:** NAMED with the OLD hand = CX1's BRAIN (cited, same seeds and code); LEARN with the old hand would never poke water by construction, so it is not run. |
| Bump-and-poke is a bias | all three | | **Kept and named:** a universal reflex (every blocked kind, no exceptions, never reads the table), shared by every arm, ablated by LEARN-NP. |
| Damage/health | Gemini, DeepSeek | MBb has no health drive or layer | **Logged, not used** (named limit). |
| Report achievement rates beside the score | Gemini | | **Accepted** (drink, eat cow, wake up; co-reported). |
Estimates (on the first draft): GPT 35% / 25%, Gemini 65% / 40%, DeepSeek 55% / 15%.
