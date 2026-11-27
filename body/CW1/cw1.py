"""CW1 (questions.md, CW1-frozen; the creator's sign-off 26 Nov 2026): a small crafting world through Body v1.

W3r's lands lived through Body v1 (body/BV1/body_v1.BodyWorld), plus two kinds of loose things, A and B: 3 spots of
each on every land, a spot's thing regrowing R steps after it is taken (as food). Looks of A, B and C are three colour
codes not used by wall, food or shelter, dealt anew per land. Hands: 2 (hand 1 fills first; when hand 1 empties, hand
2's thing moves into it). Hand verbs (time passes as for rest; the ordinary step cost only):
  take        the thing underfoot (a dropped thing on top, else a full spot's thing) into a free hand
  drop        hand 1's thing onto the ground here
  use         hand 1: C is eaten (energy + 2 x MEAL, capped at EMAX) and used up; anything else: nothing
  operate(k)  k = 0..K-1 (numbers shuffled per land): one joins A and B (either order) into C in hand 1; others nothing
The mover is W3r's RM kept copy with its reflexes (w3i.policy), unchanged. The consequence model (Model) chooses at
affordance moments (something underfoot with a free hand, or something held) while hunger and tiredness are both
below 0.5; otherwise the mover's step is taken. Arms: LEARN, RANDOM-OPS, NO-MAKE, PAD (questions.md).

Build decisions (recorded; consistent with the frozen plan):
  - A hand step first lets time pass exactly as the mover's rest (BodyWorld.step(4): drift, shelter, regrowth,
    relocations, ground meals); the hand's effect follows (the cost comes before the meal, as in BV1). The mover's
    meaning table therefore learns only the ground's lessons on a hand step: a meal from the hand is not a lesson about
    the cell stood on (the frozen mover's table keys "fed" to the ground).
  - take is keyed by the look underfoot too (what it does depends on what is there: touch); the other verbs by what is
    held. "Best reachable" takes the best over looks met underfoot in this life (that is how things are met: the
    mover passes over them). Ties in reachable energy go to the sooner (a factor 0.99 per step); "pass" wins exact ties.
  - Untried actions are valued at one food meal (MEAL); a hand state never seen is valued at MEAL too (all untried).
  - Pilot fault fix (26 Nov, before any test data; no value changed): the value of empty hands counted "take with
    nothing underfoot", a situation that is never a decision moment, so its untried bonus never went away and "pass"
    tied every real option; the model stopped after a little exploration. Only situations that can be met count.
  - The model's energy signal is the world's response part of the feedback (after the body's own drift), the hand
    meal included.
  python cw1.py run ARM SEED [test|pilot]  -> output/{ARM}_{SEED}.jsonl (one line per life)
"""
from __future__ import annotations

import json
import platform
import sys
import time
from pathlib import Path

HERE = Path(__file__).parent
sys.path.insert(0, str(HERE.parent / "BV1"))
import body_v1 as B1  # noqa: E402  (W3r's chain first: the numerical settings before numpy loads)
import numpy as np  # noqa: E402
from body_v1 import w3r, W  # noqa: E402

w3k, w3i = w3r.w3k, w3r.w3n.w3i
R3 = w3k.R3
BRAINS, OUT = HERE / "brains", HERE / "output"
CW1_SEED = 20261127
TEST_LANDS, PILOT_LANDS = range(920001, 920051), range(930001, 930006)
FREE_CODES = (1, 2, 4, 7)                    # colour codes not used by wall (6), food (3), shelter (5); 0 is floor
N_SPOTS, H, GAMMA = 3, 4, 0.99
BONUS = float(W.MEAL)
ARMS = {"LEARN": {"K": 4, "chooser": "model"}, "RANDOM-OPS": {"K": 4, "chooser": "random"},
        "NO-MAKE": {"K": 0, "chooser": "model"}, "PAD": {"K": 12, "chooser": "model"}}
CFG = {"things": True, "K": 4}
PASS = "pass"


def verbs_for(K):
    return ["take", "drop", "use"] + [f"op{k}" for k in range(K)]


class CW1World(B1.BodyWorld):
    """BodyWorld plus loose things and two hands."""

    def __init__(self, land, R):
        super().__init__(land, R)
        self.hands = [0, 0]
        self.ground, self.spots = {}, {}
        self.K = CFG["K"]
        self.stats = {"chains": 0, "joins": 0, "took_A": 0, "took_B": 0, "first_join": None, "hand_meals_E": 0.0}
        if not CFG["things"]:
            self.A = self.B = self.C = -1
            self.join_op = None
            return
        rng = np.random.default_rng([CW1_SEED, int(land["seed"])])
        self.A, self.B, self.C = (int(c) for c in rng.permutation(FREE_CODES)[:3])
        self.join_op = int(rng.integers(self.K)) if self.K > 0 else None
        taken = {land["shelter"], land["start"]}
        for c in land["patches"]:
            taken |= set(W.block_cells(c))
        cand = [(x, y) for y in range(W.N) for x in range(W.N) if not self.walls[y, x] and (x, y) not in taken]
        pick = rng.choice(len(cand), size=2 * N_SPOTS, replace=False)
        for i, j in enumerate(pick):
            self.spots[cand[int(j)]] = [self.A if i < N_SPOTS else self.B, 0]   # [look, step at which it is full]

    # --- what the body senses of the things (touch underfoot, hands) ---------------------------------------------
    def underfoot(self):
        g = self.ground.get(self.pos)
        if g:
            return g[-1]
        s = self.spots.get(self.pos)
        return s[0] if (s is not None and s[1] <= self.t) else 0

    def held(self):
        return (self.hands[0], self.hands[1])

    def moment(self):
        """An affordance moment: something underfoot with a free hand, or something held."""
        return (self.underfoot() != 0 and self.hands[1] == 0) or self.hands[0] != 0

    def above_floor(self):
        hunger = 1.0 - self.E / W.EMAX
        tired = min(self.F, W.F_CAP) / W.F_CAP
        return hunger < 0.5 and tired < 0.5

    def _shift(self):
        if self.hands[0] == 0:
            self.hands = [self.hands[1], 0]

    def hand_step(self, verb):
        """One hand verb; returns (next held, gain, changed)."""
        E0, h0 = self.E, self.held()
        g0 = (tuple(self.ground.get(self.pos, ())), self.underfoot())
        B1.BodyWorld.step(self, 4)                       # time passes as for rest (the mover's rest, unchanged)
        gain = self.E - (E0 - 1.0)                       # the world's response after the body's drift (-1 at rest)
        if self.dead:
            return self.held(), gain, False
        pos = self.pos
        if verb == "take":
            u = self.underfoot()
            if u != 0 and self.hands[1] == 0:
                if self.ground.get(pos):
                    self.ground[pos].pop()
                else:
                    self.spots[pos][1] = self.t + self.R
                self.hands[0 if self.hands[0] == 0 else 1] = u
                if u == self.A:
                    self.stats["took_A"] += 1
                if u == self.B:
                    self.stats["took_B"] += 1
        elif verb == "drop":
            if self.hands[0] != 0:
                self.ground.setdefault(pos, []).append(self.hands[0])
                self.hands[0] = 0
                self._shift()
        elif verb == "use":
            if self.hands[0] == self.C:
                E1 = self.E
                self.E = min(float(W.EMAX), self.E + 2.0 * W.MEAL)
                self.stats["hand_meals_E"] += self.E - E1
                self.hands[0] = 0
                self._shift()
                self.stats["chains"] += 1
        else:
            k = int(verb[2:])
            if k == self.join_op and sorted(self.hands) == sorted([self.A, self.B]):
                self.hands = [self.C, 0]
                self.stats["joins"] += 1
                if self.stats["first_join"] is None:
                    self.stats["first_join"] = self.t
        gain = self.E - (E0 - 1.0)
        changed = self.held() != h0 or (tuple(self.ground.get(pos, ())), self.underfoot()) != g0
        return self.held(), gain, changed


class Model:
    """The consequence model: plain counts of (situation, verb) -> next held looks and the energy gained; values by
    the best energy reachable within H steps through hand states. Reset at every birth."""

    def __init__(self, K, rng):
        self.verbs = verbs_for(K)
        self.rng = rng
        self.n, self.gain, self.nxt = {}, {}, {}
        self.u_seen = {0}
        self.states = set()

    @staticmethod
    def key(h, u, v):
        return (h, u, v) if v == "take" else (h, v)

    def learn(self, h, u, v, h2, gain):
        k = self.key(h, u, v)
        self.n[k] = self.n.get(k, 0) + 1
        self.gain[k] = self.gain.get(k, 0.0) + gain
        d = self.nxt.setdefault(k, {})
        d[h2] = d.get(h2, 0) + 1
        self.states |= {h, h2}

    def _q(self, k, V):
        if k not in self.n:
            return BONUS
        n = self.n[k]
        return self.gain[k] / n + GAMMA * sum(c / n * V[h2] for h2, c in self.nxt[k].items())

    def values(self, extra=()):
        """[V_0, ..., V_H] over the hand states met (plus extra); V_0 = 0. A state with nothing tried is worth BONUS
        from V_1 on (every action in it untried)."""
        S = set(self.states) | set(extra)
        Vs = [{h: 0.0 for h in S}]
        for _ in range(H):
            Vp, V = Vs[-1], {}
            for h in S:
                best = GAMMA * Vp[h]                                  # pass: keep what is held
                for v in self.verbs:
                    if v == "take":
                        for u in self.u_seen:
                            if h == (0, 0) and u == 0:
                                continue                      # never a moment: empty hands need something underfoot
                            best = max(best, self._q((h, u, v), Vp))
                    else:
                        best = max(best, self._q((h, v), Vp))
                V[h] = best
            Vs.append(V)
        return Vs

    def q_now(self, h, u):
        """The values of pass and of each verb in the situation now (H-step)."""
        self.u_seen.add(u)
        Vp = self.values(extra=(h,))[H - 1]
        q = {PASS: GAMMA * Vp[h]}
        for v in self.verbs:
            q[v] = self._q(self.key(h, u, v), Vp)
        return q

    def choose(self, h, u):
        q = self.q_now(h, u)
        best = max(q.values())
        if q[PASS] >= best:
            return PASS, q
        top = [v for v in self.verbs if q[v] >= best - 1e-12]
        return top[int(self.rng.integers(len(top)))], q


def configure(arm, seed):
    w3r.configure("RM", seed)                       # W3r's RM (HR body, sleep reflex, the meaning table)
    W.World = CW1World
    B1.BV1["rename"] = False
    CFG.update(things=True, K=ARMS[arm]["K"])


def life(net, seed, ls, arm, chooser="arm", on_step=None):
    """One life. chooser: 'arm' (the arm's own), or None (the model off: the mover takes every step)."""
    chooser = ARMS[arm]["chooser"] if chooser == "arm" else chooser
    land, R, rng = W.make_land(ls), R3.regrowth(), np.random.default_rng(ls)
    pol = w3i.policy(net, rng)
    w = W.World(land, R)
    crng = np.random.default_rng([CW1_SEED, seed, ls])
    model = Model(w.K, crng) if chooser == "model" else None
    verbs = verbs_for(w.K)
    c = {"moments": 0, "acts": 0, "dead_acts": 0, "passes": 0, "acts_by_verb": {}}
    while not w.done():
        a = pol(w)                                   # the mover always proposes (its random stream and reflexes)
        if chooser is not None and CFG["things"] and w.moment() and w.above_floor():
            c["moments"] += 1
            h, u = w.held(), w.underfoot()
            if chooser == "model":
                v, _ = model.choose(h, u)
            else:
                opts = verbs + [PASS]
                v = opts[int(crng.integers(len(opts)))]
            if v != PASS:
                h2, gain, changed = w.hand_step(v)
                if model is not None:
                    model.learn(h, u, v, h2, gain)
                c["acts"] += 1
                c["dead_acts"] += not changed
                c["acts_by_verb"][v] = c["acts_by_verb"].get(v, 0) + 1
                continue
            c["passes"] += 1
        d0 = w.drive()
        cur, _ = w.step(a)
        if on_step is not None:
            on_step(w, a, d0, cur)
    m = W.life_measures(w)
    s = w.stats
    m.update({"land": ls, "chains": s["chains"], "joins": s["joins"], "took_A": s["took_A"], "took_B": s["took_B"],
              "first_join": s["first_join"], "hand_meals_E": s["hand_meals_E"], **c,
              "chains_per_1000": 1000.0 * s["chains"] / max(1, w.t), "reuse": max(0, s["chains"] - 1)})
    return w, m


def run(arm, seed, which="test"):
    assert arm in ARMS
    OUT.mkdir(exist_ok=True)
    lands = TEST_LANDS if which == "test" else PILOT_LANDS
    path = OUT / (f"{arm}_{seed}.jsonl" if which == "test" else f"pilot_{arm}_{seed}.jsonl")
    done = set()
    if path.exists():
        done = {json.loads(x)["land"] for x in path.read_text().splitlines() if x.strip()}
    configure(arm, seed)
    net = w3k.load_npz(BRAINS / f"RM_CS_{seed}.npz", seed)
    mach = {"platform": platform.platform(), "python": platform.python_version(), "numpy": np.__version__,
            "node": platform.node()}
    with open(path, "a") as f:
        for ls in lands:
            if ls in done:
                continue
            t0 = time.time()
            _, m = life(net, seed, ls, arm)
            m.update({"arm": arm, "seed": seed, "seconds": round(time.time() - t0, 2), "machine": mach})
            f.write(json.dumps(m, default=float) + "\n")
            f.flush()
    print("done", arm, seed, flush=True)


if __name__ == "__main__":
    if sys.argv[1] == "run":
        run(sys.argv[2], int(sys.argv[3]), sys.argv[4] if len(sys.argv) > 4 else "test")
