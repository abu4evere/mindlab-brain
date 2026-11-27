# V2-2 Goals: can Bob's own planner learn to want a place that his consequence model values? (DRAFT, not frozen)

Drafted 27 Nov 2026 ~02:10 EST under the creator's sleep-mode autonomy, as Brain v2 step 2 (`brain_v2_roadmap_draft.md`,
revised order: Goals with arbitration). Not frozen; for the council.

## Why
CW2 (final): once a join at the station has been experienced, steering to it doubles the chains in a life, but nearly
all of that came from a WRITTEN carry reflex (+0.63 [+0.43, +0.84]); through the walker's own planner (a food-layer
mark) the gain was small (+0.11 [+0.06, +0.16]), because the walker's food pull is weak when it is fed. The roadmap's
rule: a written decision is retired only when a learned part does at least as well.

## Correction to the roadmap (appended there too)
Bob's walker (RMS, used in BV1, CW1, CW2) is W3n's **DriveVIN**, not MoveVIN (MoveVIN is W3p's MBb). Its reward map is
r = W0·x + s·Ws·x + f·Wf·x + c·Wc·x + b over five map layers x (wall, unseen, food, shelter, staleness), with s, f, c
the hunger, tiredness and curiosity levels, then value iteration and a policy head.

## The part
- **A goal layer and a goal level:** a sixth map layer marking the place the consequence model's experienced value
  runs through (CW2's GUIDE rule: only after experienced value, never from the untried bonus), and a fourth level
  g = that value / (2 x a food meal), capped at 1. New weights: channel 6 in W0, Ws, Wf, Wc, and a new Wg over all six
  channels, **all starting at 0**, so before learning the walker is exactly the old one (an exact zero check).
- **Learning it (adult fine-tuning, not a new childhood):** starting from each RMS kept copy, the walker keeps
  learning with its own actor-critic rule and its own body reward (the drive: energy, tiredness, staleness; no new
  reward) for a fixed number of steps in CW2's world (things, station, the consequence model live), so it can learn
  that the goal layer, when g is high, leads to energy.
- **Arbitration (the named sub-test, round-table):** in one arm the written survival floor (the consequence model acts
  only when hunger and tiredness are below 0.5) is removed for the goal layer: the learned weights alone decide when
  the goal pull beats hunger and tiredness.

## Arms (16 seeds = RMS 1-16; test on 50 fresh CW2 lands each)
| arm | walker | goal layer | floor |
|---|---|---|---|
| **GOAL** | fine-tuned with the goal layer | the experienced-value place | kept |
| **GOAL-NOFLOOR** | fine-tuned with the goal layer, floor removed for the goal | same | removed |
| **FT-NOGOAL** | fine-tuned the same steps in the same world, goal layer always empty | none | kept |
| **SHAM-GOAL** | fine-tuned with the goal layer marking a distance-matched wrong place (CW2's sham rule) | sham | kept |
| reference: **CW2's GUIDE-REFLEX** and **NO-GUIDE** (frozen RMS), re-run on the same test lands | — | — | — |

## Measures (draft)
- **Primary:** mean chains per life on fresh CW2 lands, **GOAL − FT-NOGOAL**, paired by seed, 95% bootstrap.
- **Retirement test (the roadmap's rule):** GOAL − CW2's GUIDE-REFLEX, non-inferiority (lower end above −0.2 chains):
  if passed, the carry reflex can be retired.
- **Arbitration:** GOAL-NOFLOOR − GOAL in chains and in survival (no-loss: survival lower end above −0.03).
- **No-loss gates:** the Bob Profile of each fine-tuned walker vs its RMS parent (no test worse beyond its margin);
  survival on plain W3r lands (no things) GOAL − RMS above −0.03; an unseen evaluation world (a CW2 land layout with
  the station look and A/B looks drawn from codes never used together before) (roadmap rule).
- Secondary: GOAL − SHAM-GOAL; how strongly the walker follows the goal layer (share of steps toward the goal while g
  is high); g's learned weight.

## Checks before data
Exact zero check (all new weights 0: every arm's walker reproduces RMS bit for bit in CW2 lives with the goal layer
present); the goal layer marks only experienced-value places; fine-tuning with a zero learning rate changes nothing;
the reward is the old drive reward, unchanged (code diff); determinism.

## Compute and the cloud credits
Fine-tuning length set by a pilot on 2 seeds (the shortest that gives a stable value loss), at most 1M steps per run;
4 arms x 16 seeds of fine-tuning (W3-type training runs ~4M steps in 14-18 h, so 1M about 4 h): about 64 runs x 4 h =
256 VM-hours, about 11 h on 24 VM threads. Credits end about 19-20 Dec: start within days. Fallback: checkpoint every
100k steps and download nightly, so a stop loses nothing (round-table).

## Risks written now
- The body reward counts energy only below 150 of 200 (the drive's set point), so a meal of C eaten when fed gives
  little reward: the walker may learn the goal only when it is somewhat hungry. This is the body's law; not changed.
- Fine-tuning may cost old abilities (forgetting): the Bob Profile and plain-land gates catch it.
- First discovery of the join stays by chance (CW2); this study is about reuse.

## Expected (before data, the assistant's guess)
GOAL − FT-NOGOAL above 0: about 60%. GOAL non-inferior to the carry reflex: about 30%. No-loss gates passed: about 60%.

## Questions for the council
1. A sixth layer plus a goal level g with zero-initialised weights and adult fine-tuning: a fair way to add a goal part
   to a trained walker, or should it be a new childhood (about 18 h per brain)?
2. Is FT-NOGOAL (same training, empty goal layer) the right control, and SHAM-GOAL the right sham?
3. The arbitration sub-test (removing the floor for the goal only): enough for "learned arbitration", or a separate
   study?
4. Is "non-inferior to the carry reflex within 0.2 chains" a sensible retirement bar?
5. The drive reward counts energy only below 150: a problem for learning goals, and if so what to do without changing
   the body's law?
