# WR implementation notes (written before the run)

- **One generic child** (`wr.run_child(world, arm, n, seed)`) for every arm and both worlds. The arm name lists its
  parts (L, T, Y, R); Base and L0 have none.
  - The try is WF's `try_box` (equal to WM's and, without blocking, to WS's; checked in WM and WF), with T's block
    lists when the arm has T.
  - Y is WY's `self_copy`, through the try's prefix (blank under L).
  - R is WF's nightly replay (2 copy steps at rate 1.0 per kind with fresh stored pairs, from the kind's plain look).
  - L sets the prefix of the copy step, the try and the self-copy to empty whenever the teacher shows.
  - Every arm keeps e, the block lists and the store; only its own parts read them (questions.md).
- **Reproduction (checks_wr.py):** the changing world reproduces WY's Base-32 and TBYS-32 and WF's RP-32 and RP-128
  (seed 1001) child for child; the stable world reproduces WL2's L0 and Linf at 32 and 128 (seed 1), including the
  after-showing skill. The stable test days (7, 15, 30, 60) are WL's; the reproduction check would fail if they were
  not.
- **Output:** `output/<world>_<arm>_<n>_seed_<s>.json` with the tests, food, the number of replays and self-copies, and
  (stable world) the after-showing skill at day 30.
- **Analysis:** `analyse_wr.py`, written before the data; it also prints the five readings as YES/NO from the
  intervals.
- **Cloud:** 24 jobs on GitHub's machines (`run.yml`, each job runs `checks_wr.py` first), dispatched with
  `tools/cloud.py` from `jobs.tsv`; run ids in `run_ids.txt`.
