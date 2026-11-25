# CX2: does the brain learn what Crafter's things mean, within one life? (FROZEN, tag CX2-frozen)

**Sign-off:** the creator, 24 Nov 2026, in this Claude Code session: "yes go ahead freeze it and start".

**Why.** CX1 (final): MBb, untrained for Crafter, scored 0.56%, above random choices through the same bridge (0.53%),
because it heads for water and cows. But the bridge TOLD it which tile kinds are food and which are walls. GPT's
principle, adopted by the creator: "Every new world should require Bob to learn more, not require us to program
more." This study removes the told meanings: the brain's eyes must learn them, within each life, from what the body
feels. Council: `gpt_review_cx2_draft.md` (GPT, Gemini, DeepSeek; each claim checked).

**Honest name:** within-life learning of survival meanings (what blocks, what feeds, what waters) in an unfamiliar
world, by a fixed brain with a learning table in its eyes and a universal "bump and poke" reflex in its hand. Not
general understanding of Crafter (trees, tools, monsters are outside it).

## What changes from CX1 (MBb as it is; no training)
- **Memory:** per cell, the tile KIND last seen (Crafter's 18 semantic ids), not "food" or "wall".
- **The meaning tables** (reset at every life's start; W3r's learner), per kind:
  - **blocked:** a move into a cell of that kind (the kind seen there at that moment) did / did not move the body;
  - **fed-food** and **fed-drink**, learned per **interaction bout**: consecutive "do"s on the same target, ended when
    the target cell's kind changes or the body faces or moves elsewhere; positive if food (or drink) rose during the
    bout; a fair negative for that need only if it was below its maximum throughout the bout. (A cow that takes several
    hits is one bout, positive when eaten.)
  - prediction = positives / (positives + fair negatives); 0 before any trial (unknown is shown as nothing).
- **The brain's layers:** wall = P(blocked); food = the larger of P(fed-food), P(fed-drink) (as CX1 showed water and
  cows alike); per remembered cell's kind; unseen 0. Unseen, shelter (the player's place) and staleness as CX1.
- **The hand** (every arm): CX1's rule with the food layer above 0.5 meaning "face and do", and **bump and poke**: a
  move that is blocked = face that cell and "do" until the bout ends (a universal reflex: every blocked kind, no
  exceptions, never reads the tables).
- Health, energy and inventory changes are logged per bout (not used by the brain: a named limit).

## Arms (Crafter's protocol; seeds 1, 2, 3, ...; about 1,000,000 steps each; the PC, 2 at a time; machine recorded)
| arm | eyes | controller | hand |
|---|---|---|---|
| **LEARN** | the tables | MBb | CX1 rule + poke |
| **NAMED** | CX1's told meanings | MBb | CX1 rule + poke |
| **BLIND** | learned layers held at 0 (no meaning) | MBb | CX1 rule + poke |
| **LEARN-NP** | the tables | MBb | CX1 rule only (no poke) |
| **RANDOM-5P** | the tables (updated as LEARN) | random moves | CX1 rule + poke |
CX1's BRAIN (= NAMED with the old hand), RANDOM-5 and RANDOM are cited for scale.

## Readings (`analyse_cx2.py`, written before data; CX1's score; 95% bootstrap over lives, 2,000 resamples, seed 0, the
full score recomputed in every resample)
1. **Primary: LEARN − RANDOM-5P** (interval above 0: the learned meanings let the brain beat random choices).
2. **LEARN − BLIND** (do the learned meanings matter for the same brain and hand?).
3. **LEARN − NAMED**, read as "close" only if NAMED − RANDOM-5P is itself above 0 and the LEARN − NAMED lower bound is
   above −0.10 score points (one tenth of a percentage point).
4. LEARN − LEARN-NP (what the poke adds); NAMED − CX1 BRAIN (what the new hand does to told meanings).
5. Co-reported: drink, eat cow, wake up rates; life length; cells visited; per life, whether and when the tables first
   rank water (drink) and cow (food) above every other kind seen, with the share of lives that never do.

## Checks before data (`checks_cx2.py`, All: PASS)
- NAMED's layers equal CX1's for the same memory; with a perfect table (the true meanings) LEARN's layers equal NAMED's.
- A scripted life: one bump into water then pokes until drinking gives blocked + fed-drink positives on water only; a
  3-hit cow is one bout, one positive; full drink makes a water bout teach nothing about drink.
- The tables reset at each life; the semantic id permutation (a test-only shuffle of kind ids) changes nothing in
  LEARN's behaviour on average (no hidden hard-coded kind); BLIND's layers are all 0.
- Determinism: the same seed gives the same life twice.

## Expected (before data)
LEARN − RANDOM-5P above 0: the council 35-65% on the first draft; the assistant about 60% after the fixes (water is
stationary, abundant and one bout). LEARN − BLIND above 0: about 60%. "Close" to NAMED: about 25%.

## Limits (named now)
1. We chose the consequences (blocked, fed-food, fed-drink) and the poke reflex.
2. No health or danger in the tables; zombies and lava are not learned as bad.
3. The brain is fixed (MBb); only its eyes learn. A brain that learns in Crafter is a later step.
