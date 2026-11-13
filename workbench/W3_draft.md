# W3: drives only. Does a brain keep pushing with no task, only survival, comfort and curiosity? (DRAFT)

**Why:**
- The creator's idea (12 November): "mainly 3 things push humans forward: survival, comfort, curiosity."
- In W1–W2 the brain was taught or rewarded for one task (reach the food). ACL's people have no task: they live.
- W3 asks whether the three drives alone make the starting brain (map memory + V+) live well in a small world: stay
  alive, rest, and learn its land. Nobody tells it what to do.

## The world
- **The land:** 15 × 15 with W1b-style walls. 3 food patches that regrow slowly after eating, 1 shelter cell, and
  the rest bare.
- **The view:** 3 × 3 with a remembered map (W2). The food is no longer smelled: it must be found.
- **The body:**
  - energy falls by 1 per step and rises by 30 per meal; at 0 the brain dies;
  - fatigue rises by 1 per step and falls fast in the shelter; above 100 every move costs double energy.
- **A life** lasts up to 3,000 steps. The land and the patches are new each life (fixed seeds for the test).

## The drives (the only reward)
Homeostatic reward (Keramati & Gutkin 2014): the reward at each step is the reduction of "drive", the distance of
the body from its set points.
- **Survival:** energy below its set point.
- **Comfort:** fatigue above its set point.
- **Curiosity:** the number of map cells newly seen this step (information gain on the map), with a weight that
  falls as the land becomes known.
- There is no reward for reaching any particular place.

## The brain
- **The map memory** (W2) holds walls, food seen (and when), the shelter, and the unknown.
- **V+ plans on it.** Its reward map is built from the map channels weighted by the current drive levels (hungry:
  remembered food counts more; tired: the shelter; curious: the unknown). The weights from the drives to the reward
  map, and the planner, are learned by actor-critic on the drive reward alone.
- No teacher, no imitation.

## The brains compared
| brain | drives | role |
|---|---|---|
| **D3** | survival + comfort + curiosity | the question |
| **D2** | survival + comfort (no curiosity) | does curiosity add anything? |
| **Dc** | curiosity only | does curiosity alone keep it alive? |
| **Rand** | a random walk | floor |
| **Script** | scripted: explore the nearest unknown until food and shelter are known, then cycle eat / rest by BFS | ceiling (a hand-written good life) |

## Measures (test lands, learning off)
1. **Lifespan** (steps survived; the share of lives reaching 3,000).
2. **Land known** at 500 and 3,000 steps.
3. **Food found** after a patch moves (patches move once, at step 1,500): steps to find the new patch.
4. Time hungry and time exhausted (comfort).

## Readings (to be frozen)
- **"Drives are enough to live"** if D3 survives to 3,000 in at least 80% of lives (Script's is near 100%).
- **"Curiosity pays"** if D3 − D2 on steps to find the moved patch has an upper bound below 0 (finds it sooner), and
  D3 − D2 on lifespan is not worse.
- **"Curiosity alone is not enough"** (expected) if Dc dies more often than D3.

## Open questions for the council
1. Is homeostatic reward the right form for "drives only", or does it hide a task (energy = food)?
2. Curiosity as map information gain: fair, or too engineered? Alternatives: prediction error of a world model, or
   counts of visits.
3. Should the drive weights be learned, or fixed and inborn (as NB3's reluctance was inborn)?
4. Is moving the patch once a fair test of whether curiosity pays?

## The assistant's prior
- Drives are enough to live (D3 ≥ 80%): about 45%. Learning by reward alone has been slow in every rung so far.
- Curiosity pays: about 55%.
- Curiosity alone is not enough: about 85%.
