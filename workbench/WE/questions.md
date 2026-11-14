# WE: genes decide how the brain grows (plan, frozen before any code or data)

**Frozen** as git tag `WE-frozen`, before any code or data.
- **The creator** (14 November 2026): "go ahead with the genes growth test", after WG.
- In WG, a hand-set schedule worked: born 16, doubling at the end of days 8, 16 and 24 to 128, with "awake in, quiet
  out" neurons. It beat being born big. Here, genes set the schedule, and evolution chooses.
- **Exploratory, as WN and WG:** the creator asked for it directly, so there is no council. Any decision drawn from it
  goes through a council later.

## The task (WG's, unchanged)
6 kinds, 2 lids, 3 tries per kind per day, 60 days, one reliable demonstrator shown before each try on days 1–30, copy
rate 0.5, learning rate 0.05, WS's tests. Every child has the memory ring. Every child gets its own world (its own
seed) and fresh random starting weights: **genes pass on, learned weights do not.**

## The genes (4 numbers, continuous)
- **a:** log2 of the neurons at birth, in [2, 8] (4 to 256 neurons; rounded to a whole number).
- **g:** log2 of how many times the brain grows by the end, in [0, 8 − a] (g = 0: no growth; final size at most 256).
- **s, e:** the first and last growth days, 1 ≤ s ≤ e ≤ 60.
- **Growth:** the brain grows evenly in neuron count from the end of day s to the end of day e, a step at the end of
  each day, rounded. New neurons are WG's "awake in, quiet out" (incoming N(0, 0.1²), outgoing zero).

## Selection (by the world's payoff only)
- **Food:** a child's food is the number of lids it opens in its own practice tries over its 60 days (the tries it
  learns from, not the tests).
- **Children:**
  - each child of the next generation picks its parent with probability in proportion to the parent's food plus 1;
  - there is no other judge, and no cost for neurons (stated as a limit);
  - no crossover.
- **Mutation:** each gene gets Gaussian noise (a and g: sd 0.25; s and e: sd 3 days), then is clamped to its range,
  with s and e reordered if they cross.
- **Size:** population 32, 30 generations, 2 independent runs (evolution seeds 1 and 2).
- **Generation 0:** genes drawn uniformly: a in [2, 8]; g in [0, 8 − a]; s and e two uniform days in [1, 60], ordered.
- **Child seeds:** 100000 × run + 1000 × generation + index, unique to each child.

## Measures (descriptive)
- **Gene paths:** each run's mean genes per generation (a, g, s, e; born size and final size), and its mean food per
  generation.
- **The evolved schedule** (each run: the median genes of the last generation) is tested on 48 fresh children
  (seeds 1001–1048), beside:
  - WG's GA (16 to 128, at the end of days 8, 16 and 24);
  - M32;
  - M128.
- **Measures of that test:**
  - own skill at days 30 and 60, and after a showing at day 30;
  - lifetime food;
  - paired differences with 95% bootstrap intervals (numpy seed 20261116, 10,000 resamples).

## Limits (stated now)
- A small population with few generations, two runs.
- The food from one child's own world is noisy, so selection is weak.
- **No cost for neurons:** in a living body brains cost energy. Without it, evolution has no reason to stay small
  except learning itself.
- Fixed learning rates; one small task.

## The assistant's prior
- **Evolution moves toward birth at about 8–32 neurons, with growth during the teaching (days 1–30), in both runs:**
  about 45%.
- **The evolved schedule beats WG's GA at day 60 (interval above 0):** about 25%.
- **The evolved schedule earns more lifetime food than M128:** about 70%.
