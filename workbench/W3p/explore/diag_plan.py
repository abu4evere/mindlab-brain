"""W3p diagnosis 2 (exploratory, test-only): in the R2 detour cases, is the plan or the hand at fault?
For each case: the brain's value map at the start (max over its 8 planning channels after 30 rounds); following it
uphill (or downhill) among open neighbours from the start, does the path reach the food within 3 x the shortest path?
And the hand: the brain's own most likely first move vs the value map's best neighbour."""
import sys
from pathlib import Path

HERE = Path(__file__).parent
sys.path.insert(0, str(HERE.parents[1].parent / "scorecard" / "bp"))
import bp_tests as T  # noqa: E402
import numpy as np  # noqa: E402
from bp_tests import W, R3  # noqa: E402

seed = int(sys.argv[1])
T.w3n.configure("HR", 1)
R = R3.regrowth()
net = T.load_brain("HR", seed)
N = W.N


def follow(v, w, start, goals, path, sign):
    pos = start
    for _ in range(3 * path):
        if pos in goals:
            return True
        best, bv = None, None
        for dx, dy in W.MOVES[:4]:
            n = (pos[0] + dx, pos[1] + dy)
            if not w.walls[n[1], n[0]] and (bv is None or sign * v[n[1], n[0]] > bv):
                best, bv = n, sign * v[n[1], n[0]]
        pos = best
    return pos in goals


res = {"up": [], "down": [], "hand_agrees_up": [], "chan": []}
for ls in T.TEST_LANDS:
    c = T.detour_case(ls, R, 5, 4)
    if not c:
        continue
    i, start, path = c
    w = T.known(ls, R, food_patch=i)
    w.pos, (w.E, w.F) = start, T.HUNGRY
    goals = set(W.block_cells(w.patches[i]))
    fw = net.plan(w.obs_map()[None], np.asarray(R3.levels(w, "D3"), float)[None])
    q = fw[5].reshape(N, N, -1)
    v = q.max(2)
    res["up"].append(follow(v, w, start, goals, path, +1))
    res["down"].append(follow(v, w, start, goals, path, -1))
    # each planning channel on its own, followed uphill
    res["chan"].append([follow(q[:, :, k], w, start, goals, path, +1) for k in range(q.shape[2])])
    a, pi, _ = net.act(w.obs_map(), R3.levels(w, "D3"), w.pos, None, greedy=True)
    nb = [(a2, v[start[1] + W.MOVES[a2][1], start[0] + W.MOVES[a2][0]]) for a2 in range(4)
          if not w.walls[start[1] + W.MOVES[a2][1], start[0] + W.MOVES[a2][0]]]
    res["hand_agrees_up"].append(a == max(nb, key=lambda t: t[1])[0])
print(seed, "plan uphill reaches food", np.mean(res["up"]), "| downhill", np.mean(res["down"]),
      "| hand picks the uphill neighbour", np.mean(res["hand_agrees_up"]),
      "| per channel uphill", np.round(np.mean(res["chan"], 0), 2), "| cases", len(res["up"]))
