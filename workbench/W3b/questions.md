# W3b: living by feelings, with what the box tests taught (plan, frozen before any code or data)

**Frozen** as git tag `W3b-frozen`, before any code or data.
- **Draft:** `../W3b_draft.md` (the Opus session, 15 November, in sleep mode).
- **Council:** `../W3b_council_2026-11-15.md` (GPT, Gemini, DeepSeek; two rounds). Every choice below that came from
  the council is marked (council).
- **Sign-off:** the creator, 15 November 2026: "Yes go ahead" (11:39, Telegram, to the morning report's item 1) and
  "Lets fable give it a try then you will check" (12:07); "Yessir go ahead" (12:2x, to this session). The Opus session
  reviews W3b afterwards.

## The question
W3 (`../W3/findings.md`) showed that no brain learned to live from its feelings alone: every learned brain died at
about step 200 (random 174; the hand-written Script, using only the same map memory, 2,963). Even D3i, given the
designer's links from hunger to food, died. The reading: learning to act from sparse, delayed reward is far too slow.
The box tests of 14–15 November found what speeds learning from rare success: **"that worked!"** (WY) and **a fast
memory replayed at rest** (WF, WR). W3b asks two things, in order:
- **Step 0 (diagnostic, read-only):** which part of W3's brain is broken, the planner's values or the action head?
- **W3b proper:** do "that worked!" and a fast memory with rest replay let W3's brain live?

## Step 0: the diagnostic (read-only; W3's saved weights; written down here before it runs)
On W3's 50 test lands (the same lands and relocation schedules as W3; learning off), for **D3i and D3, all 8 seeds**:
1. **(a) the learned head,** as in W3 (W3's `test_*.json`; cited, not re-run).
2. **(b) the greedy value walk** (W1e's map read-out): at each step the planner runs as in W3; each cell's value is
   the largest of its 8 planner outputs (`q.max`); the brain moves to the open neighbour (open on its own map memory;
   unknown counts as open) with the highest value, or stays if none is higher than its own cell. No action head.
3. **(c) the one-step look-ahead walk** (council, GPT): as (b), but the chosen neighbour is the one whose own best
   neighbour value is highest (two cells ahead). It guards against (b) failing on a flat value surface.
4. **Logs at hungry steps** (council, Gemini; s ≥ 0.5, which is E ≤ 75), per life: the mean over the map's open cells of
   each of the four reward-map contributions (W0 part; s × Ws part; f × Wf part; c × Wc part), and the reward-map
   value at the remembered food cells minus the mean over the other open cells.
5. **Planner-vs-head agreement** (council, all three): on the (a) walk's steps, the share of steps where the head's
   arg-max action equals the direction the greedy value walk would take.

**Readings (size: 8 seeds × 50 lives; intervals by bootstrap over seeds, 10,000 draws, numpy seed 20261115):**
- **"The head is the broken part":** (b) or (c) survives in ≥ 0.50 of lives for D3i (mean over seeds), while (a) is
  about 0 (W3: 0.000).
- **"The values are the broken part":** (b) and (c) both below 0.10, and at hungry steps the food cells' reward-map
  value is not above the other cells' (the difference's interval includes 0).
- Otherwise: "neither alone"; the logs say what the planner does when hungry.
- **Step 0 does not change W3b's arms.** It changes the reading of W3b's result: if the values are broken, Y and FR
  train the head and may not be enough; that will be said in the findings, not used to re-plan after the data.

## W3b proper: the world, drives and test (W3's, unchanged)
- `../W3/world3.py` and `../W3/brains3.py` as frozen for W3 (R = 200 from W3's calibration; the same 50 test lands;
  the same drives, reward, planner, actor-critic, 64-step segments, γ 0.97, learning rate 0.01, entropy 0.01, clip
  1.0).
- **Training:** 2,000,000 steps per run, 8 seeds per arm, W3's training-land seeds (`1000·seed + life`), on GitHub's
  machines. A run is **resumable at life boundaries**: it checkpoints its full state (weights, the act generator's
  state, life counter, step counter, Y's statistics, the stores, logs) and stops cleanly after 4.5 hours, and a second
  job continues it. A check proves that a split run equals an unsplit run bit for bit (council, Gemini).
- **Test:** learning off; the 50 test lands; sampled actions from a fixed generator per land (W3's). Survival to
  3,000 is the primary measure; lifespan, land known, relocation finding, time hungry and exhausted, and **survival to
  1,000** (council: a pre-registered secondary, from the same lives) beside it.
- **The map memory stays perfect** (council, all three): fading is a later study.

## The parts (defined now; every number fixed here, none tuned)
**Needs:** the two consummatory deficits of W3's body, s (hunger, `E_SET − E` over 150, floored at 0) and f (fatigue,
F over 200, capped at 1). Curiosity has no Y (its relief is diffuse; council).

**Y, "that worked!" (self-imitation of a surprising relief):**
- Relief at step t, per need: r_c(t) = max(0, n_c(t) − n_c(t+1)).
- Running statistics per need, across lives within a run, from past steps only, reset at the run's start: mean μ_c
  and standard deviation σ_c of r_c over all steps so far. **Warm-up:** no event in the run's first 1,000 steps.
- **Event:** n_c(t) ≥ 0.8 and r_c(t) ≥ μ_c + 2σ_c and r_c(t) ≥ 0.05 (council, DeepSeek's rule, accepted by all).
- **Window:** the steps since the previous event of either need in this life, at most 15 (the map's width), ending at
  step t (council, Gemini's rule, two of three).
- **Weights:** w_k = min(3, (r_c(t) − μ_c) / (σ_c + 10⁻⁶)) × 0.9^k for the step k steps before t (k = 0 is step t).
- **The step:** one supervised update toward the taken actions at those (map, levels, cell) with those weights through
  W3's network (the planner and the head; the critic untouched), with W3's learning rate and clip. It runs at once,
  on the event, in addition to the normal actor-critic update.
- Logged per life: events, the window lengths, the mean weight.

**FR, a fast store replayed at rest:**
- **Store:** on each Y-type event (the same trigger; no Y step unless the arm has Y), the window above (maps, levels,
  cells, acts, weights) is stored as one path; a FIFO of 256 paths, kept across lives within the run (council: paths,
  not places; capacity Gemini's).
- **Replay:** on each step on which the body is on the shelter cell (resting), one stored path drawn uniformly is
  replayed as one supervised update (the same step as Y's, with the stored weights); **at most 64 replays per life**
  (council, Gemini's cap). The store never acts.
- Logged per life: replays.

**RR, the control (random replay; council, two of three):** the same trigger (shelter steps), the same cap (64 per
life), the same update, but the replayed path is drawn uniformly from a FIFO of 256 windows of the brain's own
recent experience (one 15-step window pushed every 15 steps), with weight 1.0 for every step. It separates "replaying
one's successes" from "extra updates while resting".

**F, the acting fast memory (engineered ceiling, labelled; test only, on W3's trained D3 weights):**
- A place per need: the cell where the need was last relieved by an event (the food cell eaten at; the shelter).
- When n_c ≥ 0.8 and the place is known, the brain walks to it by the shortest path on its own map memory (walls known;
  unknown open; W3's `bfs_path`); otherwise the learned brain (W3's D3) acts.
- It is a positive control, as W3's Script: never a candidate brain, never in the learned-arm readings.

## Arms
| arm | trained? | what |
|---|---|---|
| D3 | W3's 8 runs (cited) | the reference |
| **D3+Y** | 8 runs | "that worked!" |
| **D3+FR** | 8 runs | the store teaches at rest |
| **D3+Y+FR** | 8 runs | both |
| D3+RR | 8 runs | the control: random replay at rest |
| D3+F | test only (W3's D3 weights) | the engineered ceiling |

32 training runs of 2,000,000 steps on GitHub's machines; D3+F and step 0 are tests only.

## Measures and statistics
- Per run: the mean over its 50 test lives of each measure (as W3). Intervals: bootstrap over the 8 seeds (10,000
  draws, numpy seed 20261115, percentiles 2.5 and 97.5). Differences paired by seed (the same seed gives the same
  starting weights and training lands in every arm).
- **Also logged** per run: total gradient updates (actor-critic, Y, replay) so the arms' compute is on the table
  (council); Y events and replays per life; the final link norms and signs (W3's).

## Readings (stated now)
1. **"A learned brain lives":** D3+Y+FR, D3+Y or D3+FR has a survival share with mean ≥ 0.50 and lower bound ≥ 0.30.
2. **"The parts help":** for each of D3+Y, D3+FR, D3+Y+FR: arm − D3 on survival share has a lower bound above 0, or,
   if every survival share is 0, on lifespan (the secondary reading, said as such).
3. **"Content, not compute":** D3+FR − D3+RR on survival share (or lifespan, as above) has a lower bound above 0.
4. **"The ceiling is reachable":** D3+F survives ≥ 0.50 (if not, the learned parts had little room, and the limit is
   said).
5. **Survival to 1,000:** the same four readings on the secondary measure, reported beside, never replacing the
   primary.

## Validity (hard stops; failing one makes W3b invalid, not a finding)
- Checks All: PASS before data (`checks_w3b.py`): the base brain and world unchanged (D3 with no part reproduces W3's
  training log line for seed 1 at 3,102 steps and W3's test file for seed 1 bit for bit); a split run equals an
  unsplit run; Y's event rule fires on a hand-built eating step and not on a plain step; the window stops at the
  previous event and at 15; FR replays only on the shelter and at most 64 times per life; RR's windows are not
  success-selected (their mean weight is 1.0 and their mean relief equals the run's mean); F walks to the stored place
  only when the need is ≥ 0.8; test lands identical across arms; weights unchanged by testing; the same seed twice is
  the same.
- Every run finishes (32 of 32); any run that does not is reported and the arm's n is reduced, never refilled.

## Limits (stated now)
- W3's one world and one body; 8 seeds; the parts' numbers are the council's, fixed, not tuned.
- Y and FR train the head and the planner together through W3's update; the critic is not trained by them.
- F is engineered and test-only; it reuses D3's trained weights, so its "learned part" is W3's.
- Step 0 is a diagnosis, not a fix; nothing in the planner is changed in W3b (council, Gemini's "rising to 50% if a
  bug is fixed first" is not taken: a fix would be a new frozen study).

## The assistant's prior (after the council)
- Step 0: "the values are the broken part": about 50%; "the head": about 25%; neither alone: 25%.
- Reading 1 (a learned brain lives, ≥ 0.50): about 15% (council: 15%, 30%, 8–10%).
- Reading 2 (each part lifts lifespan with an interval above 0): about 55%.
- Reading 3 (FR beats random replay): about 45%.
- Reading 4 (the ceiling D3+F ≥ 0.50): about 60%.
