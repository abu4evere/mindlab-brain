# GPT's view of the scorecard draft (11 November 2026)

**Labelled as GPT** (ChatGPT, chat 6af41dcb, Thinking medium). These are its opinions, not verified sources. The
question was `tests_draft.md` with four questions.

## Its verdict
"Strong foundation, but I would not freeze it yet." Several probes show a useful ability without showing the mechanism
the indicator asks for.

## Weak probes, and its fixes
- **RPT-1:** a feed-forward net with stored inputs passes. Fix: require recurrence within perception, against a
  history-matched feed-forward control. **So C1's W (a window of 4) should not get RPT-1 automatically.**
- **RPT-2:** a linear probe can decode places from raw features. Fix: unseen object–relation combinations, including
  swaps that keep the single features.
- **GWT-2:** fix with two modules competing under limited capacity; change their priorities; measure selection and
  interference.
- **GWT-3:** fix by giving new information to one module and testing whether another uses it through the workspace.
- **GWT-4:** a fixed "memory, then sight" order could pass. Fix: randomise which module must be asked first.
- **HOT-1:** noise alone passes. Fix: conditional, structured generation from learned beliefs (kept apart from the
  paper's minimal condition).
- **HOT-2:** a confidence threshold passes. Fix: match coverage, measure calibration, use unfamiliar noise, and
  compare with simple confidence rules.
- **HOT-3:** a rule "noise → stop" passes. Fix: graded belief revision, with effects on several different acts.
- **HOT-4:** smooth codes are common. Fix: sparse codes whose similarity and confusions carry over to held-out inputs.
- **AST-1:** a learned "avoid the distractor" rule passes. Fix: it must predict its own attention in new conditions,
  and that prediction must improve control.
- **PP-1:** fix by requiring prediction errors to update earlier processing, and by cutting that path.
- **AE-2:** fix with counterfactual predictions of its own acts, and evidence that the model guides control.
- **Part A, learning from others:** test selective copying (a reliable vs an unreliable demonstrator), then adapting
  when the task changes.
- **Part A, curiosity:** test choosing an informative observation over an equally novel but useless one.

## The 0 / ½ / 1 marks
Sound for tracking evidence, with sharper definitions:
- **0:** the mechanism or its structure is absent;
- **½:** implemented, but the causal evidence is missing or inconclusive;
- **1:** a preregistered probe passes against proper controls.

Also:
- record failures separately;
- **never add the 14 marks into one score** (they overlap and differ in weight);
- report effect sizes, intervals and the exact ablation with each mark;
- use positive controls, so that a failed probe does not just mean a broken probe.

## What it would add (autonomy)
- **Goal ownership vs reward:** audit every reward and hard-coded drive, since a novelty reward can look like an
  invented goal.
- **Open-ended adaptation:** train in one world, test in one with changed causes, tools and chances.
- **Causal understanding:** let the agent intervene to find which of two correlated events causes the other.
- **Baselines:** scripted and model-free RL baselines for all of these, not just chance.

## Its single most important test: "the Unassigned Problem Test"
A new environment, ordinary needs, and no task-specific objective. The agent should:
1. notice a problem or an opportunity;
2. form a goal unprompted;
3. plan several actions;
4. meet an unexpected obstacle;
5. revise the plan from new evidence;
6. complete, abandon or change the goal for an intelligible reason.

It should be run in held-out environments with the success criteria hidden, against scripted, reactive and
reward-driven baselines. "This is not a consciousness test."

## The assistant's note
- **Taking most of it.** The biggest changes:
  - RPT-1 needs true recurrence (W does not count);
  - positive controls;
  - no total score;
  - the Unassigned Problem Test as Part A's headline. It fits Imagine's "own goals" plan.
- **To do before the freeze:** rewrite `tests_draft.md` with these, then a council (DeepSeek, Gemini).
