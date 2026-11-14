# WG: growing with awake neurons (plan, frozen before any code or data)

**Frozen** as git tag `WG-frozen`, before any code or data.
- **The creator** (14 November 2026): "go ahead with the awake neurons growth test", after WN.
- In WN, a growing brain's new neurons were born silent: tiny incoming connections (N(0, 0.01²)) and outgoing
  connections at zero. They stayed unused (outgoing about 0.009 against 0.41 for the born neurons), so the brain acted
  like the 16-neuron brain it was born as.
- **Exploratory, as WN:** the creator asked for it directly, so there is no council. Any decision drawn from it goes
  through a council later.

## The task
WN's (= WS's), unchanged: 6 kinds, 2 lids, 3 tries per kind per day, 60 days, one reliable demonstrator shown before
each try on days 1–30, copy rate 0.5, learning rate 0.05, the same tests.

## The brains (all with the memory ring; seeds 1–48, the same draws for every brain)
- **Born at a fixed size (references, WN's code unchanged):** M16, M32, M128.
- **G (silent growth):** WN's G: born 16, doubles at the end of days 8, 16 and 24, to 128. New incoming N(0, 0.01²);
  new outgoing zero.
- **GA (awake in, quiet out):**
  - the same growth;
  - the new neurons' incoming connections (from the senses and from all neurons) start N(0, 0.1²), the same as a born
    neuron's, so they are active at once;
  - their outgoing connections (to the hands and to old neurons) start at zero, so what the child does is unchanged
    at the moment of growth.
- **GF (fully awake):** as GA, but the outgoing connections also start N(0, 0.1²), as a born neuron's. Behaviour can
  jump at the moment of growth.
- **GA32 (grow into the best size):** as GA, but born with 8 neurons, growing to 16 at the end of day 8 and to 32 at
  the end of day 16.

## Measures (descriptive, with 95% bootstrap intervals over the 48 seeds; paired differences; numpy seed 20261115)
- **Manipulation check:** at day 60, the mean |outgoing weight to the hands| of the added neurons against the born
  ones, for G, GA, GF and GA32.
- **Skill:** own skill (full boxes, no showing) at days 7, 15, 30 and 60; success after a showing at day 30.
- **The questions:**
  1. Does waking the new neurons make growth do anything? GA − G, and GF − G, at days 30 and 60.
  2. Growing against being born big: GA − M128 and GF − M128, at days 30 and 60.
  3. Growing into the best size against being born at it: GA32 − M32, at days 30 and 60.

## Limits (stated now)
- Fixed learning rates, as in WN.
- One small task.
- References M16, M32 and M128 on seeds 1–24 are WN's children again (the same code gives the same numbers); seeds
  25–48 are new.

## The assistant's prior
- **Manipulation:** GA's added neurons are used (added outgoing at least half the born neurons' mean): about 75%.
- **Q1:** GA beats G at day 60: about 40%. In WN, M128 and M16 were level at day 60, so being used may not raise
  skill. GA may also lean on the teacher like M128, which would lower its day-30 skill.
- **Q2:** GA is ahead of M128 at day 30 (it was small early in the teaching): about 60%.
- **Q3:** GA32 is level with M32 at day 60 (interval includes 0): about 55%.
