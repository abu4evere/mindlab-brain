# W3r: learning a meaning within one life (DRAFT for the council; not frozen, no code yet)

- **Why:** W3o (final, 22 Nov 2026): when the colours of wall, food and shelter are dealt anew on each land (RV), the
  brain cannot work out within a life which colour is food (fresh-land survival 0.27; toward food 0.555, chance 0.29).
  The gap is fast learning within a life, an approved direction ("fast learning within a life", CLAUDE.md, 8 Nov).
- **Sources:** `D:\acl\docs\research\learning_meaning_within_a_life_2026-11-22.md` (Miconi et al. 2018, differentiable
  plasticity; Wang et al. 2016, meta-RL).
- **Order:** after W3q's runs (compute). Council first (GPT, Gemini, DeepSeek), then checks, then frozen.

## The idea (smallest version)
RV's world and W3o's RV brain (DriveVIN with colour eyes), plus **a plastic link from the three colour layers to the
feelings map**: a within-life trace h (one number per colour layer, zero at birth) is written at each meal by the
colours under the body ("I ate where it looked like this"), and adds α · Σ_c h_c · colour_c(x) to the value the
planner spreads. Slow training learns α (how much to trust the trace); the trace's speed η is fixed in advance (a
design choice to put to the council: learned η needs gradients through a whole life).

## Arms (seeds 1–8, paired with W3o's RV)
| arm | brain | answers |
|---|---|---|
| **PL** | RV + the plastic link | does a within-life trace let it learn the colour of food on each land? |
| **PZ** | RV + the link, trace held at zero | the extra parameter alone (sham for the structure) |
| **PS** | RV + the link, trace written at random steps (not meals) | the sham for the signal |
| RV, RE (W3o, cited) | changing colours / fixed colours | the floor and the ceiling |

## Readings to set before freezing
- Primary: fresh-land survival and test lifespan, PL − RV (and PL − PS), against RE as the ceiling.
- The probe of W3o (toward food when hungry), read after k meals on a fresh land (k = 0, 1, 3, 5): the within-life
  learning curve; PL should start at RV's level and rise.
- The swap check: exchanging food and wall colours mid-life; PL should recover after a few meals, RE should not.

## Questions for the council
1. Is a Hebbian trace written at meals designer help that gives the answer away, or a fair minimal learning channel
   (the world gives the signal, the brain learns how much to trust it)?
2. Fixed or learned trace speed?
3. Are PZ and PS the right shams? Is a recurrent-memory arm (Wang's meta-RL) worth adding?
4. The probe after k meals: sound?
