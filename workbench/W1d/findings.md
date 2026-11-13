# W1d: thinking ahead. Findings (12 November 2026)

**Status:** valid (code checks pass; W1b's controls are the reference); all 72 runs present. No brain "looks ahead"
or "navigates"; all "mixed". Both frozen comparisons pass.

**The PC slept for much of the day,** so the runs took about 11 hours instead of about 2. Nothing else changed.

## The frozen readings
- **Iteration matters:** V − V1 = +0.121 [+0.074, +0.167] on efficient detours. The 30-step planner beats the
  1-step version on every measure (control 0.73 against 0.19).
- **The max matters (just):** V − Vm = +0.054 [+0.001, +0.106].

## What the planner learned
- **Its value map is planner-like.** V's final value map correlates 0.71 (Spearman) with −(true distance to the food)
  over reachable cells, so value flows around walls. V1: 0.31. Vm (no max): −0.05, no map at all.
- **Thinking longer helps, step by step.** At test time V's efficient detours rise with K: 0.004 (K = 1), 0.04 (5),
  0.08 (10), 0.11 (15), 0.12 (20), 0.15 (30). Longer routes need more iterations: at K = 30, routes of 10 steps or
  less 0.21, more than 15 steps 0.07.
- **But not enough to take the short way round reliably.**
  - Efficient detours 0.15, the same as W1c's convolution network; pockets 0.04; held-out shapes 0.11.
  - The food moved mid-run: 0.47 replanned efficiently (V1 0.08).
- **Actor-critic** (V-ac): at 30,000 episodes it hardly navigates (control 0.31). At 100,000 (8 seeds) it navigates
  empty rooms (0.93) and controls (0.78), but detours stay at 0.15 (pockets 0.11).

## What it means (the assistant's reading)
1. **The right machinery, not yet trained to precision.** The planner's map is roughly right (0.71) but not exact.
   Taking the short way round needs the map right at the barrier's two ends, where a small error picks the long way.
   VINs in the literature are trained far longer and on many more maps. Our budget (30,000 episodes over 400 maps) is
   small.
2. **Iteration and the max are both needed.** Without the max (Vm), there is no map at all. With one step (V1), the
   brain is blind past its neighbourhood.
3. **For the brain we are building:** perception (convolution, W1c) and a planning layer (VIN, W1d) are the two parts
   so far. They are separate abilities, both learnable, but neither alone yet takes the efficient detour.
4. **Next on the workbench, choices for the council:**
   - (a) the same VIN with a longer budget (100,000–300,000 episodes) and more maps (is it just training?);
   - (b) a convolutional front-end feeding the VIN (perception and planning together);
   - (c) move on to memory and maps under a partial view (W2), and come back.

## Exploratory (after the data, labelled; not part of the frozen readings)
- **One seed trained 150,000 episodes** instead of 30,000 (`explore/`):
  - control 0.92, empty room **1.00** (it navigates);
  - efficient detour 0.25, pocket 0.31;
  - moving food 0.58;
  - value-map correlation 0.83 (the same seed at 30,000: 0.78, 0.14, –, 0.77).
- So more training helps, but slowly, and it does not close the gap to 0.80.
- **A likely structural cause (the assistant's reading, to test):** the VIN's 3 × 3 filters let value flow diagonally,
  cutting across a wall's corner, while the agent moves only in 4 directions. That distorts the distances exactly at
  a barrier's ends, where the short-way choice is made. A VIN whose filters are plus-shaped (the 4 moves only) is the
  candidate for W1e.
