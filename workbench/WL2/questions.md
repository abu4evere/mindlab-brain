# WL2: why does the leaky memory work? (plan, frozen before any code or data)

**Frozen** as git tag `WL2-frozen`, before any code or data.
- **The creator** (15 November 2026): "go ahead with the follow-up first".
- **WL found** that a wait of 8 steps with neural noise 0.6 between the showing and the try (L2) stopped the parrot.
  - At size 128: own skill at day 30, 0.823 against 0.042; day 60, 0.997 against 0.806.
- **Three explanations fit:**
  1. forgetting the details forces learning the rule (the creator's idea);
  2. noise during learning makes the network sturdier (a general training aid);
  3. the wait makes practice look more like the test, which has no showing.
- **Exploratory:** no council.

## The world and child (WL's, unchanged)
- WN's world: a showing before every try on days 1–30, none after.
- Memory children of 32 and 128 neurons; 48 children each (seeds 1–48), on GitHub's machines.

## Arms
- **L0:** no leak (WL's L0; must reproduce WL).
- **L2:** wait 8 steps, noise 0.6 in the wait (WL's L2; must reproduce WL).
- **W8, wait only:** 8 wait steps with no noise. Forgetting only by the brain's own dynamics.
- **NS, noisy memory only:** no wait; noise 0.6 added to the neurons' input on each of the 4 showing steps. The
  memory is blurred, with no delay.
- **NP, noise everywhere in practice:** no wait; noise 0.3 on the neurons' input on every step of every copy and
  practice try (none in tests). A general training aid, not aimed at memory.
- **Linf, full forgetting:** the try starts with a blank memory (no showing steps). The copy step also runs without
  the showing in memory. Nothing to replay, and practice looks exactly like the test.

**Noise draws:** the child's own streams: `[seed, 13]` for wait and showing noise; `[seed, 15]` for NP's step noise.
Tests use no noise, except the after-showing test's episode (`[seed, 14, day]`).

## Measures (descriptive; 95% bootstrap intervals, paired by seed; numpy seed 20261123)
- Own skill at days 7, 15, 30 and 60; after a showing at day 30; lifetime food.
- **Each arm minus L0, and each arm minus L2, at the same size,** on day 30 and day 60.
- **The reading:**
  - an arm "carries the effect" if its day-30 gain over L0 is at least half of L2's gain at that size;
  - (1) is supported by W8 or Linf carrying it; (2) by NP carrying it; (3) by Linf carrying it while W8 does not.

## The assistant's prior
- **W8-128 carries at least half of L2's day-30 gain:** about 35%.
- **NS-128:** about 50%. **NP-128:** about 40%.
- **Linf-128:** day 60 below L2-128 by at least 0.05 (memory still helps when it leaks rather than vanishes): about
  60%.
