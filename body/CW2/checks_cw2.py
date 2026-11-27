"""CW2's checks before any test data (questions.md, "Checks before any test data"; all must pass).
  1 zero check: no things, no station, model and steering off -> every arm's life loop reproduces BV1's BODY bit for
    bit (RMS seeds 1-8, BV1's land 910001)
  2 physics: the join only on the station, both hand orders; every operation, every held pair, on and off; the
    station cannot be taken; the station's placement rule (>= 5 path steps from every spot, not taken cells)
  3 guidance: never from the untried bonus (no target before a join on the station's look is experienced); after one
    scripted chain at the station, holding A and B makes the station's look the target (5: delayed credit through
    place); the map copy differs from the walker's map only at the marked cell; the walker's memory is not changed
  4 shams: the sham place is never a cell of the real target's look; it is at the nearest path distance
  6 adapter audit (verb list, legality, station independent of the join), determinism
  python checks_cw2.py  -> prints each check and "All: PASS" or "FAIL"
"""
from __future__ import annotations

import sys
from pathlib import Path

HERE = Path(__file__).parent
sys.path.insert(0, str(HERE))
sys.path.insert(0, str(HERE.parent / "BV1"))
import cw2  # noqa: E402
import numpy as np  # noqa: E402
import bv1  # noqa: E402
from cw2 import W, w3k, cw1  # noqa: E402

OK = []


def check(name, cond, detail=""):
    OK.append(bool(cond))
    print(f"{name}: {'PASS' if cond else 'FAIL'} {detail}", flush=True)


def zero_check():
    for s in range(1, 9):
        ref = bv1.life("BODY", s)[0]
        net = w3k.load_npz(cw2.BRAINS / f"RM_CS_{s}.npz", s)
        for arm in cw2.ARMS:
            cw2.configure(arm, s)
            cw1.CFG["things"] = False
            rec = []

            def on_step(w, a, d0, cur):
                rec.append((int(a), tuple(w.pos), float(w.E), float(w.F), w.obs_map().copy(),
                            w.mod.pos.copy(), w.mod.neg.copy()))
            cw2.life(net, s, bv1.w3i.FRESH_SEEDS[0], arm, on_step=on_step)
            cw1.CFG["things"] = True
            mm = bv1.first_mismatch(ref, rec)
            check(f"1 zero check seed {s} {arm}", mm is None, mm or f"({len(ref)} steps identical)")


def world(ls=950001):
    cw2.configure("GUIDE-REFLEX", 1)
    w = W.World(W.make_land(ls), 200)
    w.E = 1e6
    return w


def physics():
    for ls in (950001, 950002, 950003, 940001, 940002):
        w = world(ls)
        d = cw2.path_dists(lambda c: not w.walls[c[1], c[0]], w.station)
        taken = {w.land["shelter"], w.land["start"]} | set(w.spots)
        for c in w.land["patches"]:
            taken |= set(W.block_cells(c))
        check(f"2 station placement land {ls}", all(d.get(s, 99) >= cw2.STATION_MIN for s in w.spots)
              and w.station not in taken and not w.walls[w.station[1], w.station[0]],
              f"station {w.station}, min spot distance {min(d.get(s, 99) for s in w.spots)}")
    w0 = world()
    A, B, C, S, j = w0.A, w0.B, w0.C, w0.S, w0.join_op
    off = next(c for c in [(x, y) for y in range(W.N) for x in range(W.N)]
               if not w0.walls[c[1], c[0]] and c != w0.station and c not in w0.spots)
    bad = []
    for where in ("on", "off"):
        for h in [(A, B), (B, A), (A, 0), (B, 0), (C, 0), (A, A), (0, 0)]:
            for k in range(4):
                w = world()
                w.ground, w.spots = {}, {}
                w.pos = w.station if where == "on" else off
                w.hands = list(h)
                w.hand_step(f"op{k}")
                joins = where == "on" and k == j and sorted(h) == sorted([A, B])
                exp = (C, 0) if joins else h
                if w.held() != exp:
                    bad.append((where, h, k, w.held(), exp))
    check("2 physics: the join only on the station (both orders), nothing else anywhere", not bad, f"{bad[:3]}")
    w = world()
    w.ground, w.spots = {}, {}
    w.pos = w.station
    check("2 the station is felt underfoot", w.underfoot() == S)
    h2, gain, changed = w.hand_step("take")
    check("2 the station cannot be taken", h2 == (0, 0) and not changed and w.underfoot() == S)
    w.hands = [A, 0]
    w.hand_step("drop")
    check("2 a thing dropped on the station lies on top", w.underfoot() == A and w.pos == w.station)


def guidance():
    A, B, C, S = 1, 2, 4, 7
    m = cw2.Model(4, np.random.default_rng(0))
    m.u_seen |= {A, B, S}
    for u, cell in ((A, (1, 1)), (B, (5, 5)), (S, (9, 9))):
        m.feel(u, cell)
    check("3 no target with nothing experienced (the bonus never guides)", m.target_look((A, B), 0) is None)
    for k in range(4):
        m.learn((A, B), 0, f"op{k}", (A, B), 0.0)        # operations tried off the station: nothing
        if k != 2:
            m.learn((A, B), S, f"op{k}", (A, B), 0.0)
    check("3 no target after only failed operations", m.target_look((A, B), 0) is None)
    m.learn((0, 0), A, "take", (A, 0), 0.0)
    m.learn((A, 0), B, "take", (A, B), 0.0)
    m.learn((A, B), S, "op2", (C, 0), 0.0)
    m.learn((C, 0), 0, "use", (0, 0), 60.0)
    check("3/5 delayed credit through place: after one chain at the station, (A, B) off it targets the station",
          m.target_look((A, B), 0) == S, f"target {m.target_look((A, B), 0)}")
    check("3 holding A, off the B spot: target is B's look", m.target_look((A, 0), 0) == B, f"{m.target_look((A, 0), 0)}")
    check("3 on the station holding A and B: no target (act here)", m.target_look((A, B), S) is None)
    # a map-guided life: the planner's copy differs from the walker's map only at the mark; memory unchanged
    cw2.configure("GUIDE-MAP", 1)
    net = w3k.load_npz(cw2.BRAINS / "RM_CS_1.npz", 1)
    seen = {"n": 0, "ok": True, "w": None}
    orig = net.act

    def spy(mp, lev, cell, rng):
        base = seen["w"].obs_map()
        diff = np.argwhere(mp != base)
        if len(diff):
            seen["n"] += 1
            seen["ok"] &= len(diff) == 1 and diff[0][0] == W.CH_FOOD and mp[tuple(diff[0])] == 1.0
        return orig(mp, lev, cell, rng)
    net.act = spy
    WorldCls = W.World

    class Spy(WorldCls):
        def __init__(self, land, R):
            super().__init__(land, R)
            seen["w"] = self
    W.World = Spy
    try:
        for ls in (950001, 950002, 950003, 950004, 950005):
            w, mm = cw2.life(net, 1, ls, "GUIDE-MAP")
    finally:
        W.World = WorldCls
        net.act = orig
    check("3 map copy differs from the walker's map only at the marked cell (food layer = 1)", seen["ok"],
          f"{seen['n']} marked steps over 5 pilot lives")
    # the same, with guidance forced on (any remembered look other than the one underfoot) so the mark is exercised
    orig_t = cw2.Model.target_look
    cw2.Model.target_look = lambda self, h, u: next((k for k in sorted(self.places) if k != u), None)
    seen.update(n=0, ok=True)
    net.act = spy
    cw2.configure("GUIDE-MAP", 1)                       # before the spy world (configure resets W.World)
    W.World = Spy
    try:
        w, mm = cw2.life(net, 1, 950003, "GUIDE-MAP")
    finally:
        W.World = WorldCls
        net.act = orig
        cw2.Model.target_look = orig_t
    check("3 (forced guidance) the map copy differs from the walker's own map only at the marked cell, so the "
          "walker's map (from its memory, the same step) never holds the mark", seen["ok"] and seen["n"] > 0,
          f"{seen['n']} marked steps")


def shams():
    w = world()
    w.m_seen[:, :] = True
    dist = cw2.path_dists(lambda c: not w.m_wall[c[1], c[0]], w.pos)
    m = cw2.Model(4, np.random.default_rng(0))
    m.feel(w.S, w.station)
    # the rule as cw2.life applies it
    real = w.station
    bad = m.places[w.S]
    opts = [cl for cl in dist if w.m_seen[cl[1], cl[0]] and cl not in bad and cl != w.pos]
    gap = min(abs(dist[cl] - dist[real]) for cl in opts)
    near = [cl for cl in opts if abs(dist[cl] - dist[real]) == gap]
    check("4 sham: never the station, at the nearest path distance", real not in near and gap == 0,
          f"{len(near)} cells at distance {dist[real]}")


def audit_and_determinism():
    for ls in (950001, 950002):
        outs = []
        for j in range(4):
            w = world(ls)
            w.join_op = j
            outs.append((tuple(cw1.verbs_for(w.K)), tuple(w.adapter.legal(n) for n in w.adapter.verb_numbers()),
                         w.station, w.S))
        check(f"6 adapter audit land {ls}: verbs, legality, station identical whichever op joins",
              all(o == outs[0] for o in outs))
    net = w3k.load_npz(cw2.BRAINS / "RM_CS_1.npz", 1)
    for arm in ("GUIDE-REFLEX", "GUIDE-MAP", "SHAM-REFLEX"):
        cw2.configure(arm, 1)
        a = cw2.life(net, 1, 950002, arm)[1]
        cw2.configure(arm, 1)
        b = cw2.life(net, 1, 950002, arm)[1]
        check(f"6 same seed, same result ({arm}, seed 1, land 950002)", a == b, f"chains {a['chains']}")


if __name__ == "__main__":
    physics()
    guidance()
    shams()
    audit_and_determinism()
    zero_check()
    print("All:", "PASS" if all(OK) else "FAIL", f"({sum(OK)}/{len(OK)})")
