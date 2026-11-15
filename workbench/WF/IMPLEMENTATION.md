# WF implementation notes (written before the run)

- **Base and TBYS** call WY's `run_child` (they reproduce WY, checked).
- **RP, FMin and WSLS** use `wf.try_box`, which equals WM's `try_box` when it has no extras and no forcing (checked),
  plus TB's blocking and WY's "that worked!" (with expectations per kind and lid, as in WY).
- **The store:**
  - set to (pair, fresh) when a lid opens;
  - marked stale when the stored pair fails on that lid (a different failing pair leaves it as it is).
- **RP:** at the end of each day, for every kind, the fresh stored pairs from lid 1 onward are copied twice with WS's
  copy step at rate 1.0. The look is the kind's look with no noise; there is no memory prefix.
- **FMin:**
  - 9 more input columns drawn from `[seed, 16]`;
  - the showing steps get zeros for them;
  - tests see the store.
- **WSLS:**
  - lids with a fresh stored pair are forced, in practice and in tests;
  - the forced acts are learned like chosen ones (reinforcement and "that worked!").
- **Analysis:** WM's script with arms Base, TBYS, RP, FMin, WSLS; differences against TBYS.
- Run on GitHub's machines (`run.yml`): 10 jobs of 48 children. Checks: All: PASS (`checks.log`).
