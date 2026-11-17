# W3h: pain. Does pain teach a growing brain to avoid harm? (plan, frozen before any code was run or data)

**Frozen** as git tag `W3h-frozen`, before calibration, checks or data.
- **Sign-off:**
  - the creator's decision on pain (16 November 2026): "for beginning there should be pain";
  - their go-ahead tonight: "go ahead bro you got this keep it pushin".
- **Council:** `../W3h_council_2026-11-16.md` (GPT, Gemini).
- **Exploratory,** in the W3 series.

## Why
Pain is a teacher, not a punishment (`../brain_v1_plan.md`). Today the brain's only bad feeling comes late: hunger,
after the energy is already gone. W3h gives it real harm and an immediate pain, and asks what the pain teaches.

## The world: W3's, plus thorns (`w3h.py`)
- **Thorn patches:** each 2 × 2, passable, drawn from a separate stream of the land's seed (`[seed, 77]`).
  - They are not placed on food, the shelter or the start.
  - Walls, food, the shelter, the start and the relocations are W3's exactly. Relocated food may land on thorns: a
    natural trade-off, reported.
- **They are seen** in the 3 × 3 view and written to a sixth map channel, "thorn seen", whose weights start at zero.
- **Harm:** each step on a thorn costs `harm` energy. It can kill, through energy.
- **Calibration** (Script only, the calibration lands, before any brain trains):
  - patches 2 (then 3), and harm 4, 6, 8, 12, 16 in that order;
  - the first setting with a **thorn-blind Script surviving ≤ 0.60** and a **careful Script ≥ 0.90**;
  - **if none qualifies, W3h stops.**

## Pain
- **In the pain arms:** at each thorn step, the reward −1.0 × harm / 8 at that step. It is proportional to the
  injury, and stops when the injury stops.
- **Logged** every life: harm and pain.

## The parent (W3d's fading childhood; W3's Script, which reads only the child's map view)
- **Thorn-blind:** W3's MapView unchanged, so thorns look like open ground.
- **Careful:** seen thorns look like walls to it.

## Arms (W3d's PYFR: the fading parent childhood plus Y and FR; 8 seeds; 2,000,000 steps; GitHub's machines)
| | thorn-blind parent | careful parent |
|---|---|---|
| **no pain** | **TH** | **THw** |
| **pain** | **THP** | **THPw** |

## Measures (W3's 50 test lands, learning off)
1. **Thorn steps per 1,000 steps of life.** The main measure.
2. **Entries per opportunity:** steps onto a thorn from off it, divided by the steps that began beside a thorn.
3. **Bout length:** thorn steps per entry.
4. Lifespan and survival to 3,000.
5. **Fear, as over-avoidance:** the share of meals eaten within Manhattan 2 of a thorn, beside the share of the land's
   food that lies there.
6. **Training:**
   - thorn steps per 1,000 in each 100,000-step block;
   - the thorn channel's weight norm every 50,000 steps.

## Readings (95% bootstrap over the 8 seeds, paired by seed; numpy seed 20261137)
1. **"Pain teaches avoidance":** THP − TH on thorn steps per 1,000, upper bound below 0.
2. **"Pain helps it live":** THP − TH on lifespan, lower bound above 0.
3. **"Watching teaches avoidance":** THw − TH on thorn steps per 1,000, upper bound below 0.
4. **"Pain adds to watching":** THPw − THw on thorn steps per 1,000, upper bound below 0.

The other measures are reported with intervals, with no gate.

## Validity (hard stops)
- The calibration rule is met.
- **Checks All: PASS before data:**
  - the thorn layout comes only from the land's seed, and W3's land is unchanged;
  - harm and pain are applied only on thorn cells, and pain only in the pain arms;
  - the sixth channel shows only thorns seen, and its weights start at zero;
  - the careful parent never steps on a thorn it has seen, and the thorn-blind parent's view equals W3's;
  - with no thorns (patches 0), the loop reproduces W3d's PYFR training (allclose);
  - a split run equals an unsplit run;
  - the same seed twice is the same.
- Every run finishes, or is reported.

## The assistant's prior
- Reading 1: about 75%.
- Reading 2: about 35%.
- Reading 3: about 50%.
- Reading 4: about 50%.

## Amendment 1 (16 November 2026, about 22:15; after the calibration, before any brain was trained)
**The frozen calibration found no setting.** At every harm, the careful Script survived 0.84 (2 patches) or 0.74
(3 patches), never ≥ 0.90.
- **The cause:** on the calibration lands, W3's Script survives only 0.90 with no thorns at all (W3's own calibration
  chose R as the first value with Script ≥ 0.90). So a careful parent could reach 0.90 only if thorns cost nothing.
  The bar was set without knowing this.
- **The rule's purpose** was that a safe life stays possible.
- **The amended rule:** the first setting with a thorn-blind Script ≤ 0.60 and a careful Script **within 0.10 of the
  no-thorn Script** on the same lands.
- **The rows already measured** (deterministic, `calib_h.json` after the re-run):
  - 2 patches: harm 4 gives blind 0.72 and careful 0.84; harm 6 gives blind 0.40 and careful 0.84.
  - So the amended rule chooses **2 patches, harm 6** (pain at a thorn step = 0.75).
- **Learned brains played no part.** The re-run records the no-thorn reference.
