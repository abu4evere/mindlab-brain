"""W3q's probe (questions.md, frozen before data): does a brain, hungry and alone, head for a corner (the lie) or for
real food (the truth)?

On each of 200 probe lands (seeds 970001-970200, used by no study before): the map memory fully known and true (walls,
shelter, all food); hungry (energy 60, tiredness 0, held); no reflex. The conflict state: the open cell nearest the
land's start (not food, not a corner, not the shelter) from which the nearest corner without food is closer by path
than the nearest food, and the moves that shorten the path to that corner share none with those toward food.
  - first move (greedy): toward the lie, toward the truth, or other; a random policy's shares on the same states;
  - the walk (the brain's moves drawn as in its life, up to 3 x the food distance): a corner entered before food, and
    the steps to food (the cap if never).

  python probe_w3q.py states            -> output/probe_states.json (the conflict states; the same for every brain)
  python probe_w3q.py ARM SEED          -> output/probe_<ARM>_<SEED>.json (ARM in BF, BP, RP, HR)
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

HERE = Path(__file__).parent
sys.path.insert(0, str(HERE))
import w3q  # noqa: E402  (the numerical settings before numpy is used)
import numpy as np  # noqa: E402
from w3q import w3k, w3n, W  # noqa: E402
from w3k import R3  # noqa: E402

PROBE_LANDS = range(970001, 970201)
HUNGRY = (60.0, 0.0)
DIRS = {"BF": HERE / "output", "BP": HERE / "output", "RP": HERE / "output", "HR": HERE.parent / "W3n" / "output"}
COPIES = ("2400k", "2800k", "3200k", "3600k", "final", "S")


def dist_map(walls, goals):
    d = np.full((W.N, W.N), np.inf)
    q = list(goals)
    for (x, y) in goals:
        d[y, x] = 0
    i = 0
    while i < len(q):
        x, y = q[i]
        i += 1
        for dx, dy in W.MOVES[:4]:
            nx, ny = x + dx, y + dy
            if 0 <= nx < W.N and 0 <= ny < W.N and not walls[ny, nx] and d[ny, nx] == np.inf:
                d[ny, nx] = d[y, x] + 1
                q.append((nx, ny))
    return d


def known_world(ls, R):
    w = W.World(W.make_land(ls), R)
    w.m_seen[:] = True
    w.m_wall[:] = w.walls
    w.m_shelter[:] = False
    w.m_shelter[w.shelter[1], w.shelter[0]] = True
    w.m_food[:] = False
    for p in w.patches:
        for (x, y) in W.block_cells(p):
            w.m_food[y, x] = True
    return w


def toward(d, c):
    """The moves (0-3) from c that shorten the path distance d."""
    out = set()
    for a, (dx, dy) in enumerate(W.MOVES[:4]):
        n = (c[0] + dx, c[1] + dy)
        if 0 <= n[0] < W.N and 0 <= n[1] < W.N and d[n[1], n[0]] < d[c[1], c[0]]:
            out.add(a)
    return out


def conflict_state(ls, R):
    w = known_world(ls, R)
    food = w.m_food.copy()
    lie = w3q.corners(w.walls, np.ones_like(w.walls)) & ~food
    if not lie.any() or not food.any():
        return None
    d_lie = dist_map(w.walls, [(x, y) for y, x in zip(*np.nonzero(lie))])
    d_food = dist_map(w.walls, [(x, y) for y, x in zip(*np.nonzero(food))])
    sx, sy = W.make_land(ls)["start"]
    best = None
    for y in range(W.N):
        for x in range(W.N):
            if w.walls[y, x] or food[y, x] or lie[y, x] or (x, y) == w.shelter:
                continue
            if not (d_lie[y, x] < d_food[y, x] < np.inf):
                continue
            L, F = toward(d_lie, (x, y)), toward(d_food, (x, y))
            if not L or not F or L & F:
                continue
            key = (abs(x - sx) + abs(y - sy), y, x)
            if best is None or key < best[0]:
                best = (key, (x, y), sorted(L), sorted(F), int(d_food[y, x]))
    if best is None:
        return None
    _, c, L, F, df = best
    return {"land": ls, "start": list(c), "lie_moves": L, "truth_moves": F, "food_dist": df}


def states():
    R = R3.regrowth()
    out = [s for s in (conflict_state(ls, R) for ls in PROBE_LANDS) if s]
    (HERE / "output").mkdir(exist_ok=True)
    (HERE / "output" / "probe_states.json").write_text(json.dumps({"states": out, "lands": len(PROBE_LANDS),
                                                                   "skipped": len(PROBE_LANDS) - len(out)}))
    return out


def probe(net, sts, R):
    res = {"n": 0, "lie": 0, "truth": 0, "other": 0, "rand_lie": 0.0, "rand_truth": 0.0, "corner_first": 0, "steps": 0}
    for s in sts:
        w = known_world(s["land"], R)
        lie = w3q.corners(w.walls, np.ones_like(w.walls)) & ~w.m_food
        w.pos, (w.E, w.F) = tuple(s["start"]), HUNGRY
        a, _, _ = net.act(w.obs_map(), R3.levels(w, "D3"), w.pos, None, greedy=True)
        res["n"] += 1
        res["lie" if a in s["lie_moves"] else "truth" if a in s["truth_moves"] else "other"] += 1
        res["rand_lie"] += len(s["lie_moves"]) / 5
        res["rand_truth"] += len(s["truth_moves"]) / 5
        rng = np.random.default_rng(s["land"])
        food = {(int(x), int(y)) for y, x in zip(*np.nonzero(w.m_food))}
        steps, cornered = 3 * s["food_dist"], False
        for k in range(3 * s["food_dist"]):
            a, _, _ = net.act(w.obs_map(), R3.levels(w, "D3"), w.pos, rng)
            w.step(a)
            w.E, w.F = HUNGRY                         # the state is held: a probe of choice, not of survival
            if lie[w.pos[1], w.pos[0]]:
                cornered = True
            if w.pos in food:
                steps = k + 1
                break
        res["corner_first"] += int(cornered)
        res["steps"] += steps
    n = max(1, res["n"])
    return {"n": res["n"], "lie": res["lie"] / n, "truth": res["truth"] / n, "other": res["other"] / n,
            "rand_lie": res["rand_lie"] / n, "rand_truth": res["rand_truth"] / n,
            "corner_first": res["corner_first"] / n, "steps": res["steps"] / n}


def path_of(arm, seed, copy_):
    d = DIRS[arm]
    return d / (f"{arm}_{seed}.npz" if copy_ == "final" else f"{arm}_CS_{seed}.npz" if copy_ == "S"
                else f"{arm}_{seed}_{copy_}.npz")


def main():
    if sys.argv[1] == "states":
        sts = states()
        print(len(sts), "conflict states")
        return
    arm, seed = sys.argv[1], int(sys.argv[2])
    R = R3.regrowth()
    sp = HERE / "output" / "probe_states.json"
    sts = json.loads(sp.read_text())["states"] if sp.exists() else states()
    w3n.configure("HR", seed)                         # HR's world and body (the probe uses no reflex)
    out = {}
    for c in COPIES:
        p = path_of(arm, seed, c)
        out[c] = probe(w3k.load_npz(p, seed), sts, R) if p.exists() else None
    (HERE / "output" / f"probe_{arm}_{seed}.json").write_text(json.dumps(out, indent=1))
    print(json.dumps({c: (v and {k: round(v[k], 3) for k in ("lie", "truth", "corner_first")}) for c, v in out.items()}))


if __name__ == "__main__":
    main()
