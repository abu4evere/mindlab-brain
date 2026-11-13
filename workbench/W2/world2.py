"""W2's world (questions.md, W2-frozen): W1b's area and layouts with a 3 x 3 view, a remembered map, scripted tours,
the scripted brains, and the test sets.

  python workbench/W2/world2.py        # builds sets.json (seed 20261122) and prints the counts
"""
from __future__ import annotations

import json
import sys
from collections import Counter
from pathlib import Path

import numpy as np

HERE = Path(__file__).parent
sys.path.insert(0, str(HERE.parent / "W1b"))
sys.path.insert(0, str(HERE.parent / "W1"))
import world_b as W  # noqa: E402

N, MOVES, MAX_STEPS, EFF = W.N, W.MOVES, W.MAX_STEPS, W.EFF
blocked, manhattan, shortest = W.blocked, W.manhattan, W.shortest
SET_SEED = 20261122
R = 1                       # view radius (3 x 3)
COVER = 0.60                # the tour stops when this share of the open cells has been in view


# --- the remembered map ----------------------------------------------------------------------------------------------
class Mem:
    """known[y, x] and wall[y, x]; the fixed writer stores what the view shows. `erase` forgets everything."""

    def __init__(self):
        self.known = np.zeros((N, N), bool)
        self.wall = np.zeros((N, N), bool)

    def see(self, walls, pos):
        for dy in range(-R, R + 1):
            for dx in range(-R, R + 1):
                x, y = pos[0] + dx, pos[1] + dy
                if 0 <= x < N and 0 <= y < N:
                    self.known[y, x] = True
                    self.wall[y, x] = (x, y) in walls

    def copy(self):
        m = Mem()
        m.known, m.wall = self.known.copy(), self.wall.copy()
        return m

    def walls(self):
        """Known walls as a set of cells (unknown cells count as open)."""
        ys, xs = np.nonzero(self.known & self.wall)
        return set(zip(xs.tolist(), ys.tolist()))

    def channels(self, goal):
        """The planner's input: known wall, unknown, food (3, N, N)."""
        f = np.zeros((N, N))
        f[goal[1], goal[0]] = 1.0
        return np.stack([(self.known & self.wall).astype(float), (~self.known).astype(float), f])


def view_mem(walls, pos):
    m = Mem()
    m.see(walls, pos)
    return m


def flood(walls, start):
    """Every cell reachable from start (one BFS)."""
    seen, todo = {start}, [start]
    while todo:
        c = todo.pop()
        for dx, dy in MOVES[:4]:
            n = (c[0] + dx, c[1] + dy)
            if n not in seen and not blocked(walls, *n):
                seen.add(n)
                todo.append(n)
    return seen


# --- tours -----------------------------------------------------------------------------------------------------------
def tour(lay, rng):
    """From a random open cell, shortest walks between random open waypoints until COVER of the open cells have been in
    view. The start cell's 3 x 3 is never walked through. Returns the list of cells visited (in order)."""
    walls, s = lay["walls"], lay["start"]
    banned = {(s[0] + dx, s[1] + dy) for dx in range(-R, R + 1) for dy in range(-R, R + 1)}
    tw = set(walls) | banned
    opens = [(x, y) for x in range(N) for y in range(N) if (x, y) not in walls]
    cand = [c for c in opens if c not in banned]
    pos = cand[int(rng.integers(len(cand)))]
    fl = flood(tw, pos)
    reach = [c for c in cand if c in fl]
    mem, cells = Mem(), [pos]
    mem.see(walls, pos)
    need = lay.get("must_see")
    for _ in range(200):
        seen = sum(mem.known[y, x] for x, y in opens) / len(opens)
        if seen >= COVER and (need is None or mem.known[need[1], need[0]]):
            break
        wp = reach[int(rng.integers(len(reach)))]
        if need is not None and seen >= COVER:
            wp = min(reach, key=lambda c: (manhattan(c, need), c))
        for c in shortest(tw, pos, wp)[1][1:]:
            cells.append(c)
            mem.see(walls, c)
        pos = wp
    return cells


def tour_mem(lay, cells):
    m = Mem()
    for c in cells:
        m.see(lay["walls"], c)
    return m


# --- the scripted brains (they act on what they are allowed to know) -------------------------------------------------
class ViewEnv:
    """What a brain sees: walls only in the 3 x 3 view (enough for every move), plus its cell and the food's."""

    def __init__(self, env):
        self.pos, self.goal = env.pos, env.goal
        self.walls = view_mem(env.walls, env.pos).walls()


class MapBFS:
    """Bp: BFS on the remembered map (unknown = open), replanning each step. B0: the same on the current view only."""

    def __init__(self, name):
        self.name = name

    def reset(self, env, mem=None):
        self.mem = mem.copy() if (mem is not None and self.name == "Bp") else Mem()

    def act(self, env):
        if self.name == "B0":
            self.mem = Mem()
        self.mem.see(env.walls, env.pos)
        path = shortest(self.mem.walls(), env.pos, env.goal)[1]
        if path is None or len(path) < 2:
            return 4
        return MOVES.index((path[1][0] - env.pos[0], path[1][1] - env.pos[1]))


class OnView:
    """W1b's reactive controls (G, W, W2, H2) and M-, acting on the 3 x 3 view."""

    def __init__(self, brain):
        self.b, self.name = brain, brain.name

    def reset(self, env, mem=None):
        self.b.reset(ViewEnv(env))

    def act(self, env):
        return self.b.act(ViewEnv(env))


def controls():
    return {"Bp": MapBFS("Bp"), "B0": MapBFS("B0"), "G": OnView(W.Greedy()), "W": OnView(W.Bug("W")),
            "W2": OnView(W.Bug("W2")), "H2": OnView(W.Bug("H2")), "M-": OnView(W.Wander())}


def run(brain, lay, mem=None):
    """One episode; mem is the map after the tour (familiar room) or None (new room)."""
    env = W.Env(lay)
    brain.reset(env, mem)
    path = [env.pos]
    while not env.done:
        env.step(brain.act(env))
        path.append(env.pos)
    ok = env.pos == env.goal
    return {"solved": ok, "steps": env.t, "efficient": ok and env.t <= EFF * lay["shortest"], "path": path}


# --- the look-alike pairs --------------------------------------------------------------------------------------------
def rot(c, k):
    x, y = c
    for _ in range(k):
        x, y = N - 1 - y, x
    return (x, y)


def lookalike(rng):
    """A barrier across the room with one gap k = 3-4 to the left (A) or right (B) of the start's column; start below,
    food above, in that column. The same rotation for both rooms."""
    k = int(rng.integers(3, 5))
    x0 = int(rng.integers(k, N - k))
    yb = int(rng.integers(3, 8))
    d1, d2 = int(rng.integers(2, 4)), int(rng.integers(2, 4))
    if yb + d1 > N - 1 or yb - d2 < 0:
        return None
    t = int(rng.integers(4))
    out = []
    for side, gx in (("A", x0 - k), ("B", x0 + k)):
        walls = {rot((x, yb), t) for x in range(N) if x != gx}
        s, g = rot((x0, yb + d1), t), rot((x0, yb - d2), t)
        lay = {"family": "lookalike", "walls": walls, "start": s, "goal": g, "detour": True,
               "shortest": shortest(walls, s, g)[0], "side": side, "gap": rot((gx, yb), t),
               "axis": "x" if t % 2 == 0 else "y"}
        lay["must_see"] = lay["gap"]
        out.append(lay)
    return out


# --- the sets --------------------------------------------------------------------------------------------------------
def to_json(lay):
    out = {**lay, "walls": sorted(lay["walls"])}
    return out


def build():
    rng = np.random.default_rng(SET_SEED)
    d = W.load()
    seen = {(tuple(sorted(l["walls"])), l["start"], l["goal"]) for l in d["learn"] + d["test"]}
    ctl = controls()
    det, con, tried = [], [], 0
    while len(det) < 120:
        lay = W.draw(rng, True)
        tried += 1
        if (tuple(sorted(lay["walls"])), lay["start"], lay["goal"]) in seen:
            continue
        if any(run(ctl[b], lay)["efficient"] for b in ("B0", "H2", "W2")):
            continue
        cells = tour(lay, rng)
        if not run(ctl["Bp"], lay, tour_mem(lay, cells))["efficient"]:
            continue
        seen.add((tuple(sorted(lay["walls"])), lay["start"], lay["goal"]))
        det.append(dict(lay, set="detour", tour=cells))
    while len(con) < 120:
        lay = W.draw(rng, False)
        if (tuple(sorted(lay["walls"])), lay["start"], lay["goal"]) in seen:
            continue
        seen.add((tuple(sorted(lay["walls"])), lay["start"], lay["goal"]))
        con.append(dict(lay, set="control", tour=tour(lay, rng)))
    pairs = []
    while len(pairs) < 40:
        pr = lookalike(rng)
        if pr is None:
            continue
        for lay in pr:
            while True:                     # redrawn if trapped in a pocket without seeing the gap
                lay["tour"] = tour(lay, rng)
                if tour_mem(lay, lay["tour"]).known[lay["gap"][1], lay["gap"][0]]:
                    break
        pairs.append(pr)
    return det, con, pairs, tried


def load():
    d = json.loads((HERE / "sets.json").read_text(encoding="utf-8"))

    def fix(lay):
        lay["walls"] = {tuple(c) for c in lay["walls"]}
        lay["start"], lay["goal"] = tuple(lay["start"]), tuple(lay["goal"])
        lay["tour"] = [tuple(c) for c in lay["tour"]]
        for k in ("gap", "must_see"):
            if k in lay:
                lay[k] = tuple(lay[k])
        return lay
    d["detour"] = [fix(l) for l in d["detour"]]
    d["control"] = [fix(l) for l in d["control"]]
    d["pairs"] = [[fix(a), fix(b)] for a, b in d["pairs"]]
    d["learn"] = W.load()["learn"]
    return d


if __name__ == "__main__":
    det, con, pairs, tried = build()
    (HERE / "sets.json").write_text(json.dumps({"seed": SET_SEED, "detour": [to_json(l) for l in det],
                                                 "control": [to_json(l) for l in con],
                                                 "pairs": [[to_json(a), to_json(b)] for a, b in pairs]},
                                                separators=(",", ":")), encoding="utf-8")
    print("detours", len(det), "of", tried, "drawn;", Counter(l["family"] for l in det))
    print("controls", len(con), "; look-alike pairs", len(pairs))
