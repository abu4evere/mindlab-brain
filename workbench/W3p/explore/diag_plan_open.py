"""W3p diagnosis 3 (exploratory): the same value-map check on M2's open cases (food about 8 steps away, any route)."""
import sys
from pathlib import Path
HERE = Path(__file__).parent
sys.path.insert(0, str(HERE.parents[1].parent / "scorecard" / "bp"))
sys.argv = [sys.argv[0], sys.argv[1]]
import diag_plan as D  # noqa: E402  (runs the detour check first)
import numpy as np  # noqa: E402
T, W, R3, net, R, N = D.T, D.W, D.R3, D.net, D.R, D.N
up, hand = [], []
for ls in T.TEST_LANDS:
    w = T.known(ls, R)
    goals = W.block_cells(w.patches[0])
    d = T.dist_map(w.walls, goals)
    cand = [(int(d[y, x]), (x, y)) for y in range(N) for x in range(N)
            if np.isfinite(d[y, x]) and d[y, x] >= 6 and not w.walls[y, x] and (x, y) != w.shelter]
    if not cand:
        continue
    path, start = min(cand, key=lambda c: (abs(c[0] - 8), c[1]))
    w = T.known(ls, R, food_patch=0, age=100)
    w.pos, (w.E, w.F) = start, T.HUNGRY
    fw = net.plan(w.obs_map()[None], np.asarray(R3.levels(w, "D3"), float)[None])
    v = fw[5].reshape(N, N, -1).max(2)
    up.append(D.follow(v, w, start, set(goals), path, +1))
print("open cases: plan uphill reaches food", np.mean(up), "cases", len(up))
