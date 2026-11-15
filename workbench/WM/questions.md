# WM: learning from mistakes (plan, frozen before any code or data)

**Frozen** as git tag `WM-frozen`, before any code or data.
- **The creator** (14 November 2026): "go ahead with the learning from mistakes test", after WC.
- In WC, no brain relearned changed codes in useful time (best 0.11 after 14 days); old habits stuck (0.85–0.95
  stale two days after).
- **The creator's aim** (7 November): "The important ability isn't never making mistakes. It's learning from them."
- **Exploratory, as WN to WC:** the creator asked for it directly, so there is no council.

## The world (WC's, unchanged)
- WT's p = 0.5 grown-up on days 1–30; no teacher on days 31–60.
- Kinds 0–2 (group A) get new codes at the start of day 31, kinds 3–5 (group B) at day 46 (WC's draws).
- Single children; WC's tests at days 30, 33, 38, 45, 48, 53 and 60.

## The brain parts (each added to WC's memory child; sizes 32 and 128)
- **Base:** WC's child exactly. Base-128 must reproduce WC's M128 (a check).
- **SU, surprise:**
  - each kind keeps an expectation e (lids opened / 2, e += 0.2 × (r − e)) and a surprise trace u
    (u = 0.7u + 0.3 × max(0, e − r), updated after each practice try);
  - during practice tries the acts are drawn from softmax(z / (1 + 3u)) (more exploring);
  - the learning step is multiplied by (1 + 4u) (faster learning).
  - It is a body-level signal (like a prediction error), not a rule about boxes.
- **TB, don't repeat a failure:**
  - for each kind and lid, a list of the pairs that failed since that lid last opened;
  - during practice tries a listed pair cannot be chosen again: its second act is blocked after the same first act,
    and a first act whose four pairs are all listed is blocked;
  - the list clears when the lid opens.
  - Engineered short memory (labelled so).
- **LSi, learned lose-shift:**
  - the child also senses its own last try on this kind's lid: the two acts tried (one-hot 4 + 4) and the result
    (opened / failed / none; 2 inputs), 10 inputs more;
  - nothing tells it what to do with them; it must learn to use them.
- **SU+TB:** both.
- **Tests stay plain:**
  - no blocking and no surprise temperature (greedy, as WS);
  - so the test measures what the connections learned, not the in-the-moment help;
  - LSi's test sees its last practice try, since that is part of its senses.

## Children
48 per arm and size (seeds 1001–1048, as WC's final test), run on GitHub's machines (`run.yml`).

## Measures (descriptive; 95% bootstrap intervals over the 48 seeds, paired by seed; numpy seed 20261120)
- **Relearning:** group A at days 38 and 45; group B at days 53 and 60.
- **Before the change (no harm):** group A at day 30; group B at day 45.
- **Stale habit:** at days 33 and 48 (WC's measure).
- **Lifetime food** (includes any in-the-moment help).
- **Each arm minus Base, at the same size,** on: A45, B60, A30, B45, food.

## Limits (stated now)
- One task.
- **The parts' numbers are fixed, not tuned:** surprise factors 0.2, 0.7, 0.3, 3 and 4; the block list size
  unbounded.
- TB is engineered. SU is a general signal. LSi is learned.

## The assistant's prior
- **TB-128:** relearning up by at least 0.15 on both A45 and B60, against Base-128: about 50%.
- **SU-128:** the same: about 30%.
- **LSi-128:** the same: about 20%.
- **No part harms skill before the change** (A30 and B45 within −0.05 of Base, at size 128): about 65%.
