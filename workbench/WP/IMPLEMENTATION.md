# WP implementation notes (written before the run)

- `wp.py` builds on WS's task and learning, WT's grown-up draws (p = 0.2) and WC's change and tests.
  - All six children share one world: `ws.Home(g)`, the same daily draws and the same test looks.
  - Child c of group g uses seed 1000 × g + c for its weights and its act draws.
- **Watching:** a child watches only on tries with no grown-up, choosing among the other children who have a latest
  try on that kind.
  - The choice draws come from one stream per group, `[g, 11]`.
  - The watched lids that opened become memory steps and are copied (copy rate 0.5).
  - Trust is updated after watching, from the lids that opened.
  - All children watch before any child tries in the same slot. Their new tries become visible only after the slot.
- The S6-alone children never watch, and checks show they do not affect each other.
- Run: after WC finishes, one Idle process for each world (stable, then change), then the analysis.
  Checks: All: PASS (`checks.log`).
