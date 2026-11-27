"""CW2 (questions.md, CW2-frozen; the creator's sign-off 26 Nov 2026): a station, through Body v1.

CW1's world (body/CW1/cw1.py, unchanged) plus one station: a fixed passable cell per land with its own look (the
fourth free colour code), at least 5 shortest-path steps from every A and B spot, not on a food patch, the shelter or
the start. The join works only when Bob stands on the station cell.

Consequence model: CW1's, with operations keyed by what is held and the look underfoot (as take), and a place memory
(the cells where each look was felt underfoot this life).
Guidance: when, from what is held now, the model's best EXPERIENCED reachable energy (the value with the untried
bonus set to 0) runs through a look that is not underfoot but is in its place memory, the nearest remembered cell of
that look (shortest path on the walker's remembered map) becomes the target; only above the survival floor; cleared
when the hands change, the target is reached, or Bob falls below the floor.
Steering (arms): GUIDE-REFLEX / SHAM-REFLEX: a carry reflex walks by shortest path on the remembered map to the target
(the sleep and hunger reflexes keep priority). GUIDE-MAP / SHAM-MAP: the target cell is marked as food in a copy of the
map fed to the walker's planner (the walker's memory untouched). SHAM: the target is a remembered (seen, non-wall)
cell that is not a cell of the real target's look, at the path distance nearest the real target's (ties by a seeded
draw), chosen at the same moments, cleared by the same rules. NO-GUIDE: no steering. RANDOM-OPS: CW1's random arm.

Build decisions (recorded; consistent with the frozen plan):
  - The walker's policy is built here exactly as w3m.policy builds it (the Body reflex object around net.act on the
    map), so the reflex state can be read and the map copy fed; with no mark it is the same computation (zero check).
  - "A remembered non-station place" for the sham = any seen, non-wall cell of the walker's map that is not a cell of
    the real target's look (the place memory alone holds too few cells to match distances).
  - With empty hands, a station underfoot is an affordance moment (something underfoot), as CW1's rule reads.
  python cw2.py run ARM SEED [test|pilot]  -> output/{ARM}_{SEED}.jsonl
"""
from __future__ import annotations

import json
import platform
import sys
import time
from collections import deque
from pathlib import Path

HERE = Path(__file__).parent
sys.path.insert(0, str(HERE.parent / "CW1"))
import cw1  # noqa: E402  (BV1's and W3r's chain: the numerical settings before numpy loads)
import numpy as np  # noqa: E402
from cw1 import W, w3k, R3  # noqa: E402

w3m = cw1.w3r.w3m
BRAINS, OUT = HERE / "brains", HERE / "output"
CW2_SEED = 20261128
TEST_LANDS, PILOT_LANDS = range(940001, 940051), range(950001, 950006)
STATION_MIN = 5
H, GAMMA, BONUS, PASS = cw1.H, cw1.GAMMA, cw1.BONUS, cw1.PASS
ARMS = {"GUIDE-REFLEX": ("model", "reflex", False), "GUIDE-MAP": ("model", "map", False),
        "SHAM-REFLEX": ("model", "reflex", True), "SHAM-MAP": ("model", "map", True),
        "NO-GUIDE": ("model", None, False), "RANDOM-OPS": ("random", None, False)}
CFG = {"station": True}


def path_dists(passable, start):
    """Shortest-path steps from start over cells where passable(cell) (4 moves)."""
    d = {start: 0}
    q = deque([start])
    while q:
        c = q.popleft()
        for dx, dy in W.MOVES[:4]:
            n = (c[0] + dx, c[1] + dy)
            if 0 <= n[0] < W.N and 0 <= n[1] < W.N and n not in d and passable(n):
                d[n] = d[c] + 1
                q.append(n)
    return d


class CW2World(cw1.CW1World):
    def __init__(self, land, R):
        super().__init__(land, R)
        self.station, self.S = None, -1
        if not (cw1.CFG["things"] and CFG["station"]):
            return
        self.S = int(np.random.default_rng([cw1.CW1_SEED, int(land["seed"])]).permutation(cw1.FREE_CODES)[3])
        taken = {land["shelter"], land["start"]} | set(self.spots)
        for c in land["patches"]:
            taken |= set(W.block_cells(c))
        far = None
        for s in self.spots:
            d = path_dists(lambda c: not self.walls[c[1], c[0]], s)
            ok = {c for c, k in d.items() if k >= STATION_MIN}
            far = ok if far is None else far & ok
        cand = sorted(c for c in far if c not in taken)
        rng = np.random.default_rng([CW2_SEED, int(land["seed"])])
        self.station = cand[int(rng.integers(len(cand)))]

    def underfoot(self):
        u = super().underfoot()
        if u == 0 and self.station is not None and self.pos == self.station:
            return self.S
        return u

    def hand_step(self, verb):
        if verb == "take" and cw1.CW1World.underfoot(self) == 0:
            E0, h0 = self.E, self.held()                 # only the station is underfoot: it cannot be taken
            cw1.B1.BodyWorld.step(self, 4)
            return self.held(), self.E - (E0 - 1.0), False
        real = self.join_op
        if verb.startswith("op") and self.pos != self.station:
            self.join_op = -1                            # the join does nothing off the station
        try:
            return super().hand_step(verb)
        finally:
            self.join_op = real


class Model(cw1.Model):
    """CW1's model; operations keyed by the look underfoot too; a place memory."""

    def __init__(self, K, rng):
        super().__init__(K, rng)
        self.places = {}                                  # look -> set of cells where it was felt underfoot

    @staticmethod
    def key(h, u, v):
        return (h, u, v) if (v == "take" or v.startswith("op")) else (h, v)

    def feel(self, u, cell):
        if u != 0:
            self.places.setdefault(u, set()).add(cell)

    def _q(self, k, V, bonus=BONUS):
        if k not in self.n:
            return bonus
        n = self.n[k]
        return self.gain[k] / n + GAMMA * sum(c / n * V[h2] for h2, c in self.nxt[k].items())

    def values(self, extra=(), bonus=BONUS):
        S = set(self.states) | set(extra)
        Vs = [{h: 0.0 for h in S}]
        for _ in range(H):
            Vp, V = Vs[-1], {}
            for h in S:
                best = GAMMA * Vp[h]
                for v in self.verbs:
                    if v == "take" or v.startswith("op"):
                        for u in self.u_seen:
                            if h == (0, 0) and u == 0:
                                continue                  # never a moment: empty hands need something underfoot
                            best = max(best, self._q((h, u, v), Vp, bonus))
                    else:
                        best = max(best, self._q((h, v), Vp, bonus))
                V[h] = best
            Vs.append(V)
        return Vs

    def q_now(self, h, u):
        self.u_seen.add(u)
        Vp = self.values(extra=(h,))[H - 1]
        q = {PASS: GAMMA * Vp[h]}
        for v in self.verbs:
            q[v] = self._q(self.key(h, u, v), Vp)
        return q

    def target_look(self, h, u_now):
        """The look (in the place memory, not underfoot now) that the best experienced reachable energy from what is
        held runs through, if it beats what is experienced here; else None."""
        Vp = self.values(extra=(h,), bonus=0.0)[H - 1]
        uverbs = [v for v in self.verbs if v == "take" or v.startswith("op")]

        def best_at(u):
            if h == (0, 0) and u == 0:
                return 0.0
            return max(self._q(self.key(h, u, v), Vp, 0.0) for v in uverbs)
        here = max([best_at(u_now)] + [self._q(self.key(h, u_now, v), Vp, 0.0) for v in self.verbs
                                         if v not in uverbs])
        best, look = here, None
        for u in sorted(self.places):
            if u == u_now:
                continue
            b = best_at(u)
            if b > best + 1e-9:
                best, look = b, u
        return look if (look is not None and best > 0) else None


def configure(arm, seed):
    cw1.configure("LEARN", seed)                        # W3r's RM, BodyWorld, CW1's things with K = 4
    W.World = CW2World
    CFG["station"] = True


def life(net, seed, ls, arm, chooser="arm", on_step=None, trace=None):
    """One life. chooser 'arm' (the arm's own) or None (model and steering off: the walker takes every step)."""
    kind, steer, sham = ARMS[arm]
    if chooser != "arm":
        kind, steer, sham = chooser, None, False
    land, R, rng = W.make_land(ls), R3.regrowth(), np.random.default_rng(ls)
    rfx = w3m.Reflex()                                   # = w3m.policy, built here to read the reflex and feed a map
    marked = {"cell": None}

    def planner_map(w):
        m = w.obs_map()
        if marked["cell"] is not None:
            m = m.copy()
            x, y = marked["cell"]
            m[W.CH_FOOD, y, x] = 1.0
        return m

    def pol(w):
        return rfx.act(w, net.act(planner_map(w), R3.levels(w, "D3"), w.pos, rng)[0])

    w = W.World(land, R)
    crng = np.random.default_rng([cw1.CW1_SEED, seed, ls])
    srng = np.random.default_rng([CW2_SEED, seed, ls])
    model = Model(w.K, crng) if kind == "model" else None
    verbs = cw1.verbs_for(w.K)
    c = {"moments": 0, "acts": 0, "dead_acts": 0, "passes": 0, "acts_by_verb": {}, "guide_starts": 0,
         "guided_steps": 0, "station_guides": 0, "carry_steps": 0, "acts_while_carrying": 0, "joins_on_guide": 0,
         "station_arrivals_after_first_join": 0, "carry_to_join": []}
    tgt = {"cell": None, "hands": None, "look": None}
    carry_start = None
    things = cw1.CFG["things"]

    def passable(cell):
        return not w.m_wall[cell[1], cell[0]]

    while not w.done():
        h, u = w.held(), w.underfoot()
        if model is not None and things:
            model.feel(u, w.pos)
        pair = things and sorted(h) == sorted([w.A, w.B])
        if pair:
            c["carry_steps"] += 1
            carry_start = w.t if carry_start is None else carry_start
        else:
            carry_start = None
        # --- guidance (steering arms only) ------------------------------------------------------------------
        if steer is not None and things:
            if tgt["cell"] is not None and (h != tgt["hands"] or w.pos == tgt["cell"] or not w.above_floor()):
                tgt.update(cell=None, hands=None, look=None)
            if tgt["cell"] is None and w.above_floor():
                look = model.target_look(h, u)
                if look is not None:
                    dist = path_dists(passable, w.pos)
                    cells = [cl for cl in model.places[look] if cl in dist and cl != w.pos]
                    if cells:
                        real = min(cells, key=lambda cl: (dist[cl], cl))
                        cell = real
                        if sham:
                            bad = model.places[look]
                            opts = [cl for cl in dist if w.m_seen[cl[1], cl[0]] and cl not in bad and cl != w.pos]
                            if opts:
                                gap = min(abs(dist[cl] - dist[real]) for cl in opts)
                                near = sorted(cl for cl in opts if abs(dist[cl] - dist[real]) == gap)
                                cell = near[int(srng.integers(len(near)))]
                            else:
                                cell = None
                        if cell is not None:
                            tgt.update(cell=cell, hands=h, look=look)
                            c["guide_starts"] += 1
                            c["station_guides"] += look == w.S
            marked["cell"] = tgt["cell"] if steer == "map" else None
        a = pol(w)                                       # the walker always proposes (its stream and reflexes)
        if steer == "reflex" and tgt["cell"] is not None and not rfx.on and not rfx.hungry:
            b = W.bfs_path(passable, w.pos, [tgt["cell"]])
            if b is None:
                tgt.update(cell=None, hands=None, look=None)
            else:
                a = b
        if tgt["cell"] is not None:
            c["guided_steps"] += 1
        # --- the hands (CW1's arbitration) ------------------------------------------------------------------
        if kind is not None and things and w.moment() and w.above_floor():
            c["moments"] += 1
            if kind == "model":
                v, _ = model.choose(h, u)
            else:
                opts = verbs + [PASS]
                v = opts[int(crng.integers(len(opts)))]
            if v != PASS:
                joins0 = w.stats["joins"]
                h2, gain, changed = w.hand_step(v)
                if model is not None:
                    model.learn(h, u, v, h2, gain)
                c["acts"] += 1
                c["dead_acts"] += not changed
                c["acts_while_carrying"] += pair
                c["acts_by_verb"][v] = c["acts_by_verb"].get(v, 0) + 1
                if w.stats["joins"] > joins0:
                    c["joins_on_guide"] += tgt["look"] == w.S
                    if carry_start is not None:
                        c["carry_to_join"].append(w.t - carry_start)
                if trace is not None:
                    trace.append((w.t, h, u, v, h2, tgt["cell"]))
                continue
            c["passes"] += 1
        before = w.pos
        d0 = w.drive()
        cur, _ = w.step(a)
        if things and w.station is not None and w.pos == w.station != before and w.stats["joins"] > 0:
            c["station_arrivals_after_first_join"] += 1
        if on_step is not None:
            on_step(w, a, d0, cur)
    m = W.life_measures(w)
    s = w.stats
    ctj = c.pop("carry_to_join")
    m.update({"land": ls, "chains": s["chains"], "joins": s["joins"], "took_A": s["took_A"], "took_B": s["took_B"],
              "first_join": s["first_join"], "hand_meals_E": s["hand_meals_E"], **c,
              "carry_to_join_mean": float(np.mean(ctj)) if ctj else None, "carry_to_join_n": len(ctj),
              "chains_per_1000": 1000.0 * s["chains"] / max(1, w.t), "reuse": max(0, s["chains"] - 1),
              "station": list(w.station) if w.station else None})
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
