# WL4 implementation notes (written before the run)

- `wl4.py` uses WL2's network, episodes and wait-aware prefix runner, with its own `Home`.
  - 30 looks and random codes are drawn from `[seed, 31]`; the RULE codes are computed from the looks.
  - The daily order is WS's arithmetic over the 24 practised kinds.
- **Tests:** greedy, no showing, every kind once (test-look noise `[seed, 6, day, 0]`), split into practised (24) and
  held-out (6) shares.
- **Seen in the checks, before any data:** the look noise (0.2) changes at least one arg-max in 27% of encounters.
  - So a perfect rule-follower reading the noisy look would open a held-out box about 0.73 of the time.
  - That is the realistic ceiling for held-out success; it is a property of the frozen design.
- Run locally at Idle (2 processes) after WD. Checks: All: PASS (`checks.log`).
