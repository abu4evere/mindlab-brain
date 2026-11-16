# W3g implementation notes (written before the run)

- **`w3g.py` patches W3's module classes before training:**
  - `World` becomes `FedWorld`, which records cells eaten at and appends them as a sixth `obs_map` channel;
  - `DriveVIN` becomes `FedVIN`, whose first 5 channels are W3's own draw and whose 6th channel starts at zero;
  - `brains3.C` becomes 6 for the backprop reshape.
  
  Training is W3d's `train_net_parent` (parent childhood + Y + FR) under the arm name FM.
- **The parent** (W3's Script) reads its MapView, not `obs_map`, so it does not see the new channel.
- **The reproduction check** (the channel held at zero) matches W3d's PYFR training within 1e-10, but not bit for bit:
  the extra all-zero column changes the floating-point summation order. Long sampled runs diverge from W3d's child
  anyway, so FM − PYFR is a paired comparison by seed (the same starting weights for channels 1–5, the same lands
  and tests), not a bit-replica.
- **Analysis:** lifespan and survival paired against W3d's test files, plus WX's death recorder on FM's test lives.
- Cloud: 8 jobs; `manage_w3g.py` (with retries) resumes paused runs. Checks: All: PASS (6).
