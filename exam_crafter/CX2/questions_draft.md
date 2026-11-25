# CX2: does the brain learn what Crafter's things mean, within one life? (DRAFT for the council; not frozen)

**Why.** CX1 (final): MBb, untrained for Crafter, scored 0.56%, above random choices through the same bridge (0.53%),
because it heads for water and cows. But the BRIDGE told it which tiles are food (water, cow, ripe plant) and which are
walls. That is our programming, not the brain's learning. GPT's principle, adopted by the creator: "Every new world
should require Bob to learn more, not require us to program more." The creator's roadmap: Mind Lab -> Crafter ->
Craftax -> ACL. W3r (running) tests the same idea in Mind Lab: a brain that learns, within a life, what colours do.

**The question.** With the bridge's hand-made meanings removed and replaced by a meaning module that learns them from
the body's own consequences within each life, does the brain still find water and food in Crafter (as CX1's BRAIN
did), or does it fall to the random floor?

## The change: the eyes learn meanings (nothing else changes; MBb as it is, no training)
- The bridge still writes a memory of what the player has seen, but per cell only **the tile's kind** (Crafter's
  semantic id: 18 kinds, water, grass, tree, cow, ...), not "food" or "wall".
- A **meaning table** (W3r's learner), reset at the start of every life: per kind, positives and fair negatives of two
  consequences the body itself feels:
  - **blocked:** the body tried to move into a cell of this kind and did not move;
  - **fed:** after "do" on a cell of this kind, food or drink rose (Crafter's own inventory numbers). A fair negative
    when "do" on that kind left both unchanged while either was below its maximum.
  - prediction = positives / (positives + fair negatives); 0 before any trial.
- The brain's wall and food layers = the table's predictions for each remembered cell's kind (unseen 0); unseen,
  shelter and staleness as in CX1.
- **The hand** (CX1's rule, one change): a move into a cell the table predicts as food above 0.5 = face it and "do"
  (CX1: the bridge's named food); **a move that is blocked** = face that cell and "do" once ("bump and poke": the only
  way a body learns that water, which blocks walking, can be drunk). The poke can also chop a tree or hit a cow: the
  table counts only the two consequences above.

## Arms (Crafter's protocol: seeds 1, 2, 3, ...; about 1,000,000 steps each; the PC or a VM, recorded)
| arm | eyes | hand |
|---|---|---|
| **LEARN** | the meaning table | CX1's rule + bump-and-poke |
| **NAMED** | CX1's named meanings (rerun) | CX1's rule + bump-and-poke (so only the eyes differ) |
| **RANDOM-5P** | none (random moves) | the same hand (matched floor) |
CX1's BRAIN, RANDOM-5 and RANDOM are cited for scale.

## Readings (to freeze; the CX1 score and bootstrap: 2,000 resamples over lives, seed 0)
1. **Primary: LEARN − RANDOM-5P** Crafter score (does a brain with learned meanings beat random choices?).
2. **LEARN − NAMED** (what learning the meanings costs, versus being told them): "close" if the interval's lower bound
   is above −0.10 points.
3. Per life: steps until the table first ranks water (and cow) as food; the share of lives that ever learn each.
4. Achievement rates (drink, eat cow, wake up), life length, cells visited.

## Questions for the council
1. Is "bump and poke" fair (the body tries the thing it bumped into) or a hidden hint?
2. Are blocked and fed the right two consequences for Crafter? (Sleep is anywhere in Crafter; no shelter to learn.)
3. Is NAMED with the same new hand the right control for LEARN, so only the eyes differ?
4. The power: ~5,000 lives per arm; is that enough to read LEARN − NAMED within 0.10 points?
