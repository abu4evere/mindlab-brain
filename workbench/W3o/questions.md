# W3o: raw eyes (plan, to be frozen before any study data)

**Frozen** as git tag `W3o-frozen` (20 Nov 2026), after the council.
- **Sign-off:** the creator, 20 Nov 2026, on the living-brain picture ("so our current brain more specialized for its
  own world right ... does that mean we ain't building itself"), choosing this test: "yes u can go ahead with first one".
- **Council:** GPT and Gemini, asked neutrally (`../W3o_council_2026-11-20.md`). Gemini answered (taken: bare co-primary,
  RV framed as a ceiling test, swap check on RE only, deaths per 1,000 steps). GPT answered (taken: the probe of
  object-directed moves, the swap defined exactly, median and early deaths; named: the parent also reads sorted memory,
  a second privileged channel; 8 seeds are a pilot, an important comparison may be extended later).
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
1. **Two primary readings, both on RE (Bonferroni, 97.5%), on test-land lifespan** (Gemini: the reflexes read the
   sorted memory and could carry a blind brain, so the brain alone is co-primary):
   - **RES-bare − HRS-bare** (both reflexes off: can the brain see through mixed colours by itself?);
   - **RES − HRS** (its real life, reflexes on).
   - Margin fixed now: a loss is **small** if the interval's lower bound is above −200 steps; **real** if its upper bound
     is below 0.
2. **RV is a ceiling test, not a fair test** (Gemini): a fixed linear 3 × 3 first layer gives every colour the same
   average meaning across lands, so RV asks whether anything else (shape, place, the planner) can make up for it. Its
   readings, RVS-bare − HRS-bare and RVS − HRS, are reported at 95%, expected to be a large loss.
3. **Secondary (95%):** RE − HR and RV − HR (the ends); RVS − RES; **the manipulation check, RES-swap − RES** (RE only:
   expected below 0; if it is not, RE's brain is not using the colours and its result says little about eyes);
   deaths per 1,000 steps, median lifespan and deaths before step 1,000 for every arm (lifespan is capped at 3,000);
   **the probe** (GPT; `probe_w3o.py`, frozen): with the map memory fully known and no reflex, on the 50 test lands, the
   share of first moves toward the nearest food when hungry (energy 60) and toward the shelter when tired (tiredness
   150), for HRS, RES, RVS and RES-swap; RES − HRS and RVS − HRS per state (paired by seed). Checked on W3n's HRS before
   any W3o data: toward food 0.87 (chance 0.29), toward the shelter 0.76 (chance 0.35), 7 seeds.
   - **The swap, exactly:** at test only, the colour code of wall and of food are exchanged (food cells shown as 110,
     walls as 011; the shelter unchanged). It is a check for RE only: RV is trained on changing colours, so it may
     rightly ignore a swap (GPT, Gemini).
4. Fresh-land survival of RES and RVS (reflexes on and bare) against the 0.80 bar, with intervals.
5. **Machines:** runs on the PC and on the Google Cloud VM do not train bit-identically (Windows and Linux; the same
   code trains identically again on the same machine). Each run's machine is recorded; every run is a valid sample.

## Validity (hard stops)
Checks All: PASS before data (`checks_w3o.py`: settings; arms; sorted eyes = W3n's HR bit for bit; the colour layers
each cover two kinds and give back the sorted layers exactly; the body acts the same with any eyes; RV deals all six
colour orders and the same land always the same; RE and RV train differently, split = unsplit, repeatable; a staged
run saves its copies and runs every test including swap, and writes nothing into W3n's folder).

## The assistant's prior
- RES − HRS lower bound above −200 (mixed colours cost little): about 65% (Gemini 55%); bare, about 50%.
- RVS − HRS upper bound below 0 (changing colours cost a real loss): about 75%.
- RES-swap − RES below 0 (the brain uses colours): about 80%.
- RVS fresh-land survival at or above 0.80: about 15% (Gemini 5% bare / 45% reflexes on; GPT 25%).
- GPT: RE costs little 75%, RV a real loss 85%, swap passes 65%. Gemini: 55%, 92% (bare), 85%.
