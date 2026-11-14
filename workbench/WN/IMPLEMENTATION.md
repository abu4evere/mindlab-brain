# WN implementation notes (written before the run)

- `wn.py` reuses WS's task, learning rule and tests (`../WS/ws.py`); only the network size changes. Each child's
  starting weights use WS's draw `[seed, 4]` and every brain uses WS Bm's act draws `[seed, 3, 4]`, so **M-32 is WS's
  Bm exactly** (checked against WS's saved output, seeds 1 and 2). F-n therefore uses different act draws from WS's B0
  (which used `[seed, 3, 0]`); the plan said "the same seeds and draws for every brain", which this follows.
- **G grows at the end of days 8, 16 and 24** (after that day's practice), so its sizes at the tests are 16 (day 7),
  32 (day 15), 128 (days 30 and 60). The growth draws use their own stream `[seed, 9]`.
- Tests: success (both lids, no showing) at days 7, 15, 30, 60; after a showing at day 30. Run time is CPU seconds per
  child (`time.process_time`).
- **Correction 1 (before data):** check 5 first compared F-n's after-showing test with its plain day-30 test. The two
  draw different look noise by design (as in WS), so they need not match; the check was wrong, not the code. It now
  checks that F-n's after-showing test uses no showing prefix. Checks: All: PASS (`checks.log`).
- **Seen before the analysis was written:** a timing run of seed 1 for M256, M128 and F128 (CPU 4.6, 1.1, 0.6 s; their
  skill numbers printed too). The study has no gated readings and the analysis is the plan's descriptive list, so this
  changes nothing, but it is recorded.
