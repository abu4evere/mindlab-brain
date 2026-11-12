# W1c: spatial structure. Findings (12 November 2026)

**Status:** valid (code checks pass; W1b's controls are the reference); all 92 runs present. No blind recompute:
this is a workbench test, and its numbers are in `output/` for anyone to check.

## The frozen readings: every brain "mixed", none "navigates" at 30,000 episodes
| brain | control | empty room | efficient detour | pocket | imitation accuracy (test) |
|---|---|---|---|---|---|
| W1b's flat net imitating B (reference) | 0.08 | – | 0.00 | 0.00 | 0.43 (one seed) |
| E (egocentric, actor-critic) | 0.01 | 0.02 | 0.00 | 0.00 | 0.22 |
| E-imit (egocentric, imitation) | 0.22 | 0.27 | 0.01 | 0.01 | 0.52 |
| C (convolution, actor-critic) | 0.02 | 0.03 | 0.00 | 0.00 | 0.22 |
| **C-imit (convolution, imitation)** | **0.73** [0.65, 0.78] | **0.78** | 0.15 | 0.02 | **0.74** |
| C-dag (convolution, DAgger) | 0.68 | 0.77 | 0.13 | 0.02 | 0.72 |

## The 100,000-episode check (4 seeds, secondary)
- **C learns from reward alone, given time:** control 0.76, empty room **0.95**. At 30,000 episodes it had learned
  nothing.
- **C-imit:** control 0.85, empty room 0.86, efficient detour **0.34**.
- **E (no convolution):** still nothing (control 0.02).

## What it means (the assistant's reading)
1. **The convolution is the brain part that was missing for navigation.** The same small filters applied everywhere
   take imitation from 0.08 (W1b, flat) to 0.73 on the controls in the same budget. The egocentric view alone gives
   0.22. With enough experience (100,000 episodes) the convolutional brain learns to walk to food **from reward alone**
   (0.95 in empty rooms). The flat network never does.
2. **Navigation is not looking ahead.** Even the best brain takes the short way round a barrier only a third of the
   time, and almost never escapes a pocket (0.02). Pattern-matching walls nearby is not planning a route. GPT
   predicted this as "the most informative outcome".
3. **DAgger did not help** over plain imitation here (0.68 against 0.73 on the controls).
4. **For the five projects:**
   - **ACL:** the people's brain is a flat network, the kind that cannot learn to walk to visible food. A
     convolutional view of the nearby land (food, water, kin) is the brain part that could let the network, not the
     old instincts, find food. Round 86's option (d).
   - **Mind Lab:** looking ahead needs more than perception. The next workbench test (W1d) should add an iterative
     part: a learned value-iteration layer, or a small recurrent planner run for several steps before acting.
