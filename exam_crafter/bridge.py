"""The Outside Exam: Mind Lab's best brain (MBb, MoveVIN, 236 learned numbers) living in Crafter, AS IT IS.

Draft, exploratory until the plan is frozen. Nothing here teaches the brain or adds a goal. The bridge only TRANSLATES
Crafter into what the brain was raised on (Mind Lab W3), the same way the ACL bridge (BX1) did:

  the map  - a memory of the 64 x 64 world written only from what the player sees (Crafter's 9 x 7 view), the same
             "fixed writer" as W3; the brain reads a 15 x 15 window of it centred on the player, in W3's 5 channels:
               wall      : a place the body cannot step into (tree, stone, table, coal, iron, diamond, furnace, an
                           animal or monster, the world's edge); lava is NOT a wall (the body can step on it, and dies);
               unseen    : never seen;
               food      : water, a cow, a ripe plant (where "going there" feeds or waters the body);
               shelter   : the player's own place (in Crafter one can sleep anywhere);
               staleness : W3's own uncertainty, 1 - exp(-age / 200); unseen = 1; walls = 0.
  the body - W3's 3 drives, scaled to [0, 1]: hunger = the worse of food and drink, (9 - min(food, drink)) / 9;
             tiredness = (9 - energy) / 9; curiosity = mean staleness over the window's open places (W3's rule).
  the hand - the brain picks one of its 5 moves by sampling its own softmax at its own place (as in W3 lives):
               a move into a food place = turn to face it, then "do" (in W3, stepping on food eats it);
               any other move = Crafter's move; stay = "sleep" (in W3, staying at the shelter rests).
The brain has no move for chopping, placing or making: in Crafter those never happen unless by accident of the hand
rule above. That is the point of "as it is".
"""
from __future__ import annotations

import numpy as np

import brain_mv as M

N = M.N                     # 15
H = N // 2                  # 7
TAU = 200.0                 # W3's staleness time
CH_WALL, CH_UNSEEN, CH_FOOD, CH_SHELTER, CH_UNC = range(5)
# Crafter's semantic ids: materials in order after None, then objects (crafter/env.py, engine.SemanticView)
MAT = ["none", "water", "grass", "stone", "path", "sand", "tree", "lava", "coal", "iron", "diamond", "table", "furnace"]
OBJ = ["player", "cow", "zombie", "skeleton", "arrow", "plant"]
SEM = MAT + OBJ
GROUND = {"grass", "path", "sand", "lava", "player"}
FACE = {0: "move_up", 1: "move_down", 2: "move_right", 3: "move_left"}
DIRS = {0: (0, -1), 1: (0, 1), 2: (1, 0), 3: (-1, 0)}
ACTIONS = ["noop", "move_left", "move_right", "move_up", "move_down", "do", "sleep", "place_stone", "place_table",
           "place_furnace", "place_plant", "make_wood_pickaxe", "make_stone_pickaxe", "make_iron_pickaxe",
           "make_wood_sword", "make_stone_sword", "make_iron_sword"]
A = {n: i for i, n in enumerate(ACTIONS)}


def softmax(z):
    e = np.exp(z - z.max())
    return e / e.sum()


def load(path, seed=1):
    import brains3  # noqa: F401  (numerical settings)
    d = np.load(path)
    net = M.MoveVIN(seed)
    for k in net.p:
        net.p[k] = d[k].copy()
    return net


class Memory:
    """The fixed writer: what the player has seen of the 64 x 64 world, and when."""

    def __init__(self, area=64):
        self.area = area
        self.seen = np.zeros((area, area), bool)       # indexed [x, y] like Crafter
        self.wall = np.zeros((area, area), bool)
        self.food = np.zeros((area, area), bool)
        self.water = np.zeros((area, area), bool)       # which food is water (for the SATED arm)
        self.last = np.full((area, area), -1, int)

    def write(self, sem, pos, t, ripe_cells):
        x0, y0 = pos
        for x in range(x0 - 4, x0 + 5):                 # Crafter's local view: 9 wide, 7 tall
            for y in range(y0 - 3, y0 + 4):
                if 0 <= x < self.area and 0 <= y < self.area:
                    name = SEM[sem[x, y]]
                    food = name in ("water", "cow") or (name == "plant" and (x, y) in ripe_cells)
                    self.seen[x, y] = True
                    self.food[x, y] = food
                    self.water[x, y] = name == "water"
                    self.wall[x, y] = (name not in GROUND) and not food
                    self.last[x, y] = t

    def window(self, pos, t, inv=None):
        """inv given (the SATED arm): a food kind shows only while the body is not full of it (water while drink < 9,
        cow and ripe plant while food < 9)."""
        m = np.zeros((5, N, N))
        x0, y0 = pos
        for wy in range(N):
            for wx in range(N):
                x, y = x0 + wx - H, y0 + wy - H
                if not (0 <= x < self.area and 0 <= y < self.area):
                    m[CH_WALL, wy, wx] = 1.0                 # the world's edge
                    continue
                if not self.seen[x, y]:
                    m[CH_UNSEEN, wy, wx] = 1.0
                    m[CH_UNC, wy, wx] = 1.0
                    continue
                m[CH_WALL, wy, wx] = float(self.wall[x, y])
                food = self.food[x, y]
                if inv is not None and food:
                    food = inv["drink"] < 9 if self.water[x, y] else inv["food"] < 9
                    if not food:                                # hidden food is still a place the body cannot enter
                        m[CH_WALL, wy, wx] = 1.0
                        continue
                m[CH_FOOD, wy, wx] = float(food)
                if not self.wall[x, y]:
                    m[CH_UNC, wy, wx] = 1.0 - np.exp(-(t - self.last[x, y]) / TAU)
        m[CH_SHELTER, H, H] = 1.0
        return m


def ripe_plants(env):
    from crafter import objects
    return {tuple(o.pos) for o in env._world.objects if isinstance(o, objects.Plant) and o.ripe}


def levels(inv, m):
    hunger = (9 - min(inv["food"], inv["drink"])) / 9.0
    tired = (9 - inv["energy"]) / 9.0
    open_ = m[CH_WALL] == 0
    cur = float(m[CH_UNC][open_].mean()) if open_.any() else 0.0
    return np.array([hunger, tired, cur], float)


class BrainPlayer:
    """MBb as it is, through the bridge. sated=True: the SATED arm (questions.md, secondary)."""

    def __init__(self, net, rng, sated=False):
        self.net, self.rng, self.sated = net, rng, sated

    def reset(self):
        self.mem, self.t, self.facing = Memory(), 0, (0, 1)    # Crafter's player starts facing down
        self.visited = set()

    def choose(self, m, info):
        lev = levels(info["inventory"], m)
        fw = self.net.plan(m[None], lev[None])
        z, _ = self.net.head(fw, np.array([H * N + H]))
        return int(self.rng.choice(5, p=softmax(z[0])))

    def act(self, env, info):
        pos = tuple(int(v) for v in info["player_pos"])
        self.mem.write(info["semantic"], pos, self.t, ripe_plants(env))
        m = self.mem.window(pos, self.t, info["inventory"] if self.sated else None)
        a = self.choose(m, info)
        self.visited.add(pos)
        self.t += 1
        if a == 4:
            return A["sleep"]
        dx, dy = DIRS[a]
        if m[CH_FOOD, H + dy, H + dx] > 0:                    # into food: face it, then "do"
            return A["do"] if self.facing == (dx, dy) else A[FACE[a]]
        return A[FACE[a]]

    def after(self, env):
        self.facing = tuple(int(v) for v in env._player.facing)


class RandomHandPlayer(BrainPlayer):
    """RANDOM-5: the same bridge and hand, but each of the 5 moves uniformly at random (the matched floor).
    sated=True: RANDOM-5S, the matched floor for the SATED arm."""

    def __init__(self, rng, sated=False):
        super().__init__(None, rng, sated)

    def choose(self, m, info):
        return int(self.rng.integers(5))


class RandomPlayer:
    """Crafter's own floor: a uniformly random action each step."""

    def __init__(self, rng):
        self.rng = rng

    def reset(self):
        self.visited = set()

    def act(self, env, info):
        self.visited.add(tuple(int(v) for v in info["player_pos"]))
        return int(self.rng.integers(len(ACTIONS)))

    def after(self, env):
        pass
