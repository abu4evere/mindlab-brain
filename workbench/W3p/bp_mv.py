"""W3p's readout: the Bob Profile tests (BP-frozen, scorecard/bp/bp_tests.py, unchanged) on W3p's MoveVIN brains, plus
the mechanism measure (does the value map, followed uphill, reach the food in the R2 detour cases?) for MV and HR.
The frozen test file is not edited: this script only tells it where MV's brains are and how to load them.

  python bp_mv.py TEST ARM SEED     TEST in the BP tests, PLAN or WALLS; ARM in MV, MB, MBb, HR
"""
import json
import sys
from pathlib import Path

HERE = Path(__file__).parent
sys.path.insert(0, str(HERE.parent.parent / "scorecard" / "bp"))
sys.path.insert(0, str(HERE))
import bp_tests as T  # noqa: E402  (the numerical settings first)
import numpy as np  # noqa: E402
import w3p  # noqa: E402
from bp_tests import W, R3  # noqa: E402

T.BRAIN_DIRS["MV"] = T.BRAIN_DIRS["MB"] = T.BRAIN_DIRS["MBb"] = HERE / "output"


def load_brain(arm, seed):
    if arm in ("MV", "MB", "MBb"):
        w3p.configure(arm, seed)                     # HR's world and body; the loader builds a MoveVIN
        return w3p.w3k.load_npz(HERE / "output" / f"{arm}_CS_{seed}.npz", seed)
    w3p.B.DriveVIN = w3p.DRIVE
    return T.w3k.load_npz(T.BRAIN_DIRS[arm] / f"{arm}_CS_{seed}.npz", seed)


def plan_uphill(net, R):
    """In R2's detour cases: the value map at the start (max over moves), followed uphill among open neighbours."""
    res = []
    for ls in T.TEST_LANDS:
        c = T.detour_case(ls, R, 5, 4)
        if not c:
            continue
        i, start, path = c
        w = T.known(ls, R, food_patch=i)
        w.pos, (w.E, w.F) = start, T.HUNGRY
        goals = set(W.block_cells(w.patches[i]))
        fw = net.plan(w.obs_map()[None], np.asarray(R3.levels(w, "D3"), float)[None])
        q = fw[5] if type(net).__name__ == "DriveVIN" else fw[8].reshape(5, -1).T
        v = q.reshape(W.N, W.N, -1).max(2)
        pos = start
        for _ in range(3 * path):
            if pos in goals:
                break
            nbs = [(pos[0] + dx, pos[1] + dy) for dx, dy in W.MOVES[:4]]
            nbs = [n for n in nbs if not w.walls[n[1], n[0]]]
            pos = max(nbs, key=lambda n: v[n[1], n[0]])
        res.append(pos in goals)
    return {"uphill": float(np.mean(res)), "cases": len(res)}


def walls(net, R):
    """MoveVIN only: mean "can I enter here?" at walls and at open places, memory fully known, on the 50 test lands."""
    import brain_mv as M
    pw, po = [], []
    for ls in T.TEST_LANDS:
        w = T.known(ls, R)
        c = M.B.cols(w.obs_map()[None])
        pas = M.sig(c @ net.p["Wp"].reshape(-1) + net.p["bp"][0]).reshape(W.N, W.N)
        pw.append(pas[w.walls].mean())
        po.append(pas[~w.walls].mean())
    return {"walls": float(np.mean(pw)), "open": float(np.mean(po)), "gap": float(np.mean(po) - np.mean(pw))}


def main():
    test, arm, seed = sys.argv[1], sys.argv[2], int(sys.argv[3])
    T.OUT.mkdir(exist_ok=True)
    R = R3.regrowth()
    T.w3n.configure("HR", 1)
    agent = load_brain(arm, seed)
    name = f"{arm}S_{seed}"
    if test == "PLAN":
        res = plan_uphill(agent, R)
    elif test == "WALLS":
        res = walls(agent, R)
    else:
        prev = T.body(test not in T.BARE)
        res = T.TESTS[test](agent, R)
        T.body(prev[0] == "walk")
    res.update(test=test, agent=name)
    (T.OUT / f"{test}_{name}.json").write_text(json.dumps(res, indent=1))
    print(json.dumps(res), flush=True)


if __name__ == "__main__":
    main()
