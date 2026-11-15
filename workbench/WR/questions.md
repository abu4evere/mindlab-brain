# WR: the recipe in one brain (plan, frozen before any code or data)

**Frozen** as git tag `WR-frozen`, before any code or data.
- **The creator** (15 November 2026, the first message of a new assistant account): "In Mind Lab we found four brain
  parts that each helped … Nobody has tested them together. Design a test that puts them into ONE brain, in WC's
  changing world (and the stable world if you think it's needed). Compare it against the best single parts." And:
  "I'm giving my OK for this task now, so after showing me the plan you can go ahead."
- **Exploratory, as WN to WF:** the creator asked for it directly, so there is no council.

## The four parts (each exactly as built in its own study; no number re-tuned)
- **L, learn without the showing in mind (WL2's Linf):** on a try where the teacher shows, the copy step and the try
  both start from a blank memory (no showing steps before them). The showing teaches only through the copy step.
- **T, don't repeat a failure (WM's TB, with WM's correction 1):** for each kind and lid, the pairs that failed since
  the lid last opened are blocked in practice tries (a second act after the same first act; a first act whose four
  pairs all failed). A list that reaches all 16 pairs clears. Never in tests.
- **Y, "that worked!" (WY's YS):** after a practice try, each lid that opened is copied from the child's own acts at
  the full copy rate, weighted by 1 − e (e: that lid's expectation of opening, step 0.2, from before the try), through
  the same memory steps as the try.
- **R, a fast memory replayed at night (WF's RP):** a store holds, for each kind and lid, the last pair that opened
  it, fresh until that pair fails there. At the end of each day, each kind's fresh stored pairs from the first lid
  onward are copied twice at rate 1.0 from the kind's plain look, with no showing in memory. **Tests use the network
  only;** the store never acts.

**When the parts are combined (defined now, so the code makes no unfrozen choice):**
- With L, the copy step, the try and Y's self-copy all run from the same blank memory; without L they all run through
  the showing steps (as in WY and WF).
- Every arm keeps the expectations e, the block lists and the store (they cost nothing), but only the arm's own parts
  use them: T reads the block lists, Y reads e, R reads the store.
- Each day's order is WF's: the showing and copy step (if the teacher is here), the try, then T's and R's bookkeeping,
  e's update, Y's self-copy; at the end of the day, R's replay; then that day's tests.
- The act draws come from one stream per child (`[seed, 3, 4]`, WS's Bm), so arms differ only through what they
  learn; L consumes no extra draws.

**The plan was reviewed by the assistant alone:** three independent critic sessions were started before the freeze but
all three stopped on a usage limit before reporting. Recorded here so that nobody reads "reviewed" into it.

## The worlds
1. **The changing world (WC's):** WT's teacher present on each try of days 1–30 with probability 0.5 (the world's
   draws); kinds 0–2 (group A) get new codes at the start of day 31 and kinds 3–5 (group B) at day 46 (WC's draws);
   no teacher after day 30. Tests at days 30, 33, 38, 45, 48, 53 and 60: no showing, greedy, the network only, each
   kind once. Seeds 1001–1048 (as WC, WM, WY and WF).
2. **The stable world (WL2's, which is WN's):** a showing before every try on days 1–30, none after; the codes never
   change. Tests at days 7, 15, 30 and 60 (no showing); WL's after-showing test at day 30 (for L arms the memory is
   blank, as in WL2). Seeds 1–48 (as WL and WL2).

Everything else is WS's: 6 kinds, 2 lids, 3 tries per kind per day, 60 days, copy rate 0.5, learning rate 0.05, the
memory ring, step limit 1.0. Memory children of 32 and 128 neurons.

## Arms (48 children per arm and size; GitHub's machines)
**Changing world** (8 arms × 2 sizes):

| arm | parts | what it is |
|---|---|---|
| Base | none | WC's child (WY's Base; must reproduce WY) |
| L | L | Linf alone, for the first time in a changing world |
| TY | T, Y | WY's TBYS (must reproduce WY) |
| TYR | T, Y, R | WF's RP, the best brain so far at relearning (must reproduce WF) |
| **LTYR** | **all four** | **the recipe** |
| LTY | L, T, Y | the recipe without night replay |
| LYR | L, Y, R | the recipe without don't-repeat |
| LTR | L, T, R | the recipe without "that worked!" |

TYR is also the recipe without L. WF's engineered acting store (WSLS) is not a part of the recipe and is not run.

**Stable world** (4 arms × 2 sizes):

| arm | parts | what it is |
|---|---|---|
| L0 | none | WL2's L0, the perfect memory (must reproduce WL2) |
| L | L | WL2's Linf, the best brain so far here (must reproduce WL2) |
| TYR | T, Y, R | the habit parts without L: does night replay alone cure the parrot? |
| **LTYR** | **all four** | **the recipe** |

## Measures
- **Changing world (WF's):** own skill on group A at days 30, 38 and 45 (A30, A38, A45) and on group B at days 45, 53
  and 60 (B45, B53, B60); the stale habit at days 33 and 48 (the share of changed kinds whose first lid still gets
  its old pair); lifetime food (lids opened in practice, judged by that day's codes).
- **Stable world:** own skill at days 7, 15, 30 and 60; after-showing skill at day 30; lifetime food.
- **Statistics:** means per cell; paired differences by seed with 95% bootstrap intervals (10,000 resamples, numpy
  seed 20261126, percentiles 2.5 and 97.5); 48 children beside every number.
- **Differences, changing world,** on A45, B60, A30, B45 and food (the stale habit in the table only):
  - **LTYR − TYR** (the main one: the recipe against the best brain so far);
  - LTYR − LTY, LTYR − LYR, LTYR − LTR (each part's share inside the recipe; L's share is LTYR − TYR);
  - every arm − Base.
- **Differences, stable world,** on days 7, 15, 30, 60, the after-showing day 30 and food:
  - **LTYR − L** (the main one); LTYR − L0; TYR − L0; TYR − L.

## Readings (descriptive, stated now; size 128 is the reading size, size 32 reported beside it)
1. **"The recipe loses nothing":** LTYR − TYR has a lower bound above −0.05 on each of A45, B60, A30 and B45.
2. **"The recipe gains":** LTYR − TYR has a lower bound above 0 on A45 or on B60.
3. **"Each part earns its place":** for each of the four parts, LTYR minus the arm without that part has a lower
   bound above 0 on at least one of A45, B60, A30, B45 or food. A part that fails this is "not needed here", which is
   a finding, not a fault.
4. **"No cost in the stable world":** LTYR − L has a lower bound above −0.05 at days 30 and 60, at both sizes.
5. **"Night replay alone cures the parrot":** TYR-128 in the stable world has a mean own skill of at least 0.50 at
   day 30 (WL2's L0-128: 0.04).

## Checks (`checks_wr.py`, All: PASS before any data)
- One generic child (`wr.py`, one function for every arm and world) reproduces, child for child: WY's Base-32 and
  TBYS-32 (seed 1001), WF's RP-32 and RP-128 (seed 1001), WL2's L0 and Linf at 32 and 128 (seed 1): the tests, the
  food and, in the stable world, the after-showing skill.
- With L the copy step and the try get an empty prefix even when the teacher is present; without L they get the
  showing steps.
- T: a blocked pair is never chosen in practice; R: replays happen; Y: a self-copy raises the copied act.
- The same child twice is the same; the eight changing-world arms give eight different lives (seed 1002, size 32).

## After the data
- `analyse_wr.py` (written before the data) writes `analysis.md` and `analysis.json`; `findings.md` reads them.
- **An independent recompute** of the main differences (LTYR − TYR on A45 and B60; LTYR − L at day 30, size 128) from
  the raw output files, by a fresh session that does not see the analysis script, recorded as `recompute.md`.
  Mind Lab's exploratory studies did not have one; this one does because it joins four findings.

## Limits (stated now)
- One task family (2-lid boxes); the parts keep their own studies' numbers, not re-tuned for each other.
- Tests count the slow network only (as WM, WY and WF); a brain whose fast store also acts (WF's WSLS) is a separate
  question.
- Two sizes; 48 children per cell; no evolution.

## The assistant's prior
- Reading 1 (loses nothing, size 128): about 55%. Night replay already trains the network with no showing in memory,
  so L may add little on top of it.
- Reading 2 (gains): about 25%.
- Reading 3 (each part earns its place): about 30% for all four at once. By part: R about 90%, T about 60%, Y about
  40%, L about 25%.
- Reading 4 (no cost in the stable world): about 60%. T's exploring could cost early skill; day 7 and 15 will show it.
- Reading 5 (replay alone cures the parrot in the stable world): about 60%.
