# WD implementation notes (written before the run)

- `wd.py` follows WR's `run_child` for the recipe (L: no showing in mind, so the copy step has an empty prefix; T, Y
  and R as WR). With no bad kinds, Naive reproduces WR's change-world LTYR at day 30 (checked; the two worlds are the
  same up to day 30).
- The teacher's shown code on bad kinds is WC's new-code draw `[seed, 8]` (each lid differs from the true pair).
- **Doubt:**
  - the copy step's rate is 0.5 × trust;
  - trust updates only on tries where the teacher was present, after the practice try, one update per lid with an
    outcome (`trust_updates`).
- **Alone** never copies; its trust stays 1.0 and is unused.
- **Tests:** WS's (greedy, no showing, the network only). "Believe" = the first lid's chosen pair equals the
  teacher's wrong first pair, on bad kinds.
- **The pilot** used seed 901 (outside the study): Doubt's trust at day 30 was 0.0 on bad kinds and 1.0 on good ones.
- Run locally at Idle (2 processes) after WL3. Checks: All: PASS (`checks.log`).
