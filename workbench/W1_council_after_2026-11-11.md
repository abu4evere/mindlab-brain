# W1 (detour) council: answers (11 November 2026)

Question: `W1_detour_draft.md`, attached as a file, with four questions. DeepSeek was not reached (its page does not
take input).

## GPT (chat 6af52773), labelled as GPT
- **Verdict:** "Approve the direction, but revise before freezing." Passing a detour is not proof of looking ahead: a
  memorised navigation policy can pass too.
- **Q1:** the window and smell are fair. M must learn (build) its own map. Check that smell does not encode the route,
  add unseen wall shapes and longer detours, and make sure every test can be solved within 60 steps.
- **Q2:** fair, but M must be labelled "learned map + engineered planning", not learned planning. Add M's map without
  the BFS.
- **Q3:** a feed-forward net trained by **imitation of an expert**, on the same inputs as F. It separates "actor-critic
  failed" from "this kind of brain cannot".
- **Biggest risk:** mistaking navigation for planning: R may learn wall-following, and M's BFS does the planning.
- **Changes:**
  - a wall-following baseline;
  - the imitation control;
  - M without its planner;
  - new wall topologies and longer detours;
  - not the gap alone (a brain failing both kinds has no gap): absolute detour success and excess path length;
  - intervals fixed in advance.
- **Probabilities:** F reactive 70%; R looks ahead 30%; M looks ahead 65%.

## Gemini (chat 0b992304), labelled as Gemini
- **View:** "clean, minimal". The held-out layouts prevent rote memory.
- **Q1:** fair. M must build its own map.
- **Q2:** fair for one ability at a time.
- **Q3:** F given the true shortest-path direction, or the full grid.
- **Biggest risk:** the same, a wall-following "bug algorithm". Also, M's rule for unseen cells is unspecified: it
  should be optimistic (unseen = open).
- **Changes:**
  - **add dead ends (T-junctions, false pockets)** so wall-hugging wastes steps;
  - **a cost bound:** median path at most 1.5 × the shortest;
  - specify M's unseen-cell rule;
  - the control baseline.
- **Probabilities:** F reactive 70%; R looks ahead 35%; M looks ahead 65%.

## Taken (the assistant)
- **A wall-follower W** as a second negative control.
- **Dead-end pockets** in a share of the layouts.
- **Unseen topologies** in the test.
- **"Looks ahead"** needs high detour success *and* a path-length bound.
- **F-imit:** F's network trained by imitating the planner B, on F's own inputs.
- **M** is "remembers what it saw + plans on it (optimistic BFS)", labelled engineered planning.
- **M−:** M's map, but greedy on it, no planning.
- **Intervals:** paired over seeds and layouts.
