# WY: "that worked!" (learning strongly from one's own unexpected success) (plan, frozen before any code or data)

**Frozen** as git tag `WY-frozen`, before any code or data.
- **The creator** (14 November 2026): "go ahead", to the order "that worked!", then the leaky memory, then the
  doubting test.
- **What WM found:**
  - no part made the brain relearn changed codes;
  - "don't repeat a failure" (TB) found new codes in practice (food +133 at size 32), but the connections kept nothing;
  - its reading: a success after failures moves the connections only a little.
- **Exploratory, as WN to WM:** no council.

## The world (WC's and WM's, unchanged)
- WT's p = 0.5 grown-up on days 1–30.
- Group A gets new codes at day 31, group B at day 46.
- Single children; tests at days 30, 33, 38, 45, 48, 53 and 60.

## The new part: YS ("that worked!")
- **Each kind and lid keeps an expectation** that the lid opens: e, starting at 0, updated after each practice try in
  which the lid was tried (e += 0.2 × (opened − e)).
- **After a practice try, each lid that opened gets a copy step of the child's own acts:**
  - the copy runs through the same memory steps as the try;
  - each lid is weighted by its positive surprise, 1 − e (e taken from before this try);
  - the step is the full copy rate (1.0 × LR).
- **So an expected success writes almost nothing, and a success after failures writes nearly as strongly as a full
  showing.** It is a body-level signal (like a dopamine burst on an unexpected reward), not a rule about boxes.

## Arms (sizes 32 and 128; 48 children each, seeds 1001–1048, on GitHub's machines)
- **Base:** WM's Base, which reproduces WC (checked again).
- **YS:** Base plus "that worked!".
- **TBYS:** WM's TB (with correction 1) plus "that worked!". TB finds; YS keeps.
- WM's TB and SU results are cited from WM and not re-run.

## Measures (as WM; 95% bootstrap intervals, paired by seed; numpy seed 20261121)
- **Relearning:** A38, A45, B53, B60.
- **Before the change:** A30, B45.
- **Stale habit:** day 33 and day 48.
- **Food.**
- **Each arm minus Base, at the same size,** on A45, B60, A30, B45 and food.
- **Also TBYS − TB** (TB from WM's output, the same seeds and code) on A45 and B60.

## Limits
- One task.
- Fixed numbers (0.2, full rate); not tuned.

## The assistant's prior
- **YS-128:** relearning up by at least 0.15 on both A45 and B60, against Base: about 40%.
- **TBYS-128:** the same: about 55%.
- **No harm before the change** (A30 and B45 within −0.05 of Base) for YS-128: about 70%.
