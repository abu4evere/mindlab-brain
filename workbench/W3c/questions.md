# W3c: when a need is strong, it takes over (plan, frozen before any code or data)

**Frozen** as git tag `W3c-frozen`, before any code or data.
- **The creator** (15 November 2026, about 18:5x): "go ahead", to "fix the drowned hunger … a part where a strong need
  takes over its attention, plus a fair remembered-food memory".
- **Exploratory, as the Mind Lab series since WN:** the creator asked directly, so there is no council. This is noted
  as a weaker footing than W3 and W3b, which had councils.

## Why
- **W3b found** that at hungry steps of W3's D3i (the brain given hunger → food), the hunger part of the reward map
  was about 0.009 per open cell. The drive-free base map W₀ was 0.875 and curiosity 0.551, so hunger was drowned.
  Even walking straight down D3i's value map died (0.000).
- **W3b's engineered ceiling (F) also died, because it walked back to the cell last eaten at,** which is empty for 200
  steps. A fair ceiling walks to food remembered as full, as W3's Script does (0.96).

## The new part: the need gate (G)
**In the reward map,** a strong need turns down everything that is not about it:

  r_map = (1 − g)·conv(W₀, map) + s·conv(W_s, map) + f·conv(W_f, map) + c·(1 − g)·conv(W_c, map) + b,
  with **g = max(s, f)** (0 when fed and rested; 1 when starving or exhausted).

- No new numbers are learned or tuned.
- The gate is a body-level property: when the need is strong, the rest of the world matters less.
- Gradients run through the gated map exactly (the gate depends only on the drive levels).

## Step 0c (test only; W3's saved weights; written down before it runs)
1. **D3i + gate:** W3's 8 trained D3i brains, tested with the gate on. This is W3b's step 0 with the gate:
   - (a) the learned head;
   - (b) the greedy walk down the value map;
   - (c) the one-step look-ahead walk;
   - on W3's 50 test lands, survival to 3,000.
2. **F2, the fair ceiling** (engineered, labelled; test only, on W3's D3 weights):
   - when hunger is high (s ≥ 0.2) and the map memory holds a cell remembered as full food, walk by the shortest path
     (W3's `bfs_path`) to the nearest such cell;
   - when fatigue is high (f ≥ 0.4) and the shelter is known, walk to it;
   - otherwise W3's D3 acts.

## Trained arms (W3's world, drives, training and test; 8 seeds each, 2,000,000 steps, on GitHub's machines)
| arm | what |
|---|---|
| **G** | D3 + the gate (links learned from zero) |
| **GYFR** | D3 + the gate + W3b's "that worked!" (Y) and rest replay (FR), unchanged |
| **Gi** | D3i (the designer's links, fixed) + the gate, trained |
| **Z0** | D3 with no gate, but W₀ starts at zero instead of N(0, 0.3) (the other way to stop the drowning) |

The references are cited, not re-run: W3's D3 and D3i, and W3b's Y+FR.

## Measures and readings (as W3 and W3b; 95% bootstrap intervals over the 8 seeds, paired, numpy seed 20261129)
- Survival to 3,000 (primary), survival to 1,000, lifespan, land known, time hungry and exhausted, found share.
1. **"The gate un-drowns hunger"** (step 0c): D3i + gate, walk (b) or (c), survives ≥ 0.50.
2. **"The fair ceiling is reachable":** F2 survives ≥ 0.50.
3. **"A learned brain lives":** G, GYFR or Gi survives with mean ≥ 0.50 and lower bound ≥ 0.30.
4. **"The gate helps":**
   - G − D3 and Gi − D3i on survival (or, if every survival is 0, on lifespan), lower bound above 0;
   - and GYFR − W3b's Y+FR the same.
5. **"Gate or quiet start":** G − Z0 on survival (or lifespan), reported with its interval.

## Validity (hard stops)
- **Checks All: PASS before data:**
  - with the gate off and W₀ random, the class reproduces W3's planner exactly;
  - the gated map's gradients match finite differences;
  - at g = 1, W₀ and W_c have no effect on the map;
  - Gi's links stay fixed through training;
  - Z0 starts with W₀ = 0;
  - F2 walks only to cells remembered as full;
  - a split run equals an unsplit run;
  - the same seed twice is the same.
- Every run finishes. Any that does not is reported, never refilled.

## Limits (stated now)
- W3's one world and body. The gate is one fixed form (max of the two needs); not tuned. No council.

## The assistant's prior
- **Reading 1** (D3i + gate walks alive): about 40%.
- **Reading 2** (F2 ≥ 0.50): about 70%.
- **Reading 3** (a learned brain lives): about 15%.
- **Reading 4** (the gate lengthens life with an interval above 0): about 55%.
- **Z0 against G:** no clear difference: about 50%.
