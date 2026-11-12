# W1: the detour. Findings (11 November 2026)

**Reading: not valid. The frozen controls failed, so nothing is concluded about any brain.**

## What happened
- **The scripted brains** ran first (one run each, on the 240 test layouts):

  | brain | detour | pocket | unseen shapes | control | path ratio | frozen reading |
  |---|---|---|---|---|---|---|
  | G (greedy) | 0.000 | 0.000 | 0.000 | 0.917 | – | reactive |
  | **W (wall-follower)** | **1.000** | **1.000** | 1.000 | 1.000 | **1.44** | **looks ahead** |
  | B (planner, true map) | 1.000 | 1.000 | 1.000 | 1.000 | 1.00 | looks ahead |
  | M (planner, own map) | 1.000 | 1.000 | 1.000 | 1.000 | 1.00 | looks ahead |
  | M− (own map, no planning) | 0.792 | 0.725 | 0.700 | 0.983 | 1.27 | neither |

- **The validity rule needed W *not* to pass.** It passed every part of "looks ahead": the pockets did not trap it,
  and its median path stayed under the 1.5 bound.
- **So the test cannot tell wall-following from looking ahead.** This is exactly the risk both councils named. The
  learning brains (F, R, F-imit) were not run: their numbers could not be read.

## What it teaches
- **With a 5 × 5 view, looking ahead and wall-following can hardly differ.** Neither can see which way round the wall is
  shorter, so both must explore. M's planning gained little over W here (path ratio 1.00 against 1.44, but both
  solve everything).
- **The pockets were too easy.** They sat on the outside of the cup's base. The plan's "on the side facing the agent"
  was not forced (IMPLEMENTATION.md).
- **M− (memory of the map, no planning) already solves 79%.** Remembering where one has been goes a long way.

## For a W1b (to the council)
- **Let the brain see the barrier,** as in the classic animal detour tasks (the goal seen through a fence): a full view
  of the 11 × 11 area. A planner can then choose the shorter way round at once. A wall-follower with a fixed hand goes
  the long way in about half the layouts.
- **Make the long way much longer** (ratio over 2), so a path bound of 1.25 separates them.
- **Put the pockets on the agent's side**, on the greedy line.
- **Keep W as the negative control.** The validity rule worked as intended: it stopped a false reading.
