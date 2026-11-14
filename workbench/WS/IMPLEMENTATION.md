# WS: implementation notes (before any data)

- `ws.py`: one network class for every brain. Non-recurrent brains use a zero previous state (each step stands alone, as C2's network). Bm and Brm use a learned recurrent state over the showing steps and the try.
- **A reading of the frozen text (before data):** "each night the last 4 showings are rehearsed" applies to the nights of days 1–30 (the days with showings). After day 30 there are no new showings, and replaying the same last 4 for 30 more nights would turn retention into rehearsal. Bu's matched amount (4/18 per showing on days 1–30) uses the same reading. Check: the copy amounts are equal (`checks.log`).
- Skill tests start from a zero state with no showing. The "after a showing" tests feed the right sequence's showing steps to Bm and Brm; for the other brains a showing has no input pathway.
- It runs locally (Mind Lab has no cloud), as one process at Idle priority, while W3's 4 jobs run: 384 short children, a few minutes.
