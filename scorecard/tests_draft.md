# Scorecard: the tests, made concrete (DRAFT v2, not frozen)

- **v1** (11 November 2026) came from reading Butlin, Long et al. (2023), sections 2.1–2.5 (local copy, gitignored).
- **v2** takes in GPT's view (`gpt_view_tests_2026-11-11.md`, labelled as GPT).

Their claim, which we take over: these are **indicators**. A system with more of them is a better *candidate*. None
proves anything, and the authors do not endorse "necessary" or "sufficient". We score features and behaviour, never
"it is conscious".

## The marks (one per item, never summed)
- **0:** the mechanism, or the structure it needs, is absent.
- **½:** the mechanism is built in, but causal evidence that the brain uses it is missing or inconclusive. A failed
  probe is recorded as a failure next to the ½.
- **1:** a preregistered probe passes against its cut control **and** a positive control. The positive control is a
  system built to have the feature; it must pass, so that a failure means the brain failed, not the probe.

**With every mark:** the effect size, its interval, and the exact cut.

**There is no total.** The items overlap and weigh differently. We report the chains instead (GWT-1→4; PP-1 ⇒ RPT-1
and HOT-1; HOT-3 ⇒ AE-1).

## Part B: the indicators

| Code | What it asks (our words) | Probe and its controls (v2) |
|---|---|---|
| RPT-1 | Is perception itself recurrent? | a task needing the past. Against a **history-matched feed-forward control** (the same past given as a window). A window of stored inputs (C1's W) does not count |
| RPT-2 | Organised scenes (objects in relations)? | **unseen** object–relation combinations, including swaps that keep every single feature |
| GWT-1 | Specialised parts in parallel? | each part ablated in turn harms a different skill |
| GWT-2 | A small shared stage with selection? | two parts compete under the limit. Change their priority: the selection and the interference follow it |
| GWT-3 | Broadcast back to all parts? | new information given to one part is used by another *through the stage*. Cut the stage, and the use stops |
| GWT-4 | State-steered queries for multi-step tasks? | the part to ask first is **randomised**; the brain must choose the order from its own state |
| HOT-1 | Top-down or noisy perception? | the minimal condition (noise), and separately a stronger one: structured generation from what it has learned |
| HOT-2 | A monitor telling reliable perception from noise? | opt-out with **matched coverage**, calibration, and unfamiliar noise. It must beat simple confidence rules |
| HOT-3 | A belief system updated by the monitor? | graded belief revision that changes several different acts, not one stop rule |
| HOT-4 | Sparse, smooth coding (a quality space)? | its codes' similarity and confusions carry over to held-out inputs |
| AST-1 | A model of its own attention? | it predicts its own attention in new conditions, and cutting that prediction worsens control |
| PP-1 | Prediction errors on the input side? | the errors update earlier processing; cutting that path changes perception |
| AE-1 | Learning from feedback, for competing goals? | when two needs compete, the choice tracks their sizes; **every reward and fixed drive is audited** |
| AE-2 | A model of how its own acts change what it senses? | counterfactual predictions of its own acts, which guide control (cut it: control worsens) |

## Part A: autonomy

**Headline: the Unassigned Problem Test (GPT's proposal).** A new, held-out world, ordinary needs, no task-specific
objective and no hidden task reward. The agent should:
1. notice a problem or an opportunity;
2. form a goal unprompted;
3. plan several acts;
4. meet an unexpected obstacle;
5. revise the plan;
6. end, drop or change the goal for an intelligible reason.

It is compared with scripted, reactive and reward-driven (model-free RL) baselines.

| # | Test | Concretely (v2) |
|---|---|---|
| 1 | Own goals | as above. Every reward is audited, since a novelty reward can look like an invented goal |
| 2 | Looking ahead | a detour: the payoff is 3+ steps away, behind a short-term cost |
| 3 | Learning from its own mistakes | a second try beats the first, with no teacher |
| 4 | Learning from others | **selective** copying (a reliable over an unreliable model), then adapting when the task changes |
| 5 | Curiosity | it chooses an **informative** observation over an equally new but useless one |
| 6 | Holding a project | a 4-step plan survives an interruption |
| 7 | Open-ended adaptation | trained in one world, tested in one with changed causes and tools |
| 8 | Causal understanding | it intervenes to find which of two linked events causes the other, then uses that |

Baselines for every test: chance, a scripted agent and a model-free RL agent.

## The baseline we expect (our guess, before scoring)
- **NB2 and NB3's networks:** AE-1 ½; 0 elsewhere.
- **C1's R:** RPT-1 ½ at most, since its recurrence carries memory across steps rather than within perception.
- **C1's W:** RPT-1 0, since a window is not recurrence (GPT).
- **Workbench part 2 (Mirror):** aimed at HOT-2 and GWT-2/3.

## Next
1. A council (DeepSeek; Gemini when its tab works).
2. Build the positive controls.
3. Freeze.
4. Score.
