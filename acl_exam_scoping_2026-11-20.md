# The one ACL comparison: scoping notes (draft for the creator, 20 November 2026)

**The creator's decision (20 Nov):** "we will test this brain inside acl once to compare current brain data with last
acl brain data and then we will go back to brain itself again by stoping acl". This file only scopes it. The plan
itself will be frozen, with the creator's sign-off, after W3n's findings are final.

## What "the last ACL brain" is (ACL `experiments/INDEX.md`)
| study | the brain | result |
|---|---|---|
| v17 "old minds" | hand-written instincts and habits (`acl/mind.py`): each week a list of options (action, tile, score) and the best is taken | the baseline: viable |
| NB1 | an inherited, evolving network on top of the old minds | viable, but "decorative": the network's learning did not help (learning on − off −0.045) |
| NB2 | the network chooses among the body's options itself | not viable: population 0.18 of the old minds'; killing ×910 |
| NB3 | NB2 + feelings (an inborn reluctance to harm, empathy, …) | not viable: population 0.49; starvation 44% of deaths |
| NB4 | a household that weighs another child, and shares | draft only, never run |

So the ACL brains so far either rode on the old minds (NB1) or died out (NB2, NB3).

## Why the new brain does not drop straight in
| | Mind Lab's W3 world (the new brain's home) | ACL v17 |
|---|---|---|
| time | one step = one move | one tick = one week; a person can act up to 3 tiles away |
| choices | 5 moves | many kinds: forage, hunt, gather, drink, give, court, make, rest, explore, … each at a tile |
| others | alone | households, kin, partners, children, strangers |
| body | energy, tiredness | food, water, health, cold, illness, age, pregnancy |
| life | 3,000 steps | about 2,000–3,500 weeks |

The new brain is a **navigator with feelings**: it learns what each place is worth, given hunger, tiredness and
curiosity, and plans a way there. ACL needs that, but also needs choosing *what to do*, and living with others.

## Three ways to do the comparison (the assistant's view; the creator decides)
1. **Transplant the navigator (recommended).** Each ACL person keeps the old mind for *what* to do. The new brain
   chooses *where*: from the person's own map memory around them (food on tiles, water, home, never seen, staleness),
   it builds the worth map from its feelings and scores the old mind's candidate tiles. It is trained inside ACL from
   birth (a parent as teacher, as in W3d), with the same recipe and kept copies.
   - **Fair test:** the same worlds (16 paired seeds, nature v17, frozen) with the old minds' "where" against the
     new brain's "where".
   - **Smallest change, clearest answer.**
   - **Limit:** it tests only the part the new brain is good at.
2. **The whole mind.** The new brain chooses everything, like NB2 and NB3. This would be the most honest test of
   "is it better than the last ACL brain", but it needs parts the new brain does not have yet (choosing among kinds of
   action, living with others). NB2 and NB3 died out this way.
3. **A Mind Lab copy of ACL's survival core.** Rebuild ACL's food, water and seasons as a Mind Lab world. This is
   cheap and fast, but it is no longer ACL.

## Compute
- ACL studies ran on GitHub Actions; that is over. A 600-year, 16-seed study must run on the PC, Oracle and Google
  Cloud.
- Its run time on these machines has to be measured first, on one seed, before the plan is frozen.

## Readings (proposed, NB3's rules so the numbers compare)
- Viable: extinct worlds at most the old minds' + 3, and the population ratio's upper bound at least 0.80.
- Beside it: starvation share of deaths, child survival to 16, adult lifespan, and the same against NB1, NB2, NB3's
  published numbers ("current brain data compared with the last ACL brain data").
