# W3o: raw eyes (plan, to be frozen before any study data)

**Status:** draft; to be frozen as git tag `W3o-frozen` after the council.
- **Sign-off:** the creator, 20 Nov 2026, on the living-brain picture ("so our current brain more specialized for its
  own world right ... does that mean we ain't building itself"), choosing this test: "yes u can go ahead with first one".
- **Council:** GPT and Gemini, asked neutrally (`../W3o_council_2026-11-20.md`); the Chrome extension was not connected
  when this draft was written.
- **Exploratory,** in the W3 series. **Local runs only** (the PC; never GitHub Actions).

## Why
The brain's eyes give it a sorted world: one layer each for walls, food and shelter. Its links from hunger, tiredness
and curiosity to those layers start at zero and are learned, so it already learns which layer feeds it. But the
sorting itself is ours. A baby does not get a "food" layer; it sees colours and shapes and learns what they mean.
**Does the brain still work when its world is not sorted for it?**

## Arms (`w3o.py`: W3n's HR exactly, the best brain so far, except what the brain sees; seeds 1–8, paired with HR's)
| arm | what the brain sees instead of the wall, food and shelter layers |
|---|---|
| **RE, mixed colours** | three colour layers: wall 110, food 011, shelter 101, floor and never-seen 000. Each layer is on for two kinds of thing, so no layer means one thing. The same information as before (an exact linear mix), so the brain *can* untangle it; the question is whether it learns to. |
| **RV, colours that change** | the same three colours, dealt to wall, food and shelter at random on each land (from the land's seed). Colour means nothing across lands; only shape and place (food in 2 × 2 patches, the shelter one cell, walls in lines and the border) and what happens there tell them apart. |
| HR, HRS, HRS-bare (W3n, cited) | the sorted eyes; with eyes "sorted", `w3o.py` trains W3n's HR bit for bit (checked) |

- Unchanged: the unseen and staleness layers; the map memory itself; the body's sleep and hunger reflexes (they read the
  world's own memory, so the body still "knows" food: a limit of this test, named here); the parent (W3's Script);
  4.0M steps, 2.4M fade, the kept copies (S, Y); the test lands and the fresh lands.
- Each kept copy is also tested **bare** (both reflexes off: what the brain does on its own), **S-off** (hunger reflex
  off), and **swap** (a test-only check: the wall and food colours exchanged; a brain that uses what colours mean
  should do worse).
- Seeds 1–8 per arm (16 runs of 4.0M steps, about 14 hours each on the PC, up to 7–8 at once, after W3n's runs).

## Readings (`analyse_w3o.py`, frozen; paired by seed with W3n's HR; bootstrap over 8 seeds, numpy seed 20261220)
1. **Two primary readings (Bonferroni, 97.5%), on test-land lifespan:** **RES − HRS** and **RVS − HRS**.
   - Margin fixed now: a loss is **small** if the interval's lower bound is above −200 steps; **real** if its upper bound
     is below 0.
2. **Secondary (95%):** RES-bare − HRS-bare and RVS-bare − HRS-bare (the brain alone); RE − HR and RV − HR (the ends);
   RVS − RES; **the manipulation check, RES-swap − RES** (expected below 0; if it is not, RE's brain is not using
   the colours and its result says little about eyes).
3. Fresh-land survival of RES and RVS against the 0.80 bar, with intervals.

## Validity (hard stops)
Checks All: PASS before data (`checks_w3o.py`: settings; arms; sorted eyes = W3n's HR bit for bit; the colour layers
each cover two kinds and give back the sorted layers exactly; the body acts the same with any eyes; RV deals all six
colour orders and the same land always the same; RE and RV train differently, split = unsplit, repeatable; a staged
run saves its copies and runs every test including swap, and writes nothing into W3n's folder).

## The assistant's prior
- RES − HRS lower bound above −200 (mixed colours cost little): about 65%.
- RVS − HRS upper bound below 0 (changing colours cost a real loss): about 75%.
- RES-swap − RES below 0 (the brain uses colours): about 80%.
- RVS fresh-land survival at or above 0.80: about 15%.
