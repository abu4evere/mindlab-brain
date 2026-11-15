# WP: one big brain among small ones (plan, frozen before any code or data)

**Frozen** as git tag `WP-frozen`, before any code or data, and before WC's results were seen.
- **The creator** (14 November 2026): "what if we run one big brain with other small ones", then "go ahead with the
  group test after this one".
- **Until now** each child learned alone from one grown-up. Here children live in groups of six and can watch each
  other.
- **Exploratory, as WN to WC:** the creator asked for it directly, so there is no council.

## The world (WS/WT task)
- 6 kinds, 2 lids, 3 tries per kind per day, 60 days, copy rate 0.5, learning rate 0.05; every child has the memory
  ring.
- **One world per group:** same looks, codes, daily draws and test looks (`ws.Home(group seed)`, test draws
  `[group seed, 6, day, 0]`).
- **The grown-up:** present on each try of days 1–30 with probability **0.2** (WT's draws `[group seed, 5, day]`),
  for all six children at once. When present, it shows the box and each child copies, exactly as in WT.
- **Two worlds:**
  - **stable:** the codes never change;
  - **changing:** WC's change (kinds 0–2 get new codes at the start of day 31, kinds 3–5 at day 46; WC's new-code
    draws `[group seed, 8]`).

## Watching each other (all 60 days)
- **A child's latest try on each kind is visible to the group:** its acts and how many lids opened.
- **On a try with no grown-up,** each child first watches one other child's latest try on that kind, if there is one:
  - it holds the lids that opened in its memory (the showing steps) and copies them (copy rate 0.5);
  - a lid that did not open is seen as failed and not copied.
- **Whom to watch:**
  - each child keeps a trust number for each other child, starting at 0.5;
  - it picks the one to watch with probability in proportion to max(trust, 0.05);
  - afterwards it updates that trust: t += 0.3 × (lids opened by the watched try / 2 − t).
- **Order in a try slot:** every child watches (using tries from earlier slots), then every child tries; then the new
  tries become visible.

## The groups (48 groups each, group seeds 1–48)
- **S6:** six children with 32 neurons.
- **B1S5:** child 0 has 128 neurons; children 1–5 have 32.
- **B6:** six children with 128 neurons.
- **S6-alone:** six 32-neuron children who never watch each other (each as in WT, the grown-up only).

**Child seeds:** child c of group g uses seed 1000 × g + c for its starting weights and its act draws. So small child c
in S6 and in B1S5 starts identical.

## Measures (descriptive, 95% bootstrap intervals over the 48 groups; numpy seed 20261119)
- **Own skill** (full boxes, no showing) at days 30 and 60. In the changing world also group A at day 45 and group B
  at day 60 (relearning).
- **The questions:**
  1. **Does one big brain lift the small ones?** Small children 1–5: B1S5 − S6.
  2. **Do they choose to watch it?** In B1S5, the share of the small children's watching that goes to the big child
     (chance = 0.2), over days 1–30 and days 31–60.
  3. **Does watching each other help at all?** S6 − S6-alone.
  4. **Group means:** S6, B1S5 and B6.
  5. **The big child itself:** child 0 in B1S5 against child 0 in B6.
- Lifetime food, per child and per group.

## Limits (stated now)
- One small task; fixed learning rates.
- Trust from seen success only.
- A child copies only the lids it saw open.
- No cost for neurons, and no evolution here.

## The assistant's prior
- **Q1, stable world, day 60:** small children in B1S5 above S6 (interval above 0): about 45%.
- **Q2:** small children's watching share to the big child above 0.30 over days 1–30: about 55%.
- **Q3, stable world, day 60:** S6 above S6-alone (interval above 0): about 70%.
- **Changing world:** small children in B1S5 relearn group B (day 60) better than in S6: about 35%.
