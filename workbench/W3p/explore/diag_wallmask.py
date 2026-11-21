"""W3p diagnosis (exploratory, test-only, no retraining): does value leaking through walls explain the failed detours?
In the trained W3n HRS brains, each planning iteration's value map is pushed down at remembered walls (to its own minimum
minus MARGIN x its spread) before it is passed to neighbours; then the Bob Profile's R2 detour probe (BP-frozen) runs.

  python diag_wallmask.py SEED MODE      MODE in none, min, deep
"""
import sys
from pathlib import Path

HERE = Path(__file__).parent
sys.path.insert(0, str(HERE.parents[1].parent / "scorecard" / "bp"))
import bp_tests as T  # noqa: E402  (numerical settings first)
import numpy as np  # noqa: E402
from bp_tests import W, R3  # noqa: E402

B = T.w3k.B
MODE = sys.argv[2]


def masked_plan(self, maps, levels):
    p, T_ = self.p, maps.shape[0]
    N = B.N
    c_x = B.cols(maps)
    Wstack = np.stack([p["W0"].reshape(-1), p["Ws"].reshape(-1), p["Wf"].reshape(-1), p["Wc"].reshape(-1)], 1)
    parts = c_x @ Wstack
    lev = np.concatenate([np.ones((T_, 1)), levels], 1)
    lev_cells = np.repeat(lev, N * N, axis=0)
    r = (parts * lev_cells).sum(1) + p["br"][0]
    c_r = B.cols(r.reshape(T_, 1, N, N))
    Rq = c_r @ p["Wq"].reshape(B.A, 9).T
    q, idx = Rq, np.arange(T_ * N * N)
    Wv9 = p["Wv"].reshape(B.A, 9).T
    wall = maps[:, W.CH_WALL].reshape(-1) > 0.5
    for _ in range(B.K - 1):
        v = q.max(1)
        if MODE != "none":
            lo = v.min() - (0.0 if MODE == "min" else 3.0 * (v.std() + 1e-9))
            v = np.where(wall, lo, v)
        q = Rq + B.cols(v.reshape(T_, 1, N, N)) @ Wv9
    return (T_, c_x, lev_cells, c_r, [], q)


B.DriveVIN.plan = masked_plan
seed = int(sys.argv[1])
T.w3n.configure("HR", 1)
R = R3.regrowth()
net = T.load_brain("HR", seed)
T.body(False)
print(MODE, seed, T.t_R2(net, R), T.t_M2(net, R), flush=True)
