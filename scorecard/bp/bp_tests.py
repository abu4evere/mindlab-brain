"""The Bob Profile tests, levels 2 and 5, in W3's world (scorecard/bob_profile_draft.md). DRAFT until tag BP-frozen.

Agents: a W3n brain (its kept copy, with the body as trained or bare), W3's Script (the positive control), a random
agent (the negative control), and for the detours a greedy agent (the bar to beat). Every test returns per-seed values
for brains and fixed values for the controls; bp_score.py turns them into levels.

  python bp_tests.py TEST ARM SEED      e.g.  python bp_tests.py R2 HR 3       (writes output/<TEST>_<ARM>_<SEED>.json)
  python bp_tests.py TEST CONTROL       CONTROL in script, random, greedy
"""
from __future__ import annotations

import json
import sys
from collections import deque
from pathlib import Path

HERE = Path(__file__).parent
WB = HERE.parent.parent / "workbench"
sys.path.insert(0, str(WB / "W3n"))
import w3n  # noqa: E402  (W3n, W3m, W3k: the numerical settings before numpy loads)
import numpy as np  # noqa: E402
from w3n import w3k, w3m, W  # noqa: E402
from w3k import R3, w3i  # noqa: E402

OUT = HERE / "output"
BRAIN_DIRS = {"HR": WB / "W3n" / "output", "RE": WB / "W3o" / "output", "RV": WB / "W3o" / "output"}
TEST_LANDS = list(W.TEST_SEEDS)                      # 900001-900050, held out from every W3 training
FRESH_LANDS = list(w3i.FRESH_SEEDS)                  # 910001-910050
BIG_LANDS = list(range(930001, 930051))              # G5's bigger map (21 x 21), never used before
DENSE_LANDS = list(range(940001, 940051))            # G2 (v2, council): W3's land generator with 8 wall segments, not 4
TRAIN_LIVES = range(1, 51)                           # G2: the first 50 lands of the brain's own training
HUNGRY, TIRED = (60.0, 0.0), (150.0, 150.0)


# ── agents ────────────────────────────────────────────────────────────────────────────────────────────────────────
def body(on):
    """The W3n HR body (sleep and hunger reflexes) on or off; returns the previous setting."""
    prev = (w3m.PART["reflex"], w3n.BODY["hunger"])
    w3m.PART["reflex"], w3n.BODY["hunger"] = ("walk", True) if on else (False, False)
    return prev


def load_brain(arm, seed):
    w3n.configure("HR", seed)                        # HR's world and body; W3o's eyes for RE and RV
    if arm in ("RE", "RV"):
        sys.path.insert(0, str(WB / "W3o"))
        import w3o
        w3o.configure(arm, seed)
    return w3k.load_npz(BRAIN_DIRS[arm] / f"{arm}_CS_{seed}.npz", seed)


def life_policy(agent, rng):
    """A fresh policy for one whole life: agent is a net, or 'script', or 'random'."""
    if agent == "script":
        s = W.Script()
        return lambda w: s.act(W.MapView(w))
    if agent == "random":
        return lambda w: int(rng.integers(5))
    return w3i.policy(agent, rng)                    # the brain, with the body's reflexes as currently set


import inspect  # noqa: E402
_src = inspect.getsource(W.make_land).replace("for _ in range(4):", "for _ in range(8):").replace(
    "def make_land(", "def make_dense_land(")
assert "range(8)" in _src
_ns = dict(W.__dict__)
exec(compile(_src, "make_dense_land", "exec"), _ns)
make_dense_land = _ns["make_dense_land"]


def run_life(agent, ls, R, dense=False):
    rng = np.random.default_rng(ls)
    land = make_dense_land(ls) if dense else W.make_land(ls)
    _, m = R3.run_life(life_policy(agent, rng), land, R, rng)
    return m


def first_move(agent, w, rng):
    """The agent's chosen move in a set state (no reflex): the brain's most likely move."""
    if agent == "script":
        return W.Script().act(W.MapView(w))
    if agent == "random":
        return int(rng.integers(5))
    if agent == "greedy":
        raise ValueError("greedy acts only in walks")
    a, _, _ = agent.act(w.obs_map(), R3.levels(w, "D3"), w.pos, None, greedy=True)
    return a


# ── set states on a land ─────────────────────────────────────────────────────────────────────────────────────────
def dist_map(walls, goals):
    d = np.full((W.N, W.N), np.inf)
    q = deque()
    for (x, y) in goals:
        d[y, x] = 0
        q.append((x, y))
    while q:
        x, y = q.popleft()
        for dx, dy in W.MOVES[:4]:
            nx, ny = x + dx, y + dy
            if 0 <= nx < W.N and 0 <= ny < W.N and not walls[ny, nx] and d[ny, nx] == np.inf:
                d[ny, nx] = d[y, x] + 1
                q.append((nx, ny))
    return d


def known(ls, R, food_patch=None, age=0):
    """A world whose map memory knows the walls and the shelter, and food only on one patch (or none). age: every
    memory was written that many steps ago (the clock is moved on, the memory's times are left at 0)."""
    w = W.World(W.make_land(ls), R)
    w.m_seen[:] = True
    w.m_wall[:] = w.walls
    w.m_shelter[:] = False
    w.m_shelter[w.shelter[1], w.shelter[0]] = True
    w.m_food[:] = False
    if food_patch is not None:
        for (x, y) in W.block_cells(w.patches[food_patch]):
            w.m_food[y, x] = True
    if age:
        w.t = age
        w.m_last[:] = 0
    return w


def manhattan_to(goals, c):
    return min(abs(c[0] - g[0]) + abs(c[1] - g[1]) for g in goals)


def detour_case(ls, R, min_path, min_extra):
    """The start cell on this land with the smallest detour (path minus Manhattan distance) that still qualifies:
    path >= min_path and detour >= min_extra (the easiest case at that level; ties: the shorter path, then the first
    cell in reading order); patches tried in order; None if the land has none."""
    w = known(ls, R)
    for i in range(3):
        goals = W.block_cells(w.patches[i])
        d = dist_map(w.walls, goals)
        best = None
        for y in range(W.N):
            for x in range(W.N):
                if w.walls[y, x] or not np.isfinite(d[y, x]) or (x, y) == w.shelter:
                    continue
                path, extra = int(d[y, x]), int(d[y, x]) - manhattan_to(goals, (x, y))
                if path >= min_path and extra >= min_extra and (best is None or (extra, path) < (best[0], best[2])):
                    best = (extra, (x, y), path)
        if best:
            return i, best[1], best[2]
    return None


def walk_to_food(agent, ls, R, patch, start, path, age=0, rng=None, erase=False):
    """From start, hungry, memory knowing only that patch: does the agent reach it within 3 x the shortest path?
    erase: the cheater control for memory, the same walk with the food erased from memory."""
    w = known(ls, R, food_patch=None if erase else patch, age=age)
    w.pos, (w.E, w.F) = start, HUNGRY
    goals = set(W.block_cells(w.patches[patch]))
    for _ in range(3 * path):
        if agent == "greedy":
            here = manhattan_to(goals, w.pos)
            opts = [a for a in range(4) if not w.walls[w.pos[1] + W.MOVES[a][1], w.pos[0] + W.MOVES[a][0]]
                    and manhattan_to(goals, (w.pos[0] + W.MOVES[a][0], w.pos[1] + W.MOVES[a][1])) < here]
            a = opts[0] if opts else 4
        elif agent in ("script", "random"):
            a = first_move(agent, w, rng)
        else:                                        # a walk uses the brain's moves as in its life: drawn from it
            a, _, _ = agent.act(w.obs_map(), R3.levels(w, "D3"), w.pos, rng)
        w.step(a)
        w.E, w.F = HUNGRY                            # the state is held: a probe of choice, not of survival
        if w.pos in goals:
            return True
    return False


# ── the tests ────────────────────────────────────────────────────────────────────────────────────────────────────
def t_L2(agent, R):
    """Learning 2: lifespan on the 50 test lands, body as trained (normalised against random and Script in scoring)."""
    return {"lifespan": float(np.mean([run_life(agent, ls, R)["lifespan"] for ls in TEST_LANDS]))}


def t_detour(agent, R, min_path, min_extra):
    rng = np.random.default_rng(7)
    res = []
    for ls in TEST_LANDS:
        case = detour_case(ls, R, min_path, min_extra)
        if case:
            res.append(walk_to_food(agent, ls, R, *case, rng=rng))
    return {"success": float(np.mean(res)), "cases": len(res)}


def t_R2(agent, R):
    """Reasoning 2: a goal 5+ steps away behind a wall (detour 4+), memory known, hungry, no reflex."""
    return t_detour(agent, R, 5, 4)


def t_R5d(agent, R):
    """Reasoning 5, the detour half: 10+ steps away with a detour of 10+."""
    return t_detour(agent, R, 10, 10)


def t_M2(agent, R, erase=False):
    """Memory 2: food seen 100 steps ago, now out of sight (6+ steps away), any memory; hungry, no reflex.
    erase: the same with the food erased from memory (the cheater control: success must drop)."""
    rng = np.random.default_rng(11)
    res = []
    for ls in TEST_LANDS:
        w = known(ls, R)
        goals = W.block_cells(w.patches[0])
        d = dist_map(w.walls, goals)
        cand = [(int(d[y, x]), (x, y)) for y in range(W.N) for x in range(W.N)
                if np.isfinite(d[y, x]) and d[y, x] >= 6 and not w.walls[y, x] and (x, y) != w.shelter]
        if cand:
            path, start = min(cand, key=lambda c: (abs(c[0] - 8), c[1]))   # the cell nearest 8 steps away
            res.append(walk_to_food(agent, ls, R, 0, start, path, age=100, rng=rng, erase=erase))
    return {"success": float(np.mean(res)), "cases": len(res)}


def t_M2e(agent, R):
    return t_M2(agent, R, erase=True)


def t_G2(agent, R, seed=None):
    """Generalization 2 (v2, council): lifespan on 50 lands of a new kind (twice the wall segments) against its own
    lifespan on the standard test lands; body as trained."""
    dense = float(np.mean([run_life(agent, ls, R, dense=True)["lifespan"] for ls in DENSE_LANDS]))
    test = float(np.mean([run_life(agent, ls, R)["lifespan"] for ls in TEST_LANDS]))
    return {"dense": dense, "test": test, "ratio": dense / test}


def t_A2(agent, R):
    """Autonomy 2: the first move follows the larger need. On lands where the first step toward food and toward the
    shelter differ: P(toward food | hungry) - P(toward food | tired), and the same for the shelter."""
    rng = np.random.default_rng(13)
    counts = {"food|hungry": [], "food|tired": [], "shelter|tired": [], "shelter|hungry": []}
    for ls in TEST_LANDS:
        base = known(ls, R, food_patch=0)
        dfood = dist_map(base.walls, W.block_cells(base.patches[0]))
        dshel = dist_map(base.walls, [base.shelter])
        p = base.land["start"]

        def toward(d, a):
            nx, ny = p[0] + W.MOVES[a][0], p[1] + W.MOVES[a][1]
            return a != 4 and not base.walls[ny, nx] and d[ny, nx] < d[p[1], p[0]]
        if any(toward(dfood, a) and toward(dshel, a) for a in range(4)):
            continue                                   # one step serves both: the land cannot tell them apart
        for state, (E, F) in (("hungry", HUNGRY), ("tired", TIRED)):
            w = known(ls, R, food_patch=0)
            w.E, w.F = E, F
            a = first_move(agent, w, rng)
            counts[f"food|{state}"].append(toward(dfood, a))
            counts[f"shelter|{state}"].append(toward(dshel, a))
    m = {k: float(np.mean(v)) for k, v in counts.items()}
    m["tracks"] = 0.5 * ((m["food|hungry"] - m["food|tired"]) + (m["shelter|tired"] - m["shelter|hungry"]))
    m["cases"] = len(counts["food|hungry"])
    return m


def t_A5s(agent, R):
    """Autonomy 5, the survival half: bare (no reflexes) full lives on the 50 fresh lands."""
    return {"survived": float(np.mean([run_life(agent, ls, R)["survived"] for ls in FRESH_LANDS]))}


TESTS = {"L2": t_L2, "R2": t_R2, "R5d": t_R5d, "M2": t_M2, "M2e": t_M2e, "G2": t_G2, "A2": t_A2, "A5s": t_A5s}
BARE = {"R2", "R5d", "M2", "M2e", "A2", "A5s"}             # tests run with the reflexes off (probes, and A5's bare survival)


def main():
    test, who = sys.argv[1], sys.argv[2]
    OUT.mkdir(exist_ok=True)
    R = R3.regrowth()
    w3n.configure("HR", 1)                           # the world every agent is tested in (HR's body for brains)
    if who in ("script", "random", "greedy"):
        if test in ("L2", "A5s", "G2") and who == "greedy":
            return
        agent, seed, name = who, None, who
    else:
        seed = int(sys.argv[3])
        agent, name = load_brain(who, seed), f"{who}S_{seed}"
    prev = body(test not in BARE)
    res = TESTS[test](agent, R)
    body(prev[0] == "walk")
    res.update(test=test, agent=name)
    (OUT / f"{test}_{name}.json").write_text(json.dumps(res, indent=1))
    print(json.dumps(res), flush=True)


if __name__ == "__main__":
    main()
