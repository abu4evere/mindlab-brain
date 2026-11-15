# WF: a fast memory beside the slow habit (relearning after a change) (plan, frozen before any code or data)

**Frozen** as git tag `WF-frozen`, before any code or data.
- **The creator** (15 November 2026): "go ahead with your road" (after WO: the fast memory).
- **What WY found:**
  - "that worked!" (YS) plus "don't repeat a failure" (TB) finds and writes in a little of a changed code
    (B60 +0.06);
  - but the old habit blocks relearning.
- **The idea** (complementary learning systems; McClelland and colleagues, 1995, from memory): a fast memory stores
  what just worked; the slow network builds habits; the fast memory can act at once and also teach the slow one by
  replay.
- **Exploratory:** no council.

## The world (WC's, unchanged)
- p = 0.5 grown-up on days 1–30.
- Group A changes at day 31, group B at day 46.
- Single children; tests at days 30, 33, 38, 45, 48, 53 and 60.

## The fast memory (one store per child)
For each kind and lid, the last pair that opened it (set when the lid opens; marked stale when that pair fails on that
lid).

## Arms (sizes 32 and 128; 48 children each, seeds 1001–1048; GitHub's machines)
- **Base** and **TBYS:** WY's, re-run with the same code (must reproduce WY).
- **TBYS+RP, replay:**
  - each night (end of each day), every kind and lid with a fresh stored pair is copied again from the store: two copy
    steps at the full copy rate, through the lids in order (a stale lid stops the replay of that kind);
  - the store teaches the slow network offline, like sleep replay.
  - Tests use the network only.
- **TBYS+FMin, the store as a sense:**
  - 9 more inputs show the stored pair for the current lid (4 + 4 one-hot, and "fresh");
  - the network must learn to use them;
  - tests include the store (it is part of the senses).
- **WSLS, an engineered ceiling (labelled):**
  - on each lid, if the store holds a fresh pair, do it (win, stay); otherwise the network chooses, with TB's blocking
    in practice (lose, shift);
  - YS as in TBYS;
  - tests count what the whole child does, the store included.
  - It shows how much a working fast memory could give. It is not a learned brain.

## Measures (as WM and WY; 95% bootstrap intervals paired by seed; numpy seed 20261125)
- Relearning A38, A45, B53, B60; before the change A30, B45; stale habit at days 33 and 48; food.
- **Each arm − TBYS at the same size** on A45, B60, A30, B45 and food.

## The assistant's prior
- **TBYS+RP-128:** B60 above TBYS by at least 0.15: about 35%.
- **TBYS+FMin-128:** the same: about 25%.
- **WSLS-128:** B60 above 0.60: about 75%.
