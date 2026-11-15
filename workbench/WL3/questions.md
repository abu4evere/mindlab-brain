# WL3: does forgetting still help in a richer world? (plan, frozen before any code or data)

**Frozen** as git tag `WL3-frozen`, before any code or data.
- **The creator** (15 November 2026): "alr go ahead we gotta work like yesterday find something useful", after the
  morning report's item 2 ("forgetting in a richer world").
- **Why:**
  - WL and WL2 found that forgetting the showing before trying stops the parrot. A memory wiped before each try (Linf)
    learned perfectly in WN's world (6 kinds, 2 lids).
  - Rohde and Plaut (1999) found that limited memory hindered learning in a richer task
    (`D:\acl\docs\research\mindlab_sources_2026-11-15.md`).
  - Before "forget the showing" becomes a design rule, it is tested in richer worlds.
- **Exploratory:** no council.

## The worlds (WN's teaching: a showing before every try on days 1–30; none after; 60 days; codes never change)
- **K6L2:** WN's world (6 kinds, 2 lids, 3 tries per kind per day). The reference; WL2's numbers are not re-used, the
  arms are re-run here with the same code.
- **K24L2, more things:** 24 kinds, 2 lids, 3 tries per kind per day.
- **K6L3, longer sequences:** 6 kinds, 3 lids (each lid its own pair of 4 acts, in order; the three lids differ),
  3 tries per kind per day.
- Everything else is WS's: looks N(0, 1) per kind with noise 0.2 per encounter, copy rate 0.5, learning rate 0.05,
  WS's learning rule and tests.
  - Codes and looks come from `ws.Home` with the world's numbers of kinds and lids.
  - The lid input already has 3 places (WS's MAXL = 3).

## Arms (WL2's episodes; memory children of 32 and 128 neurons; 24 children each, seeds 1–24)
- **L0:** perfect memory of the showing.
- **L2:** wait 8 with noise 0.6.
- **Linf:** the memory wiped before each try (the copy step also without the showing in memory).

## Measures (descriptive; 95% bootstrap intervals over seeds, paired; numpy seed 20261126)
- Own skill (all lids, no showing) at days 15, 30 and 60; after a showing at day 30; lifetime food.
- **Linf − L0 and L2 − L0, at each size and world,** at days 30 and 60.
- **Floor rule (set now):** a world is "not readable" if every arm at both sizes has own skill below 0.10 at day 60.

## The questions
1. Does Linf still beat L0 at day 30 in K24L2 and K6L3 (interval above 0)?
2. Does Linf still reach the final skill (day 60), or does it fall below L0 there?

## The assistant's prior
- **Q1:** Linf above L0 at day 30, in both richer worlds, at size 128: about 60%.
- **Q2:** Linf at least as good as L0 at day 60 (interval not below −0.05), in both richer worlds, at size 128: about
  55%.
- At least one richer world at the floor: about 25%.
