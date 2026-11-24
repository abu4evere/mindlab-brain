# Council on the W3r draft (24 Nov 2026): GPT, Gemini, DeepSeek

Each answer is the model's OPINION, NOT sign-off. The same question (one paragraph, below in short) went to each in a
fresh chat: is W3r a fair test of learning a meaning within one life; confounds; disagreement vs staleness; changes
before freezing; probability that RM beats RV with the CI above zero.

## GPT (chatgpt.com, fresh chat, "Instant"), opinion, not sign-off
- **Name:** "within-lifetime sensorimotor grounding through learned consequence prediction"; a narrow but legitimate
  rung: the designer chose which consequences matter.
- **Confounds:** (a) wrong negative labels, the most dangerous: not eating on a food cell does not mean it is not food
  (eligibility masks: train "fed" only where a meal could happen, "rested" only where rest could happen); (b)
  attribution: blocked belongs to the attempted cell, fed and rested to the occupied cell; (c) oracle leakage through
  the parent and reflexes (assisted, not independent grounding); (d) soft predictions vs what MoveVIN expects; (e) rare
  positive events swamped by negatives; (f) reset at each new colour mapping, including fresh-land tests; (g) knowing
  what a colour means is not knowing whether remembered food is still there; (h) choosing the kept copy on test lands
  would inflate results.
- **Disagreement:** add it, do not replace staleness (different uncertainties). With 3 binary inputs (8 patterns) 5
  linear members converge fast and can agree on a wrong answer; showing variance as an input is not Plan2Explore's
  intrinsic objective. Make it secondary.
- **Changes:** arms RV, RM, **RM-F (a random frozen module: controls for the change itself)**, **RM-T (a learned
  lookup table over the 8 colour codes instead of the linear ensemble)**, RMD, HR. Measure grounding accuracy (hidden
  true labels, for evaluation only), encounters needed per colour; calibrate the learning rate on pilot seeds by
  prediction accuracy, not survival; a secondary test with the reflexes off; survival primary, lifespan secondary;
  bootstrap over training seeds. Whole-body prediction later (it needs action and body state as inputs).
- **Probabilities:** RM > RV in mean 85%; with the CI above zero **70%** (35% without masking and correct attribution);
  RM recovers half the RV-HR gap 50%; RMD > RM significantly 20%; lookup table matches or beats the ensemble 75%.
  Verdict: approve with revisions.

## Gemini (gemini.google.com, fresh chat), opinion, not sign-off
- **Name:** "online supervised sensory-to-affordance grounding": the 3 targets were hand-matched to the 3 layers the
  brain expects, so representation discovery is solved by hand; honest only if framed so.
- **Confounds:** (a) the parent and reflex leak, "critical": they read the true memory, drive the body onto food and
  shelter and so make the module's labels, and keep the body alive even if the learned layers are garbage; fix: they
  read the learned layers, or test with reflexes off; (b) soft mid-range inputs could upset the tiny planner; (c) class
  imbalance: blocked is learned in ~10 steps, fed and rested need rare finds; a cold-start deadlock if "unknown" reads
  as "not food"; (d) colour cross-talk if floor is 000 with a bias term.
- **Disagreement:** add or gate, do not replace: staleness is what finds relocated food. Variance of 5 linear models
  with 1 step per event is mostly initialisation noise and ~1/visits; as a novelty bonus it might still work if scaled
  to staleness's [0, 1].
- **Changes:** reflexes and parent read the learned layers (or reflexes ablated at test); a diagnostic: HR fed soft
  0.85/0.15 layers; normalized LMS or recursive least squares per colour (exact for 4 numbers, no learning-rate
  tuning), outputs sharpened toward 0/1; keep the 3 targets for W3r, whole-body prediction later (it would change
  what the brain's channels mean).
- **Probability:** **65%** (above 80% if early-life finds of food and shelter are verified).

## DeepSeek (chat.deepseek.com, fresh chat, DeepThink), opinion, not sign-off
- Said first that no code was supplied, so its review is design-level.
- **Name:** "online body-affordance remapping" / "supervised consequence-to-layer translation": a useful engineering
  ablation, not open-ended meaning learning.
- **Confounds:** (a) the parent and reflexes reading the true memory (ablate, or let them read the learned layers);
  (b) soft vs binary layers; (c) sparse fed/rested labels; (d) one-step SGD, bootstrap and moving food make the module
  order-dependent (no replay or class balance); (e) the extra 60 numbers: needs a random-module control; (f) "a perfect
  module reproduces HR bit for bit is likely false" (body-consequence labels are not the true current layers; means
  are continuous); (g) the kept copy and two endpoints: one primary, chosen on validation, not on test lands.
- **Disagreement:** add, do not replace (or run both); 5 linear members of ~4 numbers each give near-zero or
  initialisation-noise variance; use a Bayesian linear posterior or a nonlinear ensemble, else the arm is confounded.
- **Changes:** fixed labels and timing; learning rate calibrated in a pilot; oracle, shuffled-label, random-module and
  true-layer controls; class balance or replay; module accuracy by age; whole body change as extra layers later; a
  power analysis for 16 seeds.
- **Probability:** **about 40%** (55-60% if the parent and reflexes are ablated and labels and calibration are fixed).

## The council (Claude), each claim checked against the code
| Claim | Who | Checked | Verdict |
|---|---|---|---|
| The parent and the hunger reflex read the true memory | all three | `W3/world3.py` Script.act reads `mem.m_food`, `mem.m_wall`; `W3n/w3n.py` line 65 reads `mem.m_food` | **True.** But it is the same in RV, the control, so RM vs RV stays fair; it does mean survival is partly the body's. Keep the bare test (reflexes off) as W3o did, named as secondary. Making the parent read learned layers would change the parent, not the eyes: not done. |
| Wrong negative labels ("not fed here" is not "not food") | GPT (most dangerous), DeepSeek | `world3.py` step: a meal needs a FULL food cell and E < EMAX; an eaten cell regrows for R steps | **True and important.** Fixed: "fed" and "rested" learn from positives and from fair negatives only (a meal was possible: E < EMAX; rest was possible: F > 0). |
| A lookup table over the 8 colour codes would match or beat the linear ensemble | GPT (75%), Gemini (RLS, exact) | RV's colours are 3 bits: 8 codes, 3 used | **Accepted.** The main module becomes a per-colour count table (the simplest learner: how often each consequence followed, on each colour, with fair negatives). The borrowed ensemble moves to a second arm. |
| "Perfect module = HR bit for bit" is false | DeepSeek | the learned layers are (prediction for the colour of each REMEMBERED cell); an oracle module that maps each colour to its true kind gives exactly W3n's sorted memory layers | **False as a claim about the check, true as a warning.** The check is defined with the oracle colour-to-kind map (not an oracle of consequences), and then it is exact; written out in the plan. |
| Disagreement should be added, not replace staleness; 5 linear members give weak variance | all three | MoveVIN has 5 fixed input layers; staleness is what finds relocated food | **Accepted.** RMD dropped from W3r (adding a 6th layer changes the brain; replacing staleness confounds). Curiosity-by-not-knowing becomes its own later study with a better uncertainty (e.g. a count-based or Bayesian one). |
| Soft inputs could upset the tiny planner | Gemini, DeepSeek, GPT | in every arm the brain trains from scratch for 4.0M steps with its own eyes (as W3o) | **Partly.** It is not a pretrained brain seeing soft inputs: it grows up with them. Still, a test-only diagnostic (HR's brain with soft 0.85/0.15 layers) is cheap: added. |
| A random or shuffled module control | GPT, DeepSeek | | **Accepted as a test-only check** (the learned layers shuffled across colours at test, like W3o's swap): it shows the brain uses what the module learned, without a whole training arm. |

Estimates: GPT 70%, Gemini 65%, DeepSeek 40%; Claude about 60% (the table fixes the main risks GPT and DeepSeek named;
the reflex leak is shared with the control).
