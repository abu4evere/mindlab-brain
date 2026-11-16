# W3f implementation notes (written before the run)

- **`w3f.py` builds `train_net_choose` from W3b's `train_net` source,** with two anchored insertions (each checked
  once):
  1. at the start of each life during childhood, `choose(life)` picks the adult for that life;
  2. on every 4th childhood step, that adult's argmax act on the child's view is copied with W3b's `imitate`, the
     weight fading as in W3d.
  
  The recipe parts are on. The adults are fixed nets.
- **Visible success:** `make_pool` lets each pool adult live (sampled, learning off) on W3's calibration lands
  800001–800005, and takes its mean lifespan.
  - Generation 1's pool (W3e's G2) was computed locally before any data: 319, 798, 309, 259, 177, 234, 594 and 193 for
    seeds 1–8. The same file serves CH and RN.
- **Chaining:** generation k's children (`CH<k>_<s>.npz`, `RN<k>_<s>.npz`) are committed, and the next pools are
  computed from them, before stage k + 1 is dispatched.
- **The thread count is 1 before numpy is imported.** Checks: All: PASS (`checks.log`).
