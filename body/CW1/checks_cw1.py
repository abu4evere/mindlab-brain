"""CW1's checks before any test data (questions.md, "Checks before any test data"; all must pass).
  1 zero check: the consequence model off and no loose things -> every arm reproduces BV1's BODY bit for bit
    (RMS seeds 1-8, BV1's land 910001; action, position, energy, fatigue, the brain's input layers, the table)
  2 physics: every hand verb and operation on every held pair, scripted
  3 delayed credit (GPT's condition): after one scripted chain, join > the dead operations in (A, B) and
    take B > drop in (A)
  4 adapter audit for hands and operations: the verb list and legality do not depend on which operation joins, and
    nothing the body senses differs between two worlds that differ only in which operation joins
  5 same seed, same result (a LEARN life twice)
  python checks_cw1.py  -> prints each check and "All: PASS" or "FAIL"
"""
from __future__ import annotations

import sys
from pathlib import Path

HERE = Path(__file__).parent
sys.path.insert(0, str(HERE))
sys.path.insert(0, str(HERE.parent / "BV1"))
import cw1  # noqa: E402
import numpy as np  # noqa: E402
import bv1  # noqa: E402
from cw1 import W, w3k  # noqa: E402

OK = []


def check(name, cond, detail=""):
    OK.append(bool(cond))
    print(f"{name}: {'PASS' if cond else 'FAIL'} {detail}", flush=True)


def record_life(arm, seed):
    """CW1's life loop with the model off and no loose things, recorded as bv1.life records BODY."""
    cw1.configure(arm, seed)
    cw1.CFG["things"] = False
    net = w3k.load_npz(cw1.BRAINS / f"RM_CS_{seed}.npz", seed)
    rec = []

    def on_step(w, a, d0, cur):
        rec.append((int(a), tuple(w.pos), float(w.E), float(w.F), w.obs_map().copy(),
                    w.mod.pos.copy(), w.mod.neg.copy()))
    _, m = cw1.life(net, seed, bv1.w3i.FRESH_SEEDS[0], arm, chooser=None, on_step=on_step)
    cw1.CFG["things"] = True
    return rec


def zero_check():
    for s in range(1, 9):
        ref = bv1.life("BODY", s)[0]
        for arm in cw1.ARMS:
            mm = bv1.first_mismatch(ref, record_life(arm, s))
            check(f"1 zero check seed {s} {arm}", mm is None, mm or f"({len(ref)} steps identical)")


def scripted_world(K=4, join=None, land_seed=930001):
    cw1.configure("LEARN", 1)
    cw1.CFG["K"] = K
    w = W.World(W.make_land(land_seed), 200)
    if join is not None:
        w.join_op = join
    w.E = 100.0
    return w


def physics():
    w0 = scripted_world()
    A, B, C, j = w0.A, w0.B, w0.C, w0.join_op
    ops = [f"op{k}" for k in range(4)]
    looks = (0, A, B, C)
    bad = []
    for h1 in looks:
        for h2 in looks:
            if h1 == 0 and h2 != 0:
                continue
            for v in ["take", "drop", "use"] + ops:
                w = scripted_world()
                w.hands = [h1, h2]
                w.ground = {}
                w.spots = {}
                w.ground[w.pos] = [B]                     # a B lies underfoot
                E0 = w.E
                h, gain, changed = w.hand_step(v)
                pair = sorted([h1, h2]) == sorted([A, B])
                if v == "take":
                    exp = (h1, h2) if h2 != 0 else ((B, 0) if h1 == 0 else (h1, B))
                elif v == "drop":
                    exp = (h2, 0) if h1 != 0 else (0, 0)
                elif v == "use":
                    exp = (h2, 0) if h1 == C else (h1, h2)
                else:
                    exp = (C, 0) if (v == f"op{j}" and pair) else (h1, h2)
                want_gain = 2 * W.MEAL if (v == "use" and h1 == C) else 0.0
                ground_ok = True
                if v == "drop" and h1 != 0:
                    ground_ok = w.ground[w.pos] == [B, h1]
                if v == "take" and h2 == 0:
                    ground_ok = w.ground[w.pos] == []
                if h != exp or abs(gain - want_gain) > 1e-9 or not ground_ok:
                    bad.append((h1, h2, v, h, exp, gain, want_gain))
    check("2 physics: every verb on every held pair (B underfoot)", not bad, f"{len(bad)} wrong {bad[:3]}")
    # join in both hand orders; a spot regrows R steps after it is taken; C dropped keeps on the ground
    w = scripted_world()
    w.hands = [B, A]
    w.hand_step(f"op{j}")
    check("2 physics: join in the order (B, A) gives C", w.held() == (C, 0))
    w = scripted_world()
    w.ground, w.spots = {}, {w.pos: [A, 0]}
    w.E = 1e6                                    # scripted: no death during the long checks
    w.hand_step("take")
    t_taken = w.t
    check("2 physics: taking empties the spot", w.underfoot() == 0 and w.held() == (A, 0))
    while w.t < t_taken + w.R - 1:
        w.hand_step("use")
    check("2 physics: not back before R steps", w.underfoot() == 0, f"t={w.t}")
    w.hand_step("use")
    check("2 physics: the spot is full again R steps after", w.underfoot() == A, f"t={w.t}, taken {t_taken}")
    w = scripted_world()
    w.hands, w.ground, w.spots = [C, 0], {}, {}
    w.E = 1e6
    w.hand_step("drop")
    for _ in range(300):
        w.hand_step("op0" if j != 0 else "op1")
    check("2 physics: C dropped keeps on the ground (300 steps)", w.underfoot() == C)
    w = scripted_world()
    w.hands, w.ground, w.spots = [C, 0], {}, {}
    w.E = 190.0
    w.hand_step("use")
    check("2 physics: a meal of C is capped at EMAX and C is used up", w.E == W.EMAX and w.held() == (0, 0))
    w = scripted_world(K=12)
    check("2 physics: PAD has 12 operations, one joins", len(cw1.verbs_for(w.K)) == 15 and 0 <= w.join_op < 12)
    w = scripted_world(K=0)
    check("2 physics: NO-MAKE has no operations", cw1.verbs_for(w.K) == ["take", "drop", "use"])


def delayed_credit():
    A, B, C = 1, 2, 4
    for tried_dead in (False, True):
        m = cw1.Model(4, np.random.default_rng(0))
        m.u_seen |= {A, B}
        m.learn((0, 0), A, "take", (A, 0), 0.0)
        m.learn((A, 0), B, "take", (A, B), 0.0)
        m.learn((A, B), 0, "op2", (C, 0), 0.0)
        m.learn((C, 0), 0, "use", (0, 0), 60.0)
        if tried_dead:
            for k in (0, 1, 3):
                m.learn((A, B), 0, f"op{k}", (A, B), 0.0)
            m.learn((A, 0), 0, "drop", (0, 0), 0.0)
        q = m.q_now((A, B), 0)
        dead = max(q[f"op{k}"] for k in (0, 1, 3))
        check(f"3 delayed credit ({'dead ops tried' if tried_dead else 'dead ops untried'}): join > dead ops in (A, B)",
              q["op2"] > dead, f"join {q['op2']:.2f} vs {dead:.2f}")
        q = m.q_now((A, 0), B)
        check(f"3 delayed credit ({'tried' if tried_dead else 'untried'}): take B > drop in (A)",
              q["take"] > q["drop"], f"take {q['take']:.2f} vs drop {q['drop']:.2f}")


def reachable_only():
    """The pilot's fault, guarded: with every situation that can be met tried and nothing giving energy, empty hands
    are worth 0 (a never-met situation, empty hands with nothing underfoot, must not keep a bonus alive)."""
    m = cw1.Model(4, np.random.default_rng(0))
    m.u_seen |= {1}
    for v in m.verbs:
        m.learn((0, 0), 1, v, (1, 0) if v == "take" else (0, 0), 0.0)
        for u in (0, 1):
            m.learn((1, 0), u, v, (0, 0) if v == "drop" else ((1, 1) if (v == "take" and u == 1) else (1, 0)), 0.0)
            m.learn((1, 1), u, v, (1, 0) if v == "drop" else (1, 1), 0.0)
    V = m.values()[cw1.H]
    check("3 only situations that can be met count (all tried, no energy -> V(empty hands) = 0)",
          abs(V[(0, 0)]) < 1e-12, f"V = {V[(0, 0)]:.3f}")


def adapter_audit():
    for K in (4, 12):
        for ls in (930001, 930002, 930003):
            seqs = []
            for j in range(K):
                w = scripted_world(K=K, join=j, land_seed=ls)
                vs = cw1.verbs_for(w.K)
                legal = [w.adapter.legal(n) for n in w.adapter.verb_numbers()]
                trace = []
                for v in ["take", "drop", "take", "use"] + [f"op{k}" for k in range(K) if k != j][:2]:
                    w.hand_step(v)
                    s = w.adapter.senses()
                    trace.append((w.held(), w.underfoot(), round(w.E, 6), w.F, s["touch"], tuple(s["feelings"].items())))
                seqs.append((tuple(vs), tuple(legal), trace))
            same = all(x == seqs[0] for x in seqs)
            check(f"4 adapter audit K={K} land {ls}: verb list, legality and senses identical whichever op joins", same)


def determinism():
    cw1.configure("LEARN", 1)
    net = w3k.load_npz(cw1.BRAINS / "RM_CS_1.npz", 1)
    a = cw1.life(net, 1, 930001, "LEARN")[1]
    cw1.configure("LEARN", 1)
    b = cw1.life(net, 1, 930001, "LEARN")[1]
    check("5 same seed, same result (LEARN, seed 1, land 930001)", a == b, f"chains {a['chains']}, acts {a['acts']}")


if __name__ == "__main__":
    physics()
    delayed_credit()
    reachable_only()
    adapter_audit()
    determinism()
    zero_check()
    print("All:", "PASS" if all(OK) else "FAIL", f"({sum(OK)}/{len(OK)})")
