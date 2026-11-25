# W3r: learning what colours DO within one life (FROZEN, tag W3r-frozen)

**Sign-off:** the creator, 24 Nov 2026, in this Claude Code session: "yes go ahead freeze it and start".

**Why.** W3o: when the colours of wall, food and shelter are dealt anew on each land (RV), the brain breaks (RVS − HRS
−1,482; fresh-land survival 0.27). It cannot learn within one life "I ate where it was this colour, so this colour is
food". ACL's BX1 school showed the same gap (it learned how a week felt, not which choice caused it). The top Crafter
brains all learn a model of consequences (`D:\acl\docs\research\crafter_brains_borrow_2026-11-24.md`). The creator, 24
Nov 2026: "learn it and if there are things we should take, take it use in ours".
Earlier draft (22 Nov, a plastic colour trace written at meals, Miconi et al. 2018): `questions_v0_plastic.md`. This
plan keeps its sham for the signal (written at random steps), its learning curve after k meals and its mid-life swap.

**Honest name** (council: GPT, Gemini, DeepSeek; `gpt_review_w3r_draft.md`): *within-life grounding of colours in the
body's own consequences* (online body-affordance remapping). Not open-ended meaning: we chose the three consequences
and that they stand in for the three layers the brain already has. A first rung.

## The meaning module (body only; no names, no new rewards; reset at every birth)
Three consequences the body itself feels, each tied to the colour of the cell involved as remembered **just before**
the step (the colour memory holds what was last seen: an eaten food cell shows floor until seen full again):
- **blocked**: the body tried to step into a cell and did not move (the attempted cell's colour);
- **fed**: the body ate on the cell it stands on (its colour before the meal). A fair negative only when a meal was
  possible had the colour meant food: energy below EMAX;
- **rested**: tiredness fell on the cell it stands on. A fair negative only when rest was possible: tiredness above 0.
Steps where a consequence could not happen teach nothing about it (no wrong negatives; GPT's most dangerous risk).

Two learners:
- **Table** (the simplest learner; GPT and Gemini): for each of the 8 colour codes, counts of positives and fair
  negatives per consequence; prediction = positives / (positives + fair negatives); 0 before any fair trial (unknown is
  shown as nothing). No learning rate, no random start.
- **Ensemble** (Plan2Explore's learner, borrowed): 5 linear members (3 colour bits + bias → 3 consequences), each with
  its own seeded random start and a bootstrap mask (each event used by each member with probability 0.5), one step of
  squared error per event; prediction = the members' mean, clipped to [0, 1]. Its learning rate is set in a pilot
  BEFORE the study (pilot seeds 9001-9004, never study seeds) by how fast it ranks the food colour first; then frozen.

**What the brain sees:** in its wall, food and shelter layers, the module's prediction for each remembered cell's colour
(blocked → wall, fed → food, rested → shelter). Unseen and staleness unchanged. The brain is MoveVIN, trained from
scratch in every arm for 4.0M steps with its own eyes, exactly as W3o (W3n's HR body: both reflexes, the parent's
childhood, the kept copy).

## Arms (W3o's changing-colour lands; seeds 1-16; each machine's runs paired on that machine)
| Arm | The brain's wall / food / shelter layers | Answers |
|---|---|---|
| **RV** (control, rerun) | the 3 colour layers (W3o) | the floor |
| **RM** | the table, learned from consequences | does learning what colours do help? (primary) |
| **RMX** (sham for the signal) | the same table, but each event is credited to a colour drawn at random from the colours in view (seeded), not the cell where it happened | is it the consequence, or just having an extra learned layer? |
| **RE5** | the ensemble, learned from consequences | does the borrowed Plan2Explore learner do as well? |
| **HR** (ceiling, rerun) | the true kinds (sorted memory) | the ceiling |
Curiosity-by-disagreement is **dropped** from W3r (council: add, do not replace staleness; 5 linear members give weak
variance): its own later study, with a better uncertainty.

## Measures (as W3o)
- **Primary:** fresh-land survival of the kept copy (S): **RMS − RVS**, the paired difference over the 16 training seeds
  with a 95% bootstrap interval (10,000 resamples of seeds, seed 1). The kept copy is chosen on training lives only
  (W3k's rule), never on test lands.
- Secondary: RMS − RMXS (the sham); RE5S − RVS; RMS − HRS (the gap left); lifespan; toward-food-alone; deaths by cause.
- The bare test (both reflexes off). The parent and reflexes read the true kinds in every arm (the council's shared
  confound, named): survival is partly the body's.
- The learning curve: toward-food-alone on a fresh land after k fair "fed" trials (k = 0, 1, 3, 5); RM should start at
  RV's level and rise.
- The module itself: fair trials until "fed" ranks the true food colour first; its accuracy against the hidden true kinds
  by age (evaluation only; the brain never sees the kinds).
- Test-only checks: **mid-life swap** (food and wall colours exchanged halfway through a test life: RM should recover
  after a few meals, a fixed-meaning brain should not); **soft** (HR's brain with 0.85/0.15 layers in place of 1/0: does
  softness alone hurt?).

## Checks before data (`checks_w3r.py`, All: PASS required)
- RM with the **oracle colour-to-kind map** in place of the table reproduces HR bit for bit (the layers are then exactly
  the sorted memory; the defined check, not "an oracle of consequences", as DeepSeek warned).
- RV reproduces W3o's RV bit for bit on the same machine; HR reproduces W3n's HR.
- Labels: a scripted life that eats, rests and bumps once each gives the table exactly 1 positive in the right colour
  cell; full-energy steps on food and zero-tiredness steps at the shelter teach nothing; RMX credits a colour in view.
- The module resets at every birth and every test land; the hidden kinds never reach the brain or the module.
- Same seed, same result; split runs = unsplit runs.

## Expected (before data)
RMS − RVS lower bound above 0: GPT 70%, Gemini 65%, DeepSeek 40% (asked before the label and table fixes); the
assistant about 65%. RMS − RMXS above 0: about 60%. RE5S − RVS above 0: about 50%. RMS within 200 steps' lifespan of
HRS: about 35%.

## Compute
5 arms × 16 seeds × 4.0M steps on the Oracle VM and the Google VM (never GitHub), after W3q and BX1's test free them;
each run's machine recorded.

## Limits (named now)
1. Colours are 3 clean bits; real eyes are noisier.
2. We chose the three consequences and their match to the three layers.
3. The parent and reflexes read the true kinds (as in RV): the body helps in every arm.
4. Food moves twice per life: knowing what a colour means is not knowing where food is now (staleness still does that).

## Amendments before any study data (24 Nov 2026, recorded openly)
1. **The pilot's rule picked an unstable rate.** On pilot seeds 9001-9004 the fastest rate, 1.0, made the ensemble's
   weights diverge (to about 1e37-1e39 on every pilot land; its predictions were garbage). The rule now chooses the
   fastest among STABLE rates (every member's weights finite and at most 10 on every pilot land): **0.3** (median 7.5
   steps; 0.1: 8.0). `calib_w3r.py`, `calib_w3r.json`. The ensemble's starting spread N(0, 0.1) is a pre-data choice.
2. **"Fed ranks food first" is read only after the first meal**, so a random start cannot count as learning
   (evaluation only; the brain never sees it).
3. **A note on "fed":** a step always costs energy before the meal check, so energy is always below EMAX when a meal
   could happen: every step is a fair trial for "fed" (the rule stays as written; it only ever excludes nothing).
4. **The learning curve is read after k meals** (positive "fed" events; k = 0, 1, 3, 5), as the 22 Nov draft had it:
   every step is a fair "fed" trial (note 3), so "k fair trials" would not separate the curve. `probe_w3r.py` gives the
   module a fixed small history first (5 bumps on the wall colour, 1 rest on the shelter colour, 5 floor steps) and then
   k meals on the food colour.
5. **Keeping old abilities** (the creator, 24 Nov 2026: "Bob must retain his previous abilities while acquiring new
   ones"). After the runs, the Bob Profile (`scorecard/bp`) is run on the kept copies of RM and HR, each with its own
   eyes, and read as a secondary: does learning meanings cost any earlier ability? A loss is reported as a regression.
   *Correction (24 Nov 2026):* the quoted sentence is GPT's (from the creator's ACL chat), which the creator pasted
   and agreed with ("yes you are right"); not the creator's own words. The amendment stands.
6. **How the Bob Profile reads W3r's brains** (before any W3r data, 24 Nov 2026): `bp_w3r.py` loads them into the
   frozen tests unchanged (as W3p's bp_mv.py). Whole-life tests start each life with an empty module; single-state
   probes first give the module a fixed small history (5 bumps on the wall colour, 1 rest on the shelter colour, 5 floor
   steps, 3 meals on the food colour). W3r's HR rerun is scored as "HRr". A smoke run with a stand-in brain (W3n's HR
   seed 1, not a W3r brain) showed the module's layers then equal the sorted memory.
