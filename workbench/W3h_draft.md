# W3h: pain. Does pain teach a growing brain to avoid harm? (DRAFT)

**Why:**
- **The creator, 16 November 2026:** "i think for growth there should be suffering also at least for some period … for
  beginning there should be pain".
- The decision is recorded in `../brain_v1_plan.md`. Pain is a teacher, not a punishment: proportional to real harm,
  logged, and measured for what it teaches.
- Today the brain has no danger to learn from. Its only bad feelings come late: hunger after energy is already gone.

## The world: W3's, plus thorns
- **2 thorn patches per land,** each 2 × 2. They are passable, are not on food, the shelter or the start, and are drawn
  from a separate stream of the land's seed, so walls, food, shelter and relocations are W3's exactly.
- **Thorns are visible** in the 3 × 3 view. The map memory writes them as a sixth channel, "thorn seen", whose weights
  start at zero (as W3g).
- **Harm:** every step on a thorn cell costs 8 energy. That is real injury: it can kill through hunger.
- **Calibration** (before any brain trains): Script, walking on the thorns as on open ground, must still survive
  ≥ 0.80 on the calibration lands. If not, the harm is lowered (8 → 6 → 4), the first value that passes.

## Pain (the new feeling)
- **The pain reward:** at each thorn step, −p × (energy lost) / 8, with p = 1.0. One thorn step hurts about as much as
  one meal relieves.
- **Pain stops when harm stops.** It does not kill and does not last.
- **Logged** every life, in training and in the test: thorn steps, and pain felt.

## Arms (all on W3d's best brain, PYFR: the parent's fading childhood plus "that worked!" and rest replay; 8 seeds,
2,000,000 steps, on GitHub's machines)
| arm | harm | pain | the parent | role |
|---|---|---|---|---|
| **TH** | yes | no | thorn-blind (walks through thorns) | harm alone: the only lesson is the later hunger |
| **THP** | yes | yes | thorn-blind | **the question:** does pain teach avoidance? |
| **THPw** | yes | yes | avoids thorns it has seen (treats them as walls) | does watching a careful parent add? |

## Measures (W3's test lands, learning off)
1. **Thorn steps per 1,000 steps of life.** The main measure.
2. Lifespan and survival to 3,000.
3. Pain felt per life (the log).
4. **Learning curve:** thorn steps per 1,000 in each 100,000-step block of training. Shows how fast avoidance comes
   after the first pains.

## Readings (to be frozen; paired by seed; 95% bootstrap)
1. **"Pain teaches avoidance":** THP − TH on thorn steps per 1,000, upper bound below 0.
2. **"Pain helps it live":** THP − TH on lifespan, lower bound above 0.
3. **"Watching adds":** THPw − THP on thorn steps, upper bound below 0.

## Open questions for the council
1. Is pain as an immediate negative reward, proportional to harm, a fair model of pain? Or should it be a separate
   signal (a state the brain feels, which the critic sees)?
2. Should the thorn channel exist at all? Without it, avoidance would need the brain to remember where it hurt (the
   W3g problem).
3. Is p = 1.0 the right scale? Too strong may stop the brain exploring (fear). Should a second p be tested?
4. How do we measure fear (avoiding food next to thorns, longer detours) without designing it in?

## The assistant's prior
- Pain teaches avoidance: about 70%.
- Pain helps it live: about 40% (avoiding thorns may cost food that grows near them).
- Watching adds: about 45% (W3f: the copy is lossy).
