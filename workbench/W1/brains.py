"""W1's brains (questions.md, W1-frozen).
Scripted: G greedy, W wall-follower, B BFS on the true map, M BFS on its own map (unknown = open), M- its map without
planning. Learning: F feed-forward actor-critic, R Elman actor-critic, F-imit F's network trained to imitate B."""
from __future__ import annotations

import numpy as np

from world import MOVES, N, blocked, manhattan, shortest

H = 32
GAMMA, LR, ENT, CLIP = 0.97, 0.01, 0.01, 1.0
TRUNC = 16


def neighbours(c):
    return [(i, (c[0] + dx, c[1] + dy)) for i, (dx, dy) in enumerate(MOVES[:4])]


# --- scripted brains ------------------------------------------------------------------------------------------------
class Greedy:
    name = "G"

    def reset(self, env):
        pass

    def act(self, env):
        here = manhattan(env.pos, env.goal)
        best, bd = 4, here
        for i, n in neighbours(env.pos):
            if not blocked(env.walls, *n) and manhattan(n, env.goal) < bd:
                best, bd = i, manhattan(n, env.goal)
        return best


LEFT = {0: 3, 3: 1, 1: 2, 2: 0}        # heading -> the heading to its left (north 0, south 1, east 2, west 3)
RIGHT = {v: k for k, v in LEFT.items()}
BACK = {0: 1, 1: 0, 2: 3, 3: 2}


class WallFollower:
    """The bug algorithm: greedy until blocked, then keep the wall on the left until nearer the food than where it was
    blocked and a step toward the food is open."""
    name = "W"

    def reset(self, env):
        self.mode, self.hit, self.head = "greedy", None, 0

    def _open(self, env, a):
        dx, dy = MOVES[a]
        return not blocked(env.walls, env.pos[0] + dx, env.pos[1] + dy)

    def _toward(self, env):
        dx, dy = env.goal[0] - env.pos[0], env.goal[1] - env.pos[1]
        prefs = []
        if abs(dx) >= abs(dy):
            prefs = [2 if dx > 0 else 3] + ([1 if dy > 0 else 0] if dy else [])
        else:
            prefs = [1 if dy > 0 else 0] + ([2 if dx > 0 else 3] if dx else [])
        return prefs

    def act(self, env):
        d = manhattan(env.pos, env.goal)
        if self.mode == "follow" and d < self.hit and any(self._open(env, a) for a in self._toward(env)):
            self.mode = "greedy"
        if self.mode == "greedy":
            for a in self._toward(env):
                if self._open(env, a):
                    return a
            self.mode, self.hit = "follow", d
            self.head = RIGHT[self._toward(env)[0]]          # turn right, so the wall is on the left
        for a in (LEFT[self.head], self.head, RIGHT[self.head], BACK[self.head]):
            if self._open(env, a):
                self.head = a
                return a
        return 4


class Planner:
    """B: BFS on the true map."""
    name = "B"

    def reset(self, env):
        _, path = shortest(env.walls, env.pos, env.goal)
        self.path = path

    def act(self, env):
        i = self.path.index(env.pos)
        nxt = self.path[i + 1]
        return MOVES.index((nxt[0] - env.pos[0], nxt[1] - env.pos[1]))


class MapPlanner:
    """M: remembers every cell it has seen in its 5 x 5 window and replans each step by BFS on that map, unknown cells
    counted open. M-: the same map, no planning: nearest-to-food unvisited neighbour, else any unvisited, else any."""

    def __init__(self, plan=True):
        self.plan = plan
        self.name = "M" if plan else "M-"

    def reset(self, env):
        self.wall, self.visited = set(), set()

    def _see(self, env):
        x0, y0 = env.pos
        for j in range(-2, 3):
            for i in range(-2, 3):
                x, y = x0 + i, y0 + j
                if blocked(env.walls, x, y):
                    self.wall.add((x, y))

    def act(self, env):
        self._see(env)
        self.visited.add(env.pos)
        if self.plan:
            _, path = shortest(self.wall, env.pos, env.goal)
            if path is None or len(path) < 2:
                return 4
            nxt = path[1]
            return MOVES.index((nxt[0] - env.pos[0], nxt[1] - env.pos[1]))
        opts = [(i, n) for i, n in neighbours(env.pos) if n not in self.wall]
        if not opts:
            return 4
        fresh = [(manhattan(n, env.goal), i) for i, n in opts if n not in self.visited]
        if fresh:
            return min(fresh)[1]
        return min((manhattan(n, env.goal), i) for i, n in opts)[1]


# --- learning brains -------------------------------------------------------------------------------------------------
def softmax(z):
    e = np.exp(z - z.max())
    return e / e.sum()


class Net:
    """52 inputs -> 32 tanh (optionally Elman: + the previous hidden state) -> 5 action scores and a value."""

    def __init__(self, seed, recurrent):
        r = np.random.default_rng(seed)
        self.rec = recurrent
        self.p = {"Wx": r.normal(0, 0.1, (H, 52)), "b": np.zeros(H), "Wa": r.normal(0, 0.1, (5, H)),
                  "ba": np.zeros(5), "Wv": r.normal(0, 0.1, H), "bv": np.zeros(1)}
        if recurrent:
            self.p["Wh"] = r.normal(0, 0.1, (H, H))

    def reset(self):
        self.h = np.zeros(H)

    def step(self, x):
        p = self.p
        pre = p["Wx"] @ x + p["b"] + (p["Wh"] @ self.h if self.rec else 0.0)
        hp, h = self.h, np.tanh(pre)
        if self.rec:
            self.h = h
        return hp, h, p["Wa"] @ h + p["ba"], float(p["Wv"] @ h + p["bv"][0])

    def backward(self, xs, hps, hs, dlogits, dvals):
        """Gradients (to subtract) for a whole episode. For R, the backprop through time is cut every 16 steps."""
        p = self.p
        g = {k: np.zeros_like(v) for k, v in p.items()}
        dh_next = np.zeros(H)
        T = len(xs)
        for t in reversed(range(T)):
            g["Wa"] += np.outer(dlogits[t], hs[t])
            g["ba"] += dlogits[t]
            g["Wv"] += dvals[t] * hs[t]
            g["bv"] += dvals[t]
            dh = p["Wa"].T @ dlogits[t] + dvals[t] * p["Wv"]
            if self.rec and (t + 1) % TRUNC != 0:
                dh = dh + dh_next
            dpre = dh * (1.0 - hs[t] ** 2)
            g["Wx"] += np.outer(dpre, xs[t])
            g["b"] += dpre
            if self.rec:
                g["Wh"] += np.outer(dpre, hps[t])
                dh_next = p["Wh"].T @ dpre
        return g

    def apply(self, g):
        n = float(np.sqrt(sum(float((v * v).sum()) for v in g.values())))
        s = min(1.0, CLIP / n) if n > 0 else 1.0
        for k in self.p:
            self.p[k] -= LR * s * g[k]


def episode_ac(net, env, rng):
    """One actor-critic episode (Monte Carlo returns, advantage = return - value, entropy bonus)."""
    net.reset()
    xs, hps, hs, logits, vals, acts, rews = [], [], [], [], [], [], []
    while not env.done:
        x = env.obs()
        hp, h, z, v = net.step(x)
        pi = softmax(z)
        a = int(rng.choice(5, p=pi))
        r, _ = env.step(a)
        xs.append(x); hps.append(hp); hs.append(h); logits.append(z); vals.append(v); acts.append(a); rews.append(r)
    G, rets = 0.0, []
    for r in reversed(rews):
        G = r + GAMMA * G
        rets.append(G)
    rets = rets[::-1]
    dl, dv = [], []
    for z, v, a, R in zip(logits, vals, acts, rets):
        pi = softmax(z)
        adv = R - v
        d = pi.copy()
        d[a] -= 1.0
        d *= adv                                   # d(-adv log pi(a)) / dz
        logp = np.log(pi + 1e-12)
        ent_grad = pi * (logp + 1.0) - pi * float(pi @ (logp + 1.0))   # d(-H)/dz ... sign below
        dl.append(d + ENT * ent_grad)              # minimise -adv log pi - ENT * H
        dv.append(v - R)                           # d(0.5 (v - R)^2) / dv
    net.apply(net.backward(xs, hps, hs, dl, dv))
    return env.pos == env.goal


def episode_imit(net, env, layout):
    """One imitation episode: walk B's path; at each state, cross-entropy toward B's action."""
    net.reset()
    _, path = shortest(layout["walls"], layout["start"], layout["goal"])
    xs, hps, hs, dl, dv = [], [], [], [], []
    for c, nxt in zip(path[:-1], path[1:]):
        env.pos = c
        x = env.obs()
        hp, h, z, v = net.step(x)
        a = MOVES.index((nxt[0] - c[0], nxt[1] - c[1]))
        d = softmax(z)
        d[a] -= 1.0
        xs.append(x); hps.append(hp); hs.append(h); dl.append(d); dv.append(0.0)
    if xs:
        net.apply(net.backward(xs, hps, hs, dl, dv))


class Learned:
    def __init__(self, name, net):
        self.name, self.net = name, net

    def reset(self, env):
        self.net.reset()

    def act(self, env):
        _, _, z, _ = self.net.step(env.obs())
        return int(np.argmax(z))
