# WO: stopped at the floor before any study data (15 November 2026)

Plan: `questions.md` (WO-frozen). The study seeds (1–48) were **never run**. Every number below comes from pilot
seeds 901–903 (outside the study), from `wo.py` as frozen and then as corrected.

## What happened
1. **As frozen (new boxes from day 1):** every arm was at the floor.
   - Immediate success after the single showing: L0-128 0.02–0.04; all others 0.
   - Retention after 1 day: 0–0.02.
   - Food about 30 of 784.
   - A newborn brain has never learned *how* to use a showing.
2. **Correction 1 (before study data):** days 1–30 became WL2's childhood (6 familiar kinds, the arm's own episodes
   before every try), and the new boxes moved to days 31–60. Still at the floor:

| arm | size | immediate (pilot seeds 901, 902, 903) | retention 1 day |
|---|---|---|---|
| L0 | 32 | 0.065, 0.043, 0.130 | 0.02, 0, 0 |
| L0 | 128 | 0.043, 0.109, 0.109 | 0, 0, 0 |
| L2 | 32, 128 | 0, 0, 0 | 0 |
| Linf | 32, 128 | 0, 0, 0 | 0–0.02 |

- **The frozen plan had no floor rule.** The C2-K2 practice was followed: stop rather than read a floor.

## What the pilot shows (the assistant's reading)
- **None of these brains can copy a brand-new box from one showing.**
  - The perfect-memory brain replays showings of the boxes it grew up with (WL: 1.000 after a showing). On a new look
    it manages about 4–13%.
  - Its "copy what you just saw" was learned per familiar box, not as a general ability.
  - With only 6 familiar kinds, the look and the shown moves always come together, so the network never had to learn
    "do the shown move, whatever the box".
- **This is a missing ability:** general, one-shot imitation (seeing something new once and doing it).
  - Children have it early. It seems to need either many different things shown in childhood, or a brain part that
    routes "shown move" to "do move" whatever the context.
  - Both are design choices for a later test, with the creator.
- **The question WO asked** (is a held showing worth it for new things?) needs that ability first. It waits.

## Status
Stopped. Code as corrected is kept (`wo.py`, `checks_wo.py`); no study output exists.
