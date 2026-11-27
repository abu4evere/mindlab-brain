"""V2-1's checks before data (questions.md, "Checks before data"; all must pass).
  1 PLAIN reproduces W3r's saved RMS lives (seed 1, W3r's test lands 900001-900050, swap and stable; lifespans equal)
  2 the reset fires exactly at the thresholds (n = 2 never; n = 3, |y - p| = 0.75 yes; |y - p| < 0.75 no)
  3 after a reset the look reads 0 in all three predictions until new fair trials
  4 SHAM resets another look with counts at the same moment, never the contradicted one
  5 WINDOW multiplies only the touched cell (key)
  6 CW1's join changes at step 1,500 to a different operation; with no change, PLAIN reproduces CW1's LEARN life
    (seed 1, land 930003: 7 chains, 74 acts)
  7 determinism (SURPRISE swap life twice; SURPRISE B life twice)
  python checks_v21.py [quick]  -> prints each check and "All: PASS" or "FAIL"
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

HERE = Path(__file__).parent
sys.path.insert(0, str(HERE))
import v21  # noqa: E402
import numpy as np  # noqa: E402

OK = []
W3R_OUT = HERE.parents[1] / "workbench" / "W3r" / "output"


def check(name, cond, detail=""):
    OK.append(bool(cond))
    print(f"{name}: {'PASS' if cond else 'FAIL'} {detail}", flush=True)


def reproduce(n_lives):
    net = v21.w3k.load_npz(v21.BRAINS / "RM_CS_1.npz", 1)
    for cond, ref_name in (("swap", "test_RMS-midswap_1.json"), ("stable", "test_RMS_1.json")):
        ref = json.loads((W3R_OUT / ref_name).read_text())
        bad = []
        for i in range(n_lives):
            _, m = v21.life_a(net, 1, 900001 + i, "PLAIN", cond == "swap")
            if m["lifespan"] != ref[i]["lifespan"] or m["survived"] != ref[i]["survived"]:
                bad.append((900001 + i, m["lifespan"], ref[i]["lifespan"]))
        check(f"1 PLAIN reproduces W3r's saved RMS lives ({cond}, seed 1, {n_lives} lands)", not bad, f"{bad[:3]}")


def table_rules():
    rng = np.random.default_rng(0)
    t = v21.RevTable("SURPRISE", rng)
    t.add(3, 0, False)
    t.add(3, 0, False)
    t.add(3, 0, True)                                    # n = 2 before: no reset
    check("2 no reset with n = 2", t.resets == 0 and t.pos[3, 0] == 1)
    t = v21.RevTable("SURPRISE", rng)
    for _ in range(3):
        t.add(5, 1, True)
    t.add(5, 2, True)
    t.add(5, 1, False)                                   # n = 3, p = 1, |0 - 1| = 1 >= 0.75: reset look 5
    check("2 reset with n = 3 and a full contradiction", t.resets == 1)
    check("3 after the reset the look reads 0 except the new event",
          t.pos[5].sum() == 0 and t.neg[5, 1] == 1 and t.neg[5, [0, 2]].sum() == 0 and (t.pred()[5] == 0).all())
    t = v21.RevTable("SURPRISE", rng)
    for y in (True, True, True, False):
        t.add(6, 0, y)                                   # p = 0.75 after 3 trues + 1 false? (first false: |0-1| = 1)
    t2 = v21.RevTable("SURPRISE", rng)
    for y in (True, False, True, True):
        t2.add(6, 0, y)                                  # before the 4th: n = 3, p = 2/3, |1 - 2/3| < 0.75: no reset
    check("2 no reset when |y - p| < 0.75", t2.resets == 0)
    t3 = v21.RevTable("SURPRISE", rng)
    for y in (True, True, True, False, False, False):
        t3.add(2, 0, y)                                  # 4th event: n = 3, p = 1: reset; then 2 more
    t3.pos[2, 0], t3.neg[2, 0] = 1.0, 3.0               # p = 0.25: a True gives |1 - 0.25| = 0.75 exactly
    r0 = t3.resets
    t3.add(2, 0, True)
    check("2 reset at exactly |y - p| = 0.75", t3.resets == r0 + 1)
    s = v21.RevTable("SHAM", np.random.default_rng(1))
    for c in (1, 4):
        s.add(c, 0, True)
    for _ in range(3):
        s.add(5, 1, True)
    before = (s.pos.copy(), s.neg.copy())
    s.add(5, 1, False)
    hit = [c for c in range(8) if (before[0][c] + before[1][c]).sum() > 0 and (s.pos[c] + s.neg[c]).sum() == 0]
    check("4 SHAM resets another look with counts, never the contradicted one",
          s.resets == 1 and len(hit) == 1 and hit[0] in (1, 4) and s.pos[5, 1] == 3)
    wdw = v21.RevTable("WINDOW", rng)
    wdw.add(3, 0, True)
    wdw.add(4, 0, True)
    wdw.add(3, 0, True)
    check("5 WINDOW multiplies only the touched cell", abs(wdw.pos[3, 0] - 1.95) < 1e-12 and wdw.pos[4, 0] == 1)
    v21.CFG["mode"] = "SURPRISE"                         # RevModel takes its mode from CFG when it is made
    m = v21.RevModel(4, np.random.default_rng(0))
    for _ in range(3):
        m.learn((1, 0), 0, "op0", (1, 0), 0.0)
    m.learn((1, 0), 0, "op0", (4, 0), 0.0)               # a confident key contradicted: reset, then this event
    check("2 CW1 key reset on a confident contradiction (SURPRISE)", m.resets == 1 and m.n[((1, 0), "op0")] == 1)


def cw1_parts():
    net = v21.w3k.load_npz(v21.BRAINS / "RM_CS_1.npz", 1)
    w, m = v21.life_b(net, 1, 930003, "PLAIN", change=False)
    check("6 with no change, PLAIN reproduces CW1's LEARN life (seed 1, land 930003)",
          m["chains"] == 7 and m["acts"] == 74, f"chains {m['chains']}, acts {m['acts']}")
    v21.cw1.configure("LEARN", 1)
    v21.W.World = v21.ChangeWorld
    v21.CFG["change"] = True
    w = v21.W.World(v21.W.make_land(970001), 200)
    j1, j2 = w.join_op, w.join2
    w.E = 1e6
    while w.t < v21.SWAP_T - 1:                           # stop at t = 1,499; the next step ends at 1,500
        w.hand_step("use")
    before = w.join_op
    w.hand_step("use")
    check("6 the join changes at step 1,500 to a different operation", before == j1 and w.join_op == j2 and j1 != j2,
          f"t {w.t}, {j1} -> {w.join_op}")


def determinism():
    net = v21.w3k.load_npz(v21.BRAINS / "RM_CS_2.npz", 2)
    a = v21.life_a(net, 2, 980001, "SURPRISE", True)[1]
    b = v21.life_a(net, 2, 980001, "SURPRISE", True)[1]
    check("7 same seed, same result (A, SURPRISE, swap)", a == b, f"lifespan {a['lifespan']}, resets {a['resets']}")
    a = v21.life_b(net, 2, 980001, "SURPRISE")[1]
    b = v21.life_b(net, 2, 980001, "SURPRISE")[1]
    check("7 same seed, same result (B, SURPRISE)", a == b, f"chains {a['chains']}, resets {a['resets']}")


if __name__ == "__main__":
    quick = len(sys.argv) > 1 and sys.argv[1] == "quick"
    table_rules()
    cw1_parts()
    determinism()
    reproduce(3 if quick else 50)
    print("All:", "PASS" if all(OK) else "FAIL", f"({sum(OK)}/{len(OK)})")
