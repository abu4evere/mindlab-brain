# W1c: does spatial structure let a network learn to navigate, and then to detour? (frozen plan)

**Frozen** as git tag `W1c-frozen` (Mind Lab), before any code or data. The network code (`nets_c.py`) was written and
gradient-checked before the freeze; no network has been trained.
**Sign-off:** the creator, 11 November 2026: "go ahead with w1c".
**Draft:** `../W1c_draft.md`. **Council:** GPT (chat 6af53925) and Gemini (chat 112218f0).

## The council, in short
- **Both:** test the egocentric view and the convolution before a learned planner; the most informative outcome would
  be "navigates but does not look ahead".
- **GPT** (probabilities: E-imit controls 60%, C-imit 75%, looks ahead 20%, actor-critic controls 25%):
  - a pre-set 100,000-episode check;
  - a learning audit (training and held-out action accuracy);
  - held-out wall topologies;
  - an empty-room navigation check;
  - matched demonstrations.
- **Gemini** (65%, 80%, 20%, 25%):
  - a deeper convolution so the receptive field covers the room;
  - imitation that asks the planner about the states the learner itself visits (DAgger), against drift;
  - walls outside the area encoded as 1;
  - a geometric holdout.
  - Gemini also suggested a lower learning rate. **Not taken:** the updates are plain gradient steps with the
    gradient norm clipped at 1.0, so each step is already at most 0.01 long; W1b's settings are kept for comparison.

## Kept from W1b (unchanged)
The world, the 400 learning and 240 test layouts (`W1b/layouts.json`), the scripted controls and their results, the
measures (efficient detour within 1.15 × the shortest, pocket, control, first 3 moves), the readings and the validity
rule.

## New probe sets (made before any training, seed 20261118; probes only, never learned from)
- **Empty rooms:** 60 layouts with no inner walls (start and food at least 4 apart). This is the navigation check.
- **Held-out topologies:** 60 detour + 60 control layouts from three families never seen in learning:
  - "zigzag": two offset bars forming an S-corridor;
  - "hook": a cup with an inward hook at one tip;
  - "comb": a bar with three teeth on one side.
  Drawn by W1b's rules, without the adversarial filter.

## The brains (16 seeds each unless stated)
| brain | input | network | learning |
|---|---|---|---|
| **E** | egocentric 21 × 21, two channels (walls with outside = wall, food) | 882 → 64 tanh → 5 + value | actor-critic |
| **E-imit** | as E | as E | imitation of B on B's paths (W1b's rule) |
| **C** | as E | **conv** 3 × 3 (2 → 8, padding 1) → ReLU → 3 × 3 stride 2 (8 → 8) → ReLU → **3 × 3 stride 2 (8 → 16)** → ReLU → 4 × 4 × 16 = 256 → 64 tanh → 5 + value | actor-critic |
| **C-imit** | as C | as C | imitation of B on B's paths |
| **C-dag** | as C | as C | **DAgger:** each episode, a learning layout is walked with B's move (chance ½) or C's own best move (chance ½); every visited state is labelled with B's move from there; one update (cross-entropy) per episode |

- **Settings as W1b:** 30,000 episodes, learning rate 0.01, gradient-norm clip 1.0, γ 0.97, entropy 0.01.
- **The 100,000-episode check** (pre-set, secondary): E, C and C-imit, 4 seeds each (seeds 1–4), 100,000 episodes.
- **The learning audit:** every 3,000 episodes, the training success (actor-critic). At the end, imitation accuracy
  (matches B's move) on 100 learning and 100 test layouts, for every brain.

## Readings (frozen; W1b's rules)
- **Per brain:** "looks ahead" (efficient detour ≥ 0.80, pocket ≥ 0.70, above G), "reactive" (control ≥ 0.80 and
  efficient detour ≤ 0.60), or "mixed".
- **Navigation:** a brain "navigates" if its control success ≥ 0.80 **and** its empty-room success ≥ 0.90.
- **Held-out topologies:** efficient detour success there, reported beside the main one, for every brain that looks
  ahead on the main test.
- **Statistics:** means over 16 seeds with 95% bootstrap intervals (10,000 draws, NumPy seed 20261118).
- **Validity:** W1b's scripted results stand (valid); the code checks (`checks.log`) must pass.
- **Even a pass is behaviour, not proof of an internal look-ahead.**

## The assistant's prior
- E-imit navigates: about 50%. C-imit navigates: about 65%. C-dag navigates: about 75%.
- Any brain looks ahead: about 20% (most likely C-dag).
- Actor-critic brains (E, C) navigate at 30,000: about 20%; at 100,000: about 35%.
