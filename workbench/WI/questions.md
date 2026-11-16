# WI: imagination in the silent room (plan, frozen before any code or data)

**Frozen** as git tag `WI-frozen`, before any code or data.
- **The creator** (16 November 2026, about 00:2x): "yes add it", to "an imagination part … then the silent room
  again".
- **Exploratory:** the creator asked directly, so there is no council.
- **Scope:** imagination only. The "getting-better" (learning-progress) curiosity is left for the next study, to keep
  one change at a time.

## Why
WQ found that no brain fell silent, but none invented anything either. The recipe brain paced a tight loop. Inventing
seems to need an inner source of input.

## The imagination part (engineered, labelled)
- **A dream:** every 500 steps of room time, the brain dreams for 200 imagined steps.
- **The imagined world is built only from its own memory:**
  - the walls it remembers, with unknown cells imagined open and the border always wall;
  - the shelter where it remembers it (or a random remembered open cell if unknown);
  - **three food patches placed at new random spots** (recombined, not remembered);
  - an imagined body: energy drawn uniformly from 40–150, fatigue from 0–150;
  - it starts where it stands.
- **In the dream it acts and learns** by its usual rule: W3's advantage actor-critic and W3's reward, including
  hunger relief. The real room does not change.
- **Draws:** the dream's own stream `[seed, 51]`.

## The room and brains
- **WQ's silent room:** needs held at 0, nothing eaten or moved, 10,000 steps; room 900001 only.
- **The brain:** W3c's GYFR (the recipe brain, with its need gate active in dreams), 8 seeds, always learning
  ("living").
- **Arms:**
  - **L:** the room, living, no dreams (WQ's GYFR living, re-run on room 900001);
  - **IM:** the room, living, with dreams.

## Measures
- **In the room** (WQ's, per 1,000-step window): activity, reach, pattern.
- **In the dreams:** food eaten per dream, from the first 5 dreams to the last 5.
- **After the room:**
  - each brain, its weights as they leave the room, is tested on W3's 50 test lands (learning off, as in W3);
  - survival to 3,000 and lifespan;
  - reference "Pre": the same seeds before the room (W3c's own GYFR test).

## Readings (descriptive; 95% bootstrap intervals over the 8 seeds, paired; numpy seed 20261132)
1. **"Imagination changes life in the silent room":** IM − L on reach, activity and pattern in the last window.
2. **"Dreams keep the skill alive":** after the room, IM − L on lifespan; and IM − Pre.
3. **"Dreams get better":** food per dream, last 5 against first 5 (IM).

## Limits (stated now)
- The imagination is engineered: a world simulated from the brain's own map memory, not a learned model. It shows
  what an imagination would do, not that one can be learned.
- One room; 8 seeds; fixed dream length and frequency.

## The assistant's prior
- IM has more reach and a less repetitive pattern than L: about 55%.
- IM lives longer than L after the room: about 55%; longer than Pre: about 40%.
- Dreams get better: about 60%.
