# W3d implementation notes (written before the run)

- **`w3d.py` builds `train_net_parent` from W3b's own `train_net` source,** with three anchored insertions, each checked
  to occur exactly once:
  1. a W3 Script per life (the parent);
  2. after the child's own action, if the parent is present: the parent's act on the child's MapView. On every 4th
     step (`total % 4 == 0`), one `imitate` step toward it with the planned weight;
  3. the function name.
  
  Everything else is W3b's code, so the parent's teaching is the only change (check 1: with no parent, W3b's D3
  training is reproduced exactly).
- **The parent's act** is computed on every step while present, so its own resting state follows the child's life. It
  uses no random draws.
- **`configure` points W3b's `train()` at `train_net_parent`** and W3b's output folder at `W3d/output`. Testing is W3b's
  `test()`, alone.
- **Cloud:** run.yml jobs; `manage_w3d.py` (W3b's manager with W3d's paths) resumes paused runs. Checks: All: PASS
  (`checks.log`; 10 checks).
