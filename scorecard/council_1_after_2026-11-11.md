# Scorecard council 1: answers on draft v2 (11 November 2026)

- **Asked:** `tests_draft.md` (v2) with four questions: view, biggest weakness, changes before freezing, and which 2
  tests to build first.
- **GPT's view of v1** is in `gpt_view_tests_2026-11-11.md`; v2 took it in.
- **DeepSeek** was not reached: its page did not take the text.

## Gemini (chat a4645f4f), labelled as Gemini
- **View:** "a sharp, empirically grounded operationalization". The 0 / ½ / 1 marks keep "it is built in" apart from
  "it is shown to be used". Positive controls stop a broken probe from looking like a failed brain. No single score
  avoids Goodhart's law.
- **Biggest weakness:**
  - **positive-control bloat:** 14 separate reference brains could eat about 80% of the budget;
  - **goal ownership is under-specified:** without a strict rule for auditing built-in drives, reward shaping will
    "leak through as invented goals".
- **Changes before freezing:**
  - **group the positive controls into about 3 reference families:** one modular-workspace brain for GWT-1 to 4, one
    metacognitive-monitor brain for HOT-1 to 3, and so on;
  - **formalise the drive audit** for "own goals", for example a limit on the information shared between the reward
    state and the policy;
  - **state RPT-1's bounds:** the recurrence depth and a non-linear state update, so long history windows (W) or caches
    cannot pass.
- **Build first:**
  1. GWT-3 (broadcast): cheap in toy worlds, with a clear causal signal from ablations;
  2. Part A #2, the detour (looking ahead): a short-term penalty before a long-term payoff cleanly separates reactive
     agents from planners.

## Taken (the assistant)
- **Reference families** instead of 14 positive controls: workspace, monitor, predictive, and a planner.
- **RPT-1:** recurrence within perception, with a non-linear state update; a window or cache does not count.
- **The drive audit:** every reward term is listed. "Own goals" passes only if the goal's choice is not predicted by
  any listed reward term (an exact rule is to be written).
- **Build first:**
  - the detour (Part A #2);
  - GWT-3, with the workbench's two-part brain.
  - GPT's headline (the Unassigned Problem Test) stays the goal, and is built later.
