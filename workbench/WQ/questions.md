# WQ: the silent room (plan, frozen before any code or data)

**Frozen** as git tag `WQ-frozen`, before any code or data.
- **The creator** (15 November 2026, about 23:2x): "If you put real human in one room for like 1 month isolated no
  time nothing just food and bathroom provided … how our agent would react to silence is it gonna react with silence
  to silence our that agent will react at least different way". Then "yes go for it".
- **Exploratory:** the creator asked directly, so there is no council.

## The room
- **W3's world (15 × 15 lands, walls, a shelter), but nothing ever changes and the body is always satisfied:**
  - energy is held at 150 and fatigue at 0, so hunger and tiredness are always 0, and no death is possible;
  - no food relocations, and no eating, so food cells never empty or regrow; the room's contents are fixed.
- **One stay** lasts 10,000 steps (W3's life is 3,000). The map memory starts empty; the brain sees its 3 × 3 view as
  in W3.
- **The only thing that can change** is what the brain does, and its own memory of when it last saw each cell (W3's
  uncertainty grows back with time unseen, τ = 200).
- **Rooms:** W3's test lands 900001, 900002 and 900003 (3 stays per brain and seed).

## The brains (W3's and W3c's trained weights; 8 seeds each)
| brain | its feelings in W3 | what that means here |
|---|---|---|
| D2 | hunger + fatigue (no curiosity) | no feeling has anything to say |
| D3 | hunger + fatigue + curiosity | only curiosity can speak |
| Dc | curiosity only | curiosity only |
| GYFR (W3c) | D3 + the recipe | only curiosity can speak |
| Rand | random moves (8 seeds) | the floor: activity with no reasons |
| Script | W3's hand-written forager (deterministic; one run per room) | it patrols the stalest cell by rule |

**Two modes for each learned brain:**
- **still:** weights fixed, as in W3's tests; it acts on what it learned;
- **living:** it keeps learning by W3's own rule (advantage actor-critic, the same settings), with the reward its
  feelings give. Here that is only curiosity (0.05 × the staleness of the cells it sees), times its curiosity weight
  (D2: 0).

## Measures (per stay, over ten windows of 1,000 steps)
- **Activity:** the share of steps it actually moved.
- **Reach:** distinct cells visited per window.
- **Pattern:** compressed size over raw size of the window's move sequence (zlib, level 9). Lower means more
  repetitive or patterned. Rand is the reference.
- **Curiosity collected per window.**

## Readings (descriptive; 95% bootstrap intervals over the 8 seeds, paired; numpy seed 20261131)
1. **"Silence to silence":** in the last 1,000 steps, does each brain still move (activity), and does activity fall
   from the first window to the last?
2. **"Curiosity keeps a mind busy":** D3 and Dc against D2 on activity and reach in the last window.
3. **"It makes patterns":** pattern (compression) in the last window, against Rand.
4. **"Living changes it":** living − still, for each learned brain, on activity and reach in the last window.

## Limits (stated now)
- W3's curiosity is defined as staleness, so the design itself pays for re-checking. A patrol here is a property of
  that definition, as much as of any brain.
- These brains have no imagination and no inner input; nothing here can show self-talk.

## The assistant's prior
- D2 keeps moving at a rate near its sampling noise (its policy is random-ish when no feeling speaks), with no clear
  fall: about 60%.
- D3 and Dc have more reach than D2 in the last window: about 70%.
- Patterns stronger than Rand (lower compression) for the curiosity brains: about 60%.
- Living makes D2 more random (the entropy term with no reward): about 50%.
