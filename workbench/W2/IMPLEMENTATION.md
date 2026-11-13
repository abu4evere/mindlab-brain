# W2: implementation notes (before any training)

- **world2.py:** the 3 x 3 view, the remembered map (a fixed writer), the tours, the scripted brains, the test sets
  (seed 20261122). The learning set is W1b's 400 layouts (`W1b/layouts.json`).
- **brains2.py:**
  - **MapVIN:** W1e's V+ (plus mask, K = 30, max) on 3 channels (known wall, unknown, food). Within an episode the
    map changes, so in learning every step's map is planned in one batch; a check shows the batch equals planning one
    map at a time.
  - **RNet:** W1's Elman arithmetic, 55 inputs, 64 units. "W1c's convolution on the 3 x 3 view" reduces to a dense
    layer on its 9 cells. R steps through the tour with the food's inputs at zero. Learning does not backprop into
    the tour (truncation at the episode start); what R keeps from the tour is carried in its state only.
- **Learning:** each episode is new or familiar with equal chance, with a fresh random tour. The teacher (Bp for M
  and R; B0 for M0) acts; the brain is taught at every state the teacher visits.
- **The look-alike measure:** per room, 1 if the brain's first sideways move (across the start-food axis) goes
  toward the gap, else 0 (also 0 if it never moves sideways). B0 and the reactive controls score exactly 0.5 per pair
  (they act the same in both rooms). Bp scores 0.66: its tour shows the gap but not always the whole barrier, and
  unknown cells count as open.
- **M-erase** equals M in a new room on the same layout (the map starts empty), as specified.
- **Pre-data corrections (no data existed):**
  1. two look-alike tours were trapped in a pocket behind the start's 3 x 3 and never saw the gap (the check caught
     it). A pair's tour is now redrawn until it sees its gap. The detour and control sets are unchanged (verified
     identical);
  2. the tour's reachability uses one flood fill instead of a search per cell (the same cells; the sets were
     verified identical).
- **Speed:** about 0.017 s per episode for M, 0.037 for M0 (its teacher wanders), 0.004 for R; 48 runs at 4 at a
  time take about 10 hours.
