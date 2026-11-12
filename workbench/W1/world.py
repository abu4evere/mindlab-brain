"""W1's world and layouts (questions.md, W1-frozen). An 11 x 11 open area inside a border wall; one agent, one food.
Layouts come from a fixed generator (seed 20261115) before any brain runs.

  python workbench/W1/world.py        # builds layouts.json and prints the counts
"""
from __future__ import annotations

import json
from collections import deque
from pathlib import Path

import numpy as np

HERE = Path(__file__).parent
N = 11
MAX_STEPS = 60
MAX_SHORTEST = 30
MOVES = [(0, -1), (0, 1), (1, 0), (-1, 0), (0, 0)]    # north, south, east, west, stay
LAYOUT_SEED = 20261115


def blocked(walls, x, y):
    return not (0 <= x < N and 0 <= y < N) or (x, y) in walls


def manhattan(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])


def shortest(walls, start, goal):
    """BFS distance and one shortest path (list of cells, start first), or (None, None)."""
    prev = {start: None}
    q = deque([start])
    while q:
        c = q.popleft()
        if c == goal:
            path = [c]
            while prev[path[-1]] is not None:
                path.append(prev[path[-1]])
            return len(path) - 1, path[::-1]
        for dx, dy in MOVES[:4]:
            n = (c[0] + dx, c[1] + dy)
            if n not in prev and not blocked(walls, *n):
                prev[n] = c
                q.append(n)
    return None, None


def is_detour(walls, start, goal):
    """A detour layout: no path that never lets the Manhattan distance to the food grow (each step must shrink it)."""
    seen = {start}
    q = deque([start])
    while q:
        c = q.popleft()
        if c == goal:
            return False
        for dx, dy in MOVES[:4]:
            n = (c[0] + dx, c[1] + dy)
            if n not in seen and not blocked(walls, *n) and manhattan(n, goal) < manhattan(c, goal):
                seen.add(n)
                q.append(n)
    return True


# --- wall shapes (cells relative to an anchor; turned by r quarter turns) -------------------------------------------
def turn(cells, r):
    out = cells
    for _ in range(r % 4):
        out = [(-y, x) for x, y in out]
    return out


def bar(rng):
    n = int(rng.integers(3, 8))
    return [(i, 0) for i in range(n)]


def ell(rng):
    a, b = int(rng.integers(3, 6)), int(rng.integers(3, 6))
    return [(i, 0) for i in range(a)] + [(0, j) for j in range(1, b)]


def cup(rng, base=None, arm=None):
    b = base or int(rng.integers(3, 8))
    a = arm or int(rng.integers(2, 5))
    return [(i, 0) for i in range(b)] + [(0, -j) for j in range(1, a + 1)] + [(b - 1, -j) for j in range(1, a + 1)]


def cup_with_pocket(rng):
    """A cup with a dead-end pocket on its outside face: two short parallel walls off the base."""
    b, a = int(rng.integers(5, 8)), int(rng.integers(2, 4))
    cells = cup(rng, b, a)
    depth = int(rng.integers(3, 5))
    i = int(rng.integers(1, b - 2))
    cells += [(i, j) for j in range(1, depth + 1)] + [(i + 2, j) for j in range(1, depth + 1)]
    return cells


def double_wall(rng):
    n = int(rng.integers(5, 9))
    gap = 2
    first = [(i, 0) for i in range(n) if i < n - gap]            # gap at the right end
    second = [(i, 2) for i in range(n) if i >= gap]               # gap at the left end
    return first + second


def c_with_inner(rng):
    b, a = int(rng.integers(5, 8)), int(rng.integers(3, 5))
    cells = cup(rng, b, a)
    cells += [(i, -a + 1) for i in range(2, b - 2)]               # an inner bar near the cup's mouth
    return cells


def nested_cups(rng):
    outer = cup(rng, 8, 4)
    inner = [(x + 2, y - 1) for x, y in cup(rng, 4, 2)]
    return outer + inner


FAMILIES = {"bar": bar, "ell": ell, "cup": cup}
POCKET = {"pocket": cup_with_pocket}
UNSEEN = {"double": double_wall, "c_inner": c_with_inner, "nested": nested_cups}


def place(rng, shape_fn):
    cells = turn(shape_fn(rng), int(rng.integers(4)))
    xs, ys = [c[0] for c in cells], [c[1] for c in cells]
    w, h = max(xs) - min(xs) + 1, max(ys) - min(ys) + 1
    if w > N - 2 or h > N - 2:
        return None
    ox = int(rng.integers(1, N - w)) - min(xs)
    oy = int(rng.integers(1, N - h)) - min(ys)
    return {(x + ox, y + oy) for x, y in cells}


def draw(rng, family_fns, want_detour, tries=5000):
    for _ in range(tries):
        name = list(family_fns)[int(rng.integers(len(family_fns)))]
        walls = place(rng, family_fns[name])
        if walls is None:
            continue
        open_cells = [(x, y) for x in range(N) for y in range(N) if (x, y) not in walls]
        for _ in range(30):
            s = open_cells[int(rng.integers(len(open_cells)))]
            g = open_cells[int(rng.integers(len(open_cells)))]
            if manhattan(s, g) < 4:
                continue
            d, _ = shortest(walls, s, g)
            if d is None or d > MAX_SHORTEST:
                continue
            if is_detour(walls, s, g) == want_detour:
                return {"family": name, "walls": sorted(walls), "start": s, "goal": g, "detour": want_detour,
                        "shortest": d}
    raise RuntimeError("could not draw a layout")


def build():
    rng = np.random.default_rng(LAYOUT_SEED)
    learn = [draw(rng, FAMILIES, True) for _ in range(200)] + [draw(rng, FAMILIES, False) for _ in range(200)]
    test = ([dict(draw(rng, FAMILIES, True), set="learning_shapes") for _ in range(40)] +
            [dict(draw(rng, POCKET, True), set="pocket") for _ in range(40)] +
            [dict(draw(rng, UNSEEN, True), set="unseen") for _ in range(40)] +
            [dict(draw(rng, FAMILIES, False), set="control_learning_shapes") for _ in range(40)] +
            [dict(draw(rng, POCKET, False), set="control_pocket") for _ in range(40)] +
            [dict(draw(rng, UNSEEN, False), set="control_unseen") for _ in range(40)])
    return {"seed": LAYOUT_SEED, "learn": learn, "test": test}


def load():
    d = json.loads((HERE / "layouts.json").read_text(encoding="utf-8"))
    for lay in d["learn"] + d["test"]:
        lay["walls"] = {tuple(c) for c in lay["walls"]}
        lay["start"], lay["goal"] = tuple(lay["start"]), tuple(lay["goal"])
    return d


class Env:
    def __init__(self, layout):
        self.walls, self.goal = layout["walls"], layout["goal"]
        self.pos = layout["start"]
        self.t = 0
        self.done = False

    def obs(self):
        """5 x 5 window (wall, food) around the agent, then the smell (dx, dy) / 10: 52 numbers."""
        x0, y0 = self.pos
        win = np.zeros((2, 5, 5))
        for j in range(5):
            for i in range(5):
                x, y = x0 + i - 2, y0 + j - 2
                win[0, j, i] = 1.0 if blocked(self.walls, x, y) else 0.0
                win[1, j, i] = 1.0 if (x, y) == self.goal else 0.0
        smell = [(self.goal[0] - x0) / 10.0, (self.goal[1] - y0) / 10.0]
        return np.concatenate([win.ravel(), smell])

    def step(self, a):
        dx, dy = MOVES[a]
        n = (self.pos[0] + dx, self.pos[1] + dy)
        if not blocked(self.walls, *n):
            self.pos = n
        self.t += 1
        reached = self.pos == self.goal
        self.done = reached or self.t >= MAX_STEPS
        return (1.0 if reached else 0.0) - 0.01, reached


if __name__ == "__main__":
    d = build()
    out = {"seed": d["seed"], "learn": d["learn"], "test": d["test"]}
    (HERE / "layouts.json").write_text(json.dumps(out, separators=(",", ":")), encoding="utf-8")
    from collections import Counter
    print("learn:", Counter((l["family"], l["detour"]) for l in d["learn"]))
    print("test:", Counter((l["set"], l["family"]) for l in d["test"]))
    print("test shortest path, detour layouts: mean", np.mean([l["shortest"] for l in d["test"] if l["detour"]]))
