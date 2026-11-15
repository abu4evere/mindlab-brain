# WL: a leaky memory (does forgetting the details stop the parrot?) (plan, frozen before any code or data)

**Frozen** as git tag `WL-frozen`, before any code or data.
- **The creator's idea** (14 November 2026): "i think this is different from humans cuz humans cannot be parrot like
  agents. Our brain cannot easily remember things and act like that and i think thats where these two differs from
  each other". Then "go ahead".
- **In testable form:** a short-term memory that fades forces a brain to learn the skill as its own instead of
  replaying the showing.
- **Background** (from memory, not re-read): Newport's "less is more"; Elman 1993 "starting small".
- **Exploratory, as WN to WY:** no council.

## The world (WN's, where the parrot was strongest)
- A grown-up shows the box before every try on days 1–30 (copy rate 0.5); no teacher on days 31–60.
- The codes never change.
- WS's task (6 kinds, 2 lids, 3 tries per kind per day, 60 days), with the memory child.

## The leak (a body property, the same during learning and tests)
- **Between the showing and the try there is a wait** of D steps with no input. On each wait step the neurons get
  noise added before their activation (N(0, σ²) each).
- The copy step and the try use the same showing and the same noise (one memory episode).
- Gradients run through the wait steps as through any other step.
- **Levels:**
  - **L0:** no wait (WN's child; L0-n must reproduce WN's M-n, a check);
  - **L1:** D = 4, σ = 0.3;
  - **L2:** D = 8, σ = 0.6.
- **Noise draws:** each child's own stream `[seed, 13]` in practice; `[seed, 14, day]` in the after-showing test.
- Tests with no showing have no wait.

## Brains
Memory children with 32, 128 and 256 neurons × L0, L1, L2. 48 children each (seeds 1–48), on GitHub's machines.

## Measures (descriptive; 95% bootstrap intervals, paired by seed; numpy seed 20261122)
- Own skill (no showing) at days 7, 15, 30 and 60.
- Success after a showing at day 30 (with the wait).
- Lifetime food (lids opened in practice).
- **The questions:**
  1. **Does the leak stop the parrot?** L1 − L0 and L2 − L0 on own skill at day 30, at sizes 128 and 256.
  2. **Does it cost the final skill?** The same at day 60.
  3. **Big and leaky against small:** L2-128 and L2-256 against L0-32 at day 60.
  4. **Manipulation check:** after-showing success, L − L0, by size (it should fall).

## Limits
- The leak levels are fixed, not tuned.
- One task. Noise only in the wait, not on every step.

## The assistant's prior
- **Q1, size 128:** own skill at day 30 up by at least 0.10 with L2: about 50%; with L1: about 40%.
- **Q2:** no loss at day 60 for L1-128 (interval not below −0.05): about 55%.
- **Q3:** L2-128 at least as good as L0-32 at day 60: about 45%.
- **Q4:** after-showing success falls with the leak at size 128: about 85%.
