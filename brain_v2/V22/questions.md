# V2-2 Goals: FROZEN PLAN (Brain v2, step 2)

Frozen 27 Nov 2026 ~04:30 EST by the assistant under the creator's sleep-mode autonomy ("if u need permission i am
giving u right now just ask council then go ahead"; ACL docs/autonomous_decisions.md). Council: GPT, Gemini, DeepSeek
(`roundtable_v22_2026-11-27.md`); this is `questions_draft.md` revised by it.

## Question
Can Bob's own planner (the walker, W3n's DriveVIN) learn to want a place that his consequence model values, so that the
written carry reflex of CW2 can be retired?

## The part
- **Goal layer + goal level:** a sixth map layer marking the place the consequence model's EXPERIENCED value runs
  through (CW2's GUIDE rule, never the untried bonus), and a fourth level g = that value / (2 x MEAL), capped at 1.
  New weights (channel 6 of W0, Ws, Wf, Wc; a new Wg over all six channels) start at exactly 0.
- **Adult fine-tuning** from each RMS kept copy (seeds 1-16) with the walker's own actor-critic update and its own drive
  reward, unchanged (no new reward), in CW2's world (things, station, the consequence model live, the floor kept unless
  stated), with checkpoints every 100k steps.
- **Training length, fixed now and blind to chains:** a pilot on seeds 1-2 (GOAL arm) records ||Wg|| and the critic
  loss every 100k steps; the length is the first of 300k, 600k, 1M at which both changed by less than 10% over the last
  100k; 1M if neither settles. The same length for every arm and seed. Pilot runs are not reused as test brains.

## Arms (fine-tuned per seed, then tested on 50 fresh CW2 lands 990001-990050)
| arm | goal layer during fine-tuning and test | floor |
|---|---|---|
| **GOAL** | the experienced-value place | kept |
| **GOAL-NOFLOOR** (diagnostic) | same; the goal layer is shown also below the survival floor | removed for the goal |
| **FT-NOGOAL** | always empty (same training otherwise) | kept |
| **SHAM-GOAL** | a distance-matched wrong place (CW2's sham rule), same g | kept |
| **GOAL-ABLATE** (test only) | GOAL's walker tested with the goal layer and g set to 0 | kept |
| references (frozen RMS, same test lands) | CW2's GUIDE-REFLEX and NO-GUIDE | kept |

## Measures (fixed now)
- **Primary:** mean chains per life, **GOAL − FT-NOGOAL**, paired by seed, 95% bootstrap over 16 seeds (10,000
  resamples); a real gain if the lower end is above 0. Also reported without seeds 1-2 (the pilot seeds).
- **Retirement test:** the carry reflex is retired only if ALL hold: GOAL − GUIDE-REFLEX in chains, lower end above
  −0.2; survival GOAL − GUIDE-REFLEX, lower end above −0.03; the Bob Profile of GOAL's walker vs its RMS parent with no
  test worse beyond its margin.
- **No-loss gates (every fine-tuned arm):** plain W3r lands (no things) survival vs RMS, lower end above −0.03; the Bob
  Profile; an unseen evaluation world: fresh land seeds (995001-995050) with a fresh deal of looks (a different seed
  for the colour-code permutation, so A, B, C and the station wear looks in combinations never met in training).
- Secondaries: GOAL − SHAM-GOAL; GOAL − GOAL-ABLATE (does the gain need the goal input?); GOAL-NOFLOOR − GOAL in chains
  and survival; goal pursuit by energy band (share of steps moving closer to the goal while g > 0, for energy < 150 and
  >= 150); the learned ||Wg||.

## Checks before data
1. Exact zero check: with the new weights at 0 every arm's walker reproduces RMS bit for bit in CW2 lives (goal layer
   present); 2. fine-tuning with learning rate 0 changes nothing; 3. the reward is the drive reward unchanged (code
   diff against W3k's training); 4. the goal layer marks only experienced-value places (CW2's checks reused); 5. the
   sham place is never a goal-look cell; 6. checkpoints restore bit for bit; 7. determinism.

## Limits (written now)
- The consequence model chooses the destination; this tests learned pursuit of experience-derived goals, not goal
  generation or full executive control (GPT). Learned arbitration is its own later study.
- The drive rewards energy only below 150 of 200: goal learning may be confined to hungry states (reported by band);
  Gemini's hunger-scaled g is the fallback study if GOAL fails.
- Fine-tuning without a parent may erode rare skills; the gates catch it.

## Compute
4 fine-tuned arms x 16 seeds = 64 runs (+2 pilot runs); at ~4M steps per 14-18 h, 1M steps is about 4 h: about 256
VM-hours on Oracle (16 threads) and Google (8); test lives after. Checkpoints downloaded nightly (cloud credits end about
19-20 Dec).

## Expected (before data)
GOAL − FT-NOGOAL above 0: about 60%. Retirement test passed: about 30%. No-loss gates passed: about 60%.
