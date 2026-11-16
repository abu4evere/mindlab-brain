# WX: why do the best learned brains die? (a diagnosis; plan, written before any logging)

**Frozen** as git tag `WX-frozen`, before any logging.
- **The creator** (16 November 2026, about 14:0x): "what we can do in that period" (while W3f trains); the assistant
  chose this.
- **A read-only diagnosis:** no training. It reuses W3d's trained PYFR brains (8 seeds) and W3's Script, on W3's test
  lands, exactly as W3's test runs them (the same generator per land, so the lives are W3d's test lives).

## Logged per life (the death is always energy reaching 0 in W3's body)
- lifespan; meals eaten; steps since the last meal at death;
- **fatigue:** the share of steps with F > 100 (where moving costs double), and F at death;
- **at death:**
  - does the map memory hold any cell remembered as full food;
  - the BFS distance to the nearest one, if any;
- **food-finding:** the share of the land seen by step 500; steps until the first meal.

## Classification of each death (rules fixed now)
1. **"No food known":** the map memory holds no cell remembered as full food at death.
2. **"Food known but not reached":** a remembered full food cell exists within BFS distance ≤ energy-at-hunger-onset
   steps. In practice: it was known at any point in the last 100 steps and lay within 30 steps.
3. **"Exhaustion":** F > 100 for at least half of the last 100 steps (moving cost doubled).

A death can carry several labels; shares are reported per label.

## Readings (descriptive; per seed, then the mean over the 8 seeds; Script beside them for its rare deaths)
- the share of deaths per label;
- meals per life and steps to the first meal, PYFR against Script.

## Limits
Diagnosis only; no causal claim beyond the labels' definitions.
