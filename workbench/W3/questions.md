# W3: drives only. Does the brain live well with no task, only survival, comfort and curiosity?

**Frozen plan** (git tag `W3-frozen`, before any code or data).
- **Draft:** `../W3_draft.md`.
- **Council:** `../W3_council_2026-11-13.md` (GPT, Gemini and DeepSeek, two rounds; all changes below are theirs unless
  said).
- **Sign-off:**
  - the creator's standing instruction (10 November 2026): "do not ask me go ahead bro";
  - and their "Yes" (13 November 2026) to "I'll send it to them now, then freeze it, build it and run it".

**The question.** In W1–W2 the planner was taught by copying a scripted teacher. Here **nothing teaches it**. Its only
rewards are its own feelings:
- staying fed (survival);
- not exhausted (comfort);
- learning its land (curiosity).

Does the starting brain (the W2 map memory plus V+) then stay alive, rest and know its land? And does curiosity help it
notice a changing world? This is the first time V+ learns from reward alone.

## The world (`world3.py`)
**The land:**
- 15 × 15 with a wall border;
- 4 interior wall segments (length 3–6, straight, random) per land, redrawn until every open cell is connected;
- **3 food patches**, each a 2 × 2 block of open cells (4 food cells), not overlapping and not on the shelter;
- **1 shelter cell.**

**The view and the actions:**
- **View:** the 3 × 3 cells around the brain. No smell, no distant sight.
- **Actions:** north, south, east, west, stay. Moving into a wall is a stay.

**The body:**
- **Energy E:** starts at 150, maximum 200.
  - −1 every step, or −2 on a move while fatigue is above 100.
  - Entering or staying on a full food cell eats it automatically (if E < 200): +30, capped at 200. The cell is then
    depleted and regrows after **R** steps (R is set by calibration, below).
  - **E ≤ 0 is death.**
- **Fatigue F:** starts at 0.
  - +1 every step outside the shelter;
  - −10 every step on the shelter (minimum 0).
- **A life** lasts at most 3,000 steps.

**Relocations:**
- Each patch relocates **twice per life**, at steps drawn uniformly in [500, 2,700], at least 400 apart for the same
  patch.
- The patch's 4 cells vanish, and a new 2 × 2 block appears, full, at a random valid place at least 5 cells (Manhattan)
  from the old one.

**Seeds and schedules:** each land and its relocation schedule come from the land's seed. The seed sets:
- **training:** a training stream (seed `1000·run_seed + life`);
- **calibration:** 800001–800050;
- **test:** 900001–900050.

## The map memory (a fixed writer, as W2)
**What it writes:** every step it writes the 3 × 3 view for every cell seen:
- wall or open;
- food full or not (so **a food cell seen empty is cleared**);
- shelter or not;
- the step last seen.

Cells out of view keep their last-seen state. So a regrown cell, or a patch that has moved away, looks as it did when
last seen. A depleted cell and an emptied cell look alike, as they would to an animal.

**The planner's channels (C = 5):**
- known wall;
- never seen;
- food (full at last sighting);
- shelter;
- **uncertainty u.**

**Uncertainty u:**
- 1 if never seen;
- 0 for a seen wall;
- otherwise 1 − exp(−age/τ), where τ = 200 and age is the steps since last seen.

## The drives (the only reward; inborn and fixed)
**The deficits:**
- **Survival:** s = max(0, 150 − E)/150.
- **Fatigue:** f = min(F, 200)/200.
- **The drive:** D = s² + f² (convex, after Keramati & Gutkin 2014), with D ≤ D_max = 2.

**Homeostatic reward** each step: r_h = 10·(D_t − D_{t+1}).
- **At death** the drive jumps to D_max, so the last reward is 10·(D_t − D_max), and the life ends.
- **At the 3,000-step cap** the life ends with no extra reward.

**Curiosity reward** each step: r_c = 0.05 · Σ u (taken before the update) over the cells in this step's view. A cell
just seen has u ≈ 0, so it pays again only after it goes stale; walls pay nothing.

**Total:** r = w_h·r_h + w_c·r_c, with weights fixed per brain (table below).

**Dying is never better than living** (checked by the assistant; council round 2). For γ < 1, a continuation from step
t ending at death or at the cap has the discounted return

  Σ_k γ^k·10·(D_{t+k} − D_{t+k+1}) = 10·[D_t − Σ_{k≥1}(γ^{k−1} − γ^k)·D_{t+k} − γ^{T}·D_{t+T}] ≥ 10·(D_t − D_max),

because every D ≤ D_max and the weights sum to 1. That bound is exactly the return of dying now. The curiosity reward
is never negative. A numerical check is added.

## The brain (V+ from W1e and W2, drive-weighted)
**The reward map:** r_map = conv(W₀, map) + s·conv(W_s, map) + f·conv(W_f, map) + c·conv(W_c, map) + b.
- Each W is a 1 × 5 × 3 × 3 filter.
- c = the curiosity level, the mean u over all cells not known to be walls.
- W₀ (no drive) starts random N(0, 0.3), as W2's.
- **W_s, W_f and W_c start at zero and are learned**, so no designer link from hunger to food is given.

**The rest:**
- **The planner and read-out:** V+ (plus mask, K = 30, max) on r_map → q at the brain's cell → 5 action scores and a
  value (W2's MapVIN).
- **Learning:**
  - advantage actor-critic on the reward above;
  - segments of 64 steps, bootstrapped with the critic;
  - γ = 0.97, learning rate 0.01, entropy 0.01, gradient clip 1.0 (W1's settings);
  - the same for every learned brain.
- **No teacher, no imitation.**

## Brains
| brain | reward weights (w_h, w_c) | drive levels fed to the map | mapping W_s, W_f, W_c | role |
|---|---|---|---|---|
| **D3** | (1, 1) | s, f, c | learned from 0 | the question |
| **D2** | (1, 0) | s, f (c = 0) | learned from 0 | does curiosity add anything? |
| **Dc** | (0, 1) | c (s = f = 0) | learned from 0 | does curiosity alone keep it alive? |
| **D3i** | (1, 1) | s, f, c | **fixed by design:** W_s = +1 on the food channel, W_f = +1 on shelter, W_c = +1 on uncertainty (centre taps; all else 0) | reference: the designer's link given |
| **D3−** | the trained D3, tested with c = 0 | | | lesion: does D3 use its curiosity? (read beside D2) |
| **Rand** | random actions | | | floor |
| **Script** | the same view and map memory only (no world access). It: <br>– goes to the nearest remembered full food if E < 120 (BFS; unknown cells treated as open); <br>– goes to the shelter if F > 80 and it is known, staying until F = 0; <br>– otherwise goes to the nearest never-seen cell, else the stalest cell with u ≥ 0.5, else stays | | | ceiling: a hand-written good life |

**Runs:**
- 8 training seeds per learned brain (D3, D2, Dc, D3i), so 32 runs;
- 2,000,000 training steps each, on training lands;
- at most 4 runs at a time on this PC.
- **If the measured speed (before any data) means more than 14 hours, the step budget is cut** to fit, the same for
  every brain, and recorded as a pre-data correction.

## Calibration (before any brain is trained; calibration lands only)
- **The regrowth list R:** 400, 200, 100, 50, 25 steps, in this order, from scarcest to most abundant.
- **The rule:** R is **the first value at which Script survives to 3,000 in ≥ 0.90 of the 50 calibration lives, and
  Rand in ≤ 0.20.**
- **If none qualifies, W3 stops,** and the world is revised in a new frozen amendment.
- **Learned brains play no part** in calibration.

## Test (learning off; the 50 test lands, the same land and relocation schedule for every brain)
**Per life, the measures:**
1. Survival to 3,000 (0/1), and the lifespan.
2. Land known: the share of non-wall cells ever seen, at steps 500 and 3,000 (or at death).
3. **Relocation finding:**
   - for each relocation event while the brain is alive at the move: **found** = any cell of the new patch is in view
     within 300 steps;
   - **dying first counts as not found;**
   - the life's share found is over its events.
4. Time hungry (E < 50) and time exhausted (F > 100), as shares of the life.

**Per run:** the mean over its 50 test lives. **Learned weights:** the row norms ‖W_s‖, ‖W_f‖, ‖W_c‖ every 50,000
steps.

**Statistics:**
- 95% intervals by bootstrap over the 8 training seeds (10,000 draws, `numpy.random.default_rng(20261113)`, percentiles
  2.5 and 97.5);
- differences between brains are paired by seed number (the same seed gives the same initial W₀, planner and training
  lands);
- n = 8 runs × 50 lives beside every measure.

## Readings (exploratory)
1. **"Drives are enough to live":** D3's survival share has a mean ≥ 0.80 and a lower bound ≥ 0.70.
2. **"Curiosity pays":** all of the following must hold:
   - D3 − D2 on the share found has a lower bound above 0;
   - D3 − D2 on survival share has a lower bound above −0.10 (non-inferiority);
   - D3's curiosity row did not collapse.

   **Collapse:** in a seed, the final ‖W_c‖ is under 0.1 × the largest final row norm. If more than 2 of the 8 D3
   seeds collapse, reading 2 is "not readable", not "no".
3. **"Curiosity alone is not enough"** (expected): Dc − D3 on survival share has an upper bound below 0.

**Secondary (intervals, no gate):**
- D3i − D3 (does learning the link cost?);
- D3− − D3 on finding (does D3 rely on curiosity?);
- D3 against Script and Rand;
- land known;
- time hungry and time exhausted;
- the learned weight trajectories, and whether s ends up weighting the food channel and f the shelter.

## Validity (hard stops; failing one means W3 is invalid, not a finding)
- The calibration rule is met.
- **Code checks** (`checks.log`, All: PASS, before data):
  - the map writer never writes a cell outside the view;
  - the batched planner equals planning one map at a time;
  - a numerical gradient check of the drive-weighted reward map, with W_s, W_f, W_c receiving non-zero gradients from
    zero;
  - the death bound holds on 10,000 random continuations;
  - test lands and relocation schedules are identical across brains;
  - weights are unchanged by testing;
  - Script reads only the map memory;
  - the same seed gives the same result twice;
  - Rand and Script reproduce their calibration numbers.

## The assistant's prior (after the council)
- Drives are enough to live (reading 1): about 35%. V+ has never learned from reward alone; the rewards are sparse,
  and lives are long.
- Curiosity pays (reading 2): about 40%.
- Curiosity alone is not enough (reading 3): about 90%.
- D3i at least as good as D3: about 70%.
