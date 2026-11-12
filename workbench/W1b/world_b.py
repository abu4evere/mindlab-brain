"""W1b's world, layouts and scripted brains (questions.md, W1b-frozen). The brain sees the whole 11 x 11 area.

  python workbench/W1b/world_b.py        # builds layouts.json (seed 20261116) and prints the counts
"""
from __future__ import annotations

import json
import sys
from collections import Counter
from pathlib import Path

import numpy as np

HERE = Path(__file__).parent
sys.path.insert(0, str(HERE.parent / "W1"))
from world import MOVES, N, MAX_STEPS, blocked, manhattan, shortest, is_detour, turn, bar, ell, cup  # noqa: E402

LAYOUT_SEED = 20261116
EFF = 1.15
LEFT = {0: 3, 3: 1, 1: 2, 2: 0}        # heading -> heading to its left (north 0, south 1, east 2, west 3)
RIGHT = {v: k for k, v in LEFT.items()}
BACK = {0: 1, 1: 0, 2: 3, 3: 2}


# --- families --------------------------------------------------------------------------------------------------------
def cup_pocket(rng):
    """A cup with a dead-end pocket (3-4 deep) on the outside of its base; kept only if the greedy walk ends in it."""
    b, a = int(rng.integers(5, 8)), int(rng.integers(2, 4))
    cells = cup(rng, b, a)
    depth = int(rng.integers(3, 5))
    i = int(rng.integers(1, b - 2))
    return cells + [(i, j) for j in range(1, depth + 1)] + [(i + 2, j) for j in range(1, depth + 1)]


def double_wall(rng):
    n = int(rng.integers(5, 9))
    return [(i, 0) for i in range(n - 2)] + [(i, 2) for i in range(2, n)]


def nested(rng):
    return cup(rng, 8, 4) + [(x + 2, y - 1) for x, y in cup(rng, 4, 2)]


def two_gap(rng):
    """A barrier with two gaps at different distances from its middle."""
    n = int(rng.integers(8, 11))
    g1, g2 = int(rng.integers(1, 3)), int(rng.integers(5, n - 1))
    return [(i, 0) for i in range(n) if i not in (g1, g2)]


FAMILIES = {"bar": bar, "ell": ell, "cup": cup, "pocket": cup_pocket, "double": double_wall, "nested": nested,
            "two_gap": two_gap}


def place(rng, fn):
    cells = turn(fn(rng), int(rng.integers(4)))
    xs, ys = [c[0] for c in cells], [c[1] for c in cells]
    w, h = max(xs) - min(xs) + 1, max(ys) - min(ys) + 1
    if w > N - 2 or h > N - 2:
        return None
    ox, oy = int(rng.integers(1, N - w)) - min(xs), int(rng.integers(1, N - h)) - min(ys)
    return {(x + ox, y + oy) for x, y in cells}


# --- the scripted brains ---------------------------------------------------------------------------------------------
def toward(pos, goal):
    dx, dy = goal[0] - pos[0], goal[1] - pos[1]
    if abs(dx) >= abs(dy):
        return [2 if dx > 0 else 3] + ([1 if dy > 0 else 0] if dy else [])
    return [1 if dy > 0 else 0] + ([2 if dx > 0 else 3] if dx else [])


def step_ok(walls, pos, a):
    dx, dy = MOVES[a]
    return not blocked(walls, pos[0] + dx, pos[1] + dy)


class Greedy:
    name = "G"

    def reset(self, env):
        pass

    def act(self, env):
        here = manhattan(env.pos, env.goal)
        best, bd = 4, here
        for i, (dx, dy) in enumerate(MOVES[:4]):
            n = (env.pos[0] + dx, env.pos[1] + dy)
            if not blocked(env.walls, *n) and manhattan(n, env.goal) < bd:
                best, bd = i, manhattan(n, env.goal)
        return best


def segment(walls, cell):
    """The wall cells 8-connected to `cell` (inside the area)."""
    if cell not in walls:
        return set()
    seen, todo = {cell}, [cell]
    while todo:
        x, y = todo.pop()
        for dx in (-1, 0, 1):
            for dy in (-1, 0, 1):
                n = (x + dx, y + dy)
                if n in walls and n not in seen:
                    seen.add(n)
                    todo.append(n)
    return seen


class Bug:
    """Greedy until blocked; then follows the wall in a chosen direction until nearer the food than where it was blocked
    and a step toward the food is open. `choose` picks the first heading along the wall:
      W   always turns right (wall on the left), as W1's;
      W2  turns toward the food's side (the sign of its lateral offset);
      H1  heads for the end of the touched wall segment nearer to itself;
      H2  heads for the end minimising (own distance to it + its distance to the food), straight-line."""

    def __init__(self, name):
        self.name = name

    def reset(self, env):
        self.mode, self.hit, self.head, self.hand = "greedy", None, 0, "L"

    def _perp(self, b):
        return (0, 1) if b in (2, 3) else (2, 3)          # blocked in x -> move in y; blocked in y -> move in x

    def choose(self, env, b):
        p_neg, p_pos = self._perp(b)                        # (north, south) or (east, west)
        if self.name == "W":
            return RIGHT[b]
        pos, goal = env.pos, env.goal
        if self.name == "W2":
            lat = (goal[1] - pos[1]) if b in (2, 3) else (goal[0] - pos[0])
            if b in (2, 3):
                return 1 if lat > 0 else 0
            return 2 if lat > 0 else 3
        dx, dy = MOVES[b]
        seg = segment(env.walls, (pos[0] + dx, pos[1] + dy))
        if not seg:
            return RIGHT[b]
        if b in (2, 3):                                     # the barrier runs north-south: its two ends in y
            lo, hi = min(c[1] for c in seg) - 1, max(c[1] for c in seg) + 1
            ends = {0: (pos[0] + dx, lo), 1: (pos[0] + dx, hi)}
        else:
            lo, hi = min(c[0] for c in seg) - 1, max(c[0] for c in seg) + 1
            ends = {3: (lo, pos[1] + dy), 2: (hi, pos[1] + dy)}
        if self.name == "H1":
            return min(ends, key=lambda h: (np.hypot(ends[h][0] - pos[0], ends[h][1] - pos[1]), h))
        return min(ends, key=lambda h: (np.hypot(ends[h][0] - pos[0], ends[h][1] - pos[1]) +
                                        np.hypot(ends[h][0] - goal[0], ends[h][1] - goal[1]), h))

    def act(self, env):
        d = manhattan(env.pos, env.goal)
        if self.mode == "follow" and d < self.hit and any(step_ok(env.walls, env.pos, a) for a in toward(env.pos,
                                                                                                         env.goal)):
            self.mode = "greedy"
        if self.mode == "greedy":
            prefs = toward(env.pos, env.goal)
            for a in prefs:
                if step_ok(env.walls, env.pos, a):
                    return a
            b = prefs[0]
            self.mode, self.hit = "follow", d
            self.head = self.choose(env, b)
            self.hand = "L" if LEFT[self.head] == b else "R"
        order = ((LEFT[self.head], self.head, RIGHT[self.head], BACK[self.head]) if self.hand == "L" else
                 (RIGHT[self.head], self.head, LEFT[self.head], BACK[self.head]))
        for a in order:
            if step_ok(env.walls, env.pos, a):
                self.head = a
                return a
        return 4


class Planner:
    name = "B"

    def reset(self, env):
        self.path = shortest(env.walls, env.pos, env.goal)[1]

    def act(self, env):
        nxt = self.path[self.path.index(env.pos) + 1]
        return MOVES.index((nxt[0] - env.pos[0], nxt[1] - env.pos[1]))


class Wander:
    """M-: remembers where it has been; steps to the unvisited neighbour nearest the food, else any unvisited, else the
    nearest open one. No planning."""
    name = "M-"

    def reset(self, env):
        self.visited = set()

    def act(self, env):
        self.visited.add(env.pos)
        opts = [(i, (env.pos[0] + dx, env.pos[1] + dy)) for i, (dx, dy) in enumerate(MOVES[:4])]
        opts = [(i, n) for i, n in opts if not blocked(env.walls, *n)]
        if not opts:
            return 4
        fresh = [(manhattan(n, env.goal), i) for i, n in opts if n not in self.visited]
        return min(fresh)[1] if fresh else min((manhattan(n, env.goal), i) for i, n in opts)[1]


def controls():
    return [Greedy(), Bug("W"), Bug("W2"), Bug("H1"), Bug("H2"), Wander()]


# --- the environment -------------------------------------------------------------------------------------------------
class Env:
    def __init__(self, lay):
        self.walls, self.goal, self.pos = lay["walls"], lay["goal"], lay["start"]
        self.t, self.done = 0, False

    def obs(self):
        o = np.zeros((3, N, N))
        for (x, y) in self.walls:
            o[0, y, x] = 1.0
        o[1, self.pos[1], self.pos[0]] = 1.0
        o[2, self.goal[1], self.goal[0]] = 1.0
        return o.ravel()

    def step(self, a):
        dx, dy = MOVES[a]
        n = (self.pos[0] + dx, self.pos[1] + dy)
        if not blocked(self.walls, *n):
            self.pos = n
        self.t += 1
        reached = self.pos == self.goal
        self.done = reached or self.t >= MAX_STEPS
        return (1.0 if reached else 0.0) - 0.01, reached


def run(brain, lay):
    env = Env(lay)
    brain.reset(env)
    path = [env.pos]
    while not env.done:
        env.step(brain.act(env))
        path.append(env.pos)
    return env.pos == env.goal, env.t, path


def efficient(brain, lay):
    ok, steps, _ = run(brain, lay)
    return ok and steps <= EFF * lay["shortest"]


# --- the sets --------------------------------------------------------------------------------------------------------
def draw(rng, want_detour, adversarial=False, tries=50000):
    """The family is drawn first (each equally likely), then layouts of that family are drawn until one fits."""
    names = list(FAMILIES)
    fam = names[int(rng.integers(len(names)))]
    for _ in range(tries):
        walls = place(rng, FAMILIES[fam])
        if walls is None:
            continue
        cells = [(x, y) for x in range(N) for y in range(N) if (x, y) not in walls]
        s, g = cells[int(rng.integers(len(cells)))], cells[int(rng.integers(len(cells)))]
        if manhattan(s, g) < 4:
            continue
        d, _ = shortest(walls, s, g)
        if d is None or d > 30 or is_detour(walls, s, g) != want_detour:
            continue
        lay = {"family": fam, "walls": walls, "start": s, "goal": g, "detour": want_detour, "shortest": d}
        if fam == "pocket" and want_detour:              # the pocket must be on the agent's side: greedy ends in it
            _, _, path = run(Greedy(), lay)
            end = path[-1]
            if sum(blocked(walls, end[0] + dx, end[1] + dy) for dx, dy in MOVES[:4]) < 3:
                continue
        if adversarial and all(efficient(b, lay) for b in controls()[1:5]):
            continue
        return lay
    raise RuntimeError("could not draw")


def build():
    rng = np.random.default_rng(LAYOUT_SEED)
    learn = [draw(rng, True) for _ in range(200)] + [draw(rng, False) for _ in range(200)]
    seen = {(tuple(sorted(l["walls"])), l["start"], l["goal"]) for l in learn}

    def fresh(**kw):
        while True:
            lay = draw(rng, **kw)
            if (tuple(sorted(lay["walls"])), lay["start"], lay["goal"]) not in seen:
                return lay
    test = ([dict(fresh(want_detour=True), set="ordinary") for _ in range(60)] +
            [dict(fresh(want_detour=True, adversarial=True), set="adversarial") for _ in range(60)] +
            [dict(fresh(want_detour=False), set="control") for _ in range(120)])
    return learn, test


def to_json(lay):
    return {**lay, "walls": sorted(lay["walls"])}


def load():
    d = json.loads((HERE / "layouts.json").read_text(encoding="utf-8"))
    for lay in d["learn"] + d["test"]:
        lay["walls"] = {tuple(c) for c in lay["walls"]}
        lay["start"], lay["goal"] = tuple(lay["start"]), tuple(lay["goal"])
    return d


if __name__ == "__main__":
    learn, test = build()
    (HERE / "layouts.json").write_text(json.dumps({"seed": LAYOUT_SEED, "learn": [to_json(l) for l in learn],
                                                    "test": [to_json(l) for l in test]}, separators=(",", ":")),
                                       encoding="utf-8")
    print("learn:", Counter((l["family"], l["detour"]) for l in learn))
    print("test:", Counter((l["set"], l["family"]) for l in test))
