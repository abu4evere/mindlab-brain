"""W3p diagnosis (exploratory): the pilot's bump brains (PMB, seeds 1-3) with their passability replaced by the truth from
their own map memory (walls 0, everything else 1), no retraining; R2 and R5d probes (BP-frozen functions). Also the
longest shortest path among the probes' cases (the planner runs 30 rounds)."""
import sys
from pathlib import Path
HERE = Path(__file__).parent
sys.path.insert(0, str(HERE.parent))
import bp_mv  # noqa: E402
from bp_mv import T, w3p, R3, W  # noqa: E402
import numpy as np  # noqa: E402
import brain_mv as M  # noqa: E402

R = R3.regrowth()
paths = {"R2": [], "R5d": []}
for ls in T.TEST_LANDS:
    for k, (mp, me) in (("R2", (5, 4)), ("R5d", (10, 10))):
        c = T.detour_case(ls, R, mp, me)
        if c:
            paths[k].append(c[2])
print("longest shortest path: R2", max(paths["R2"]), "R5d", max(paths["R5d"]), "(planner rounds:", M.K, ")")
orig = M.MoveVIN.plan


def oracle_plan(self, maps, levels):
    fw = list(orig(self, maps, levels))
    T_ = maps.shape[0]
    pas = 1.0 - maps[:, W.CH_WALL]
    # recompute the loop with the true passability (same code path as brain_mv.plan, from r)
    r, gam = fw[3], fw[6]
    pn = [M.shift_in(pas, dx, dy) for dx, dy in M.MOVES]
    v = r
    for _ in range(M.K):
        m = [pn[a] * M.shift_in(v, *M.MOVES[a]) + (1 - pn[a]) * v for a in range(4)] + [v]
        q = r[None] + gam * np.stack(m)
        v = q.max(0)
    fw[8], fw[9] = q, v
    return tuple(fw)


T.w3n.configure("HR", 1)
T.body(False)
for s in (1, 2, 3):
    w3p.configure("PMB", s)
    net = w3p.w3k.load_npz(HERE.parent / "output" / f"PMB_CS_{s}.npz", s)
    M.MoveVIN.plan = orig
    learned = (T.t_R2(net, R)["success"], T.t_R5d(net, R)["success"])
    M.MoveVIN.plan = oracle_plan
    ideal = (T.t_R2(net, R)["success"], T.t_R5d(net, R)["success"])
    M.MoveVIN.plan = orig
    print(f"seed {s}: learned walls R2 {learned[0]:.2f} R5d {learned[1]:.2f} | ideal walls R2 {ideal[0]:.2f} R5d {ideal[1]:.2f}")
