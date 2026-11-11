# Scorecard: the tests, made concrete (DRAFT, not frozen)

Written 11 November 2026 after reading Butlin, Long et al. (2023), sections 2.1–2.5 (local copy, gitignored). Their
claim, which we take over: these are **indicators**. A system with more of them is a better *candidate*. None proves
anything, and the authors do not endorse "necessary" or "sufficient". We score features and behaviour, never
"it is conscious".

Each item gets one of three marks:
- **0:** absent;
- **½:** present in the code, but no behavioural evidence that the brain uses it;
- **1:** present, and a frozen behavioural probe shows it is used (with an interval, against a control where the
  feature is cut).

## Part B: the indicators, and how we check each one

| Code | What it asks (our words) | Code check | Behavioural probe (the "cut" control) |
|---|---|---|---|
| RPT-1 | Does input processing loop back on itself over time (algorithmic recurrence)? | a recurrent layer or memory state on the input side | a task needing the past (C1's routines). Cut the recurrence: the score must drop |
| RPT-2 | Does perception build organised scenes (objects in relations), not loose features? | a representation of objects and their places | an "odd one out" or "what is next to what" probe read from the hidden state (a linear probe, against a shuffled-label probe) |
| GWT-1 | Several specialised parts working in parallel? | ≥ 2 modules with their own inputs or jobs | each module ablated in turn changes a different skill |
| GWT-2 | A small shared stage that the parts compete for, with selection? | a bottleneck smaller than the modules' total, plus a selector | the bottleneck's size matters: a wider stage changes behaviour, and the selector's choice predicts the action |
| GWT-3 | Is what is on the stage sent back to all parts, inputs included? | links from the stage to every module | cut the broadcast to one module: that module's later processing changes |
| GWT-4 | Can the brain's own state steer what gets onto the stage, to query parts in turn for a multi-step task? | a state-dependent selector | a two-step task (first ask memory, then ask sight) solved above the cut control |
| HOT-1 | Can perception run from the top down (imagination) or with noise? | a generative path, or noise in perception | it produces sensory-like states with no input (Imagine's job) |
| HOT-2 | Does a monitor tell reliable perception from noise or imagination? | a second-order part reading the first | **opt-out task:** it may skip a trial when unsure; it must do better on the trials it keeps than on all trials, above a random-skip control |
| HOT-3 | Does a general belief-and-choice system act on what it holds true, and update from the monitor? | beliefs that feed any choice | after the monitor flags a perception as noise, the brain stops acting on it |
| HOT-4 | Sparse, smooth coding (a "quality space")? | the hidden code's sparseness and smoothness | similar inputs get nearby codes; a code's distance predicts confusions |
| AST-1 | A model of its own attention that predicts and controls it? | a part that predicts where attention goes next | it pre-empts a known distractor; cut the model, the distractor costs more |
| PP-1 | Does input processing predict its input and pass on the error? | a prediction-error signal on the input side | a surprise (an expectation broken) is processed differently from the same input expected |
| AE-1 | Does it learn from feedback and pick acts for goals, balancing goals that compete? | learning from r; more than one drive | when two needs compete (hunger vs danger), its choice shifts with their sizes |
| AE-2 | Does it model how its own acts change what it senses, and use that? | a forward model (action → next input) | it predicts the result of its own act better than of the same change made by the world |

Notes from the reading:
- **RPT-1 is a weak condition** that many systems meet. The paper calls RPT-1, GWT-1 and HOT-1 plausible
  necessaries that raise the chance little on their own.
- **GWT-1 to 4 build on one another.** GWT-3 and 4 entail RPT-1. PP-1 entails RPT-1 and HOT-1. HOT-3 entails AE-1.
  The scorecard will report the chains, not just the count.
- **AE-1 and AE-2 must be written "narrowly":** about what the system computes (learns from feedback; models its
  output-to-input effects), not about its surroundings. So a body in a simulation counts.
- **IIT is left out,** as in the paper: it says no ordinary computer qualifies, so it cannot rank systems.

## Part A: autonomy (made concrete)

Each test runs as a pass or fail with an interval, against a cut control.

| # | Test | Concretely |
|---|---|---|
| 1 | Own goals | with no reward for it, does it pick a goal and keep it, and switch when the world changes? Imagine's free-goal setting |
| 2 | Looking ahead | a detour: the payoff is 3+ steps away behind a short-term cost |
| 3 | Learning from its own mistakes | a second try after a failure beats the first, with no teacher, above chance |
| 4 | Learning from others | after watching a better way, it copies it, then does better than the model |
| 5 | Curiosity | with needs met, it explores what is new more than what is known |
| 6 | Holding a project | a 4-step plan survives an interruption |

## The baseline we expect (our guess, before scoring)
- **NB2's network** (feed-forward, one critic): AE-1 ½ (learns from r, but the old instincts carry it); 0 elsewhere.
- **NB3 (feelings):** as NB2. The feelings are more drives, so they bear on AE-1's "competing goals".
- **C1's arms:** RPT-1 ½ to 1 for R (Elman RNN) and W (working memory); 0 for N.
- **Workbench part 2 (Mirror):** aimed at HOT-2 (the opt-out test) and GWT-2/3.

## Next
1. GPT's view, labelled as GPT.
2. A council.
3. Freeze the probes and their controls.
4. Score.
