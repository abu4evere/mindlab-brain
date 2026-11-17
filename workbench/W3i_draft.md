# W3i: more practice, a longer childhood. Is the best brain just too young? (DRAFT)

**Why:**
- **The best brain** (W3d's PYFR) lives 806 steps on average and survives a full life 0.128 of the time. The
  creator's bar for ACL is 0.80.
- **Its lives are uneven.** Seed 2 survives 20 of 50 lives; seed 8 survives none. Watching seed 2's lives (the
  viewer, "Child of the Field"), it dies mostly after its remembered food has gone. It keeps returning to empty places.
- **Two cheap levers have not been tried:**
  1. **More practice.** In W1e the same planner went from 0.17 to 0.54 to 0.70 efficient detours between 30,000,
     150,000 and 500,000 episodes, and was still rising. W3d trained 2,000,000 steps, about 2,700 lives.
  2. **A longer childhood.** W3d's parent fades out over the first 400,000 steps (a fifth of the run). A parent who
     never leaves (PA) was worse (272 steps), so the open question is the length of the fade, not the parent's
     presence.

## The design (W3d's PYFR unchanged except the two levers; 8 seeds; GitHub's machines)
| arm | training steps | childhood (parent fades out over) |
|---|---|---|
| **L** (longer life of practice) | 6,000,000 | 400,000 (as W3d) |
| **C** (longer childhood) | 2,000,000 | 1,200,000 |
| **LC** (both) | 6,000,000 | 1,200,000 |
| cited: **PYFR** (W3d) | 2,000,000 | 400,000 |

- **Snapshots:** L and LC are tested at 2, 4 and 6 million steps, giving a learning curve.
- **A free reproduction check:** L's first 2,000,000 steps are W3d's PYFR run exactly (the same seed, childhood and
  code), so L's 2-million snapshot must equal W3d's PYFR weights.

## Measures (W3's test, alone, 50 lands)
Lifespan, survival to 3,000 and to 1,000, and WX's death labels (no food known, exhaustion, food known but not
reached).

## Readings (to be frozen; paired by seed; 95% bootstrap)
1. **"More practice helps":** L(6M) − PYFR on lifespan, lower bound above 0.
2. **"A longer childhood helps":** C − PYFR on lifespan, lower bound above 0.
3. **"They add":** LC − max(L, C), reported.
4. **Toward the bar:** the best arm's survival against 0.80.

## Open questions for the council
1. Is 3× enough to see a trend, or should one arm go to 10 million steps?
2. Is a 1,200,000-step fade the right "longer childhood", or should the parent's weight stay full for longer and then
   fade?
3. Snapshots at 2, 4 and 6 million: any risk of reading the curve after the data?

## The assistant's prior
- More practice helps: about 55%.
- A longer childhood helps: about 45%.
- The best arm reaches survival 0.80: about 3%.
